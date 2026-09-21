# Open WOs weekly tracker — HANDOFF

Workbook `Open_WOs.xlsm` (created 2022-03-30 by Kristine Michael, last edited by Jonathan
Weber). It counts open work orders per plant (Burnsville, Lakeville) from a TabWare export
"All Open Work Orders & PMs" and logs the weekly totals to a table that feeds a trend chart.

## 1. Files

| File | What |
|---|---|
| `Open_WOs_fixed.xlsm` | Repaired workbook, 2026-09-21. Deliverable. |
| `Open_WOs_original_2026-09-21.xlsm` | As received on 2026-09-21, for reference. |
| `build_fix.py` | Script that produced the fixed file from the original by editing the OOXML parts directly (keeps VBA, chart, table style byte-for-byte). |
| `Open_WOs_simple.xlsx` | Two-tab version requested 2026-09-21: `Sheet1` (paste tab) + the original `Totals` page unchanged in layout. The 9/21/2026 block (D:E) counts from Sheet1 with COUNTIFS; the 9/15 block stays typed. No macro, so the date in E1 is typed. |
| `Open_WOs_with_graph.xlsx` | Current version (2026-09-21, third request): `Sheet1` = the weekly-history chart page transplanted from the original workbook (table `WeeklyLog` + line chart, weeks 9/15 and 9/21 filled in); `Totals` = the user's page with the values they typed in Excel (9/21 block: 7, 6, 38, 241). No formulas count from an export; the user types the four counts each week. Built by `build_graph.py` from the original. |
| `Open_WOs_auto.xlsx` | Current version (2026-09-21, fourth request): same two tabs, but the `WeeklyLog` table on `Sheet1` is all formulas that read the dated blocks on `Totals` (every 3 columns: A:B, D:E, G:H, J:K, M:N ...; a block counts when its date cell in row 1 is a real date). 26 rows pre-built; Tab in the last cell adds more. Chart names are dynamic (`INDEX():INDEX()` sized by `COUNT` of dates). Built by `build_auto.py`. Not opened in Excel here (LibreOffice cannot load files in the sandbox) — **VERIFY** in Excel that the table fills and the chart shows both weeks. |
| `Open_WOs_tracker.xlsx` | Current version (2026-09-21, fifth request; user confirmed the auto-updating chart works in Excel). Adds empty blocks in G:H, J:K and M:N (the next three weeks), removes the header-only leftover block in M:N, sets label-column widths for future blocks, and adds three conditional formats that turn a block's empty date/count cells yellow until filled (`ISBLANK` + column-stride check + header in row 3). Two-line how-to in Totals rows 16–17 naming Aptean EAM > Open Work Orders. Built by `build_tracker.py`. |

## 2. How the workbook is meant to work

1. Paste the TabWare export onto tab **Sheet1** (header row in row 1, `Work Order #` in
   column A, `Area Description` in column B).
2. **Totals** counts from Sheet1 with `COUNTIFS`: PMs = work-order numbers starting with `PM`;
   repair tickets = every other work order. Only areas Burnsville and Lakeville are counted.
   Rows 16–17 show the total rows on Sheet1 and how many were not counted (red if not 0).
   Row 19 is a status line.
3. The **Refresh** button runs `Module2.UpdateData` (unchanged VBA): stamps today's date in
   Totals!B1 and copies Sheet1 to the hidden **Calculation** tab. Counts do not need it.
4. Each week the date and four counts are typed into the next row of table `WeeklyLog` on
   **Weekly History**. Totals, change vs last week, and the chart fill in from the table.
5. **Directions** tab (now visible) carries the step-by-step.

## 3. Event log

- **2026-09-21** — Received file from Jonathan's Outlook/SharePoint. Findings:
  1. Tab `Sheet1` had been deleted. `UpdateData` does `Sheets("Sheet1").Range("A2:M1000").Copy`
     → runtime error 9 the moment the button is pressed. Directions still said to paste into Sheet1.
  2. Every count on Totals was a typed number (A4, A5, A9, A10 and a second block D4:D10)
     although cell comments and the Directions note claimed they "update on their own from
     Sheet1". A11 (=205) was typed while D11 was a formula.
  3. Three conditional-format rules on A16/D16/M16 referenced `COUNTA(#REF!)`.
  4. Totals held three side-by-side blocks (9/15/2026, 9/21/2026, one empty). The 9/21 block
     had no BURNSVILLE header and its numbers were not in Weekly History.
  5. Hidden leftover name `_xleta.SUM` = `#NAME?`.
  6. The Refresh button ("circular arrows icon") no longer existed on Totals.
  7. Directions was hidden and its note about auto-updating counts sat in a 9-pt spacer row.
- **2026-09-21** — Repaired (see §4). Verified by parsing (zip + XML well-formed, opens in
  openpyxl, `vbaProject.bin` identical to the original). Expected counts were computed in
  Python from the 216-row Nov-2023 export still sitting on the Calculation tab:
  Burnsville 22 repair + 67 PM = 89; Lakeville 18 + 109 = 127; combined 216; not counted 0.
  LibreOffice would not load any file in the sandbox, so the workbook has not yet been
  opened by a spreadsheet application. **VERIFY** in Excel (see §5).

- **2026-09-21** — User asked for a two-tab version with the Totals page as it was; built
  `Open_WOs_simple.xlsx` from the original with openpyxl (see file table).

- **2026-09-21** — User opened `Open_WOs_simple.xlsx` in Excel, typed 7/6/38/241 over the 9/21
  formulas, and asked for the chart page back on `Sheet1` with Totals values kept. Built
  `Open_WOs_with_graph.xlsx`. The export-counting idea is dropped: the user prefers typing.

- **2026-09-21** — User asked for the chart to update from the Totals page automatically. Built
  `Open_WOs_auto.xlsx`: table rows find the k-th dated block with `_xlfn.AGGREGATE(15,6,...)` over
  `Totals!$A$1:$ZZ$1` and pull rows 1/4/5/9/10 of that block with INDEX. Weekly routine is now:
  copy a block on Totals, paste it 3 columns to the right, type the date and four counts.

- **2026-09-21** — User confirmed `Open_WOs_auto.xlsx` works in Excel (AGGREGATE/INDEX table and
  dynamic chart names OK). Asked for a ready third block and an obvious place to enter the weekly
  Aptean EAM numbers → `Open_WOs_tracker.xlsx`. Source system is now called Aptean EAM (was TabWare).

- **2026-09-21** — User asked for one more empty block → `Open_WOs_tracker.xlsx` now has G:H and J:K
  ready (12 merges, dimension A1:K17). Same build script.

- **2026-09-21** — One more empty block requested → M:N added (15 merges, dimension A1:N17).

## 4. Changes made on 2026-09-21

- Added tab **Sheet1** (yellow tab, 13 TabWare headers, frozen header row). Macro left as is.
- **Totals** reduced to one block; all figures are formulas now. Added the rows-on-Sheet1 /
  not-counted check and the status line. Removed the D:E and M:N blocks and their comments.
- Re-added a **Refresh** button (shape assigned to `[0]!UpdateData`) at D1:E2.
- **Weekly History**: added the 9/21/2026 row (6, 6, 38, 240 → 12, 278, 290, +71). Table ref
  A21:I23; change-column conditional format extended to I22:I1000; chart caches updated.
- **Directions** unhidden and rewritten to match the fixed workflow, incl. a note on macros.
- Removed the `#REF!` conditional formats, `_xleta.SUM`, and `calcChain.xml` (Excel rebuilds
  it); workbook set to full recalculation on open.

## 5. Action list

- [ ] Open `Open_WOs_fixed.xlsm` in Excel. If Excel offers to "repair" it, note which part it
      names and report back.
- [ ] Downloaded files carry Mark-of-the-Web: right-click → Properties → Unblock, otherwise
      the Refresh macro is blocked. Copying the file into the SharePoint/OneDrive folder also works.
- [ ] Paste this week's export onto Sheet1; check Totals against TabWare; press Refresh.
- [ ] Optional VBA improvements (not done, VBA left untouched): clear `A3:N1000` instead of
      `A3:M1000` in `UpdateData` so column N does not keep stale text; append the week to
      `WeeklyLog` automatically instead of typing it.

## 6. Sources

- The workbook itself: VBA `Module2.UpdateData`, the Directions tab, cell comments on Totals
  A4 and Weekly History A22. Read 2026-09-21.
