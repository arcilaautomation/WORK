# QTS Tanks (DeJong project) — 18327 CIP Tanks + 18445 Egg Balance Tanks: Handoff Notes

Prepared 2026-09-23 for Johnathan (Maintenance Systems Planner, Buddy's Kitchen).
Purpose: project memory for Claude Code. Everything below came from the two QTS manual packages
(including the Nord gear unit and motor manuals inside them) and from entering the equipment in
Aptean EAM on 2026-09-23. Items marked **VERIFY** are unconfirmed.

Vendor manuals are **not** in this repo (QTS drawings are stamped proprietary). They are on
Johnathan's PC under `OneDrive\Desktop\XRTC FILES\QTS 18327 CIP Tanks\` and
`...\QTS 18445 Egg Balance Tanks\`.

---

## 1. Equipment

Built by Quality Tank Solutions (QTS, Oconomowoc WI), ordered through DeJong Consulting LLC (Edgar WI).
All tanks: 304SS, atmospheric (non-code), interior #4 finish with welds ground to 32 Ra, exterior 2B.

### 18327 — (3) 600 gal CIP tanks
| Tag | Service | Drawing on hand | Notes |
|---|---|---|---|
| 18327-101 | Pre-Rinse | rev H only (22SEP25) | **as-built rev J missing from the QTS package**; no chem inlet |
| 18327-102 | Acid | rev J as-built (26MAR26) | |
| 18327-103 | Caustic | rev J as-built (26MAR26) | |

- 44" OD × 96" shell, 12 GA, no jacket. 600 gal working / 621 gal to overflow, 6.5 gal/in.
  565 lb empty / 5,400 lb full. Factory passivated 12/12/2025.
- Nozzles (102/103, rev J): A 3" outlet · B 3" overflow (bottom) · C 2" level · D 2" conductivity ·
  E 18" hinged atmospheric manway (3A EPDM gasket, confined-space label) · F 2"×1" chem inlet ·
  G 2-1/2" return · H 3"×2" anti-siphon · J 3" vent. 101 (rev H): no chem inlet; F = return,
  G = anti-siphon, H = vent with screen.
- Manway has a prox sensor bracket + flag (manway open/closed). The level, conductivity and prox
  sensors themselves are not QTS supply — no manuals for them in the package.

### 18445 — (2) 1,200 gal egg balance tanks (18445-101-1, -2)
- Drawing 18445-101 rev F, as-built 3/17/2026 (the manual cover calls them "Mix Tanks").
  Factory passivated 1/26/2026.
- 10 GA inner shell Ø65" OD, 12 GA outer shell Ø71-3/16" OD, 96" shell, 3" fiberglass insulation
  (insulated, not jacketed). ~1,200 gal working / ~1,365 gal max, 14.25 gal/in.
  2,500 lb empty / 13,905 lb full. Legs 2-1/2" sch 10 with adjustable feet.
- Agitator: **Nord SK4282AFMH-100LP/4 CUS TW** (Clincher shaft mount), Nord order 204564740-100,
  ratio 52.20, 3 HP @ 34 RPM, 2" shaft, GRIPMAXX bushing, IP55, 230/460 V 60 Hz TEFC, mounting
  position M4. **Runs CLOCKWISE** (drawing note).
- Agitator sealing/guiding: 6"×2" TC split shaft seal (Delrin) with FEP O-ring #329; bottom guide
  bearing (Delrin, 2 Viton #229 O-rings); 10" neoprene deflector hood on the 6" nozzle.
- Nozzles: A 3" outlet (bottom) · C 2" level · D 2" temp · E 18" manway (confined-space +
  moving-parts labels) · F 3"×2" no-foam inlet · G 4"×2-1/2" no-foam return · H 6" agitator ·
  J1/J2 3"×1-1/2" CIP with static spray balls (360°, 40 GPM @ 25 PSI) · K 3" QTS 3A can vent ·
  L 4"×2" anti-siphon.

### Drawing notes that matter for maintenance (both jobs)
- Note 6: **the user must keep the vessel vented** — a blocked vent/anti-siphon can pull a vacuum
  and collapse these thin-wall tanks when they drain.
- Note 8: QTS will not warranty any welding done by others.

---

## 2. Manual packages — what's in them

Both packages follow the same layout: Manual Cover, QTS Thank You, Sec 1 Care of Stainless,
Sec 2 Passivation Certificate, Sec 3 Equipment Drawings, Sec 4 Warranties / Vendor Info,
Sec 5–6 Recommended Spare Parts.

- **18327** (`Dejong QTS-18327-101-103 CIP Tanks.zip`): complete **except the 101 drawing** — its
  Sec 3 folder holds `Spare Parts - TEMPLATE.xlsx` (QTS's internal price sheet) instead.
- **18445** (`Dejong QTS-18445-101-1 & 2.zip`): complete. Sec 4 has 9 Nord documents including the
  269-page Nord document collection (B1000 gear units, B1091 motors, PL1021/PL1080/PL1090 parts lists).
- Old copies in `OneDrive\Desktop\Autobake Oven\QTS Tanks\` are outdated: 18327-101/102/103 rev H,
  18445-101 rev B.
- Warranty: QTS 2 years from ship date (parts, diagnostics, labor; requires proper maintenance).
  Nord gear unit: written notice within 1 year of delivery. Ship dates are not in the packages.

---

## 3. Maintenance — what the manuals actually say

- **QTS gives no PM intervals.** Care-of-stainless rules only: never send hot CIP into a tank below
  ambient (thermal shock can crack it); remove dissimilar metals before CIP; avoid chlorine/iodine
  and quat sanitizers; always rinse well between chlorinated caustic and acid (chlorine gas);
  non-abrasive tools only; passivate when rust/discoloration appears.
- **Nord gear unit — B1000 Table 10, p.46:**
  - At least every 6 months: visual leak check, running-noise check, **oil level check**.
  - Every 10,000 operating h / at least every 2 years (oil ≤ 80 °C): **change oil**, clean or
    replace vent screw, replace radial shaft seals (when leaking; typical life ≤ 10,000 h).
  - Every 20,000 h / at least every 4 years: re-lubricate gear unit bearings (NORD service,
    Petamo GHY 133N).
  - At least every 10 years: general overhaul (NORD service).
  - Oil: order details say **VG220-MIN-EP** (mineral CLP 220). Approved equivalents (Table 13,
    p.70): Castrol Alpha EP 220 / SP 220, Fuchs Renolin CLP 220, Klüberoil GEM 1-220 N,
    Mobilgear 600 XP 220. Do not mix oils; change lubricant type only after consulting NORD.
    QTS also included a Fuchs FM Gear Oil 220 (H1 food-grade) data sheet — **VERIFY** with NORD
    before switching to food-grade.
  - Quantity: SK4282, position M4 = **5.28 qt (5.0 L)** (Clincher oil quantities U11900).
    Level = lower edge of the oil level hole, checked at standstill with oil at 10–40 °C.
- **Nord motor — B1091 §2.3, p.24:** check for noise/vibration weekly or every 100 h; check roller
  bearings at least every 10,000 h; check connections, cables and fan; replace radial shaft seals
  every 10,000 h; keep dust off the motor; complete overhaul every 5 years. Bearings are
  lubricated for life (~40,000 h at 25 °C, ~20,000 h at 40 °C up to 1,800 rpm).

### PM plans built from this (Aptean only supports monthly + semi-annual)
- `PM-18327-CIP-tanks.txt` — monthly + semi-annual, short version for techs.
- `PM-18445-egg-balance-tanks.txt` — monthly + semi-annual, short version for techs. The monthly
  covers Nord's weekly noise check; the semi-annual covers the Nord 6-month oil level check and
  includes the 2-yr/10,000-h oil change as a conditional step.
- The Nord 4-, 5- and 10-year service items can't be scheduled as monthly/semi — tracked in §6.

---

## 4. Aptean EAM

- `https://prod-eam.aptean.com` — live Production database, plant 183. No "TEST ENVIRONMENT" banner.
- Equipment IDs follow `PD-<CLASS>-###` (e.g. PD-FIL-0xx fillers/depositors). There is **no Tank
  class**; closest is `VAT - Vat`.
- **PD-TNK-001** created 2026-09-23 = the three 18327 CIP tanks in one record: Area B20 Lakeville,
  Dept 7340 Maintenance, Criticality C1, Account 57040, Shop PM, Location Status INSTALLED,
  hierarchy parent PD-OVG-21; Model "600 GAL CIP TANK DWG 18327"; Mfr Serial
  "18327-101 / 18327-102 / 18327-103"; OEM "QUALITY TANK SOLUTIONS (QTS)"; warranty + specs text.
  - Open: Class was saved as `BLR - Boiler` (likely a mis-pick).
  - Open: the NOTES custom field did not persist — not on CREATE and not after editing the saved
    record (no SAVE button; ACTIONS menu = Work Order / Delete / Rename).
- Field limits: Description 80, Model 30, Machine OEM 30, Mfr Serial 40, Instruction/Warranty/NOTES 255.
- Filling tip for Claude: fill every field in one step via `Ext.getCmp(<inputId minus -inputEl>).setValue()`;
  combos take codes (B10/B20, 7340, C1). Never click CREATE/SAVE — Johnathan reviews and saves.
- 18445 tanks: not entered yet; Johnathan is building the PM master plans.

---

## 5. Event log

- **2026-09-23** Reviewed the 18327 package: found the missing 101 drawing and wrote the monthly +
  semi-annual PM steps. Copied the manual to `XRTC FILES\QTS 18327 CIP Tanks\`.
- **2026-09-23** Filled the Aptean equipment form; Johnathan created **PD-TNK-001**. Review found
  Class = BLR and NOTES blank.
- **2026-09-23** Reviewed the 18445 package, including Nord B1000/B1091 maintenance sections and the
  drawing BOM. Wrote the monthly + semi-annual PM steps. Copied the manual to
  `XRTC FILES\QTS 18445 Egg Balance Tanks\`.

---

## 6. Action list

1. [ ] Request the 18327-101 rev J as-built drawing from QTS.
2. [ ] Fix PD-TNK-001: Class (VAT or blank) and NOTES.
3. [ ] Enter the 18445 tanks in Aptean — one record per tank? **VERIFY** (IDs PD-TNK-002/-003?).
4. [ ] Load the PM master plans (monthly + semi-annual) for 18327 and 18445.
5. [ ] Get ship/delivery dates → set warranty expiration (QTS +2 yr, Nord +1 yr).
6. [ ] Record the gearbox oil change dates (start the 2-yr clock at install **VERIFY**).
7. [ ] Set reminders for Nord service: 4-yr bearing re-lube, 5-yr motor overhaul, 10-yr gearbox overhaul.
8. [ ] Replace the outdated drawings in `OneDrive\Desktop\Autobake Oven\QTS Tanks\` with rev J / rev F.
9. [ ] 18445 manway gasket: the drawing says 3A gray EPDM but the parts list says black — confirm with QTS before ordering.

---

## 7. Spare parts (QTS lists, prices go stale)

- 18327: EG40E3.0 3" TC gasket EPDM · EG40E2.0 2" (102/103) · HD-Clamp-3.0 · HD-Clamp-2.0 (102/103) ·
  MW-RND-18-GSKT-3A-EPDM 18" manway gasket.
- 18445: EG40E3.0 · EG40E4.0 · EG40E6.0 · HD-Clamp-3.0/-4.0/-6.0 · MW-RND-18-GSKT manway gasket ·
  QV3-3 3" can vent · upper split shaft seal 6"×2" Delrin + O-Ring-VF753A-329 · QTS-GB-3.0-DEL
  guide bearing · Nord SK4282AFMH-100LP/4 CUS TW.

---

## 8. Sources
- QTS manual packages `Dejong QTS-18327-101-103 CIP Tanks.zip` and `Dejong QTS-18445-101-1 & 2.zip`
  (drawings 18327-102/103 rev J, 18445-101 rev F; QTS Warranty; Proper Care of SS 2025).
- NORD B1000 en-2424 (gear units): Table 10 p.46, §5.2 pp.47–51, Table 13 p.70.
- NORD B1091 en-5124 (motors): §2.2–2.4 pp.23–24.
- NORD Clincher oil quantities U11900; oil plug & vent locations U14200. Unit docs: www.nord.com/docs,
  order 204564740-100.
- Contacts: QTS 262-361-4252, 24/7 emergency 262-720-6313, www.qts4u.com · NORD 888-314-6673.
