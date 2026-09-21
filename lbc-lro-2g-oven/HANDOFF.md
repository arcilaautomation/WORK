# LBC LRO-2G5 Rack Oven — Will Not Reach Set Point: Handoff Notes

Prepared 2026-09-21 for Johnathan (Data Analyst / Maintenance Systems Planner, Buddy's Kitchen, Burnsville MN).
Purpose: project memory for Claude Code. Everything below came from the LBC OEM manuals, the LBC
factory schematic set (DWG 61111-174-4), and the Fenwal control datasheet. Items marked **VERIFY**
are unconfirmed and must be checked on the machine.

**Nothing here authorizes work on a running machine.** The heat circuit is live 120 VAC, the gas train is
live, and the chamber runs to 525 °F. Follow site LOTO. Gas pressure, manifold pressure, combustion and
CO testing are the work of a qualified gas technician — LBC requires factory-authorized start-up and
recommends authorized preventive maintenance every 6 months (Operators manual p.21). Burner cleaning
and adjustment, and thermostat calibration after the first 30 days, are explicitly outside LBC warranty.

---

## 1. The machine

| Item | Value | Source |
|---|---|---|
| Model | LBC Bakery Equipment **LRO-2G5**, double rack oven, gas | Spec sheet LRO-2G5 (2/19) |
| Input rate | **290 kBTU/hr** natural gas | Install/Service p.7 |
| Burner | In-shot burners, single-stage on/off, hot surface igniter | Parts list p.42; schematic sheet 4 |
| Gas supply pressure | **NG 5" wc min / 14" wc max**; propane 10"/14" wc | Install/Service p.7, p.23 |
| Manifold pressure | **NG 3.5" wc**, propane 7.0" wc — *see tag on the valve* | Install/Service p.7 |
| Orifice drill size | **NG #45**, propane **#55** (LRO-2G5) | Install/Service p.7 |
| Gas line | 1" NPT minimum, sized for full rate | Install/Service p.23 |
| Temperature range | **100–525 °F** (so a 475 °F set point is inside spec) | Spec sheet LRO-2G5 |
| Venting | 800 CFM, 1" wc pressure drop, 8" round collar; **rooftop ventilator not supplied by LBC** | Install/Service p.7 |
| Water | 40 psi min / 100 psi max; ~3.5 gal/hr normal steam use | Install/Service p.7; spec sheet |
| Ambient limit | Air around and above the oven must not exceed **104 °F** | Operators manual p.21 |
| Circulation blower | 3-phase motor M1, contactor MR1, overload OL1 — **rotation must be CCW viewed from top** | Install/Service p.26; schematic sheet 2 |

### Heat-train part numbers (Install/Service p.42, p.40)

| Part | Number |
|---|---|
| Manifold with orifices (LRO-2G) | 160-1334 |
| Gas orifices, NG | 80400-45 (propane 80400-55) |
| Gas module | 80300-18 |
| Gas valve | 80505-14 |
| Hot surface igniter | 80302-12 |
| Complete burner (LRO-2G) | 160-1332 |
| In-shot burner | 80002-14 |
| Flame sensor assembly | 150-1488 |
| Draft blower | 30200-87 |
| Over-limit (hi limit) | 30707-06 |
| Overload relay, 208–240 V blower motor | 30707-03 (480 V: 30707-02; 1-ph: 30707-05) |
| Contactor, blower motor | 30700-15 |
| Thermocouple, −70 digital control | 41100-42 |
| RTD temp sensor / K-type TC, Android touchscreen control | 41100-33 / 41100-42a |

**VERIFY** which control this oven has: **−70 digital**, **−54**, or **Android touchscreen (−100)**. It changes the
temperature sensor type (−70 = K-type thermocouple 41100-42; touchscreen = RTD 41100-33) and the
parameter names. The Install/Service start-up form lists −70 parameters as Sb, St, id, IL, PL, tP, T4, t5, t6
and −54 parameters as Temp offset, 1K Probe Cal, Serial/IR, Lock Feature, Temp Scale, AEMS, Set Back,
SB Temp, SB Delay (p.27).

---

## 2. Symptom as reported (2026-09-21)

Set point commanded to 475 °F. Oven **plateaus near 410 °F and then falls away**. Reported as "not heating."

Not yet established — see §6:
- whether the burner is still firing while the temperature falls,
- whether 410 °F is the *real* chamber temperature or only the displayed one,
- whether the oven ever held 475 °F.

---

## 3. What the symptom already tells us

The burner on this oven is **single-stage on/off** — the Fenwal energizes the gas valve or it does not; there is
no modulation to be stuck on low (schematic sheet 4). So a steady plateau below set point means one of
exactly two things, and separating them is the whole job:

**Family A — the burner is firing, but the oven cannot hold 475 °F.** Heat input equals heat loss at ~410 °F.
Causes are underfiring (gas pressure, orifices, partially lit burner), heat not reaching the chamber
(circulation blower, fouled heat exchanger), or excess loss (vent damper open, door seal, steam water,
over-exhausting hood).

**Family B — the burner is cutting out.** The oven climbs, an interlock or the flame-safety control drops the
gas valve, and the chamber coasts down. The control still shows a call for heat, so it "looks like" it is trying.

The reported "**and drops**" leans toward **Family B**, because in Family A the oven normally sits at its
equilibrium temperature rather than falling away from it. But a rising loss (door openings, a load going in,
steam) will also pull a Family A oven down, so this is a lean, not a conclusion.

### The decisive signature for Family B

The Fenwal 35-65 is a **3-try** control with a **1-hour auto-reset**: after three failed trials for ignition it locks
out, and if the thermostat is still calling for heat it **automatically resets and retries after one hour**
(Fenwal datasheet p.2). So — *if the oven goes cold for roughly an hour and then fires again on its own,
that is a lockout, full stop.* That single observation would close out the diagnosis.

---

## 4. The heat interlock chain — the best diagnostic on this machine

From LBC schematic **sheet 4, DWG 61111-174-4** ("Schematic, Rack Oven w/ Android Control"). The heat
call passes through a series string of interlocks, and **each node lights an indicator lamp**. The Operators
manual (p.28) says it plainly: *"The heat sequence lights will turn on in sequence when the thermostat
control turns the heat on. If a light does not turn on, it indicates a fault that will not allow the oven to heat."*
The lights are on the left side of the control box and are visible with no covers removed.

```
Control "Heat" output (wire 47)
   └─► THERMOSTAT LIGHT            ← control is calling for heat
   ├─ Hi Limit (over-limit 30707-06)
   │     └─► HOOD/HIGH LIMIT LIGHT (wire 48)
   ├─ Hood Air-flow Switch
   │     └─ (wire 49) ─► MR11 draft blower relay → draft blower
   ├─ Draft Blower Airflow Switch  (via sensor hose)
   │     └─► DRAFT BLOWER LIGHT (wire 49a)
   ├─ MR1 blower relay contact  (circulation blower running, OL1 not tripped)
   │     └─► CIRC. BLOWER LIGHT (wire 54)
   └─► Fenwal 35-65 HSI flame safety control, 3-try, 4-sec TFI
          ├─ Hot surface igniter (wire 54B)
          ├─ Gas valve MV1 (wire 54A)
          └─ Flame sensor → S2/FS (wire 55)
```

The control also takes **feedback inputs**: Door (60), Hood airswitch (61), Damper, and **Gas Valve (54A)** —
so the control itself knows whether the gas valve is energized (schematic sheet 3).

**Read it this way, at the moment the temperature starts to fall:**

| What you see | What it means |
|---|---|
| Thermostat light OFF | The control is not calling for heat. Set point, sensor reading, or a setback/recipe feature — go to §5 test 3. |
| Thermostat ON, Hood/High Limit light OFF | **Hi Limit tripped.** The chamber is hotter than the display says, or the limit has failed. Strongly implies a sensor/calibration fault. |
| Hood/High Limit ON, Draft Blower light OFF | Hood airflow switch or draft blower airflow switch not proving. Loaded hood filters, slipping rooftop fan belt, weak draft blower, or a cracked/condensate-plugged sensor hose. |
| Draft Blower ON, Circ. Blower light OFF | MR1 dropped — **circulation blower overload OL1 tripped** (auto-resets when cool → oven recovers, then drops again). |
| All four lights ON, no flame | Fenwal problem: flame sense, igniter, gas valve, or gas supply. Read the Fenwal LED. |

**VERIFY** this light-to-node mapping against the schematic in this oven's own control compartment. The
sheet above is the Android-control drawing; the −70 and −100 controls share the drawing set (sheet 3
references both) but confirm the lamp labels physically. The label "Hood/High Limit Light" is ambiguous —
on the drawing its lamp sits on wire 48, *after* the Hi Limit and *before* the hood air-flow switch.

### Fenwal 35-65 LED codes (Fenwal datasheet p.2)

| LED | Fault |
|---|---|
| Steady on | Internal control failure |
| 1 flash | Airflow fault (35-66 models) |
| 2 flashes | Erroneous flame signal (gas valve not closing completely) |
| **3 flashes** | **Lockout** |

Flame sensitivity is **0.7 µA minimum** (spec table); the troubleshooting section states the minimum flame
current to keep the system out of lockout is **1 µA**, measured with a DC microammeter across the
**FC+ / FC−** test pins — *"meter should read 1 microamp or higher."* The LBC start-up form has a line for
exactly this: *"Check sensor microamps or voltage at Fenwal"* (Install/Service p.27).

Also from the Fenwal datasheet: if the **airflow signal is lost while the burner is firing**, the control
immediately de-energizes the gas valve and signals an airflow fault. And if **flame is lost while running**,
the control retries immediately and makes 2 more attempts before locking out.

---

## 5. Diagnostic sequence

Ordered by information-per-minute. Tests 1–3 need no tools and no covers off.

### Test 1 — Watch the heat sequence lights as it falls (no tools, 10 minutes)
Bring the oven to the plateau, then watch the four lights while the temperature drops. Use the table in §4.
This is the single test that splits Family A from Family B and localizes Family B to one component.

### Test 2 — Is the burner actually firing at the plateau?
Look/listen at the burner compartment and confirm the gas valve is energized when the display sits at 410 °F.
Firing but not climbing → Family A. Not firing while the thermostat light is on → Family B.

### Test 3 — Is 410 °F real? (independent thermometer)
Put a calibrated probe or oven thermometer in the chamber and compare to the display.
- **Chamber really at ~410 °F** → genuine heat shortfall, Family A.
- **Chamber much hotter than 410 °F** → the sensor or its calibration is lying, the burner is over-running, and
  the Hi Limit is almost certainly what is cutting the heat. On a −70 control the sensor is a K-type
  thermocouple (41100-42); an aged or reversed-polarity thermocouple, a wrong extension lead, or a control
  offset all read low. Check the −54 "Temp offset" / "1K Probe Cal" or the −70 parameters against the
  commissioning values on the start-up form.

### Test 4 — Gas supply pressure, static and running (qualified gas tech, manometer)
The LBC start-up form takes both readings for a reason (Install/Service p.26–27): *"Gas Supply-side Pressure
(Inches WC)"* and *"Supply side gas pressure when burner is running."*
- Supply must stay **≥ 5" wc NG while the burner is firing**. A reading that is fine at rest and sags under fire
  means an undersized or shared line, a regulator at capacity, or a partially closed valve.
- **Watch what else is on the same line.** If the oven holds 475 °F alone but falls back to ~410 °F when the
  second oven / proofer / boiler fires, that is supply droop and it is a piping problem, not an oven problem.
- Manifold pressure should be **3.5" wc on NG** — and confirm against the tag on the valve.
- Never apply more than 14" wc to the gas valve (Install/Service, NOTICE p.17).

### Test 5 — Orifices and gas type
Confirm the data plate gas type against the orifices actually fitted: **#45 for natural gas, #55 for propane**.
Propane orifices on a natural-gas supply would badly underfire the oven and would produce exactly this
plateau. Worth two minutes if the oven was ever converted or a manifold was ever replaced.

### Test 6 — Rate-of-rise benchmark
LBC's own commissioning test: *"Set to 300 F. Minutes to go from 150 to 250 F"* (Install/Service p.27).
Run it and record the number. It turns "seems slow" into a figure you can compare against this oven's
start-up form and against the sister oven. **VERIFY** — retrieve the original start-up form for the target value.

### Test 7 — Heat-loss path check (Family A)
- **Vent damper.** The recipe's vent setting has three options: **OPEN** (vent open the whole bake),
  **AUTO** (opens for the last third), **CLOSED** (Operators manual p.32). A recipe left on OPEN, or a damper
  stuck open mechanically, bleeds heat continuously. Check the commanded setting *and* the actual damper.
- **Steam solenoid weeping.** A steam valve passing water continuously is a large, constant heat sink and
  will hold the chamber below set point. Tell-tale: hot water running at the drain when no steam was called.
- **Door seal and bottom sweep.** Start-up form checks the latch-side and top door gaps are even within 1/8",
  and that the floor sweep lowers and seals (Install/Service p.26).
- **Hood over-exhausting / make-up air.** The integrated hood is 800 CFM. Too much exhaust, or not enough
  make-up air in the room, hurts both heat retention and combustion.

### Test 8 — Air side (Family A)
- **Circulation blower rotation must be CCW viewed from the top** (Install/Service p.26). If the motor or its
  supply was ever re-landed and two phases swapped, rotation reverses and heat transfer collapses while
  everything still "runs." The schematic even shows an *optional circulation fan direction sensor* (sheet 3),
  which tells you LBC considers this a live failure mode.
- **Air shutter settings.** LRO-2G5 shutter gaps and angles are tabulated per row (rear 94°, middle 90°,
  front 100 (85)°) on Install/Service p.29 — measured with LBC's spacing and angle tools.
- **Draft blower, heat exchanger, flue.** Soot or fouling in the linear counterflow heat exchanger
  (weldment 160-1329-20A) or a restricted flue cuts transfer *and* makes the draft airflow switch marginal —
  and flue resistance rises as the oven gets hotter, which fits a fault that appears only near the top of the range.

### Test 9 — Combustion test (qualified tech only)
Start-up form: set 350 °F, fire one minute, measure **CO in PPM**, photograph the reading, and check flame
sensor microamps at the Fenwal (Install/Service p.27). A sooting or oxygen-starved burner shows up here.
**A cracked heat exchanger or a CO problem is a stop-work condition, not a performance note.**

### Test 10 — Back-up control bypass
The oven has back-up controls: set the electronic control off, "Lights & Rotation" on, "Heat & Blower" on,
and turn the back-up dial thermostat up — note the dial is **graduated in °C** (Operators manual p.29).
If the oven makes full heat on the back-up thermostat but not on the digital control, the fault is in the
control / sensor / set point, not in the gas train.

---

## 6. Open questions — answer these first

1. **Which control** is fitted: −70 digital, −54, or Android touchscreen? (§1)
2. **Has this oven ever held 475 °F?** Or has it always topped out lower? Gradual decline or sudden onset?
3. **What do the heat sequence lights do when the temperature falls?** (Test 1 — highest value)
4. **Is the burner firing at the 410 °F plateau?** (Test 2)
5. **Does it fail only when other gas equipment runs** — second oven, proofer, boiler? (Test 4)
6. **Empty or loaded? With steam or without?** Does it hold better empty?
7. **Recipe settings:** vent OPEN / AUTO / CLOSED, blower ON / PULSE / DELAY?
8. **Does it come back to life roughly an hour after going cold?** (Fenwal lockout signature, §3)
9. **Natural gas or propane** per the data plate — and which orifices are actually in the manifold?
10. Any **yellow flame, soot, combustion smell, or CO alarm**? Any hot water at the drain when idle?
11. Is there a **sister LRO** on site to compare readings against? Is the original **start-up form** on file?

---

## 7. Action list

1. [ ] Run Test 1 (heat sequence lights at the moment of the drop) and Test 2 (burner firing?). Record which
       light drops out — that alone selects the branch.
2. [ ] Run Test 3 (independent thermometer vs. display). Settles whether the sensor is lying.
3. [ ] Check the recipe vent setting and the damper, and check the drain for a weeping steam solenoid (Test 7).
4. [ ] Schedule the qualified gas tech for Tests 4, 5 and 9 — supply pressure static **and running**, manifold
       pressure against the valve tag, orifice size, CO, flame microamps at the Fenwal FC+/FC− pins.
5. [ ] Confirm circulation blower rotation is CCW from the top (Test 8).
6. [ ] Run the LBC rate-of-rise benchmark (Test 6) and record it as this oven's new baseline.
7. [ ] Retrieve the original LBC start-up form for this oven — it holds the commissioned gas pressure,
       rate-of-rise, control parameters and shutter settings. Attach it to the asset record in Aptean EAM.
8. [ ] Log the outcome with a date in §8 and replace the **VERIFY** markers with findings.
9. [ ] If PM is overdue: LBC recommends authorized preventive maintenance every 6 months (Operators p.21).

---

## 8. Event log

- **2026-09-21** Symptom reported: set point 475 °F, oven plateaus ~410 °F and drops. LRO-2G5 spec sheet
  supplied. No on-machine readings taken yet. This document created from OEM documentation only —
  every cause below §3 is a hypothesis until Tests 1–3 are run.

---

## 9. Sources

- LBC LRO-2G5 spec sheet (2/19), supplied as `b2600958-LBC_-_LRO-2G.pdf` — also at
  https://www.lbcbakery.com/wp-content/uploads/2017/12/LRO-2G5-Spec-12-17.pdf
- LBC LRO-1G5/2G5/1E5/2E5 **Installation, Service and Parts Manual**, Rev 10-19 (51 pp) —
  https://www.lbcbakery.com/wp-content/uploads/2019/10/LRO-Install-Service-10-19.pdf
  (specs p.7, gas connection p.23, **start-up form p.26–27**, air shutters p.28–29, parts p.40–42,
  schematics p.45–50)
- LBC LRO **Operators Manual**, Rev 12-2021 —
  https://www.lbcbakery.com/wp-content/uploads/2022/07/LRO-Operators-manual-12-2021.pdf
  (PM interval p.21, control compartment / heat sequence lights p.28, back-up controls p.29,
  blower and vent functions p.32)
- LBC factory schematic set **DWG 61111-174-4**, "Schematic, Rack Oven w/ Android Control" —
  sheet 2 power connections, sheet 3 control I/O, **sheet 4 heat circuit** (in the Install/Service manual above)
- Fenwal Series 35-65 / 35-66 24 VAC HSI control datasheet (DS 35 65 66) —
  https://www.pvi.com/dfsmedia/0533dbba17714b1ab581ab07a4cbb521/60528-source/637395363700000000/fenwal-35-65-and-35-66-24-vac-hsi-control-manual.pdf
  (flame sensitivity p.1, sequence / lockout / LED codes / troubleshooting p.2)
- LBC PDF library — https://www.lbcbakery.com/pdf-library/
- LBC Bakery Equipment, 6026 31st Ave NE, Marysville WA 98271 — 888-722-5686 (888-RACKOVN),
  sales@lbcbakery.com
