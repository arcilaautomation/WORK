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

**Decided 2026-09-09: a standing monthly email to Chase and Nhan, sent whether or not anything changed, plus a
same-week email for any disposal. No Power Automate flow, no SharePoint list.** Reasoning below.

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

### Considered and declined — SharePoint / Microsoft List

Recorded so it is not re-proposed from scratch. Moving the shared tracker off Excel and into a SharePoint /
Microsoft List is the only version of "365 automation" that actually works, because a List has real automatic
change triggers where Excel has none. Two tiers exist: built-in **Rules** (Automate ▸ Rules ▸ Create a rule) fire
on item created / deleted / column changed and email named in-org people, with no flow authoring but a **generic,
non-customizable email that carries no column values** — a nudge, not a report; and a **Power Automate flow on the
SharePoint connector**, which does have a genuine *When an item is created or modified* trigger and can build a
formatted email with the real rows (but *modified* fires on every edit, including typo fixes).

Declined 2026-09-09 for three reasons, in order of weight:
1. Nobody on this side is set up to build or maintain it, and an unmaintained flow fails silently.
2. It requires Chase and Nhan to work in a SharePoint list instead of Excel — a real ask of people whose own
   listing is an invoice-based Excel export.
3. It still watches a **copy**. A disposal never typed into the tracker fires no trigger.

Revisit only if the event volume grows enough that a manual monthly email is genuinely burdensome.

## 5. The monthly email — setup and drafts

### Outlook recurring reminder

Calendar ▸ New Appointment ▸ **Recurrence ▸ Monthly**. Subject: *"Send Aptean asset changes to Chase & Nhan."*
**Paste the standing draft below into the body of the appointment**, so the template is in front of you when the
reminder fires and there is nothing to go find. Default timing: **first business day of the month, covering the
prior month**, until Chase confirms Accounting's close date (§8 q3) — then move it a few days ahead of that.

### Standing monthly draft

Subject: `Aptean asset changes — <Month YYYY> — Buddy's Kitchen`

> Chase, Nhan —
>
> Aptean asset changes for <Month YYYY> below.
>
> *(table, or:)* No assets were added or disposed in Aptean this month.
>
> Accounting asset numbers for the additions — send them back when assigned and I'll record them against the
> Aptean records so the two lists stay tied together.
>
> Jonathan

| Aptean asset ID | Description | Line / location | Event | Event date | PO / invoice # | Cost if known | Accounting asset # | Notes |
|---|---|---|---|---|---|---|---|---|

- **Event** is one of `Added`, `Disposed`, `Replaced`, `Transferred`.
- **Accounting asset #** is left blank on additions — that is Chase's column to fill and send back (§6).
- **Send the email even when nothing changed.** The null report is the whole point: it makes a missing month
  detectable. Chase notices a monthly email that did not arrive; nobody notices an ad-hoc email never sent.
- Only send records at or above Accounting's capitalization threshold (§8 q2) — that is what keeps printer
  controllers off Chase's desk without anyone filtering by hand.

### Kickoff draft (reply on Accounting's thread, send once)

> Chase, Nhan —
>
> On the "email when assets are added or disposed" item: rather than automating off the spreadsheet, I'll send a
> standing monthly email on the first business day covering the prior month — and I'll send it even in months with
> no changes, so a missing email is a signal rather than silence. Anything disposed I'll send that same week
> instead of holding it, since a scrapped asset shouldn't sit for four weeks.
>
> Three things that would help me size what to send you:
>
> 1. What's your capitalization threshold? That tells me which Aptean records are worth sending and keeps the
>    non-capital equipment off your desk.
> 2. What's your month-end close date, so I can time the email ahead of it?
> 3. When you assign an accounting asset number to a new asset, can you send it back to me? I'd like to store it on
>    the Aptean record so future comparisons are a lookup instead of a project.
>
> I'm also checking whether Aptean can send a scheduled report automatically — if it can, I'll switch this over and
> it stops depending on me remembering.
>
> Jonathan

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
- **2026-09-09** Notification method **decided**: standing monthly email, plus same-week note for disposals.
  SharePoint/Microsoft List route evaluated and declined (§4). Kickoff and standing drafts written (§5). Not yet
  sent; Outlook recurrence not yet created.

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

1. [ ] Send the §5 kickoff draft on Accounting's thread — confirms the method and asks questions 2, 3 and the
   asset-number return path in one go.
2. [ ] Create the monthly Outlook recurrence, standing draft pasted into the appointment body (§5).
3. [ ] Pull the Aptean date columns (+ PO/invoice if present) and send to Chase — item 1.
4. [ ] Build the saved Aptean report: assets added or status-changed in the last month, in the §5 columns.
5. [ ] Ask Aptean support the §8-question-1 wording; if native scheduling exists, switch to it and retire the
   manual step.
6. [ ] Send month 1 — even if it is a null report.
7. [ ] Work item 2 (the match) with Chase and Nhan; prioritize post-Aug-2024 items and high-dollar lines.
8. [ ] Add the Accounting Asset # field in Aptean and record the numbers Chase returns — §6.

## 10. Sources

- Excel connector has no row-change trigger — https://community.powerplatform.com/forums/thread/details/?threadid=b0447678-4ff5-ef11-be20-0022482c0258
- Missing Excel triggers, and routing via SharePoint instead — https://community.powerplatform.com/forums/thread/details/?threadid=44b472e1-8ce5-ef11-be1f-7c1e52585ca6
- Power Automate for Excel: actions, patterns and limits — https://citizendevelopmentacademy.com/power-automate-for-excel/
- SharePoint / Lists Rules for notifications, and their limits — https://www.bulb.digital/blog/add-basic-notifications-to-lists-and-libraries-with-rules
- Create a rule to automate a list or library (Microsoft) — https://support.microsoft.com/en-us/sharepoint/lists/documents-and-library/create-a-rule-to-automate-a-list-or-library
- Rules in SharePoint Online / Microsoft Lists: conditions and the 15-rule limit — https://ganeshsanapblogs.wordpress.com/2021/01/27/rules-in-sharepoint-online-microsoft-lists/
- Turn on notifications for list and list item changes (Microsoft) — https://support.microsoft.com/en-us/office/turn-notifications-on-for-list-and-list-item-changes-85ca9280-f4b1-485a-a49e-a593ffa62e39
- Ghost assets / unrecorded disposals and their audit impact — https://cpcongroup.com/insights/article/ghost-asset-detection/
- Fixed asset disposal accounting — https://www.accountingtools.com/articles/fixed-asset-disposal-accounting
- Aptean EAM, TabWare Edition datasheet — https://www.aptean.com/en-US/resources/product-capabilities/datasheet/aptean-eam-tabware-edition-datasheet
