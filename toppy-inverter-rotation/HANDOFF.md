# Toppy Inverter Floor Level — Rotation Will Not Run: Handoff Notes

Prepared 2026-09-29 from photos and observations taken at the machine.
Purpose: project memory for Claude Code. Machine data below was transcribed from the nameplate, the paper schematic
set (cover sheet, title blocks, layout sheet) and photos of the valve stack and control cabinet. Component data came from
OEM datasheets (Omron, Argo-Hytos). Items marked **VERIFY** are unconfirmed.

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
| Created / edited | 22/04/2021 / 13/05/2021, by "giuseppem"; responsible: Chiossi Enzo |
| Size | 36 sheets; template F26_001-BCR-TOPPY02-2020 |

**Page numbering:** the title block carries a "Page N°" (e.g. 4) and a sheet count (e.g. 11/36). Sub-pages exist
(3.a, 3.b, 3.c). Device tags refer to "Page N°", not to the sheet count.

**Tag convention (inferred): `<page><letter code><column>`.** Example: 21KA7 = relay KA on page 21, column 7. The evidence:
- 20KA1 and 21KA1 both exist, so the prefix is the page and not part of the device number.
- Wire 2111 lands on 21KA1 and wire 2181 on 21KA8, which reads as page 21, column 1 and column 8.
- Every tag on the layout sheet ends in a single digit 0–9.

If this holds, 23Y1/23Y2 are drawn on **page 23, columns 1–2**. **VERIFY** on pages 21 and 23.

### Device list (layout sheet "MACHINE LAYOUT / LAYOUT MACCHINA")
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
| 23S1 | — | roller switch at the tip of the upper platform | function **VERIFY**; same page/column as 23Y1 |
| 23S2 | — | roller switch at the tip of the middle platform | function **VERIFY**; same page/column as 23Y2 |
| 23Y1 | Platform rotation solenoid valve → 180° / Elettrovalvola rotazione piattaforma → 180° | valve solenoid | rotation valve, solenoid a |
| 23Y2 | Platform rotation solenoid valve 0° ← / Elettrovalvola rotazione piattaforma 0° ← | valve solenoid | rotation valve, solenoid b |
| 23Y3 | Platform 2 opening / Apertura piattaforma 2 | valve solenoid | |
| 23Y4 | Platform 1 opening / Apertura piattaforma 1 | valve solenoid | |
| 23Y5 | Platform 2 closure / Chiusura piattaforma 2 | valve solenoid | |
| 23Y6 | Platform 1 closure / Chiusura piattaforma 1 | valve solenoid | |
| — | Platform 0 / Piattaforma 0 | floor-level platform | |

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

| Relay | Wire on the top (coil) terminal |
|---|---|
| 20KA1 | 2011 |
| 21KA1 | 2111 |
| 21KA7 | 21?? (label hidden) |
| 21KA2 | hidden |
| 21KA8 | 2181 |

A second row of coil terminals is commoned by an orange jumper bar, and a white wire is marked 0V. Exact model
(G2RV-SL700 assumed from the look) **VERIFY** from the side label.

Omron G2RV-SL700 datasheet data:
- **Terminals:** coil A1(+)/A2(−) at one end; contact 11 = COM, 12 = NC, 14 = NO at the other end.
- **LED:** the LED is on the socket. It shows **coil voltage only, not contact state.**
- **Contact rating:** 6 A @ 30 VDC resistive, **2 A @ 30 VDC inductive** (L/R 7 ms). One 1.29 A valve coil is within
  rating.
- **Spare:** the plug-in relay for a G2RV-SL700 **24 VDC** unit is **G2RV-1-S DC21**, not DC24.

There is also a Siemens contactor (1/L1, 3/L2, 5/L3) right of the relays with 24V-labelled wires. It is probably the pump
contactor for 10M0, **VERIFY**.

---

## 2. Event log

- **2026-09-29** Symptom, manual mode:
  - Lever up/down moves the platforms. The top and bottom valves (23Y3–23Y6) energize and the bottom gauge shows pressure.
  - Lever left/right (rotation) does nothing. **23Y1 and 23Y2 never energize** and the top gauge does not move.
- **2026-09-29** Cabinet observation: relays 20KA1 / 21KA1 / 21KA7 / 21KA2 / 21KA8 light up **in pairs** as the lever goes
  up, down, left and right. The PLC therefore appears to command every move, rotation included. Which pair belongs to
  which move was not recorded yet.
- **2026-09-29** Paper schematic set found at the machine. Photographed so far:
  - cover sheet
  - title blocks of pages 3.c and 4
  - layout sheet legend

  Output and relay pages (14, 20–23) are not photographed yet.

---

## 3. What the symptoms rule in and out

1. **The hydraulics are not the suspect yet.** The rotation valve never shifts, so nothing downstream of it can
   move or build pressure. The flat top gauge is a consequence, not a second fault.
2. **The lever, PLC inputs and program permissives are probably fine.** The relays light for left/right, so the PLC is
   asking for rotation. The fault is most likely in the output path: relay contact, the 24 V feed to that contact,
   wiring or terminals, anything wired in series, the DIN plug, then the coil or its 0 V return.
3. **Both directions died at once.** One shared failure is more likely than two independent ones. Ranked:
   1. The 24 V feed to the rotation relay contacts is dead (fuse, breaker, or a safety-relay contact).
   2. A device is wired in series with both rotation solenoids. The tag numbering puts 23S1/23S2 on page 23 in the same
      columns as 23Y1/23Y2.
   3. A shared cable, junction or 0 V return for the rotation valve is broken.
   4. Two relays failed together. This is least likely, unless each direction runs through two relays with one in
      common.
4. **Caveat.** Two observations would send the diagnosis back to the PLC side:
   - the relays that light for left/right turn out to be only a shared relay (pump) plus a non-valve relay;
   - the rotation relay blinks and drops out while the lever is still held.

   Either way the program is refusing or aborting. Check the permissives:
   - Exactly one of 14S1/14S2 is on.
   - Clamp pressure is confirmed on 14SP3 (at 0°) or 14SP4 (at 180°).
   - The photocells 14BG8/9 and 15BG0/1 are clean and clear.
   - The safety circuit is reset and all guards are closed.

---

## 4. Test plan (do in order; log each result in §2 with the date)

Two people: one holds the lever, one reads the meter. Nobody inside the fence or rotation zone (see §7).

1. **Map relays to moves.** Hold up, down, left, right in turn and note which relays light for each.
   - A relay lit for every move is shared, probably the pump.
   - A relay lit only for left or right is a rotation relay. The unconfirmed guess from the numbering is 21KA1 → 23Y1
     and 21KA2 → 23Y2, possibly paired with 21KA7/21KA8.
   - Note whether the rotation relay **stays lit** while the lever is held.
2. **Look before metering.** Check for a tripped breaker, a blown fuse or a fuse indicator lamp in the 24 V section,
   and any fault lamp or HMI message.
3. **Measure at the rotation relay.** DC volts, black lead on 0 V, lever held:

   | Terminal 11 | Terminal 14 | Meaning | Next |
   |---|---|---|---|
   | 0 V | — | Nothing feeds the contact | Trace the feed upstream (page 21/23): fuse, breaker, safety contact |
   | 24 V | 0 V (LED lit) | Relay contact not closing | Swap with an identical neighbour (white latch) to confirm; replace (G2RV-1-S DC21) |
   | 24 V | 24 V | Relay OK | Step 4 |

4. **Measure at the valve.** Unplug the 23Y1 DIN plug and measure across its two coil pins with the lever held.
   - **No 24 V:** the fault is the field wiring, a terminal, or a series device (23S1/23S2?).
   - **24 V from a pin to 0 V, but nothing across the pins:** the 0 V return is open.
   - **24 V across the pins:** go to step 5.
5. **Coil check (LOTO).** Measure the coil resistance across the valve pins. About 18–19 Ω is normal (compare with the
   23Y3–23Y6 coils). OL means an open coil. Repeat for 23Y2.
6. **Once 23Y1/23Y2 energize.** If the platform still won't rotate:
   - Confirm the top gauge's isolation knob is open.
   - Then go hydraulic: rotation actuator, relief setting, and whether the valve spool is stuck.

Identifying the 23Y1/23Y2 wires without the drawing:
- **Live:** the wire on terminal **14** of the relay that lights for left (or right) goes to that solenoid, possibly
  via a terminal strip. Following the 2011/2111/2181 pattern, expect a number starting 231…/232…, **VERIFY**.
- **Dead (LOTO):** unplug the valve's DIN plug and jumper its feed pin to the ground pin. In the cabinet, find the
  terminal that now rings to ground. Remove the jumper afterward.

---

## 5. Open questions (VERIFY)

1. Tag convention = page + column? Check on pages 21 and 23.
2. Which relay(s) drive 23Y1 and 23Y2, and what 20KA1, 21KA7 and 21KA8 do.
3. What is wired in series between the rotation relays and 23Y1/23Y2 (fuse, safety contact, 23S1/23S2?).
4. Function of 23S1, 23S2, 14S5, 14BG8/9 and 15BG0/1.
5. Where 14SP3/14SP4 are and their set points. Are they the knob-adjusted devices beside the gauges?
6. Which circuit each gauge reads.
7. Spool C11 center condition and the `/M` suffix; the coil part number.
8. PLC make, model and program access; HMI or alarm display, if any.
9. Exact relay model (G2RV-SL700 vs. a later G2RV variant).

---

## 6. Action list

1. [ ] Photograph schematic pages **14, 20, 21, 22, 23** by "Page N°", full sheet, flat, with the border column
       numbers readable.
2. [ ] Record the relay-to-move map (§4 step 1).
3. [ ] Run §4 steps 2–5; log the results in §2.
4. [ ] Repair per the result (fuse, relay, wiring, switch or coil); log it in §2.
5. [ ] After rotation is restored, record the rotation and clamp pressures as a baseline, and confirm the top gauge
       responds.
6. [ ] Ask Toppy America for the manual, the schematic PDF and a PLC program backup, quoting commission 202104026,
       serial 201909002, order FR0577 and schematic 5493. Attach them to the asset in Aptean EAM.
7. [ ] Spares, after the fault is known:
       - 2 × G2RV-1-S DC21 relays
       - 1 × 24 VDC RPE3 coil (confirm the part number first)
       - a DIN 43650 LED test adapter for future valve checks

---

## 7. Safety

- Nothing here authorizes work on a running machine. Follow site LOTO and PVR procedures.
- Keep everyone out of the fence and rotation zone while testing live. If a loose wire makes contact mid-test, the
  platforms will rotate.
- **Do not** push the manual-override pins on the 23Y1/23Y2 valve, and do not jumper 24 V onto it, to "test"
  rotation. Either one rotates with every interlock bypassed and nothing confirming the load is clamped.
- The cabinet also carries 208 V 3-phase for the pump motor. Meter the 24 V side only under site live-work rules.

---

## 8. Sources
- Omron G2RV series datasheet (terminals, LED on socket, contact ratings, G2RV-1-S DC21 replacement):
  https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2375/G2RV%20Series.pdf
- Argo-Hytos RPE3-06 datasheet (ordering code, 24 V DC / 1.29 A, manual override limit):
  https://www.salhydro.fi/files/PDF/AH-RPE3-06-2018.pdf
  (also https://paro.nl/library//storage/datasheets/Argo-Hytos/EN/AH_RPE3-06_HA4010_en.pdf/datasheet.html)
- Toppy America:
  - https://www.toppyamerica.com/contact : 97 River Road, Canton, CT 06019; (860) 693-6971; toll-free
    (888) 468-6779; info@toppyamerica.com
  - An MHI member listing gives Charlotte, NC, (704) 676-1190 instead, probably outdated:
    https://www.mhi.org/members/41421
- Toppy srl (Italy): from the machine nameplate.
