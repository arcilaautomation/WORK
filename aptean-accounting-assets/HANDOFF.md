# Aptean EAM ↔ Accounting Fixed-Asset Reconciliation: Handoff Notes

Started 2026-09-08 for Jonathan (Data Analyst / Maintenance Systems Planner, Buddy's Kitchen, Burnsville MN).
Counterparties: **Chase** and **Nhan** in Accounting. Source document: Accounting's email of ~Sep 2026 with two
attachments — their fixed-asset listing and the Aptean asset export Jonathan had sent them.
Items marked **VERIFY** are unconfirmed.

---

## 1. What this project is

Two asset lists that have drifted apart and need to be joined:

| | Aptean EAM | Accounting fixed-asset register |
|---|---|---|
| Owner | Jonathan / Maintenance | Chase, Nhan |
| Unit of record | A maintainable piece of equipment | A capitalized cost, **listed by invoice** |
| Contains | Everything maintenance tracks, incl. non-capital items (printer controllers, etc.) | Kitchen Equipment **plus** building improvements, computer equipment, office equipment |
| Key | Aptean asset ID | Accounting asset number |

Last reconciliation: **Aug 2024**. Assets predating that are probably already matched; anything newer likely is not.

Structural mismatches to expect when matching (Accounting's own summary from the call):
- Aptean has equipment that is not a capital asset and will never appear on Accounting's list.
- One asset can span **multiple invoice lines** on Accounting's list.
- One invoice line can cover **multiple assets**.
- Only **"Kitchen Equipment"** on Accounting's listing is in scope for comparison.

## 2. To-do list (from Accounting's email)

| # | Item | Owner |
|---|---|---|
| 1 | Provide a listing of dates from Aptean (purchase date / in-service date / date added to Aptean) | Jonathan |
| 2 | Compare the two listings, match where possible, add the accounting asset number to the Aptean sheet | Chase, Nhan, Jonathan |
| 3 | Going forward, email Chase when assets are added / disposed in Aptean | Jonathan |
| 3a | *(optional)* See whether Aptean can send those emails automatically | Jonathan |

Accounting will call a follow-up meeting in **September 2026** to share findings.

## 3. Item 1 — the dates

Accounting needs a date per asset, but not any date: depreciation starts at the **in-service date**, not the
purchase date and not the date the record was keyed into Aptean. Send all three columns and label them plainly;
let Chase pick. Which of these Aptean actually stores, and under what field names, is **VERIFY** — check the asset
record layout and the export in Analytics.

Include the **PO or invoice number** on the export if Aptean carries it. Accounting's list is organized by invoice,
so an invoice number is the single strongest join key available and turns most of item 2 from judgment into a lookup.

## 4. Item 3 — how to notify going forward (the decision)

**Recommendation: do not build a Power Automate flow that watches the Excel file. Use a scheduled monthly
email off an Aptean report, plus a same-week email for disposals.** Reasoning below.

### Why not "automate when the Excel sheet is updated"

The automation everyone pictures does not exist. The Excel Online (Business) connector in Power Automate has **no
automatic trigger for a row being added or changed** — its only instant trigger is *For a selected row*, which a
person clicks from inside Excel. Automatic row-change detection has to come from the source system, not from Excel.
To fake it you would run a *scheduled* flow that lists the table, diffs it against a stored snapshot, and mails the
difference. That is real work to build, and it is fragile in the ways that matter here:

- Breaks silently if the file is renamed or moved, or the table is renamed.
- Fails while someone has the workbook open/locked in desktop Excel.
- Flows are owned by an individual account; it dies when that account changes or the flow is auto-disabled after
  repeated failures.
- Worst of all: it automates a **copy**. Aptean is the system of record. Anything missing from the spreadsheet is
  invisible to a flow that watches the spreadsheet.

For a handful of events a year, the build and maintenance cost exceeds the benefit.

### Why not purely ad-hoc "email each other when we remember"

It is the right instinct on volume and the wrong one on failure mode. Additions largely reach Accounting anyway
via the AP invoice. **Disposals do not** — nothing flows through AP when a machine is scrapped. A missed disposal
leaves a ghost asset on the register that keeps depreciating, keeps getting insured, and keeps getting property tax
paid on it, and it surfaces as an audit finding. Unrecorded disposals are the classic fixed-asset audit problem,
and they are exactly the events an ad-hoc process forgets, because scrapping a machine does not feel like
paperwork the way buying one does.

### What to do instead

1. **Monthly standing email, sent whether or not anything changed.** A recurring Outlook calendar reminder a few
   days before Accounting's month-end close; run the saved Aptean report; paste the rows into the standing email.
   Roughly two minutes a month. The critical design property is the **null report** — "no additions or disposals in
   August" is a real message. It makes a missing month detectable, which an ad-hoc process never is: Chase notices a
   monthly email that did not arrive; nobody notices an ad-hoc email that was never sent.
2. **Same-week email for any disposal**, in addition to the monthly. A machine scrapped on the 2nd should not wait
   four weeks, and disposals are the high-value half of this.
3. **Send to Chase and Nhan both** (or an accounting distribution list / shared mailbox), on one continuous thread,
   so the process survives one person being out.
4. **Chase the automatic option (item 3a) first** — if Aptean can schedule a saved query and email it, that beats
   everything here, because it needs no human discipline and reads the system of record directly. See §8.

### If an automation is wanted anyway

Do not automate the Excel file — move the shared tracker to a **SharePoint / Microsoft List**. Lists *do* have real
automatic triggers, and a built-in **Rules** feature (Automate ▸ Create a rule) that emails someone when an item is
created or a column changes, with no Power Automate authoring at all. Caveats: the rule emails are generic and not
customizable, the recipient must be in the organization (no guests), and a rule cannot notify a whole team group.
A List can be created directly from the existing Excel file. This is the only version of "365 automation" here that
is worth the setup — but it still watches a copy, so it ranks below an Aptean-native report.

## 5. Standing email format

Subject: `Aptean asset changes — <Month YYYY> — Buddy's Kitchen`

One table, same columns every month, so Chase can paste it straight into the register:

| Aptean asset ID | Description | Line / location | Event | Event date | PO / invoice # | Cost if known | Accounting asset # | Notes |
|---|---|---|---|---|---|---|---|---|

- **Event** is one of `Added`, `Disposed`, `Replaced`, `Transferred`.
- **Accounting asset #** is left blank on additions — that is Chase's column to fill and send back (§6).
- When nothing changed, send the email anyway with "No additions or disposals this month."
- Only send records at or above Accounting's capitalization threshold (§8) — that is what keeps printer controllers
  off Chase's desk without anyone having to filter by hand.

## 6. The durable fix — join the two systems permanently

Item 2 is a one-time cleanup. Without this, it has to be redone in 2027:

- Add an **Accounting Asset #** user-defined field to the Aptean asset record, and populate it from the item-2
  reconciliation. Whether Aptean allows a user-defined field here is **VERIFY**.
- Establish the **return path**: when Chase assigns a number to a new asset, they send it back and Jonathan enters
  it in that field. Item 3 as written is one-directional; without the return leg, new assets start unmatched and the
  gap reopens immediately.
- Once the field is populated, every future comparison is a join on a key rather than a matching project.

## 7. Event log

- **2026-09-08** Accounting (Chase) emailed the two listings and the four-item to-do list; follow-up meeting to be
  scheduled for September. Notification approach decided as above; nothing built or sent yet.

## 8. Open questions

1. **Can Aptean EAM email a scheduled report?** (item 3a) Aptean EAM TabWare Edition markets an Analytics module and
   "real-time notifications," but the specifics are not publicly documented — **VERIFY** with the site's Aptean admin
   or Aptean support. Ask it precisely: *"Can I schedule a saved query of assets whose created date or status changed
   in the last N days, and have it emailed to a distribution list on a monthly schedule? And can a status change to
   Disposed/Retired trigger an alert?"* A yes to either replaces most of §4.
2. **What is Accounting's capitalization threshold?** (commonly $2,500 or $5,000 — ask Chase.) This defines which
   Aptean records are even reportable and settles the "Aptean has stuff that isn't an asset" issue at the source.
3. **What is Accounting's month-end close date?** Sets when the monthly email must land.
4. **Which date fields does the Aptean asset record actually carry**, and does the export include PO/invoice? (§3)
5. **Does Aptean support a user-defined field** for the accounting asset number? (§6)
6. **What is the disposal trigger in the field** — does a scrapped machine reliably get its Aptean status changed,
   or does the record just go dormant? If the latter, item 3 has no signal to fire on and that gets fixed first.

## 9. Action list

1. [ ] Pull the Aptean date columns (+ PO/invoice if present) and send to Chase — item 1.
2. [ ] Ask Chase for the capitalization threshold and the close date (questions 2 and 3).
3. [ ] Ask Aptean support the §8-question-1 wording; decide native vs. manual on the answer.
4. [ ] Build the saved Aptean report: assets added or status-changed in the last month, in the §5 columns.
5. [ ] Set the recurring Outlook reminder and send month 1 — even if it is a null report.
6. [ ] Work item 2 (the match) with Chase and Nhan; prioritize post-Aug-2024 items and high-dollar lines.
7. [ ] Add the Accounting Asset # field in Aptean and agree the return path with Chase — §6.

## 10. Sources

- Excel connector has no row-change trigger — https://community.powerplatform.com/forums/thread/details/?threadid=b0447678-4ff5-ef11-be20-0022482c0258
- Missing Excel triggers, and routing via SharePoint instead — https://community.powerplatform.com/forums/thread/details/?threadid=44b472e1-8ce5-ef11-be1f-7c1e52585ca6
- Power Automate for Excel: actions, patterns and limits — https://citizendevelopmentacademy.com/power-automate-for-excel/
- SharePoint / Lists Rules for notifications, and their limits — https://www.bulb.digital/blog/add-basic-notifications-to-lists-and-libraries-with-rules
- Turn on notifications for list and list item changes (Microsoft) — https://support.microsoft.com/en-us/office/turn-notifications-on-for-list-and-list-item-changes-85ca9280-f4b1-485a-a49e-a593ffa62e39
- Ghost assets / unrecorded disposals and their audit impact — https://cpcongroup.com/insights/article/ghost-asset-detection/
- Fixed asset disposal accounting — https://www.accountingtools.com/articles/fixed-asset-disposal-accounting
- Aptean EAM, TabWare Edition datasheet — https://www.aptean.com/en-US/resources/product-capabilities/datasheet/aptean-eam-tabware-edition-datasheet
