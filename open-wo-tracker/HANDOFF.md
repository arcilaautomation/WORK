# Open work orders — weekly tracker

Living record for the weekly open-work-order spreadsheet covering Buddy's Kitchen
Burnsville and Lakeville.

---

## 1. What this is and who asked for it

The boss asked, in writing:

> "Can we take this data and put in on a spreadsheet each week so we can see history?
> So each week update the spreadsheet and send it out. Thanks"

The deliverable is `Open_WOs_tracker.xlsx`: four numbers typed per week, everything
else calculated, one dashboard to send out.

## 2. Files in this directory

| File | What it is |
|---|---|
| `Open_WOs_tracker.xlsx` | The workbook. This is the deliverable. |
| `build_tracker.py` | Generates the workbook from scratch. Re-run it to rebuild; it is the authoritative description of every formula. |
| `HANDOFF.md` | This file. |

`python3 build_tracker.py Open_WOs_tracker.xlsx` rebuilds the file. It needs
`openpyxl`, and `formulas` for the step that stores computed results in the file
(without it the build still works, but previews show blanks until the file is
saved once in Excel). Rebuilding
**discards any counts typed into the workbook since it was generated** — the seed
data lives in the `SEED` dict in the script. Change the script and re-seed, or
edit the workbook directly, but do not do both and expect them to merge.

## 3. Data recorded so far

Source: `Open_WOs_tracker_.xlsx` as received 2026-09-21 (its `Totals` tab, blocks
anchored at columns A and D). Carried into the rebuild unchanged.

| Count date | Burnsville repair | Burnsville PM | Lakeville repair | Lakeville PM | All open |
|---|---|---|---|---|---|
| 2026-09-15 (Tue) | 11 | 3 | 32 | 173 | 219 |
| 2026-09-21 (Mon) | 7 | 6 | 38 | 241 | 292 |

Repair tickets went 43 → 45 across those two weeks. PMs went 176 → 247. Nearly the
whole of the headline +73 is Lakeville PMs.

**VERIFY** — the Lakeville PM jump of 173 → 241 in one week is assumed to be the
maintenance system releasing a scheduled PM batch rather than genuine backlog
growth. Nothing in the source file states this. Confirm against the source report
before repeating the claim to anyone; the Read Me tab and the scorecard both lean
on it.

**VERIFY** — the report the counts are pulled from is not named anywhere in the
source file. The Read Me tab carries a yellow fill-in cell for it.

## 4. How the workbook works

Three tabs: **History** (dashboard + weekly log, the tab you send), **Totals**
(the entry grid, layout preserved from the original), **Read Me**.

- **Entry is four numbers plus an optional note**, into one 3-column block per
  week on Totals. 105 blocks are pre-built, 2026-09-15 through 2028-09-11.
- **Blocks are located by the literal text `DATE` in row 1**, not by counting
  columns. Hidden rows 30–35 on Totals turn that into an index the History tab
  looks up with `MATCH`. This is what the original's
  `MOD(COLUMN()-1,3)=0` arithmetic did, without breaking when a column moves.
- **A week only enters the history once all four counts and a real date are
  present.** A part-filled block is excluded and raises a red bar on the
  dashboard, because `INDEX` into an empty cell returns 0, which would otherwise
  publish a believable but wrong "improvement".
- **Two blocks sharing a date raise the same red bar**, and the duplicate dates
  turn red on Totals. That is the one mistake that produces a plausible wrong
  number, and the documented way to add a week is the thing that causes it.
- **Notes live on the Totals block, not in the log**, so a note can never drift
  onto the wrong week when the sequence of filled blocks changes.
- **Every formula uses functions that predate Excel 2010.** Nothing needs an
  `_xlfn.` prefix, so nothing renders as `#NAME?` in Excel for the web or older
  desktop Excel. Keep it that way: no `XLOOKUP`, `TEXTJOIN`, `IFS`, `AGGREGATE`.
- **All ranges are bounded to column OJ (400).** Full-row references are slow and
  the Read Me health check warns if blocks are ever created past that.
- **The three sheets are protected with no password.** Only the blue input cells
  and the two yellow fill-ins are unlocked.
- **Every formula ships with its computed result stored beside it**, and every
  chart ships with its points cached, in the same shape Excel itself wrote in the
  original workbook. Excel still recalculates on open, but previews that only read
  stored results (Outlook attachment preview, iPhone Quick Look, SharePoint
  thumbnails) show the real dashboard instead of blanks.
- **The charts read dynamic named ranges** (a rolling 26-week window). This is the
  same construct as the original workbook, which was last saved by Microsoft
  Excel with Excel's own cached results for it — so Excel evaluates it correctly.
  LibreOffice cannot evaluate it and draws from the stored cache instead.

## 5. Event log

- **2026-09-21** — Received `Open_WOs_tracker_.xlsx` (created by Kristine Michael,
  last modified by Jonathan Weber). Reviewed it against the boss's request.
  Verdict: sound design, but this week's numbers sat below the chart and a growing
  table; one chart mixed Lakeville (279) with Burnsville (13) so Burnsville was
  flat on the axis; repair tickets and PMs were lumped into one headline; pre-built
  weeks ran out 2026-12-28; nothing documented how to update or extend it.
- **2026-09-22** — Rebuilt as `Open_WOs_tracker.xlsx` via `build_tracker.py`.
  Verified by evaluating every formula with the `formulas` Python engine (5,481
  cells, no errors other than `HYPERLINK`, which that engine does not implement)
  and by running eight scenarios against the real file: baseline, a third full
  week, a part-filled week, a duplicated date, a skipped week, one week only, no
  weeks, and a week of genuine zeros.
- **2026-09-22** — LibreOffice in the build environment could not load any
  `.xlsx`, so the recalculate-and-render check could not be run at first. Formula
  results were verified with the `formulas` engine instead.
- **2026-09-22 (evening)** — Found why LibreOffice failed: only its core was
  installed, not the spreadsheet component (`libreoffice-calc`). Installed it and
  rendered the workbook for the first time. Findings: all three charts drew empty,
  because LibreOffice cannot evaluate formula-based chart ranges; the file stored
  no computed results at all, so any previewer would show a blank dashboard; the
  scorecard's headline label was truncated; chart titles wrapped and crowded the
  plots; the headline said "6 days earlier" for what is a normal weekly gap.
  Checked the original workbook: its `docProps/app.xml` names Microsoft Excel as
  the application that last saved it, and its chart carries Excel's own cached
  points for the same dynamic ranges, endpoint labels included — so the chart
  construct is proven in Excel. Fixed: results stored for all 3,701 formulas and
  chart points cached in Excel's format; scorecard regrouped under REPAIR TICKETS /
  PMs / ALL OPEN with short row labels; email box moved beside the scorecard,
  above the fold; charts widened with short titles; a recent-notes panel beside
  the third chart; a 5-to-9-day gap now reads "last week"; empty future weeks on
  Totals show blank totals instead of zeros. Re-rendered and re-ran all eight
  scenarios. **VERIFY** — still not opened in real Excel. First open is the
  outstanding check, now lower-risk given the original's evidence.

## 6. Action list

1. **Open the file in Excel once and look at it.** Confirm the three charts draw,
   the endpoint labels sit sensibly, and no "repaired records" dialog appears.
   This is the one check the build environment could not perform.
2. **Decide where it lives on SharePoint**, paste the link into the yellow cell on
   the Read Me tab, and share the link view-only to readers and edit to whoever
   updates it. Do not move or rename the file afterwards or the link breaks.
3. **Name the source report** in the second yellow cell on the Read Me tab.
4. **Confirm or kill the PM-batch hypothesis** in §3 before the framing gets
   repeated in the weekly email.
5. To render or recalculate the workbook in a future cloud session, add
   `apt-get install -y --no-install-recommends libreoffice-calc` to the cloud
   environment's setup script (environment menu in the session title bar, then
   Edit, then Setup script). The base image has LibreOffice's core but not its
   spreadsheet component, so without it every `.xlsx` fails to load.
6. Optional: if the weekly send becomes routine, consider whether the boss also
   wants work orders *closed* per week, which this file does not track — it counts
   what is open at the moment of the pull, not flow.

## 7. Open questions

- Is Monday the right count day, and is the count pulled at a consistent time of
  day? A count taken Monday morning and one taken Friday afternoon are not
  comparable.
- Should a week with no count pulled be left blank (current behaviour: skipped,
  and the change is labelled with the real gap in days) or carried forward?
- Does anyone other than the boss receive this, and do they need the log or only
  the dashboard?

## 8. Sources

- Boss's request, quoted verbatim in §1.
- `Open_WOs_tracker_.xlsx`, received 2026-09-21 — the two recorded weeks, the
  Totals block layout, and the original chart conventions.
- Chart colours checked against the `dataviz` palette validator: `2a78d6` (repair
  tickets) and `eb6834` (PMs) pass lightness, chroma, colourblind separation
  (ΔE 24.7 protan), normal-vision separation (ΔE 33.6) and 3:1 contrast on all
  pairs. The neutral `3f3f3c` used for the total is a neutral, not a third
  categorical hue, and is distinguished by a heavier line.
