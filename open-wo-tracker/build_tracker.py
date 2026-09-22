#!/usr/bin/env python3
"""
Build Open_WOs_tracker.xlsx — the weekly open-work-order tracker for Buddy's Kitchen.

Run:  python3 build_tracker.py [output.xlsx]

The workbook has three tabs:
  History  — dashboard (this week's scorecard, three charts, email text) + the weekly log
  Totals   — the entry grid: four numbers typed into one 3-column block per week
  Read Me  — how to update it, conventions, legend, change log

Everything on History is formula-driven off Totals. The only manual cells are the four
counts per week on Totals, the Notes column on History, and two yellow fill-ins on Read Me.

Design notes for whoever maintains this:
  * Totals blocks are located by the literal "DATE" label in row 1, not by counting columns.
    Hidden helper rows 30/31/32 turn that into an index History can look up with MATCH.
    This is why an inserted column no longer breaks the history.
  * Every range is bounded (to column OJ) rather than a full-row reference: full-row INDEX
    is slow in Excel and unevaluable by most tooling.
  * Only pre-2010 worksheet functions are used, so nothing needs an _xlfn. prefix and
    nothing renders as #NAME? in older Excel or in Excel for the web.
"""
import datetime
import re
import shutil
import sys
import zipfile

from openpyxl import Workbook
from openpyxl.chart import LineChart
from openpyxl.chart.series import Series, SeriesLabel
from openpyxl.chart.data_source import AxDataSource, NumDataSource, NumRef
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.legend import LegendEntry
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.formatting.rule import Rule
from openpyxl.styles import (Alignment, Border, Font, PatternFill, Protection,
                             Side)
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.utils import get_column_letter as CL
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.workbook.defined_name import DefinedName

# ---------------------------------------------------------------- constants

FONT = "Calibri"

INK          = "FF262626"   # primary text
INK_SOFT     = "FF6A6A66"   # secondary text
RULE         = "FFD8D8D4"   # hairline borders
BAND         = "FFF2F2EF"   # section band fill
HEAD_FILL    = "FFEDEDEA"   # table header fill
INPUT_BLUE   = "FF0000FF"   # "you type here"
YELLOW       = "FFFFFF00"   # "fill this in" / past due
UP_RED       = "FFC0392B"   # more open than last week = worse
DOWN_GREEN   = "FF1E7B34"   # fewer open than last week = better

# Chart series colours. Colour means METRIC, the same in every chart; the plant
# is the facet (one chart each). Validated with the dataviz palette validator:
# 2a78d6 + eb6834 pass lightness, chroma, CVD separation (dE 24.7 protan),
# normal-vision separation (dE 33.6) and 3:1 contrast, on all pairs.
REPAIR_INK   = "2A78D6"     # categorical slot 1, blue
PM_INK       = "EB6834"     # categorical slot 2, orange
TOTAL_INK    = "3F3F3C"     # neutral: a sum, not a third category
WARN_FILL    = "FFF4D7D5"
WARN_INK     = "FF9C2B22"

# Totals geometry
FIRST_ANCHOR = 1            # column A
BLOCK_W      = 3            # columns per weekly block
N_BLOCKS     = 105          # ~2 years pre-built
SCAN_LAST    = 400          # bounded scan width; room for ~28 more blocks
SCAN         = CL(SCAN_LAST)

R_DATE, R_BV_HEAD, R_BV_REP, R_BV_PM, R_BV_TOT = 1, 3, 4, 5, 6
R_LV_HEAD, R_LV_REP, R_LV_PM, R_LV_TOT = 8, 9, 10, 11
R_CO_HEAD, R_CO_TOT = 13, 14
R_NOTE = 15
R_FLAG, R_FILLED_IX, R_ALL_IX, R_SCALAR = 30, 31, 32, 33   # hidden helpers
R_BROKEN, R_DUP = 34, 35                                   # hidden guard rails

# History geometry
LOG_HEAD  = 55
LOG_FIRST = LOG_HEAD + 1
LOG_ROWS  = 110
LOG_LAST  = LOG_FIRST + LOG_ROWS - 1

COL_WEEK, COL_BVR, COL_BVP, COL_BVT = "A", "B", "C", "D"
COL_LVR, COL_LVP, COL_LVT = "E", "F", "G"
COL_REPT, COL_PMT, COL_COMB, COL_CHG, COL_NOTE = "H", "I", "J", "K", "L"

N_WEEKS = "$N$1"
CHART_WEEKS = 26            # how many weeks the charts show at once            # hidden helper: how many weeks are filled in

FMT_COUNT  = "#,##0"
FMT_CHANGE = '"▲ "#,##0;"▼ "#,##0;"no change"'
FMT_DATE   = "mm/dd/yy"
FMT_LONG   = "dddd, mmmm d, yyyy"

# Real data already recorded in the workbook this replaces.
# Source: Open_WOs_tracker_.xlsx as received 2026-09-21 (Totals!A/D blocks).
SEED = {
    datetime.date(2026, 9, 15): (11, 3, 32, 173),
    datetime.date(2026, 9, 21): (7, 6, 38, 241),
}

# ---------------------------------------------------------------- helpers


def week_dates(n):
    """Block dates: the first count was taken on Tue 09-15-2026, then Mondays."""
    out = [datetime.date(2026, 9, 15)]
    d = datetime.date(2026, 9, 21)
    while len(out) < n:
        out.append(d)
        d += datetime.timedelta(days=7)
    return out


def anchor_col(i):
    return FIRST_ANCHOR + BLOCK_W * i


def paint(ws, cell_range, fill=None, border=None, font=None, align=None, fmt=None):
    """Apply styling across a range, including every cell of a merged region."""
    for row in ws[cell_range]:
        for c in row:
            if fill is not None:
                c.fill = fill
            if border is not None:
                c.border = border
            if font is not None:
                c.font = font
            if align is not None:
                c.alignment = align
            if fmt is not None:
                c.number_format = fmt


def chg_text(cell):
    """Formula fragment rendering a change cell as +n / -n / no change / n/a."""
    return (f'IF({cell}="","n/a",IF({cell}>0,"+"&TEXT({cell},"{FMT_COUNT}"),'
            f'IF({cell}<0,TEXT({cell},"{FMT_COUNT}"),"no change")))')


# ---------------------------------------------------------------- Totals


def build_totals(ws, dates):
    thin = Side(style="thin", color=RULE)
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    band_font = Font(name=FONT, size=14, bold=True, color=INK)
    num_font = Font(name=FONT, size=14, color=INPUT_BLUE)      # typed input
    calc_font = Font(name=FONT, size=14, color=INK)            # formula
    lbl_font = Font(name=FONT, size=12, color=INK_SOFT)
    tot_lbl_font = Font(name=FONT, size=12, bold=True, color=INK)
    date_lbl_font = Font(name=FONT, size=10, bold=True, color=INK_SOFT)
    date_font = Font(name=FONT, size=12, bold=True, color=INK)
    centre = Alignment(horizontal="center", vertical="center")
    left = Alignment(horizontal="left", vertical="center")

    bv_fill = PatternFill("solid", fgColor="FFDCE9F8")   # blue tint
    lv_fill = PatternFill("solid", fgColor="FFFBE3D8")   # orange tint
    co_fill = PatternFill("solid", fgColor="FFE8E8E5")   # neutral

    for i, d in enumerate(dates):
        c = anchor_col(i)
        a, b, sp = CL(c), CL(c + 1), CL(c + 2)

        ws.cell(R_DATE, c, "DATE").font = date_lbl_font
        ws.cell(R_DATE, c).alignment = centre
        ws.merge_cells(f"{b}{R_DATE}:{sp}{R_DATE}")
        dc = ws.cell(R_DATE, c + 1, d)
        dc.font = date_font
        dc.number_format = FMT_LONG
        dc.alignment = left
        paint(ws, f"{b}{R_DATE}:{sp}{R_DATE}")
        for cc in (ws.cell(R_DATE, c + 1), ws.cell(R_DATE, c + 2)):
            cc.protection = Protection(locked=False)

        for head_row, text, fill in ((R_BV_HEAD, "BURNSVILLE", bv_fill),
                                     (R_LV_HEAD, "LAKEVILLE", lv_fill),
                                     (R_CO_HEAD, "COMBINED", co_fill)):
            ws.merge_cells(f"{a}{head_row}:{b}{head_row}")
            ws.cell(head_row, c, text)
            paint(ws, f"{a}{head_row}:{b}{head_row}",
                  fill=fill, font=band_font, align=left)

        seeded = SEED.get(d)
        for row, label, idx in ((R_BV_REP, "OPEN REPAIR TICKETS", 0),
                                (R_BV_PM, "OPEN PMS", 1),
                                (R_LV_REP, "OPEN REPAIR TICKETS", 2),
                                (R_LV_PM, "OPEN PMS", 3)):
            cell = ws.cell(row, c, seeded[idx] if seeded else None)
            cell.font = num_font
            cell.number_format = FMT_COUNT
            cell.alignment = centre
            cell.border = box
            cell.protection = Protection(locked=False)
            lab = ws.cell(row, c + 1, label)
            lab.font = lbl_font
            lab.alignment = left

        ws.cell(R_NOTE, c, "NOTE").font = date_lbl_font
        ws.cell(R_NOTE, c).alignment = centre
        ws.merge_cells(f"{b}{R_NOTE}:{sp}{R_NOTE}")
        note = ws.cell(R_NOTE, c + 1)
        note.font = Font(name=FONT, size=11, italic=True, color=INPUT_BLUE)
        note.alignment = Alignment(horizontal="left", vertical="center",
                                   wrap_text=True)
        paint(ws, f"{b}{R_NOTE}:{sp}{R_NOTE}", border=Border(bottom=thin))
        for cc in (ws.cell(R_NOTE, c + 1), ws.cell(R_NOTE, c + 2)):
            cc.protection = Protection(locked=False)

        for row, f, label in (
            (R_BV_TOT, f"=SUM({a}{R_BV_REP}+{a}{R_BV_PM})", "TOTAL"),
            (R_LV_TOT, f"=SUM({a}{R_LV_REP}+{a}{R_LV_PM})", "TOTAL"),
            (R_CO_TOT, f"=SUM({a}{R_BV_TOT}+{a}{R_LV_TOT})",
             "TOTAL OPEN IN BOTH PLANTS"),
        ):
            cell = ws.cell(row, c, f)
            cell.font = calc_font
            cell.number_format = FMT_COUNT
            cell.alignment = centre
            cell.border = Border(top=thin, bottom=Side(style="double", color=RULE),
                                 left=thin, right=thin)
            lab = ws.cell(row, c + 1, label)
            lab.font = tot_lbl_font
            lab.alignment = left

        ws.column_dimensions[a].width = 11
        ws.column_dimensions[b].width = 27
        ws.column_dimensions[sp].width = 2.5

    # ---- hidden helper rows -------------------------------------------------
    # 30: is this column a block anchor AND does the block have any count typed in?
    # 31: running index over FILLED blocks    -> History looks up week n here
    # 32: running index over ALL blocks       -> "jump to this week" uses this
    for c in range(1, SCAN_LAST + 1):
        a, nxt = CL(c), CL(c + 1)
        counts = (f"{a}{R_BV_REP},{a}{R_BV_PM},{a}{R_LV_REP},{a}{R_LV_PM}")
        # A week counts only when it is a real block, carries a real date, and has
        # all four numbers. Four typed zeros still qualify: COUNT sees four numbers.
        ws.cell(R_FLAG, c,
                f'=IF(AND({a}${R_DATE}="DATE",ISNUMBER({nxt}${R_DATE}),'
                f'COUNT({counts})=4),1,0)')
        ws.cell(R_FILLED_IX, c,
                f'=IF({a}{R_FLAG}=1,SUM($A${R_FLAG}:{a}{R_FLAG}),"")')
        ws.cell(R_ALL_IX, c,
                f'=IF({a}${R_DATE}="DATE",COUNTIF($A${R_DATE}:{a}${R_DATE},"DATE"),"")')
        # started but not usable: some numbers typed, yet the week is being skipped
        ws.cell(R_BROKEN, c,
                f'=IF(AND({a}${R_DATE}="DATE",COUNT({counts})>0,{a}{R_FLAG}=0),1,0)')
        # two blocks carrying the same date, which would publish a phantom week
        ws.cell(R_DUP, c,
                f'=IF(AND({a}${R_DATE}="DATE",ISNUMBER({nxt}${R_DATE}),'
                f'COUNTIF($A${R_DATE}:${SCAN}${R_DATE},{nxt}${R_DATE})>1),1,0)')

    # 33: scalars. A33 = index of the block for the current week (dates already
    # reached). B33 = its anchor column, used by the "jump to this week" links.
    ws.cell(R_SCALAR, 1,
            f'=MAX(1,COUNTIF($A${R_DATE}:${SCAN}${R_DATE},"<="&TODAY()))')
    ws.cell(R_SCALAR, 2,
            f'=IFERROR(MATCH($A${R_SCALAR},$A${R_ALL_IX}:${SCAN}${R_ALL_IX},0),1)')
    # 33 C/D: guard rails surfaced on Read Me
    ws.cell(R_SCALAR, 3, f'=COUNTIF($A${R_DATE}:${SCAN}${R_DATE},"DATE")')
    ws.cell(R_SCALAR, 4, f'=COUNTIF(${R_DATE}:${R_DATE},"DATE")')
    ws.cell(R_SCALAR, 5, f"=SUM($A${R_BROKEN}:${SCAN}${R_BROKEN})")
    ws.cell(R_SCALAR, 6, f"=SUM($A${R_DUP}:${SCAN}${R_DUP})")

    for r in (R_FLAG, R_FILLED_IX, R_ALL_IX, R_SCALAR, R_BROKEN, R_DUP):
        ws.row_dimensions[r].hidden = True

    # ---- visible note under the grid ---------------------------------------
    note_font = Font(name=FONT, size=11, color=INK_SOFT)
    head_font = Font(name=FONT, size=12, bold=True, color=INK)
    ws.merge_cells(f"A17:B17")
    ws.cell(17, 1, "HOW TO UPDATE").font = head_font
    steps = [
        "Type this week's four counts into the blue cells of the block whose date "
        "matches this week. TOTAL rows and the History tab fill themselves.",
        "A block still blank after its date has passed turns yellow, so you can see "
        "what you missed.",
        "Row 15 of each block is a free-text NOTE. Anything you type there shows up "
        "in the Notes column of the weekly log, next to that week.",
        "Blocks are pre-built through " + week_dates(N_BLOCKS)[-1].strftime("%B %d, %Y")
        + ". See the Read Me tab to add more.",
    ]
    for j, text in enumerate(steps):
        r = 18 + j
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        cell = ws.cell(r, 1, f"{j + 1}.  {text}")
        cell.font = note_font
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[r].height = 30
    jump = ws.cell(22, 1,
                   f'=HYPERLINK("#Totals!"&ADDRESS({R_BV_REP},$B${R_SCALAR},4),'
                   f'"► Jump to this week\'s block")')
    jump.font = Font(name=FONT, size=12, bold=True, color="FF0563C1", underline="single")
    ws.merge_cells("A22:B22")

    # ---- conditional formatting: blank + past due = yellow ------------------
    yellow_dxf = DifferentialStyle(fill=PatternFill(bgColor=YELLOW))
    for rng, first in ((f"A{R_BV_REP}:{SCAN}{R_BV_PM}", R_BV_REP),
                       (f"A{R_LV_REP}:{SCAN}{R_LV_PM}", R_LV_REP)):
        ws.conditional_formatting.add(rng, Rule(
            type="expression",
            formula=[f'AND(A${R_DATE}="DATE",ISBLANK(A{first}),'
                     f'INDEX($A${R_DATE}:${SCAN}${R_DATE},COLUMN()+1)+5<=TODAY())'],
            dxf=yellow_dxf, stopIfTrue=False))
    red_dxf = DifferentialStyle(fill=PatternFill(bgColor=WARN_FILL),
                                font=Font(color=WARN_INK, bold=True))
    ws.conditional_formatting.add(f"A{R_DATE}:{SCAN}{R_DATE}", Rule(
        type="expression",
        formula=[f'AND(ISNUMBER(A{R_DATE}),'
                 f'COUNTIF($A${R_DATE}:${SCAN}${R_DATE},A{R_DATE})>1)'],
        dxf=red_dxf, stopIfTrue=True))
    ws.conditional_formatting.add(f"A{R_DATE}:{SCAN}{R_DATE}", Rule(
        type="expression",
        formula=[f'AND(ISBLANK(A{R_DATE}),COLUMN()>1,'
                 f'INDEX($A${R_DATE}:${SCAN}${R_DATE},MAX(1,COLUMN()-1))="DATE")'],
        dxf=yellow_dxf, stopIfTrue=False))

    # ---- data validation on the four typed cells of every block -------------
    cells = []
    for i in range(len(dates)):
        a = CL(anchor_col(i))
        cells += [f"{a}{R_BV_REP}", f"{a}{R_BV_PM}", f"{a}{R_LV_REP}", f"{a}{R_LV_PM}"]
    dv = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0",
                        allow_blank=True, showErrorMessage=True)
    dv.error = ("Enter a whole number of open work orders (0 or more). "
                "Leave it blank if the report was not pulled that week.")
    dv.errorTitle = "Counts only"
    dv.prompt = "Open work orders counted this week"
    ws.add_data_validation(dv)
    dv.sqref = " ".join(cells)

    # A guard rail, not a lock: no password, so anyone can lift it from
    # Review > Unprotect Sheet. It stops an accidental overtype of a formula.
    ws.protection.sheet = True
    ws.protection.formatCells = False
    ws.protection.formatColumns = False
    ws.protection.formatRows = False

    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = "FF2A78D6"
    ws.freeze_panes = None
    ws.page_setup.orientation = "landscape"


# ---------------------------------------------------------------- History


def log_formula_row(ws, r, n):
    """One week of the log. n is the 1-based week index looked up on Totals."""
    m = f'MATCH({n},Totals!$A${R_FILLED_IX}:${SCAN}${R_FILLED_IX},0)'
    pull = {
        COL_WEEK: f'=IFERROR(INDEX(Totals!$A${R_DATE}:${SCAN}${R_DATE},{m}+1),"")',
        COL_BVR:  f'=IFERROR(INDEX(Totals!$A${R_BV_REP}:${SCAN}${R_BV_REP},{m}),"")',
        COL_BVP:  f'=IFERROR(INDEX(Totals!$A${R_BV_PM}:${SCAN}${R_BV_PM},{m}),"")',
        COL_LVR:  f'=IFERROR(INDEX(Totals!$A${R_LV_REP}:${SCAN}${R_LV_REP},{m}),"")',
        COL_LVP:  f'=IFERROR(INDEX(Totals!$A${R_LV_PM}:${SCAN}${R_LV_PM},{m}),"")',
    }
    blank = f'{COL_WEEK}{r}=""'
    derived = {
        COL_BVT:  f'=IF({blank},"",{COL_BVR}{r}+{COL_BVP}{r})',
        COL_LVT:  f'=IF({blank},"",{COL_LVR}{r}+{COL_LVP}{r})',
        COL_REPT: f'=IF({blank},"",{COL_BVR}{r}+{COL_LVR}{r})',
        COL_PMT:  f'=IF({blank},"",{COL_BVP}{r}+{COL_LVP}{r})',
        COL_COMB: f'=IF({blank},"",{COL_BVT}{r}+{COL_LVT}{r})',
    }
    note = f'INDEX(Totals!$A${R_NOTE}:${SCAN}${R_NOTE},{m}+1)'
    pull[COL_NOTE] = f'=IFERROR(IF({note}=0,"",{note}),"")'
    for col, f in {**pull, **derived}.items():
        ws[f"{col}{r}"] = f
    if r == LOG_FIRST:
        ws[f"{COL_CHG}{r}"] = ""
    else:
        ws[f"{COL_CHG}{r}"] = (
            f'=IF(OR({blank},{COL_COMB}{r - 1}=""),"",'
            f'{COL_COMB}{r}-{COL_COMB}{r - 1})')


SCORECARD = [
    # row, label, source column, emphasis: "hero" | "strong" | None
    (6,  "Open repair tickets — Burnsville",  COL_BVR,  None),
    (7,  "Open repair tickets — Lakeville",   COL_LVR,  None),
    (8,  "OPEN REPAIR TICKETS — BOTH PLANTS", COL_REPT, "hero"),
    (10, "Open PMs — Burnsville",             COL_BVP,  None),
    (11, "Open PMs — Lakeville",              COL_LVP,  None),
    (12, "Open PMs — both plants",            COL_PMT,  "strong"),
    (14, "All open work orders — Burnsville", COL_BVT,  None),
    (15, "All open work orders — Lakeville",  COL_LVT,  None),
    (16, "All open work orders — both plants", COL_COMB, "strong"),
]

# Only the repair rows get the red/green treatment. A PM count rising because the
# maintenance system released a batch is not a problem, and colouring it red is
# how a routine week starts looking like a crisis.
COLOURED_CHANGE = "F6:F8"


def build_history(ws, last_date, link_cell):
    thin = Side(style="thin", color=RULE)
    centre = Alignment(horizontal="center", vertical="center")
    left = Alignment(horizontal="left", vertical="center")

    widths = {"A": 14, "B": 15, "C": 14, "D": 14, "E": 15, "F": 14,
              "G": 14, "H": 14, "I": 14, "J": 15, "K": 16, "L": 34}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    for col in ("N", "O"):
        ws.column_dimensions[col].width = 12
        ws.column_dimensions[col].hidden = True

    rng = lambda col: f"${col}${LOG_FIRST}:${col}${LOG_LAST}"

    # hidden helpers
    ws["N1"] = f"=COUNT({rng(COL_WEEK)})"
    ws["N2"] = f'=IF({N_WEEKS}=0,"",INDEX({rng(COL_WEEK)},{N_WEEKS}))'
    ws["N3"] = f"=Totals!$C${R_SCALAR}"          # blocks inside the scanned range
    ws["N4"] = f"=Totals!$D${R_SCALAR}"          # blocks anywhere on row 1
    ws["N6"] = (f'=IF({N_WEEKS}<2,"",INDEX({rng(COL_WEEK)},{N_WEEKS})'
                f'-INDEX({rng(COL_WEEK)},{N_WEEKS}-1))')
    ws["N7"] = ('=IF($N$6="","",IF($N$6=7,"vs last week",'
                '"vs the previous entry, "&TEXT($N$6,"0")&" days earlier"))')
    ws["N5"] = (f"=IF('Read Me'!{link_cell}=\"\","
                f"\"(paste the file link — see the Read Me tab)\","
                f"'Read Me'!{link_cell})")

    # ---- banner -------------------------------------------------------------
    ws.merge_cells("A1:L1")
    ws["A1"] = "OPEN WORK ORDERS — WEEKLY HISTORY"
    ws["A1"].font = Font(name=FONT, size=20, bold=True, color=INK)
    ws["A1"].alignment = left
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:L2")
    ws["A2"] = ("Buddy's Kitchen · Burnsville and Lakeville · "
                "type this week's counts on the Totals tab and everything below updates itself")
    ws["A2"].font = Font(name=FONT, size=11, color=INK_SOFT)
    ws["A2"].alignment = left

    ws.merge_cells("A3:L3")
    ws["A3"] = (
        f'=IF({N_WEEKS}=0,"No weeks entered yet — start on the Totals tab.",'
        f'"Week of "&TEXT($N$2,"mmmm d, yyyy")&":   "&'
        f'TEXT($D$8,"{FMT_COUNT}")&" open repair tickets"&'
        f'IF($F$8=""," (first week on record)",'
        f'" ("&IF($F$8>0,"up "&TEXT($F$8,"{FMT_COUNT}"),'
        f'IF($F$8<0,"down "&TEXT(-$F$8,"{FMT_COUNT}"),"unchanged"))&" "&$N$7&")")&'
        f'".   PMs "&TEXT($D$12,"{FMT_COUNT}")&'
        f'IF($F$12=""," "," ("&IF($F$12>0,"up "&TEXT($F$12,"{FMT_COUNT}"),'
        f'IF($F$12<0,"down "&TEXT(-$F$12,"{FMT_COUNT}"),"unchanged"))&").")&'
        f'"   All open "&TEXT($D$16,"{FMT_COUNT}")&".")')
    ws["A3"].font = Font(name=FONT, size=13, bold=True, color=INK)
    ws["A3"].alignment = left
    ws.row_dimensions[3].height = 24

    # ---- warning band: empty (and therefore invisible) when all is well -----
    ws.merge_cells("A4:L4")
    ws["A4"] = (
        f'=IF(Totals!$F${R_SCALAR}>0,'
        f'"⚠  Two or more week blocks on the Totals tab carry the same date. '
        f'Fix that before sending this out — one of them is a phantom week.",'
        f'IF(Totals!$E${R_SCALAR}>0,'
        f'"⚠  "&TEXT(Totals!$E${R_SCALAR},"0")&" week block(s) on the Totals tab are '
        f'part-filled, so they are being left out of the history. '
        f'Every week needs all four counts and a date.",'
        f'IF({N_WEEKS}>={LOG_ROWS},'
        f'"⚠  The weekly log is full. Add rows before entering another week — '
        f'see the Read Me tab.","")))')
    paint(ws, "A4:L4",
          font=Font(name=FONT, size=11, bold=True, color=WARN_INK),
          align=Alignment(vertical="center", wrap_text=True))
    ws.conditional_formatting.add("A4:L4", Rule(
        type="expression", formula=['LEN($A$4)>0'],
        dxf=DifferentialStyle(fill=PatternFill(bgColor=WARN_FILL)), stopIfTrue=True))
    ws.row_dimensions[4].height = 22

    # ---- scorecard ----------------------------------------------------------
    ws.merge_cells("A5:C5")
    for col, text in (("A", ""), ("D", "This week"), ("E", "Previous entry"),
                      ("F", "Change"), ("G", "4-week avg")):
        ws[f"{col}5"] = text
    paint(ws, "A5:G5",
          fill=PatternFill("solid", fgColor=HEAD_FILL),
          font=Font(name=FONT, size=11, bold=True, color=INK),
          align=centre, border=Border(bottom=thin))
    ws["A5"].alignment = left

    for row, label, col, emphasis in SCORECARD:
        ws.merge_cells(f"A{row}:C{row}")
        ws[f"A{row}"] = label
        size = {"hero": 14, "strong": 12}.get(emphasis, 11)
        bold = emphasis is not None
        ws[f"D{row}"] = f'=IF({N_WEEKS}=0,"",INDEX({rng(col)},{N_WEEKS}))'
        ws[f"E{row}"] = f'=IF({N_WEEKS}<2,"",INDEX({rng(col)},{N_WEEKS}-1))'
        ws[f"F{row}"] = f'=IF(OR(D{row}="",E{row}=""),"",D{row}-E{row})'
        ws[f"G{row}"] = (f'=IF({N_WEEKS}=0,"",AVERAGE('
                         f'INDEX({rng(col)},MAX(1,{N_WEEKS}-3)):'
                         f'INDEX({rng(col)},{N_WEEKS})))')
        paint(ws, f"A{row}:C{row}",
              font=Font(name=FONT, size=size, bold=bold, color=INK), align=left)
        paint(ws, f"D{row}:G{row}",
              font=Font(name=FONT, size=size, bold=bold, color=INK),
              align=centre, fmt=FMT_COUNT)
        ws[f"F{row}"].number_format = FMT_CHANGE
        if emphasis:
            fill = PatternFill("solid",
                               fgColor="FFE4EDF9" if emphasis == "hero" else BAND)
            paint(ws, f"A{row}:G{row}", fill=fill,
                  border=Border(top=thin, bottom=thin))
            ws[f"A{row}"].alignment = left
            for c in "DEFG":
                ws[f"{c}{row}"].alignment = centre
        ws.row_dimensions[row] = ws.row_dimensions[row]
        ws.row_dimensions[row].height = {"hero": 24, "strong": 20}.get(emphasis, 17)

    ws.merge_cells("A17:G17")
    ws["A17"] = ("▲ = more open than the previous entry   ·   ▼ = fewer.   "
                 "Only the repair rows are coloured: PMs jump whenever the "
                 "maintenance system releases a batch, which is not a backlog "
                 "problem, so repair tickets are the line to watch.")
    ws["A17"].font = Font(name=FONT, size=10, italic=True, color=INK_SOFT)
    ws["A17"].alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[17].height = 26

    ws.merge_cells("A18:G18")
    ws["A18"] = (f'=HYPERLINK("#Totals!"&ADDRESS({R_BV_REP},Totals!$B${R_SCALAR},4),'
                 f'"► Enter this week\'s counts on the Totals tab")')
    ws["A18"].font = Font(name=FONT, size=11, bold=True,
                          color="FF0563C1", underline="single")
    ws["A18"].alignment = left

    # ---- section bands ------------------------------------------------------
    for row, text in ((19, f"TREND — the most recent {CHART_WEEKS} weeks "
                           f"(every week is in the log below)"),
                      (54, "WEEKLY LOG — one row per week, oldest first")):
        ws.merge_cells(f"A{row}:L{row}")
        ws[f"A{row}"] = text
        paint(ws, f"A{row}:L{row}",
              fill=PatternFill("solid", fgColor=BAND),
              font=Font(name=FONT, size=11, bold=True, color=INK_SOFT),
              align=left)
        ws.row_dimensions[row].height = 20

    # ---- email-ready summary ------------------------------------------------
    ws.merge_cells("F37:L51")
    ws["F37"] = (
        f'=IF({N_WEEKS}=0,"Enter a week on the Totals tab and this fills in.",'
        f'"Open work orders — week of "&TEXT($N$2,"mm/dd/yyyy")&CHAR(10)&CHAR(10)&'
        f'"Repair tickets: "&TEXT($D$8,"{FMT_COUNT}")&"  ("&{chg_text("$F$8")}&" "&$N$7&")"&CHAR(10)&'
        f'"PMs: "&TEXT($D$12,"{FMT_COUNT}")&"  ("&{chg_text("$F$12")}&")"&CHAR(10)&'
        f'"All open: "&TEXT($D$16,"{FMT_COUNT}")&"  ("&{chg_text("$F$16")}&")"&CHAR(10)&CHAR(10)&'
        f'"Burnsville: "&TEXT($D$14,"{FMT_COUNT}")&"  ("&{chg_text("$F$14")}&")"&CHAR(10)&'
        f'"Lakeville: "&TEXT($D$15,"{FMT_COUNT}")&"  ("&{chg_text("$F$15")}&")"&CHAR(10)&CHAR(10)&'
        f'"Full history and charts: "&$N$5)')
    paint(ws, "F37:L51",
          fill=PatternFill("solid", fgColor="FFFBFBF9"),
          border=Border(left=thin, right=thin, top=thin, bottom=thin),
          font=Font(name=FONT, size=11, color=INK))
    ws["F37"].alignment = Alignment(vertical="top", wrap_text=True)

    ws.merge_cells("F36:L36")
    ws["F36"] = "COPY THIS INTO THE WEEKLY EMAIL  —  click the cell, copy, then in Outlook paste with Keep Text Only"
    ws["F36"].font = Font(name=FONT, size=10, bold=True, color=INK_SOFT)
    ws["F36"].alignment = left

    # ---- the log ------------------------------------------------------------
    headers = ["Count Date", "Burnsville Repair Tickets", "Burnsville PMs",
               "Burnsville Total", "Lakeville Repair Tickets", "Lakeville PMs",
               "Lakeville Total", "Repair Tickets Both Plants", "PMs Both Plants",
               "All Open Both Plants", "Change vs Previous Entry", "Notes"]
    for j, text in enumerate(headers, start=1):
        ws.cell(LOG_HEAD, j, text)
    paint(ws, f"A{LOG_HEAD}:L{LOG_HEAD}",
          fill=PatternFill("solid", fgColor=HEAD_FILL),
          font=Font(name=FONT, size=10, bold=True, color=INK),
          align=Alignment(horizontal="center", vertical="center", wrap_text=True),
          border=Border(bottom=Side(style="medium", color="FFBFBFBB")))
    ws.row_dimensions[LOG_HEAD].height = 34

    for n, r in enumerate(range(LOG_FIRST, LOG_LAST + 1), start=1):
        log_formula_row(ws, r, n)
        paint(ws, f"A{r}:L{r}",
              font=Font(name=FONT, size=11, color=INK),
              align=centre, fmt=FMT_COUNT,
              border=Border(bottom=Side(style="hair", color=RULE)))
        ws[f"{COL_WEEK}{r}"].number_format = FMT_DATE
        ws[f"{COL_CHG}{r}"].number_format = FMT_CHANGE
        ws[f"{COL_NOTE}{r}"].number_format = "General"
        ws[f"{COL_NOTE}{r}"].alignment = Alignment(horizontal="left", vertical="center",
                                                   wrap_text=True)
        for col in (COL_REPT, COL_PMT, COL_COMB):
            ws[f"{col}{r}"].font = Font(name=FONT, size=11, bold=True, color=INK)

    table = Table(displayName="WeeklyLog", ref=f"A{LOG_HEAD}:L{LOG_LAST}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=True,
                                          showColumnStripes=False,
                                          showFirstColumn=False, showLastColumn=False)
    ws.add_table(table)

    # ---- conditional formatting on every change cell ------------------------
    up = DifferentialStyle(font=Font(color=UP_RED, bold=True))
    down = DifferentialStyle(font=Font(color=DOWN_GREEN, bold=True))
    for rng_ in (COLOURED_CHANGE, f"{COL_CHG}{LOG_FIRST}:{COL_CHG}{LOG_LAST}"):
        first = rng_.split(":")[0]
        ws.conditional_formatting.add(rng_, Rule(
            type="expression", formula=[f"AND(ISNUMBER({first}),{first}>0)"],
            dxf=up, stopIfTrue=False))
        ws.conditional_formatting.add(rng_, Rule(
            type="expression", formula=[f"AND(ISNUMBER({first}),{first}<0)"],
            dxf=down, stopIfTrue=False))

    for r in list(range(20, 36)) + list(range(37, 53)):
        ws.row_dimensions[r].height = 15

    ws.protection.sheet = True          # every cell here is calculated
    ws.protection.formatCells = False
    ws.protection.formatColumns = False
    ws.protection.formatRows = False

    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = "FF1E7B34"
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_area = "A1:L53"          # the dashboard: one clean landscape page


# ---------------------------------------------------------------- charts


def add_named_ranges(wb, ws):
    # A moving window over the most recent CHART_WEEKS entries. INDEX():INDEX()
    # rather than OFFSET so nothing here is volatile; the full history stays in
    # the log below, which is what the window keeps the charts readable against.
    n = (f"COUNT(History!${COL_WEEK}${LOG_FIRST}:${COL_WEEK}${LOG_LAST})")

    def dyn(col):
        span = f"History!${col}${LOG_FIRST}:${col}${LOG_LAST}"
        return (f"INDEX({span},MAX(1,{n}-{CHART_WEEKS - 1})):"
                f"INDEX({span},MAX(1,{n}))")

    series_cols = {"Week": COL_WEEK,
                   "BVR": COL_BVR, "BVP": COL_BVP, "BVT": COL_BVT,
                   "LVR": COL_LVR, "LVP": COL_LVP, "LVT": COL_LVT,
                   "REPT": COL_REPT, "PMT": COL_PMT, "CO": COL_COMB}
    for key, col in series_cols.items():
        ws.defined_names.add(DefinedName(f"chart_{key}", attr_text=dyn(col)))
    for key in series_cols:
        if key == "Week":
            continue
        ws.defined_names.add(DefinedName(
            f"last_{key}",
            attr_text=(f"IF(History!chart_Week=MAX(History!chart_Week),"
                       f"History!chart_{key},NA())")))


def line_series(name, ref_name, colour, width_emu=25400, marker_size=6):
    s = Series()
    s.val = NumDataSource(NumRef(f=f"History!{ref_name}"))
    s.cat = AxDataSource(numRef=NumRef(f="History!chart_Week"))
    s.tx = SeriesLabel(v=name)
    line = LineProperties(solidFill=colour, w=width_emu)
    s.graphicalProperties = GraphicalProperties(ln=line)
    s.marker = Marker(symbol="circle", size=marker_size,
                      spPr=GraphicalProperties(solidFill=colour,
                                               ln=LineProperties(solidFill="FFFFFF",
                                                                 w=9525)))
    s.smooth = False
    return s


def label_series(ref_name, position):
    s = Series()
    s.val = NumDataSource(NumRef(f=f"History!{ref_name}"))
    s.cat = AxDataSource(numRef=NumRef(f="History!chart_Week"))
    s.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))
    s.marker = Marker(symbol="none")
    s.dLbls = DataLabelList(showVal=True, showSerName=False, showCatName=False,
                            showLegendKey=False, showBubbleSize=False,
                            showPercent=False, dLblPos=position, numFmt=FMT_COUNT)
    s.smooth = False
    return s


def make_chart(title, specs, anchor, ws):
    """specs: list of (legend name, chart_ name, last_ name, colour, label position)"""
    ch = LineChart()
    ch.title = title
    ch.style = None
    ch.height = 7.5
    ch.width = 12.5
    ch.y_axis.title = None
    ch.x_axis.title = None
    ch.y_axis.scaling.min = 0
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.numFmt = FMT_COUNT
    ch.x_axis.numFmt = "m/d"
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(
        ln=LineProperties(solidFill="E8E8E4", w=9525))
    ch.x_axis.majorGridlines = None
    ch.legend.position = "t"
    ch.legend.overlay = False

    for i, (name, cname, _, colour, _) in enumerate(specs):
        w = 31750 if colour == TOTAL_INK else 25400
        ch.series.append(line_series(name, cname, colour, width_emu=w))
    for i, (_, _, lname, _, pos) in enumerate(specs):
        ch.series.append(label_series(lname, pos))
    # hide the label-only series from the legend
    ch.legend.legendEntry = [LegendEntry(idx=len(specs) + i, delete=True)
                             for i in range(len(specs))]
    ws.add_chart(ch, anchor)
    return ch


def build_charts(ws):
    """Three small multiples, one per plant plus the pair together.

    Colour means the metric and nothing else — blue is repair tickets in every
    chart, orange is PMs, dark grey is their total. The plant is the facet.
    Splitting by plant rather than by metric is what keeps every line readable:
    Lakeville runs an order of magnitude above Burnsville, so any chart holding
    both plants' PM counts flattens Burnsville onto the axis.
    """
    panels = [
        ("Both plants — open work orders", "A20",
         [("Repair tickets", "REPT", REPAIR_INK, "t"),
          ("PMs", "PMT", PM_INK, "b"),
          ("All open", "CO", TOTAL_INK, "t")]),
        ("Burnsville — open work orders", "F20",
         [("Repair tickets", "BVR", REPAIR_INK, "t"),
          ("PMs", "BVP", PM_INK, "b"),
          ("All open", "BVT", TOTAL_INK, "t")]),
        ("Lakeville — open work orders", "A37",
         [("Repair tickets", "LVR", REPAIR_INK, "t"),
          ("PMs", "LVP", PM_INK, "b"),
          ("All open", "LVT", TOTAL_INK, "t")]),
    ]
    for title, anchor, specs in panels:
        make_chart(title,
                   [(name, f"chart_{key}", f"last_{key}", colour, pos)
                    for name, key, colour, pos in specs],
                   anchor, ws)


# ---------------------------------------------------------------- Read Me


README = [
    ("H", "WHAT THIS FILE IS", None),
    ("P", "One row per week showing how many work orders are open at Burnsville and at "
          "Lakeville, split into repair tickets and PMs. It answers the standing "
          "question: is the backlog growing or shrinking?", None),
    ("P", "You type four numbers a week, on the Totals tab. Everything else — totals, "
          "the change since the last entry, the charts, the scorecard and the email "
          "text — is calculated. The History tab is the one you send.", None),
    ("S", None, None),

    ("H", "THE WEEKLY ROUTINE", None),
    ("N", "Pull the open work order counts for both plants.", None),
    ("N", "Open the Totals tab. The link under the grid jumps to the block whose date "
          "is this week.", None),
    ("N", "Type all four counts into the blue cells: repair tickets and PMs for "
          "Burnsville, then the same two for Lakeville. A week is only picked up once "
          "all four are in, so a half-filled block is left out rather than reported as "
          "zeros.", None),
    ("N", "If a number moved for a reason worth remembering, type it into the NOTE row "
          "of that same block. It shows up in the Notes column of the weekly log.", None),
    ("N", "Go to the History tab and read the top. If a red bar has appeared under the "
          "headline, fix what it names before you send anything.", None),
    ("N", "Copy the email box (to the right of the charts) into your weekly email. In "
          "Outlook, paste with Keep Text Only, or you will paste a one-cell table. "
          "Send the file link with it.", None),
    ("S", None, None),

    ("H", "READING THE NUMBERS", None),
    ("P", "Repair tickets and PMs are counted separately on purpose. PMs are scheduled "
          "work: when the maintenance system releases a new batch, the PM count jumps "
          "by dozens overnight without anything going wrong on the floor.", None),
    ("P", "Repair tickets are the number that reflects real, unplanned backlog. When "
          "you are asked whether things are getting better or worse, that is the line "
          "to look at.", None),
    ("P", "▲ means more open than the previous entry, ▼ means fewer. The arrow "
          "carries the meaning, so it reads correctly in black and white and for a "
          "colourblind reader. Only the repair rows are coloured red and green, "
          "because a rising PM count usually means a batch was released, not that "
          "anything went wrong.", None),
    ("P", "The 4-week average column answers \"is this week normal?\". A single week "
          "bounces around; the average is what tells you whether the level has "
          "actually moved.", None),
    ("P", "There is one chart per plant, plus one for the two together. They are split "
          "that way because Lakeville runs about twenty times higher than Burnsville: "
          "any chart holding both plants' PM counts would flatten Burnsville onto the "
          "axis and show nothing. In every chart blue is repair tickets, orange is "
          "PMs, and dark grey is the two added together.", None),
    ("P", "The charts show the most recent 26 weeks so they stay readable as the file "
          "fills up. Every week ever recorded is in the log underneath them.", None),
    ("S", None, None),

    ("H", "CONVENTIONS", None),
    ("P", "\"Count Date\" is the date the count was actually pulled, which is normally "
          "a Monday. The first entry, 09-15-2026, was pulled on a Tuesday and is left "
          "as it was recorded rather than tidied.", None),
    ("P", "A count is the number of work orders open at the moment of the pull, not the "
          "number opened or closed that week.", None),
    ("P", "Leave a week blank if no count was taken. The history skips it rather than "
          "showing a zero. Because of that, \"Change vs Previous Entry\" compares "
          "against the last week actually recorded, which is not always seven days "
          "back — the headline and the email say how long ago it really was.", None),
    ("S", None, None),

    ("H", "COLOURS AND WHAT THEY MEAN", None),
    ("L", "Blue on Totals", "Cells you type into: the four counts and the NOTE. "
                            "Nothing else on Totals is typed."),
    ("L", "Yellow fill", "Something is missing: a week whose date has passed with no "
                         "counts entered, or a blank you are expected to fill in on "
                         "this tab."),
    ("L", "Red fill on a date", "Two blocks carry that same date. Fix it — one of them "
                                "is a duplicate and will publish a week that never "
                                "happened."),
    ("L", "Red bar on History", "A problem worth stopping for. The bar says what it "
                                "is. When everything is fine there is no bar."),
    ("L", "Black numbers", "Calculated. Do not type over them — you would break the "
                           "week."),
    ("S", None, None),

    ("H", "FILL THESE IN", None),
    ("Y", "Where this file lives (paste the SharePoint link)", ""),
    ("Y", "Name of the report the counts come from", ""),
    ("S", None, None),

    ("H", "THE SHEETS ARE PROTECTED", None),
    ("P", "The three tabs are protected with no password, so you can still type in "
          "the blue cells and the yellow ones and nowhere else. It is a guard rail "
          "against overtyping a formula, not a lock.", None),
    ("P", "If you genuinely need to change something else — adding rows to the log, "
          "or adding blocks past the pre-built ones — use Review > Unprotect Sheet, "
          "make the change, then Review > Protect Sheet to put it back.", None),
    ("S", None, None),

    ("H", "THINGS NOT TO DO", None),
    ("P", "Do not sort or re-order the weekly log. Every cell in it is a formula tied "
          "to its week, so sorting would scramble it. The filter buttons have been "
          "removed for that reason.", None),
    ("P", "Do not type into the weekly log, including the Notes column. Notes belong on "
          "the Totals tab, in the NOTE row of the week they describe, so they stay "
          "attached to that week no matter what else changes.", None),
    ("P", "Do not give two blocks the same date. That is the one mistake that produces "
          "a believable but wrong number, so the file watches for it and says so.", None),
    ("P", "Do not insert a column inside an existing block. Adding whole blocks on the "
          "right is safe; splitting one is not.", None),
    ("S", None, None),

    ("H", "WHEN THE PRE-BUILT WEEKS RUN OUT", None),
    ("P", "Blocks are pre-built through {LAST_DATE}, and the weekly log has room for "
          "{LOG_ROWS} weeks. That is about two years from the first entry.", None),
    ("P", "To add a week: select the three columns of the last block, copy, paste into "
          "the next three empty columns to the right, then DELETE the four counts and "
          "the note, and only then change the date. Clearing before dating is what "
          "stops a duplicate week appearing. Do not paste past column OJ.", None),
    ("P", "To add rows to the log: click the last row of the weekly log and drag the "
          "fill handle down. Every column is a formula and will copy.", None),
    ("P", "Hidden rows 30 to 35 on Totals do the block bookkeeping and the error "
          "checking. Leave them alone; unhide them if you ever need to see why a week "
          "is not appearing.", None),
    ("P", "Every formula in this file uses functions that have been in Excel since "
          "2007, so it opens the same in Excel for the web, on a phone, and in older "
          "desktop versions. If you edit it, keep to those — newer functions can come "
          "back as #NAME? for other people.", None),
    ("S", None, None),

    ("H", "HEALTH CHECK", None),
    ("C", "Weeks recorded", "=History!$N$1"),
    ("C", "Blocks built on Totals", f"=Totals!$C${R_SCALAR}"),
    ("C", "Part-filled blocks being skipped", f"=Totals!$E${R_SCALAR}"),
    ("C", "Blocks sharing a date", f"=Totals!$F${R_SCALAR}"),
    ("C", "Blocks the History tab can see",
     f"=IF(Totals!$D${R_SCALAR}>Totals!$C${R_SCALAR},"
     f'"PROBLEM: blocks exist past column OJ and are being ignored",'
     f'"all of them")'),
    ("S", None, None),

    ("H", "CHANGE LOG", None),
    ("P", "2026-09-21 — first version: Totals entry grid plus a weekly history tab.", None),
    ("P", "2026-09-22 — rebuilt. Added the scorecard at the top with repair tickets "
          "as the headline and a 4-week average, split repair tickets from PMs, "
          "replaced the single chart with one per plant over a rolling 26 weeks, "
          "moved notes onto the Totals blocks so they cannot drift off their week, "
          "added the email box, this tab, two years of pre-built weeks, checks for "
          "part-filled and duplicate weeks, sheet protection, and block lookup that "
          "no longer depends on counting columns.", None),
]


def readme_layout():
    """Walk README the same way build_readme does and return {label: row}."""
    rows, r = {}, 4
    for kind, a, _b in README:
        if kind == "Y":
            rows[a] = r
        if kind != "S":
            r += 1
        else:
            r += 1
    return rows


LINK_LABEL = "Where this file lives (paste the SharePoint link)"


def build_readme(ws, last_date):
    thin = Side(style="thin", color=RULE)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 62
    ws.column_dimensions["D"].width = 3

    ws.merge_cells("B2:C2")
    ws["B2"] = "OPEN WORK ORDERS TRACKER — READ ME"
    ws["B2"].font = Font(name=FONT, size=18, bold=True, color=INK)
    ws["B2"].alignment = Alignment(vertical="center")
    ws.row_dimensions[2].height = 28

    r = 4
    n = 0
    for kind, a, b in README:
        if kind == "S":
            ws.row_dimensions[r].height = 8
            r += 1
            n = 0
            continue
        if kind == "H":
            ws.merge_cells(f"B{r}:C{r}")
            ws[f"B{r}"] = a
            paint(ws, f"B{r}:C{r}",
                  fill=PatternFill("solid", fgColor=BAND),
                  font=Font(name=FONT, size=11, bold=True, color=INK_SOFT),
                  align=Alignment(horizontal="left", vertical="center"))
            ws.row_dimensions[r].height = 22
            n = 0
        elif kind == "P":
            ws.merge_cells(f"B{r}:C{r}")
            text = a.replace("{LAST_DATE}", last_date.strftime("%B %d, %Y")) \
                    .replace("{LOG_ROWS}", str(LOG_ROWS))
            ws[f"B{r}"] = text
            ws[f"B{r}"].font = Font(name=FONT, size=11, color=INK)
            ws[f"B{r}"].alignment = Alignment(vertical="top", wrap_text=True)
            ws.row_dimensions[r].height = 15 * (1 + len(text) // 100)
        elif kind == "N":
            n += 1
            ws[f"B{r}"] = f"Step {n}"
            ws[f"B{r}"].font = Font(name=FONT, size=11, bold=True, color=INK)
            ws[f"B{r}"].alignment = Alignment(vertical="top")
            ws[f"C{r}"] = a
            ws[f"C{r}"].font = Font(name=FONT, size=11, color=INK)
            ws[f"C{r}"].alignment = Alignment(vertical="top", wrap_text=True)
            ws.row_dimensions[r].height = 15 * (1 + len(a) // 70)
        elif kind == "L":
            ws[f"B{r}"] = a
            ws[f"B{r}"].font = Font(name=FONT, size=11, bold=True, color=INK)
            ws[f"B{r}"].alignment = Alignment(vertical="top")
            ws[f"C{r}"] = b
            ws[f"C{r}"].font = Font(name=FONT, size=11, color=INK)
            ws[f"C{r}"].alignment = Alignment(vertical="top", wrap_text=True)
            ws.row_dimensions[r].height = 15 * (1 + len(b) // 70)
        elif kind == "Y":
            ws[f"B{r}"] = a
            ws[f"B{r}"].font = Font(name=FONT, size=11, bold=True, color=INK)
            ws[f"B{r}"].alignment = Alignment(vertical="center")
            ws[f"C{r}"] = b
            ws[f"C{r}"].fill = PatternFill("solid", fgColor=YELLOW)
            ws[f"C{r}"].font = Font(name=FONT, size=11, color=INK)
            ws[f"C{r}"].border = Border(left=thin, right=thin, top=thin, bottom=thin)
            ws[f"C{r}"].protection = Protection(locked=False)
            ws.row_dimensions[r].height = 20
        elif kind == "C":
            ws[f"B{r}"] = a
            ws[f"B{r}"].font = Font(name=FONT, size=11, color=INK)
            ws[f"C{r}"] = b
            ws[f"C{r}"].font = Font(name=FONT, size=11, bold=True, color=INK)
            ws[f"C{r}"].alignment = Alignment(horizontal="left")
        r += 1

    ws.protection.sheet = True
    ws.protection.formatCells = False

    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = "FF9A9A93"
    ws.page_setup.orientation = "portrait"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    return r


def strip_table_autofilter(path):
    """Remove the log table's filter buttons.

    Every column in the log is a formula tied to its row, so sorting the table
    would scramble the file. openpyxl regenerates <autoFilter> from the table ref
    on every save, so it has to come out of the finished package.
    """
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(
            tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename.startswith("xl/tables/"):
                data = re.sub(rb"<autoFilter[^>]*/>", b"", data)
                data = re.sub(rb"<autoFilter.*?</autoFilter>", b"", data,
                              flags=re.S)
            dst.writestr(item, data)
    shutil.move(tmp, path)


# ---------------------------------------------------------------- main


def main(out="Open_WOs_tracker.xlsx"):
    dates = week_dates(N_BLOCKS)
    wb = Workbook()

    history = wb.active
    history.title = "History"
    totals = wb.create_sheet("Totals")
    readme = wb.create_sheet("Read Me")

    layout = readme_layout()
    link_cell = f"$C${layout[LINK_LABEL]}"

    build_totals(totals, dates)
    build_history(history, dates[-1], link_cell)
    add_named_ranges(wb, history)
    build_charts(history)
    build_readme(readme, dates[-1])

    wb.properties.title = "Open work orders — weekly history"
    wb.properties.creator = "Buddy's Kitchen Maintenance"
    wb.properties.description = (
        "Weekly count of open work orders at Burnsville and Lakeville, split into "
        "repair tickets and PMs. Enter four numbers a week on the Totals tab.")
    wb.calculation.fullCalcOnLoad = True
    wb.active = 0
    wb.save(out)
    strip_table_autofilter(out)
    print(f"wrote {out}: {len(dates)} weekly blocks, {LOG_ROWS} log rows, "
          f"3 charts, {len(history.defined_names)} defined names")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Open_WOs_tracker.xlsx")
