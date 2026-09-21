# MicroWeigh Triple Indexer (Lakeville) — PM Schedule: Handoff Notes

Prepared 2026-09-21 for Johnathan (Data Analyst / Maintenance Systems Planner, Buddy's Kitchen).
Purpose: project memory for Claude Code, and a first-draft PM schedule for the WeighTech MicroWeigh
Triple Indexer. Machine facts and page cites come from the OEM manual archived next to this file
(`tri_index_3_lakeville.pdf`, WeighTech, 2026-04-26). Third-party intervals come from the component
OEM docs in §8. Items marked **VERIFY** are unconfirmed.

> **The schedule in §3 is a draft, not an OEM document.** WeighTech ships no PM schedule with this
> machine (§2). Every interval in §3 is engineering judgment built from the manual's own failure modes
> plus component-OEM guidance — it has not been validated against Lakeville run hours or sanitation
> frequency. Walk it with the line before loading it into EAM.

**Site note:** this manual is for **Lakeville, MN**; the rest of this repo is Burnsville. Whether
Lakeville is a second site, a line move, or shares the Burnsville EAM instance is open — see §6.

---

## 1. Machine and hardware inventory

**WeighTech MicroWeigh Triple Indexer** — 3 weigh hoppers over an indexing box line.
Drawing: "TRIPLE INDEXER", Buddy's Kitchen, Lakeville MN, drawn by Newell, 4-26-2026, 5 sheets (pp. 40–44).
Firmware: **app `tri index 3`, Build 49, compiled 02/13/2024** (read from Info menu, p. 23).

### Indicators (3×, stacked)
| Position | Role | Set in |
|---|---|---|
| Top | **Remote 1** | "Dump settings" menu, p. 9 |
| Middle | **Remote 2** | same |
| Bottom | **Master** — owns dump settings, target weight, box indexing | same |

Master/remote assignment and comm address changes require a power cycle (p. 9). Master↔remote link is
**RS-485**; loss raises "Rmt 1 comm fail?" / "Rmt 2 comm fail?" / "Mstr comm fail?" (p. 17).

### I/O module map (p. 30, confirmed on drawing sheet 1)
| Slot | Module | Function | Lit | Dark |
|---|---|---|---|---|
| **Master** M1 | ODC5 (red) | Infeed drive | Belt stop | Belt run |
| M2 | OAC5 (black) | Diverter gate | Divert | Fill |
| M3 | OAC5 (black) | Weigh gate | Shut | Open |
| M4 | IDC5 (white) | Box sensor | No box | Box |
| M5 | ODC5 (red) | Index drive | Belt stop | Belt run |
| M6 | *(empty)* | — | — | — |
| **Remotes** M1 | OAC5 (black) | Diverter gate | Divert | Fill |
| M2 | OAC5 (black) | Weigh gate | Shut | Open |
| M3–M6 | *(empty)* | — | — | — |

Remote 2 / M6 is empty in the as-built table, so the **optional downstream jam opto is probably not
installed** (p. 13 describes it at remote 2 M6). **VERIFY** at the panel.

### Drives — 2× Invertek Optidrive **E3** (ODE-3), 460 V, firmware V3.11
| Tag | Rating | Part | Key as-built settings | Manual |
|---|---|---|---|---|
| **Infeed** | 1.0 HP | EP0028 | P-01 60.0 Hz max, P-03/04 1.0/0.5 s ramps, P-08 1.7 A, P-51 **1: V/F** speed control | §13, pp. 31–34 |
| **Box takeaway** | 2.0 HP | EP0029 | P-01 **12.0 Hz** max, P-03/04 0.5/0.5 s ramps, P-51 **2: PM Vector** speed control | §14, pp. 35–38 |

Both: P-12 = 0 Terminal Mode, P-15 = 10 (close to run / open to stop), P-17 8 kHz, P-18 Drive Healthy relay.
**The §13/§14 parameter listings are the golden record for these drives** — verify live values against
them at Q2 and after any drive swap.

**Drive identity, read from the listings (P0-29 / P0-30, as of 2026-04-26):**
| Tag | Drive type | Rating | Firmware | **Serial (P0-30)** |
|---|---|---|---|---|
| Infeed | E3 | 460 V 3~ 1.0 HP | 3.11 (I/O `72B9`, Power `0E61`) | **649453 / 18 / 057** |
| Box takeaway | E3 | 460 V 3~ 2.0 HP | 3.11 (I/O `72B9`, Power `0E61`) | **654310 / 24 / 083** |

These two are the **only serial numbers anywhere in the manual** — see §2.1. Invertek documents P0-30
only as "unique drive serial number" and does not break down the three fields, so don't read `18` / `057`
as a year/week without confirming (**VERIFY**).

> "PM" in those listings means **permanent magnet**, not preventive maintenance — P-51 "PM Vector Speed
> Control" (p. 35) and part 10575 "Motor, PM" (p. 39). Don't let it fool a keyword search.

### Field devices
- **Load cells** — 1000-10, 200 lb capacity, one per weigh hopper. Wiring at the interface board:
  green/white signal, red/black excite, shield (sheet 3). Color-code cross-reference for other makes, p. 45.
- **Box detect opto** — Banner through-beam pair, **SE0066 emitter T18-2NAEL-Q8** + **SE0065 receiver
  T18-2VPRL-Q8**, cordset **SE0038** (MQDC-430RA). T18-2 series is the washdown/thermal-shock family:
  IP67/IP68/IP69K, −40…+70 °C. Works light- or dark-operate via "Opto mode" in Dump settings (p. 9).
- **Pneumatics** — Festo valve manifold (**AV0044** valve+coil, **AV0045** DIN plug, **AV0046** LED gasket,
  **AV0047** substation, **AV0048** end plate kit); **AC0001** weigh hopper cylinders, **AC0002** diverter
  cylinders (25-150); **AA0009** regulator, **AA0005** GR-QS-6 inline flow controls, **AA0006** 6 mm tubing,
  **AA0026** M10×1.25 stainless rod clevis.
- **Conveyance** — **CB0060** series 800 flattop 16" (buffer); **CB0126** series 800 16" with flight
  arrangement 24"–4"–24" centers; sprockets **11377** (12T stainless) and **CB0117** (800 series, 7.7 PD,
  12T, 1.5" square bore); **10575** PM motor (index, buffer).
- **Operator devices** — **SS0006** stop switch assembly, **SS0020** green momentary (10250T30G),
  **SS0024** red momentary (10250T30R).
- **Indicator hardware** — **WE0028** main gasket, **EF0009** strain relief, **HW0018**/**HW0019** housing
  screws, **WE0029-1** detachable power cord, **WE0076-101** interface board.

---

## 2. What the OEM manual covers — and what it doesn't

Checked all 46 pages of `tri_index_3_lakeville.pdf` for interval language (maintenance, preventive,
lubricate, grease, daily/weekly/monthly/quarterly/annual, every N hours, periodic, inspect, schedule).

**There is no PM schedule in this manual, at any interval.** Its 17 sections are operation, calibration,
menus, troubleshooting, drive parameter listings, parts, wiring and load-cell color codes. The only
maintenance-adjacent content is reactive:

| Manual content | Page | What it gives the PM |
|---|---|---|
| §6.3 Startup — "ensure all hoppers are empty and all moving parts are in good working condition"; no cylinder should move at power-up | 11 | The daily pre-start check (D1) |
| §6.5 Cleanout — "Cycle idle" locks all gates open for cleaning | 12 | Sanitation lockout step (D5) |
| §2 Washdown mode — keypad is deliberately water-stream sensitive; lock it before hosing | 5 | Sanitation lockout step (D5) |
| §12.1 Load cells — excite ≈ 4.5 V, S1+/S1− ≈ half excite and within 0.5 V, ADC drift 100–300 counts | 28 | Accept/reject limits for the weekly health read (W1) |
| §12.3 Machines — "most machine related problems can be traced to **bad air supply (excessive water and condensation), sticky air cylinders, worn or clogged solenoid air valves, and wiring**" | 28 | The failure modes the whole schedule is aimed at |
| §12.3 gate test — Cycle off energizes all valves/shuts gates, Cycle idle de-energizes/opens them | 28 | Weekly gate function test (W2) |
| §6.1 I/O test — step every output, verify module, valve, cylinder, belt, opto | 9 | Monthly functional test (M1) |
| §3.6/§3.7 Audit cfg / Audit cal counters, nonvolatile | 6 | Tamper/drift detection (M2) |
| §10.9, §11.6 Info menu live diagnostics and error counters | 23, 27 | The trend data in §4 |
| §9.1 Display messages | 16–17 | Operator-reportable fault list |

Everything in §3 below is built from that column plus the component OEM docs. Nothing in §3 is a
WeighTech-specified interval.

### 2.1 Machine identification — not in this document

The manual carries **no nameplate data for the indexer itself**: no machine model number beyond the
descriptive name, no machine serial, no WeighTech job or order number, and no serial numbers for any of
the three MicroWeigh indicators. The drawing block (sheets 1–5, pp. 40–44) reads only `JOB: TRIPLE
INDEXER` / `PLANT: BUDDY'S KITCHEN` / `LOCATION: LAKEVILLE, MN` / `DRAWN BY: NEWELL  DATE: 4-26-2026`.

What the manual does give as identity:

| Identifier | Value | Where |
|---|---|---|
| Machine designation | **MicroWeigh Triple Indexer** | Title page; drawing `JOB:` block |
| Firmware app | **`tri index 3`**, Build **49**, compiled 02/13/2024 | Info menu, pp. 23, 27 |
| Infeed drive serial | 649453 / 18 / 057 | §13 P0-30, p. 34 |
| Box takeaway drive serial | 654310 / 24 / 083 | §14 P0-30, p. 38 |

**The indicator serials must be read off the machine** — p. 30 says to "gather the indicator serial number
from the front panel" before calling WeighTech, which is also confirmation they were never printed here.
Capture them at the next line walk (§7 item 11); WeighTech will ask for the serial plus App and Build.

---

## 3. Draft PM schedule

Safety, every task: this is a live 24 VDC control panel over food-production equipment with stored
pneumatic energy. **Follow site LOTO.** Configuration *reads* (Info menu, drive P0 parameters) are
harmless and may be done running; anything that moves a gate, changes a setting, or opens a panel
belongs in a planned window. If the scale is sealed for trade, any task touching a sealed parameter
needs the **PVR/seal check** — the Audit cfg / Audit cal counters (p. 6) are what a weights-and-measures
inspector will read.

### 3.1 Daily / per shift — operator + sanitation, no tools

| ID | Task | Accept / reject | Source |
|---|---|---|---|
| D1 | Pre-start: hoppers empty, moving parts sound. Power up indicators. | **No air cylinder may move at power-on.** Any movement → stop, suspect valve or reversed plumbing. | p. 11 |
| D2 | Air prep: regulator at setpoint, drain filter bowl / confirm auto-drain working. | No free water in the bowl. Pressure at setpoint **VERIFY** (not in manual). | p. 28 names bad air as the #1 cause |
| D3 | Zero all three heads, then verify with a known test weight before production. | Reads within tolerance **VERIFY** (site tolerance TBD). Cal weights are 1/2/5/10 lb class. | p. 13 |
| D4 | Wipe box-detect opto emitter and receiver lenses; confirm box/no-box toggles. | Master M4 module LED changes as the beam breaks. | pp. 9, 30 |
| D5 | Before washdown: indicators → **Washdown** mode, machine → **Cycle idle**. | Keypad locked (5-key follow-the-leader to exit); all gates open for cleaning. Do not aim a stream into the keypad. | pp. 5, 12 |
| D6 | After washdown: no standing water in funnels, cylinders, or on drive enclosures. Check displays. | No banner from the §9.1 list showing. | pp. 16–17 |

### 3.2 Weekly — maintenance tech, ~30 min

| ID | Task | Accept / reject | Source |
|---|---|---|---|
| W1 | Record Info-menu health on **all three heads**: Excite, S1+, S1−, ADC, Offset, Deadload, Stbl err, Dump err. Reset error counters after recording. | Excite **≈4.5 V** (<1 V = short, <4.0 V blocks calibration); S1+ ≈ S1− ≈ half excite, **within 0.5 V** of each other; ADC varies **≤100–300 counts** when stable, within **±10,000 counts** of zero at no load; **>±1,000,000 counts = bent cell**. | pp. 23, 27, 28 |
| W2 | Gate function test: **Cycle off** (all valves energize, all gates shut) → **Cycle idle** (all de-energize, all gates open). | Every gate moves on both transitions. A gate that doesn't → swap parts to isolate. | p. 28 |
| W3 | Review Deadload trend per hopper against W1 history. | Climbing deadload = product build-up on the weigh hopper, or a bending cell. | p. 27 |
| W4 | Belt tracking and condition: buffer belt CB0060, takeaway CB0126 flights. | Tracking centered, no torn/missing flights, no edge damage. | §15 p. 39 |
| W5 | Drive cooling: heatsink fins and fans dust-free, cooling air free to circulate, enclosure free of dust and condensation. | Fans spin freely; no dust mat on fins. | Invertek §3.9 p. 10 |

### 3.3 Monthly — maintenance tech, planned window, ~2 h

| ID | Task | Accept / reject | Source |
|---|---|---|---|
| M1 | Full **I/O test** at the master: step every output, verify module LED, valve, cylinder and belt against the §1 module map. Confirm opto detects boxes. | Display state matches physical state. Mismatch → reversed plumbing or wrong Opto mode. | pp. 9, 30 |
| M2 | Calibration **verification** (not recalibration) on all three heads with certified weights. Record **Audit cfg** and **Audit cal** counters. | In tolerance → leave alone. Counter jumped with no work order → someone was in the sealed menus. | pp. 6, 13–14 |
| M3 | Record drive diagnostics, both drives — see §4.2. | **P0-23 and P0-24 must stay 0:00:00.** Nonzero = a cooling problem to chase before it trips. | §13/§14 pp. 33–34, 37–38 |
| M4 | Pneumatics detail: cylinder rods clean and unscored; clevis AA0026 and pins for play; flow controls AA0005 not drifted; Festo DIN plug LEDs lit; manifold and end plate for leaks. | No buzzing valve, no slow or hesitant cylinder, no audible leak. | p. 28 |
| M5 | Indicator integrity: load-cell cable and strain relief EF0009 at each head; main gasket WE0028; housing screws HW0018/HW0019. | Gasket seated and uncracked, screws tight. A leaking housing is how these fail. | §15 p. 39 |
| M6 | Opto pair alignment; cordset SE0038 connector and gland dry. | Solid detect across the full box path. | pp. 9, 28 |
| M7 | Comm health: confirm no operator-logged "Rmt 1/2 comm fail?" or "Mstr comm fail?" since last PM. | None. Any → check RS-485 wiring and head settings. | p. 17 |

### 3.4 Quarterly — planned window, ~4 h

| ID | Task | Accept / reject | Source |
|---|---|---|---|
| Q1 | **Full calibration**, all three heads, certified weights. Record before/after and the cal audit counter. PVR/seal check if sealed. | Span and zero within tolerance. | pp. 6, 13–14 |
| Q2 | Back up and archive **all** settings: Parameters, Dump settings, master/remote assignment per head; verify both drives' live parameters against the §13/§14 listings. Attach to the EAM asset record. | Live values match the as-built listing, or the delta is documented. | pp. 19–22, 31–38 |
| Q3 | Drive electrical: torque-check drive terminals — **control 0.5 N·m (4.5 lb-in), power 1 N·m (9 lb-in)** (frame sizes 1–3). Inspect power cables for heat damage. | Correct torque, no discoloration or embrittlement. | Invertek §3.9 p. 10, §3.3/3.5 |
| Q4 | Drive train: sprocket 11377 / CB0117 tooth wear, belt tension, shaft bearings, motor 10575 mounts. | No hooked teeth, no bearing noise or play. | §15 p. 39 |
| Q5 | Function-test stop switch SS0006 and pushbuttons SS0020/SS0024. | Machine stops on demand from every station. | §15 p. 39 |

### 3.5 Semiannual / annual

| ID | Task | Accept / reject | Source |
|---|---|---|---|
| A1 | Replace air prep filter element; check regulator AA0009; replace stiff or cracked tubing AA0006. | New element; tubing flexible with clean fitting seats. | p. 28 |
| A2 | Air cylinder service/replace decision on AC0001 / AC0002 from the M4 trend. | Replace anything logged slow or sticky twice. | p. 28 |
| A3 | Drive fan replacement decision from **P0-27** fan run hours and any trip **22**. | Trip 22 is IP66-only — confirm the drive's IP rating first (**VERIFY**, §6). | Invertek trip table p. 28 |
| A4 | Load cell verification: corner/shift test each hopper, review Deadload trend, check cable insulation. | Within the §12.1 limits; no drift trend across the year. | p. 28 |
| A5 | Reconcile spares on hand against the §15 parts list; reorder to min/max. | Stock at min for the §5 short list. | p. 39 |
| A6 | Re-record firmware identity per head (App / Build / Date) and re-archive configs. | Currently `tri index 3` / Build 49 / 02/13/2024 on all three. A mismatch between heads is a finding. | pp. 23, 27 |

---

## 4. Data to trend

These are the reads that turn the schedule into something with a signal in it. Both sets are read-only
and safe on a running machine.

### 4.1 Indicator — Info menu, per head (pp. 23, 27)
| Reading | Healthy | Meaning when it drifts |
|---|---|---|
| `Excite` | ≈ 4.5 V (4–5 V) | <4.0 V blocks calibration ("Check excite"); <1 V for 1 s disables the supply ("Excite Shorted!") |
| `S1+` / `S1—` | ≈ half of excite, nearly equal | >0.5 V apart = miswired or bent cell; both >4 V = open EX−; both <1 V = open EX+ |
| `ADC` | ≤100–300 counts of variation; ±10,000 of zero at no load | >±1,000,000 counts = bent cell. Full scale is ±8 M |
| `Offset` | stable | Moves on autozero; a walking offset is build-up |
| `Deadload` | stable | Rising = product build-up in the hopper |
| `Stbl err` | low and flat | Weigh hopper not stabilizing before "Weigh TO" — vibration, air, or a dying cell |
| `Dump err` | low and flat | Hopper not emptying — sticky gate, wet product, jam |

### 4.2 Drives — P0 parameters, both drives (pp. 33–34, 37–38)
| Param | Reading | Why it's on the sheet |
|---|---|---|
| P0-09 | Heatsink temperature | Trends toward trip **08** |
| P0-10 | Run time since date of manufacture | Duty basis for every hour-based decision |
| P0-13 | Trip log, 4 deep with timestamps | The drive's own event log |
| P0-20 | Internal drive temperature | Trends toward trip **23** |
| **P0-23** | Accumulated time heatsink >85 °C | **Must be 0:00:00** |
| **P0-24** | Accumulated time internal >80 °C | **Must be 0:00:00** |
| P0-26 | kWh / MWh meter | Load trend; a climbing kWh at fixed output = mechanical drag |
| P0-27 | Total run time of drive fans | Fan replacement basis (A3) |
| P0-28 | Software version + checksum | Currently `I/O V3.11 72B9`; change = someone reflashed |

Ambient limits for the drives: **−10…50 °C open, −10…40 °C enclosed**, frost and condensation free,
95% RH non-condensing. Which limit applies depends on the IP rating — **VERIFY** (§6).

---

## 5. Spares the schedule assumes on hand

Minimum to execute a PM finding without waiting on freight. All part numbers from §15 (p. 39); WeighTech
numbers, order through WeighTech (1-800-457-3720) unless noted.

- **AV0044** air valve + coil assembly (Festo) — the named wear item on p. 28
- **AV0045** DIN plug and **AV0046** LED gasket — cheap, and the usual cause of a "dead" valve
- **AC0001** weigh hopper cylinder, **AC0002** diverter cylinder
- **1000-10** load cell, 200 lb — one spare covers three hoppers
- **SE0065** / **SE0066** opto receiver/emitter and **SE0038** cordset (Banner, also stocked by distributors)
- **SR0001** / **SR0002** / **SR0003** I/O modules — one of each color; swapping modules is the p. 28 isolation method
- **WE0028** main gasket and **HW0018**/**HW0019** housing screws
- **EP0028** (1 HP) / **EP0029** (2 HP) Optidrive E3 — **VERIFY** whether a drive spare is justified here or covered by a plant-wide pool
- **11377** and **CB0117** sprockets; belting CB0060 / CB0126 are long-lead — **VERIFY** lead times

---

## 6. Open questions

1. **Lakeville vs. Burnsville.** This repo is Burnsville; this machine is Lakeville. Second site, line
   move, or shared EAM instance? Decides where these PMs get loaded and who executes them.
2. **Run hours and sanitation frequency at Lakeville.** Every interval in §3 is a guess without this.
   Daily washdown vs. weekly changes D5/D6 and the whole cylinder/valve interval.
3. **Certified test weights on site?** D3, M2 and Q1 all assume a weight set. Manual expects 1/2/5/10 lb
   (p. 13). Also: what is the site accuracy tolerance, and is this scale sealed for trade?
4. **Indexer mode actually in use** — "Clutch" (air clutch / motor drive), "Stop gate", or "Strflx"
   (Starflex bagger coordination)? The §14 drive is labeled **BOX TAKEAWAY** at 12 Hz max and master M5 is
   "index drive", which reads like clutch/motor drive, not Starflex. Read "Dump settings" / "Indexer" at
   the master to settle it — it changes M1 and the Q4 mechanical scope.
5. **Is the downstream jam opto installed?** Remote 2 M6 is empty in the as-built table (p. 30), but p. 13
   describes the option there. If absent, drop the jam-opto items; if present, add it to D4/M6.
6. **Claw option / box stop fitted?** p. 13 describes a "Claw delay" timer. If fitted, the claw and box
   stop need their own quarterly wear check.
7. **Drive IP rating — IP20 in a cabinet, or IP66/NEMA 4X?** Sets the ambient limit (50 vs 40 °C), whether
   trip 22 (cooling fan fault, IP66 only) can occur, and whether A3 is even a task.
8. **Air supply spec** — pressure setpoint, and lubricated or non-lubricated? Festo's limit is
   **0.1 mg/m³ residual oil (ISO 8573-1 Class 2)** for bio-oils and **5 mg/m³ (Class 4)** for mineral oils;
   above that the valve's basic lubricant flushes out and service life drops. Worth checking the house air
   against, given p. 28 blames air quality first.
9. **Festo manifold model.** §15 gives WeighTech numbers (AV0044–AV0048), not Festo ones. Get the Festo
   part number off the manifold to pull the right service data and price a spare independently.
10. **Load cell manufacturer** for the 1000-10. Drawing shows green/white/red/black + shield, which matches
    a dozen makers in the p. 45 table. Needed before a non-WeighTech replacement.

---

## 7. Action list

1. [ ] Walk §3 with the Lakeville line lead and maintenance supervisor; cut or re-space anything the duty
       cycle doesn't justify. The draft is deliberately conservative.
2. [ ] Answer §6 Q1 (site/EAM) and Q2 (run hours) — these gate loading anything into Aptean EAM.
3. [ ] Read at the master and record: Indexer mode, Opto mode, Target, Index/Preindex/Postindex times,
       Jam time/weight, Wiggle tm/ct, Weigh TO, Dump TO, Zero lmt, Line stop. Settles Q4–Q6 and gives Q2 a baseline.
4. [ ] Take a first §4.1 + §4.2 reading on all three heads and both drives as the **baseline**. Everything
       in §4 is a trend; the first sheet is worth little until there's a second.
5. [ ] Confirm certified test weights and site tolerance; if none, price a 1/2/5/10 lb set before D3 goes live.
6. [ ] Check the drive nameplates for IP rating (Q7) and the Festo manifold for its part number (Q9).
7. [ ] Build the §5 spares list into EAM with min/max; get lead times on CB0060 / CB0126 belting.
8. [ ] Attach `tri_index_3_lakeville.pdf` to the EAM asset record — it is the golden record for both drives'
       parameters (§13/§14) and the only copy of the as-built module map.
9. [ ] Ask WeighTech directly whether a PM schedule exists for this machine that isn't in the manual —
       1-800-457-3720 / info@weightechinc.com. Have App `tri index 3` and Build 49 ready (p. 30 says they
       will ask). If they have one, it supersedes §3.
10. [ ] Once §3 is agreed, load as EAM PM routes: D = operator round, W/M = maintenance, Q/A = planned window.
11. [ ] Capture the identity the manual lacks (§2.1): serial off each of the three indicator front
        panels, any machine nameplate on the frame, and the two drive nameplates. Record here and on the
        EAM asset record — without an indicator serial a WeighTech support call stalls at the first question.

---

## 8. Sources

**Primary (archived in this directory)**
- `tri_index_3_lakeville.pdf` — WeighTech, Inc., *MicroWeigh Triple Indexer*, Buddy's Kitchen, Lakeville MN,
  dated 2026-04-26, 46 pp. All bare page cites above refer to it.
- WeighTech, Inc., Waldron AR — 1-800-457-3720, 479-637-4182, info@weightechinc.com — https://weightechinc.com
- WeighTech MicroWeigh Digital Weight Indicator User's Guide (general indicator, not this machine) —
  https://wp.weightechinc.com/wp-content/uploads/2018/07/MicroWeigh-Digital-Weight-Indicator-Users-Guide.pdf

**Drives**
- Invertek *Optidrive ODE-3 User Guide* Rev 1.01 — §3.9 Routine Maintenance (p. 10), §9.1 Environmental
  (p. 26), §10.1 Fault codes (p. 28) — https://www.machinetoolproducts.com/content/Bardac/optidrive_e3_user_guide_v1pt01.pdf
- Invertek Optidrive E3 support resources — https://www.invertekdrives.com/variable-frequency-drives/optidrive-e3/support-resources
- §3.9 verbatim: *"The drive should be included within the scheduled maintenance program so that the
  installation maintains a suitable operating environment, this should include: Ambient temperature is at
  or below that set out in the 'Environment' section. Heat sink fans freely rotating and dust free. The
  Enclosure in which the drive is installed should be free from dust and condensation; furthermore
  ventilation fans and air filters should be checked for correct air flow. Checks should also be made on
  all electrical connections, ensuring screw terminals are correctly torqued; and that power cables have
  no signs of heat damage."*

**Sensors**
- Banner T18-2 Series (rugged/washdown) — https://www.bannerengineering.com/us/en/products/sensors/photoelectric-sensors/t18-2-series.html
- T18-2VPRL-Q8 receiver (802607) — https://www.bannerengineering.com/us/en/products/part.802607.html
- T18-2NAEL-Q8 emitter (802616) — https://www.bannerengineering.com/us/en/products/part.802616.html

**Pneumatics**
- Festo general operating conditions — compressed air quality, ISO 8573-1 classes, residual oil limits —
  https://www.festo.com/media/cms/media/mam_upload/market/Festo_General_operating_conditions_en.pdf

---

## 9. Event log

- **2026-09-21** Manual `tri_index_3_lakeville.pdf` reviewed end to end (46 pp.) in response to "what PM
  schedules does this have?". **Finding: none — the manual contains no PM schedule at any interval.** The
  two "PM" hits in it are *permanent magnet* (P-51 motor control mode, p. 35; part 10575 motor, p. 39).
  This project directory and the §3 draft schedule created from the manual's failure modes plus component
  OEM guidance. Nothing done to the machine; no readings taken on site yet.
- **2026-09-21** Manual searched for model/serial identification. **Finding: the only serials in the
  document are the two Optidrive E3 drive serials at P0-30** (infeed 649453 / 18 / 057, box takeaway
  654310 / 24 / 083). No machine serial, no WeighTech job number, and no indicator serials are printed
  anywhere — p. 30 confirms the indicator serial lives on the front panel. Recorded in §2.1; capture of
  the panel serials added to §7 as item 11. Still nothing done to the machine.
