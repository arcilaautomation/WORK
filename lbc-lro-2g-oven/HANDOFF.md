# LBC LRO-2G5 Rack Oven — Will Not Reach Set Point: Handoff Notes

Prepared 2026-09-21 for Johnathan (Data Analyst / Maintenance Systems Planner, Buddy's Kitchen, Burnsville MN).
Purpose: project memory for Claude Code. Everything below came from the LBC OEM manuals, the LBC
factory schematic set (DWG 61111-174-4), and the Fenwal control datasheet. Items marked **VERIFY**
are unconfirmed and must be checked on the machine.

**Status 2026-09-21: the oven recovered on its own and is baking normally.** The fault is therefore
**intermittent and self-clearing**, which is a finding in itself — see §3. Two control settings on this oven
are confirmed and are the leading explanations; neither is a hardware failure. Do not close this out.

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
| Control | **−70 digital control** — confirmed 2026-09-21 by Johnathan. Board **40102-70** | Install/Service p.32; confirmed on machine |
| Temperature sensor | **K-type thermocouple, P/N 41100-42** (the −70 uses a TC, not the touchscreen's RTD) | Install/Service p.32 |
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
| Circuit board, −70 digital control | 40102-70 |
| Thermocouple, −70 control | 41100-42 |

---

## 2. Symptom as reported

- **2026-09-21, reported.** Set point commanded to 475 °F. Oven **plateaus near 410 °F and then falls away**.
- **2026-09-21, later.** *"It went back to normal."* No repair was performed. The oven recovered on its own.

Not yet established — see §7:
- how long it was down, and **what changed at the moment it recovered**,
- where the temperature bottomed out before it came back (the sharpest single discriminator — see §4),
- whether the burner was still firing while the temperature fell,
- whether 410 °F was the real chamber temperature or only the displayed one.

---

## 3. What the symptom tells us

The burner on this oven is **single-stage on/off** — the Fenwal energizes the gas valve or it does not; there
is no modulating valve to be stuck on low fire (schematic sheet 4). So a plateau below set point is either
underfiring / excess heat loss, or the burner cutting out.

**The self-recovery is the most informative fact we have.** It rules out anything that would need a hand on
the machine to clear: wrong orifices, a fouled heat exchanger, a mechanically stuck damper, a failed
thermocouple. Those do not fix themselves. What is left divides into two groups:

**Group 1 — a setting, not a fault.** The oven did exactly what it was told. Both confirmed settings on this
oven (§4) sit in this group, and both "recover" the moment the operating conditions change.

**Group 2 — a genuine intermittent that self-clears on a timer or a thermal reset.** Fenwal lockout with its
1-hour auto-reset; the circulation blower overload OL1 cooling and re-closing; an auto-reset hi limit; or gas
supply pressure recovering when other equipment on the line shuts off.

Group 1 is far more likely given what we know, and costs nothing to check. But Group 2 must be excluded,
because a self-clearing hardware fault always comes back — usually mid-production.

---

## 4. Two confirmed control settings — the leading explanations

### 4a. Vent is set to OPEN — confirmed 2026-09-21

Per the Operators manual (p.32) and the LMO Max operator manual (p.16), the vent has three settings:

| Setting | Behavior |
|---|---|
| **OPEN** | Vent **open for the whole bake**, except while the steam timer is counting down |
| **AUTO** | Closed for the first third of the bake, **open for the last third** |
| **CLOSED** | Closed for the entire bake |

**OPEN is a continuous heat-loss path for the entire bake.** It is the normal setting only for products that
want a dry chamber throughout; for most bread work **AUTO** is the intended setting, because venting
belongs at the end of the bake for crust, not at the start. An oven venting continuously will settle at a lower
equilibrium temperature than one that is closed — which is exactly the shape of "climbs, then sits below
set point."

This also gives a clean recovery mechanism: **vent is a per-recipe setting**, so selecting a different recipe
whose vent is CLOSED or AUTO would make the oven "go back to normal" with nobody touching anything.

> Note: the vent function is **locked out if the control has the programming limitation feature turned on**
> (Operators manual p.32). If the setting cannot be changed at the panel, that is why. **VERIFY** which −70
> parameter carries that lock — `PL` is the plausible candidate in the start-up form's parameter list but is
> not confirmed.

### 4b. Automatic Temperature Setback — on the −70 control

The −70 control has a **Temperature Setback** feature: *"If the oven is left unattended for a period of time,
the control can adjust the temperature set point to a lower setting to conserve energy"*
(LMO Max Operator's Manual Rev B 8-16, p.17 — same 40102-70 control family; the LRO-2G5 spec sheet
lists "Selectable Automatic Temperature Setback" as a standard control feature).

| Parameter | Meaning | Range |
|---|---|---|
| **`Sb`** | Set Back on / off | `ON` / `OF` |
| **`St`** | Setback **temperature** | **180 – 300 °F** (displayed in tens: `18` = 180 °F) |
| **`id`** | Setback **delay** — how long unattended before setback occurs | **20 – 120 minutes** |

These are the first three entries in the −70 column of LBC's start-up form (Install/Service p.27), which lists
`Sb, St, id, IL, PL, tP, T4, t5, t6, t7, t8, t9, P9, T-Offset`.

**To read or change them** (LMO Max Operator's Manual p.17):
1. Turn the control **off**.
2. **Press and hold the F/C button** until the display illuminates. Keep holding it.
3. Press the **time adjust** button to step the time display through `SB` → `St` → `Id`.
4. Press the **steam adjust** button to change the displayed value.

Setback explains the self-recovery perfectly: it engages after 20–120 minutes of the oven sitting unattended,
and releases as soon as the oven is used again — so the oven would appear to "fix itself" the moment
somebody started a bake or opened the door.

### The discriminator between 4a and 4b

**Setback cannot hold the oven at 410 °F — its maximum setback temperature is 300 °F.** So:

- If the temperature kept falling past 410 and **settled somewhere in the 180–300 °F band**, that is
  **setback**, and the oven was never faulty.
- If it **hung at ~410 °F** and stayed there, setback is ruled out, and the vent (or a capacity/interlock
  problem) is in play.

410 °F is above the setback ceiling, so on the reported numbers alone the oven was most likely *on its way
down* when it was observed — but that needs the bottom-out figure to confirm. Ask the operator who saw it.

---

## 5. The heat interlock chain — the best diagnostic when it recurs

From LBC schematic **sheet 4, DWG 61111-174-4**. The heat call passes through a series string of interlocks,
and **each node lights an indicator lamp**. The Operators manual (p.28) says it plainly: *"The heat sequence
lights will turn on in sequence when the thermostat control turns the heat on. If a light does not turn on, it
indicates a fault that will not allow the oven to heat."* The lights are on the left side of the control box and
are visible with no covers removed.

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
| Thermostat light OFF | The control is **not calling for heat** — this is what **setback** looks like (§4b), or a recipe/set-point issue. |
| Thermostat ON, Hood/High Limit light OFF | **Hi Limit tripped.** The chamber is hotter than the display says — implies a sensor/calibration fault. |
| Hood/High Limit ON, Draft Blower light OFF | Hood airflow or draft blower airflow switch not proving. Loaded hood filters, slipping rooftop fan belt, weak draft blower, or a cracked/condensate-plugged sensor hose. |
| Draft Blower ON, Circ. Blower light OFF | MR1 dropped — **circulation blower overload OL1 tripped** (auto-resets when cool → oven recovers, then drops again). |
| All four lights ON, no flame | Fenwal problem: flame sense, igniter, gas valve, or gas supply. Read the Fenwal LED. |

Note the first row: **if the thermostat light is off while the display sits below set point, the control is not
even asking for heat** — which points straight at §4b rather than at anything in the gas train.

**VERIFY** this light-to-node mapping against the schematic in this oven's own control compartment. The
manual's sheet 4 is titled for the Android control; the drawing set covers the −70 as well (sheet 3 references
both), but confirm the lamp labels physically. The label "Hood/High Limit Light" is ambiguous — on the
drawing its lamp sits on wire 48, *after* the Hi Limit and *before* the hood air-flow switch.

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

**The 1-hour signature:** the Fenwal is a **3-try** control with a **1-hour auto-reset** — after three failed trials
for ignition it locks out, and if the thermostat is still calling for heat it automatically resets and retries after
one hour (Fenwal datasheet p.2). *An oven that goes cold, sits for about an hour with nobody touching it,
and then fires again on its own is a lockout.* Also: if the airflow signal is lost while the burner is firing, the
control immediately de-energizes the gas valve; if flame is lost while running, it retries immediately and
makes 2 more attempts before locking out.

---

## 6. Diagnostic sequence

### Now, while the oven is running normally — free, no tools

**Test A — read the setback parameters.** Follow the F/C-button procedure in §4b and write down `Sb`, `St`
and `id`. If `Sb` = ON, note the values. Compare against the original start-up form if it can be found.
This either confirms or eliminates the leading hypothesis in five minutes.

**Test B — check the vent setting on every recipe in use**, not just the one that was running. Confirm which
recipes are set OPEN and whether that is deliberate for that product. For most bread work the intended
setting is AUTO.

**Test C — watch it hold 475 °F empty for an hour**, deliberately leaving it unattended past the `id` delay.
If it walks down to the `St` value on schedule, the case is closed and nothing is broken.

### When it recurs — catch it in the act

**Test 1 — the heat sequence lights** (§5). The single test that localizes the fault. Start with the thermostat
light: on or off tells you immediately whether this is a control decision or a heat-train failure.

**Test 2 — is the burner firing at the plateau?** Confirm the gas valve is energized when the display sits low.

**Test 3 — is the displayed temperature real?** Independent thermometer in the chamber vs. the display.
The −70 uses a **K-type thermocouple (41100-42)**; a drifted TC, reversed polarity, or a wrong extension lead
reads low, which would make the oven over-run and trip the hi limit. The −70 parameter **`T-Offset`** is the
calibration trim — record it before changing anything.

**Test 4 — where does it bottom out?** The 180–300 °F band means setback; hanging at ~410 °F does not (§4).

### Gas side — qualified gas technician only

**Test 5 — supply pressure, static *and* running.** LBC's start-up form takes both (Install/Service p.26–27).
Supply must stay **≥ 5" wc NG while the burner fires**. Fine at rest but sagging under fire = undersized or
shared line, or a regulator at capacity. **Check what else is on the line** — if the oven holds 475 °F alone but
falls back when the second oven / proofer / boiler fires, that is supply droop and it is a piping problem.
Manifold should be **3.5" wc NG**; confirm against the tag on the valve. Never apply more than 14" wc to the
gas valve (Install/Service NOTICE p.17).

**Test 6 — orifices vs. data plate gas type.** **#45 natural / #55 propane.** Propane orifices on natural gas
would badly underfire the oven. Two minutes to check if the oven was ever converted or a manifold replaced.

**Test 7 — combustion.** Set 350 °F, fire one minute, measure **CO in PPM**, and check flame sensor
microamps at the Fenwal FC+/FC− pins (Install/Service p.27). **A cracked heat exchanger or a CO problem is
a stop-work condition, not a performance note.**

### Capacity and loss, if the oven genuinely cannot make 475 °F

**Test 8 — rate-of-rise benchmark.** LBC's own commissioning test: *"Set to 300 F. Minutes to go from 150 to
250 F"* (Install/Service p.27). Turns "seems slow" into a number comparable against the start-up form and
against any sister oven. **VERIFY** — retrieve the original start-up form for the target value.

**Test 9 — heat-loss paths.** Damper actually moving (not just commanded); steam solenoid weeping water
(hot water at the drain with no steam called = a large constant heat sink); door gaps even within 1/8" and
floor sweep sealing (Install/Service p.26); hood over-exhausting or room short of make-up air.

**Test 10 — air side.** **Circulation blower rotation must be CCW viewed from the top** (Install/Service p.26) —
if the motor supply was ever re-landed with two phases swapped, rotation reverses and heat transfer
collapses while everything still "runs." LBC offers an *optional circulation fan direction sensor* (schematic
sheet 3), which tells you they consider this a live failure mode. Air shutter gaps and angles per row are
tabulated on Install/Service p.29 (rear 94°, middle 90°, front 100 (85)°).

**Test 11 — back-up control bypass.** Electronic control off, "Lights & Rotation" on, "Heat & Blower" on,
back-up dial thermostat up — the dial is **graduated in °C** (Operators manual p.29). Full heat on the back-up
thermostat but not on the digital control puts the fault in the control / sensor / set point, not the gas train.

---

## 7. Open questions

1. **How long was the oven down before it went back to normal?** ~1 hour unattended → Fenwal lockout (§5).
2. **What changed at the moment it recovered?** This is the decisive question:
   - recovered when someone **started a bake or opened the door** → **setback** (§4b)
   - recovered when a **different recipe was selected** → **vent OPEN** (§4a)
   - recovered **on its own after ~an hour**, nobody touching it → **Fenwal lockout auto-reset**
   - recovered when **other gas equipment shut off** → **gas supply droop** (Test 5)
3. **How low did it actually go?** 180–300 °F = setback. Stuck at ~410 °F = not setback.
4. **Was the oven idle or actively baking** when it was seen at 410 °F?
5. What are `Sb`, `St`, `id` set to? (Test A)
6. Has this oven **ever** held 475 °F? Sudden onset or gradual decline?
7. Is OPEN vent deliberate for the product being run, or a recipe that was never corrected?
8. Any yellow flame, soot, combustion smell, or CO alarm? Hot water at the drain when idle?
9. Natural gas or propane per the data plate — and which orifices are actually fitted?
10. Is there a **sister LRO** on site to compare against? Is the original **start-up form** on file?

---

## 8. Action list

1. [ ] Ask the operator who saw it: **how long down, what changed when it recovered, how low it went** (§7).
2. [ ] Run Test A — read and record `Sb` / `St` / `id`. Highest value, zero cost, oven stays in service.
3. [ ] Run Test B — audit the vent setting on every recipe in use; correct OPEN → AUTO where it is not
       deliberate for the product.
4. [ ] Run Test C — hold 475 °F unattended past the setback delay and watch whether it walks down.
5. [ ] If it recurs: Test 1 (heat sequence lights) **before** anything else, and note the bottom-out temperature.
6. [ ] Record `T-Offset` and verify the display against an independent thermometer (Test 3).
7. [ ] Schedule the qualified gas tech for Tests 5, 6 and 7 — running supply pressure, manifold pressure,
       orifice size, CO, flame microamps — **if** the setting checks come back clean.
8. [ ] Retrieve the original LBC start-up form for this oven; it holds the commissioned gas pressure,
       rate-of-rise, control parameters and shutter settings. Attach it to the asset record in Aptean EAM.
9. [ ] Log every result with a date in §9 and replace the **VERIFY** markers with findings.
10. [ ] If PM is overdue: LBC recommends authorized preventive maintenance every 6 months (Operators p.21).

---

## 9. Event log

- **2026-09-21** Symptom reported: set point 475 °F, oven plateaus ~410 °F and drops. LRO-2G5 spec sheet
  supplied. Document created from OEM documentation only; no on-machine readings taken.
- **2026-09-21** Johnathan confirmed: control is the **−70 digital**, and the **vent is set to OPEN**.
  Resolved the control-type **VERIFY** in §1. Vent OPEN recorded as a standing finding (§4a).
- **2026-09-21** Johnathan reported the oven **"went back to normal"** with no repair performed. Fault is
  intermittent and self-clearing. Duration of the outage, the bottom-out temperature, and what changed at
  the moment of recovery were **not captured** — these are now the open questions in §7.

---

## 10. Sources

- LBC LRO-2G5 spec sheet (2/19), supplied as `b2600958-LBC_-_LRO-2G.pdf` — also at
  https://www.lbcbakery.com/wp-content/uploads/2017/12/LRO-2G5-Spec-12-17.pdf
- LBC LRO-1G5/2G5/1E5/2E5 **Installation, Service and Parts Manual**, Rev 10-19 (51 pp) —
  https://www.lbcbakery.com/wp-content/uploads/2019/10/LRO-Install-Service-10-19.pdf
  (specs p.7, gas connection p.23, **start-up form p.26–27**, air shutters p.28–29, control parts p.32,
  parts p.40–42, schematics p.45–50)
- LBC LRO **Operators Manual**, Rev 12-2021 —
  https://www.lbcbakery.com/wp-content/uploads/2022/07/LRO-Operators-manual-12-2021.pdf
  (PM interval p.21, control compartment / heat sequence lights p.28, back-up controls p.29,
  blower and vent functions p.32)
- LBC **LMO Max-E / LMO Max-G Operator's Manual**, Rev B 8-16 — same **40102-70** digital control family;
  the only LBC manual found that documents the −70 setback parameters —
  http://www.lbcbakery.com/wp-content/uploads/2016/09/LMO-Max-Rack-Oven-Operator-Manual-RevB-8-16.pdf
  (vent OPEN/AUTO/CLOSED p.16, **Control Setback `SB`/`St`/`Id` and programming procedure p.17**)
- LBC factory schematic set **DWG 61111-174-4** — sheet 2 power connections, sheet 3 control I/O,
  **sheet 4 heat circuit** (in the Install/Service manual above)
- Fenwal Series 35-65 / 35-66 24 VAC HSI control datasheet (DS 35 65 66) —
  https://www.pvi.com/dfsmedia/0533dbba17714b1ab581ab07a4cbb521/60528-source/637395363700000000/fenwal-35-65-and-35-66-24-vac-hsi-control-manual.pdf
  (flame sensitivity p.1, sequence / lockout / LED codes / troubleshooting p.2)
- LBC PDF library — https://www.lbcbakery.com/pdf-library/
- LBC Bakery Equipment, 6026 31st Ave NE, Marysville WA 98271 — 888-722-5686 (888-RACKOVN),
  sales@lbcbakery.com
