# Toppy Inverter Floor Level — Rotation Will Not Run: Handoff Notes

Prepared 2026-09-29 from photos and observations taken at the machine.
Purpose: project memory for Claude Code. Machine data below was transcribed from the nameplate, the paper schematic
set (cover sheet, title blocks, layout sheet, page 23) and photos of the valve stack and control cabinet. Component data
came from OEM datasheets (Omron, Argo-Hytos) and distributor listings (Pizzato). Items marked **VERIFY** are unconfirmed.

**Current lead:** the rotation valves 23Y1/23Y2 get their 24 V through two limit switches in series, 23S1 and 23S2
(schematic page 23). An open switch kills rotation in both directions and leaves the platforms working, which matches
the symptom. See §3 and §4.

---

## 1. Machine and hardware (as photographed)

### Nameplate
| Field | Value |
|---|---|
| Model | TOPPY INVERTER FLOOR LEVEL (pallet inverter; "inverter" = load turner, not a VFD) |
| Serial | **201909002** |
| Year | 2021 |
| Supply | **208 V, 3PH+G, 60 Hz, 5.5 kW** |
| Opening max / min | 2200 / 820 (mm, **VERIFY** units) |
| Max payload | 1500 kg |
| Machine mass | 1800 kg |
| Maker | Toppy srl, Via Muzza Spadetta 18, 40053 Bazzano (BO), Italy. +39 051 833701, www.toppy.it, info@toppy.it |

### Schematic set (paper, at the machine)
| Field | Value |
|---|---|
| Schematic / job number | **5493** |
| Commission | **202104026** |
| Order number | **FR0577** |
| Serial (cover sheet) | 201909002 (matches nameplate) |
| Project | "Inverter Floor Level Toppy America" / project name "Inverter Automatic Toppy America" (PLC-controlled version) |
| Customer | Toppy America |
| Standard | IEC |
| Created / edited | 22/04/2021 / 13/05/2021, by "giuseppem"; responsible: Chiossi Enzo. Page 23 shows modification date 14/05/2021. |
| Size | 36 sheets; template F26_001-BCR-TOPPY02-2020 |

**Page numbering:** the title block carries a "Page N°" (e.g. 4) and a sheet count (e.g. 11/36). Sub-pages exist
(3.a, 3.b, 3.c). Device tags refer to "Page N°", not to the sheet count.

**Tag convention (confirmed on page 23): `<page><letter code><index>`.**
- The numeric prefix is the page: 23Y1–23Y6 and 23S1/23S2 are all drawn on page 23.
- Cross-references read `/page.column`. 21KA7 is marked `/21.7`, meaning its coil is on page 21, column 7.
- The index usually equals the column (23Y1 in column 1 … 23Y6 in column 6), but not always: 23S2 is drawn in column 1.
- Wire numbers on page 23 are `23` + an index (231, 232, 233, 234, 239, 230). The 4-digit wires on the relay coils
  (2011, 2111, 2181) presumably follow the same idea for pages 20–21, **VERIFY**.

### Device list (layout sheet "MACHINE LAYOUT / LAYOUT MACCHINA", plus page 23)
| Tag | As printed (English / Italian) | Drawn as | Notes |
|---|---|---|---|
| 10M0 | Hydraulic control unit motor / Motore centralina idraulica | motor | pump motor, page 10 |
| 14S1 | 0° | sensor near rotation drive | rotation position 0° |
| 14S2 | 180° | sensor near rotation drive | rotation position 180° |
| 14S5 | — | roller switch at the column base, floor level | function **VERIFY** |
| 14SP3 | Platform 1 to 0° pressure switch / Pressostato piattaforma 1 a 0° | pressure switch, contact 1–3 | probably clamp-pressure confirm at 0°, **VERIFY** |
| 14SP4 | Platform 1 to 180° pressure switch / Pressostato piattaforma **2** a 180° | pressure switch, contact 1–3 | English and Italian disagree on platform number; Italian likely correct, **VERIFY** |
| 14BG8, 14BG9 | — | reflex photocells at the middle platform | function **VERIFY** (load presence / protrusion?) |
| 15BG0, 15BG1 | — | reflex photocells at the upper platform | function **VERIFY** |
| 23S1 | Pizzato **FR 355** (page 23) | adjustable roller-lever position switch at the tip of the upper platform | NC contact 11–12, **in series with the rotation valve feed** (§1 page 23). What actuates it: **VERIFY** |
| 23S2 | Pizzato **FR 355** (page 23) | adjustable roller-lever position switch at the tip of the middle platform | NC contact 11–12, **in series with 23S1** in the rotation feed. What actuates it: **VERIFY** |
| 23Y1 | Platform rotation solenoid valve → 180° / Elettrovalvola rotazione piattaforma → 180° | valve solenoid | page 23 col 1 "Rotation 0° → 180°" |
| 23Y2 | Platform rotation solenoid valve 0° ← / Elettrovalvola rotazione piattaforma 0° ← | valve solenoid | page 23 col 2 "Rotation 180° → 0°" |
| 23Y3 | Platform 2 opening / Apertura piattaforma 2 | valve solenoid | |
| 23Y4 | Platform 1 opening / Apertura piattaforma 1 | valve solenoid | |
| 23Y5 | Platform 2 closure / Chiusura piattaforma 2 | valve solenoid | |
| 23Y6 | Platform 1 closure / Chiusura piattaforma 1 | valve solenoid | |
| — | Platform 0 / Piattaforma 0 | floor-level platform | |

### Page 23 — Hydraulic solenoid valves / Elettrovalvole idrauliche (photographed 2026-09-29)
Supply `+24EV` (BU 1.5 mm², enters from the left; source page not legible) and return `0V` (BU-WH 1.5 mm²).
Field terminals are on strips **X5** and **X6** (Weidmüller ZDU 2.5 marked). Valve wires are BU 1 mm².

**Rotation feed (column 1)**, one series chain shared by both directions:

```
+24EV ─ X5:+24EV ─ 23S1 (11–12, NC) ─ X5:239 ─ 23S2 (11–12, NC) ─ X5:230 ─┬─ 21KA7:11
                                                                          └─ 21KA8:11
```

| Relay (coil ref) | Contact | Wire / terminal | Valve | Function |
|---|---|---|---|---|
| 21KA7 (/21.7) | 11–14, fed from X5:230 | 231 → X6:231 | **23Y1** | Rotation 0° → 180° |
| 21KA8 (/21.8) | 11–14, fed from X5:230 | 232 → X6:232 | **23Y2** | Rotation 180° → 0° |
| 21KA1 (/21.1) | 11–14, fed from +24EV | 233 → X6:233 (×2) | 23Y3 + 23Y4 | Platform 2 + platform 1 opening |
| 21KA2 (/21.2) | 11–14, fed from +24EV | 234 → X6:234 (×2) | 23Y5 + 23Y6 | Platform 2 + platform 1 closure |

Each valve returns on its own X6 `0V` terminal to the common 0V.

The consequence: **only the rotation valves pass through 23S1/23S2.** Either switch open means no 24 V on 21KA7/21KA8
terminal 11. The rotation relays still light and click, both rotation directions are dead, and the platforms still
work.

### Hydraulic power unit (Hydroven)
Three stacked directional valves, each **RPE3-063C11/02400E1/M**. They carry Hydroven Oleodinamica branding on an
Argo-Hytos RPE3-06 design. Stack order, looking at the valves:

| Stack position | Left solenoid | Right solenoid | Function |
|---|---|---|---|
| Top | 23Y6 | 23Y4 | Platform 1 close / open |
| **Middle** | **23Y1** | **23Y2** | **Rotation → 180° / → 0°** |
| Bottom | 23Y5 | 23Y3 (assumed, not seen) | Platform 2 close / open |

Decode (Argo-Hytos RPE3-06 ordering code):
- RPE3-06: 4/2 and 4/3 directional valve, solenoid operated, size 06 (D03/CETOP 3), 80 l/min, 350 bar.
- `3`: three positions (two solenoids).
- `C11`: spool symbol. Center condition **VERIFY** against the datasheet spool table.
- `02400`: 24 V DC / 1.29 A.
- `E1`: EN 175301-803-A (DIN) connector.
- `/M`: not in the 2018 ordering table; possibly a Hydroven suffix, **VERIFY**.

Coil label: `16211600 1907191 · 24VDC 100%ED 1,29A`. That means 100 % duty and **≈ 18.6 Ω cold**. The resistance is
calculated as 24 V ÷ 1.29 A, not taken from a datasheet. Whether 16211600 is the coil part number: **VERIFY**.

Datasheet notes:
- The manual override can shift the spool only while port T is below 25 bar.
- On a two-solenoid valve, one solenoid must be de-energized before the other is energized.

**Gauges:**
- Two WIKA EN 837-1 glycerin gauges, 0–250 bar / 0–3500 psi, CL 2.5, each with a blue gauge-isolation knob.
- Two adjustable devices with DIN connectors and knurled knobs sit beside them. They are probably the pressure
  switches 14SP3/14SP4, **VERIFY**.
- Which circuit each gauge reads: **VERIFY**. The operator's reading is that the bottom gauge rises on up/down and the
  top gauge is on rotation.

### Control cabinet (partial)
Omron slim relays, left to right: **20KA1, 21KA1, 21KA7, 21KA2, 21KA8**.

| Relay | Wire on coil terminal | Drives (page 23) |
|---|---|---|
| 20KA1 | 2011 | not on page 23. Lights with every lever move (shared). A wire marked 1257 leaves its contact side. Function **VERIFY** (pump contactor?) |
| 21KA1 | 2111 | 23Y3 + 23Y4, platforms open |
| 21KA7 | 21?? (label hidden) | **23Y1**, rotation 0° → 180°. Expected to light on lever right, **VERIFY** |
| 21KA2 | hidden | 23Y5 + 23Y6, platforms close |
| 21KA8 | 2181 | **23Y2**, rotation 180° → 0°. **Lights on lever left** (photo, 2026-09-29) |

A second row of coil terminals is commoned by an orange jumper bar, and a white wire is marked 0V. Exact model
(G2RV-SL700 assumed from the look) **VERIFY** from the side label.

Omron G2RV-SL700 datasheet data:
- **Terminals:** coil A1(+)/A2(−) at one end; contact 11 = COM, 12 = NC, 14 = NO at the other end. Page 23 uses 11–14.
- **LED:** the LED is on the socket. It shows **coil voltage only, not contact state.**
- **Contact rating:** 6 A @ 30 VDC resistive, **2 A @ 30 VDC inductive** (L/R 7 ms). 21KA7/21KA8 each switch one 1.29 A
  coil. 21KA1/21KA2 each switch **two** coils (≈ 2.6 A), above the 2 A inductive rating. That is a wear item for those
  two relays, not the current fault.
- **Spare:** the plug-in relay for a G2RV-SL700 **24 VDC** unit is **G2RV-1-S DC21**, not DC24.

Right of the relays are Siemens SIRIUS contactor hardware: main terminals 1/L1, 3/L2, 5/L3 plus 21NC, with 24V-labelled
wires, and a front auxiliary block (.1 NC, .3 NO / .2 NC, .4 NO) tagged **24K5**, i.e. drawn on page 24. Which contactor
switches the pump motor 10M0: **VERIFY**.

---

## 2. Event log

- **2026-09-29** Symptom, manual mode:
  - Lever up/down moves the platforms. The top and bottom valves (23Y3–23Y6) energize and the bottom gauge shows pressure.
  - Lever left/right (rotation) does nothing. **23Y1 and 23Y2 never energize** and the top gauge does not move.
- **2026-09-29** Cabinet observation: relays 20KA1 / 21KA1 / 21KA7 / 21KA2 / 21KA8 light up **in pairs** as the lever goes
  up, down, left and right. The PLC therefore appears to command every move, rotation included. Which pair belongs to
  which move was not recorded; each move has a single valve relay on page 23, so the second relay of each pair is
  probably 20KA1, **VERIFY**.
- **2026-09-29** Paper schematic set found at the machine. Photographed so far:
  - cover sheet
  - title blocks of pages 3.c and 4
  - layout sheet legend
  - **page 23** (hydraulic solenoid valves)
- **2026-09-29** Page 23 read: 23Y1 = wire 231 / X6:231 from 21KA7, and 23Y2 = wire 232 / X6:232 from 21KA8. Both
  rotation relays are fed through **23S1 → X5:239 → 23S2 → X5:230**; the platform relays are not. Next step: the X5
  voltage check in §4.
- **2026-09-29** Lever held **left** (photo): LEDs lit on **20KA1 and 21KA8** only; 21KA7 off.
  - Left = 21KA8 = 23Y2 = rotation 180° → 0°.
  - One direction at a time, held steady while the lever is held. So the PLC side is working, and the 24 V is lost
    between 21KA8 and 23Y2.
  - Lever right not photographed yet (expected: 20KA1 + 21KA7).

---

## 3. What the symptoms rule in and out

1. **The hydraulics are not the suspect yet.** The rotation valve never shifts, so nothing downstream of it can
   move or build pressure. The flat top gauge is a consequence, not a second fault.
2. **The lever, PLC inputs and program are fine for this fault.** Lever left lights 21KA8 (with 20KA1) and it stays lit
   while held (photo, 2026-09-29). The PLC is asking for rotation and not aborting.
3. **The top suspect is 23S1 or 23S2 (or their cables or X5 terminals).** Page 23 shows they are the only thing that
   both rotation valves share and the platform valves do not. One of them open produces exactly this symptom:
   - relays click;
   - no 24 V at 21KA7/21KA8 terminal 11;
   - no rotation either way;
   - platforms fine.
4. **Less likely:**
   - The X5:+24EV terminal or its feed wire is loose. The platforms share +24EV only up to the branch before X5.
   - Both rotation relay contacts failed together.
   - Both wires 231 and 232 broke together.
5. **An open switch may be doing its job.** Two NC roller-lever switches wired only into rotation look like a
   "platforms in a safe position to rotate" check, **VERIFY** the intended function with Toppy. Before replacing a
   switch, confirm whether its roller is being pressed by the platform position, the load or debris.
6. **Caveat.** If X5:230 reads 24 V and the relay terminal 11 reads 24 V, go back to the relay contact, wire 231/232,
   the DIN plug and the coil. The same applies if a rotation relay blinks and drops out while the lever is held: that
   sends it back to the PLC permissives.

---

## 4. Test plan (do in order; log each result in §2 with the date)

**Step 1: static check at X5 (no lever, nothing moves).** Machine powered, meter on DC volts. Black lead on any X6 `0V`
terminal, or where the white `0V` wire lands on the relay row. Wire `230` can also be read at terminal 11 on the bottom
of 21KA7/21KA8:

| Red lead on | Expect | If 0 V |
|---|---|---|
| X5 `+24EV` | 24 V | Loose terminal or feed wire into X5 |
| X5 `239` | 24 V | **23S1 open**: roller pressed, lever slipped or bent, switch failed, or cable broken |
| X5 `230` | 24 V | **23S2 open** (same list) |

**Step 2: at the switch that reads open.** This is 23S1 at the upper platform tip or 23S2 at the middle platform tip,
per the layout sheet.
- Is the roller held down? If so, by what: platform position, load, debris.
- Has the lever slipped or bent on its shaft? The FR 355 lever is adjustable, so a loose clamp screw can let it rotate
  into the pressed position.
- Is the cable crushed or cut at a flex point?
- Under **LOTO**, check continuity. X5 `+24EV`↔`239` tests 23S1 and `239`↔`230` tests 23S2. Each should read near 0 Ω
  with the roller free and open with the roller pushed by hand.
- If the switch is actuated by the platform position, reposition the platforms and retest. That is not a fault.

**Step 3: only if X5:230 reads 24 V.** Two people: one holds the lever, one reads the meter. Nobody inside the fence or
rotation zone (§7).
1. 21KA7 / 21KA8 terminal 11 should read 24 V.
2. Terminal 14 should read 24 V with the lever held. 11 at 24 V but 14 at 0 V with the LED lit means a bad relay:
   swap it with a neighbour, and the spare is G2RV-1-S DC21.
3. Then X6:231 / X6:232 with the lever held.
4. Then the DIN plug at the valve, across its two pins.
5. Coil resistance under LOTO: about 18–19 Ω is normal; OL means an open coil.

**Step 4: once 23Y1/23Y2 energize.** If the platform still won't rotate:
- Confirm the top gauge's isolation knob is open.
- Then go hydraulic: rotation actuator, relief setting, and whether the valve spool is stuck.

---

## 5. Open questions (VERIFY)

1. What actuates 23S1 and 23S2, and in which machine state rotation is meant to be blocked. Ask Toppy, or read the
   manual.
2. Where `+24EV` is generated (source page not legible on page 23). Is it switched by the safety circuit?
3. What 20KA1 does (page 20). It lights with every move; pump contactor is the guess. Confirm lever right lights 21KA7.
4. Function of 14S5, 14BG8/9 and 15BG0/1.
5. Where 14SP3/14SP4 are and their set points. Are they the knob-adjusted devices beside the gauges?
6. Which circuit each gauge reads.
7. Spool C11 center condition and the `/M` suffix; the coil part number; the FR 355 contact-block data.
8. PLC make, model and program access; HMI or alarm display, if any.
9. Exact relay model (G2RV-SL700 vs. a later G2RV variant).

---

## 6. Action list

1. [ ] Run §4 step 1 (X5 +24EV / 239 / 230) and log the readings in §2.
2. [ ] Inspect the open switch (§4 step 2), fix the cause (reposition, adjust or replace the lever, replace the
       switch, repair the cable) and log it in §2. Spare: Pizzato FR 355. Match the full code from the switch label
       before ordering; suffixes change the lever and cable entry.
3. [ ] If X5 is fine, run §4 step 3.
4. [ ] After rotation is restored, record the rotation and clamp pressures as a baseline, and confirm the top gauge
       responds.
5. [ ] Ask Toppy America for the manual, the schematic PDF and a PLC program backup, quoting commission 202104026,
       serial 201909002, order FR0577 and schematic 5493. Ask what 23S1/23S2 guard against. Attach the documents to
       the asset in Aptean EAM.
6. [ ] Photograph pages 14, 20, 21 and 22 for the record (not needed for this fault).
7. [ ] Spares, after the fault is known:
       - 1 × Pizzato FR 355 (if a switch failed)
       - 2 × G2RV-1-S DC21 relays
       - 1 × 24 VDC RPE3 coil (confirm the part number first)
       - a DIN 43650 LED test adapter
8. [ ] Consider the 21KA1/21KA2 loading (two coils, ≈ 2.6 A inductive, on a relay rated 2 A inductive). Watch for
       platform-move relay failures.

---

## 7. Safety

- Nothing here authorizes work on a running machine. Follow site LOTO and PVR procedures.
- **Do not jumper X5 `+24EV` to X5 `230`**, and do not jumper around 23S1/23S2, to get rotation running. That bypasses
  both rotation interlocks. Find out why the switch is open.
- Keep everyone out of the fence and rotation zone while testing live. If a loose wire makes contact mid-test, the
  platforms will rotate.
- **Do not** push the manual-override pins on the 23Y1/23Y2 valve, and do not jumper 24 V onto it, to "test"
  rotation. Either one rotates with every interlock bypassed and nothing confirming the load is clamped.
- The cabinet also carries 208 V 3-phase for the pump motor. Meter the 24 V side only under site live-work rules.

---

## 8. Sources
- Toppy schematic 5493, page 23 "Hydraulic solenoid valves / Elettrovalvole idrauliche" (paper set at the machine,
  photographed 2026-09-29). Wiring in §1 is transcribed from it.
- Omron G2RV series datasheet (terminals, LED on socket, contact ratings, G2RV-1-S DC21 replacement):
  https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2375/G2RV%20Series.pdf
- Argo-Hytos RPE3-06 datasheet (ordering code, 24 V DC / 1.29 A, manual override limit):
  https://www.salhydro.fi/files/PDF/AH-RPE3-06-2018.pdf
  (also https://paro.nl/library//storage/datasheets/Argo-Hytos/EN/AH_RPE3-06_HA4010_en.pdf/datasheet.html)
- Pizzato FR 355, adjustable roller-lever position switch (distributor listing; no full datasheet found yet):
  https://automationdistribution.com/fr-355/
- Toppy America:
  - https://www.toppyamerica.com/contact : 97 River Road, Canton, CT 06019; (860) 693-6971; toll-free
    (888) 468-6779; info@toppyamerica.com
  - An MHI member listing gives Charlotte, NC, (704) 676-1190 instead, probably outdated:
    https://www.mhi.org/members/41421
- Toppy srl (Italy): from the machine nameplate.
