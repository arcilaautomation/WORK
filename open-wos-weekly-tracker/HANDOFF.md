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
