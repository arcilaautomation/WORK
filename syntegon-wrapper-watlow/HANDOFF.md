# Syntegon Wrapper — Watlow EZ-ZONE RM Temperature Control: Handoff Notes

Prepared 2026-09-07 for Johnathan (Data Analyst / Maintenance Systems Planner, Buddy's Kitchen, Burnsville MN).
Purpose: project memory for Claude Code. Everything below came from OEM manuals (Watlow, Mettler-Toledo Safeline),
authorized-distributor listings, and the events of Sep 4–7, 2026. Items marked **VERIFY** are unconfirmed.

---

## 1. Hardware in the panel (as photographed)

| Panel tag | Module | Part number | Zone addr | Role |
|---|---|---|---|---|
| COM20801 | Ethernet switch | — | — | Machine network switch |
| TC51030 "RMA GATEWAY MOD" | Watlow EZ-ZONE **RMA** (Access) | **RMAA-A3AA-AAAA** | **J (=17, factory default)** | Comm gateway + config backup. No control loops. |
| TC18001 "RMA 4 LOOP TEMP CNTRL" (mislabeled; it is an RMC) | Watlow EZ-ZONE **RMC** (Controller) | **RMC1U1U1U1UAAAA** | **1** | 4-loop PID controller; thermocouples land here |

### RMA (RMAA-A3AA-AAAA) decode
- Digit 6 = **3** → EtherNet/IP + Modbus TCP (10/100) on slot E screw terminals: **E1 = TX+ (white/orange), E2 = TX− (orange), E3 = RX+ (white/green), E6 = RX− (green)**. Cat5 to COM20801.
- Digit 8 = **A** → limited backup: backs up ≤4 RM modules to RMA on-board memory ("Auto-Clone").
- Mini-USB port = SD-card mass storage only. **Not** a configuration port.
- Both Modbus TCP and EtherNet/IP enabled by default; PLC almost certainly uses EtherNet/IP.

### RMC (RMC1U1U1U1UAAAA) decode
- Positions 4/6/8/10 = **1** → four universal inputs (control loops).
- Positions 5/7/9/11 = **U** → output 1/3/5/7 = switched DC / open collector (22–32 VDC, 30 mA) on X/W/Y; output 2/4/6/8 = none (blank terminal positions).
- Position 12 = A (right-angle screw connector); 13 = A (Standard Bus only — no fieldbus on the RMC itself; PLC talks through the RMA); 14–15 = AA (no options).
- Ships from factory at address 1 with default config. Change address: hold orange button ~2 s, then press to step.

### Slot → loop → terminal map (RMC)
| Physical position | Slot | Input / loop | TC terminals | Heat output terminals |
|---|---|---|---|---|
| bottom-left | A | Input 1 | T1 S1 R1 | X1 W1 Y1 (output 1) |
| bottom-right | B | Input 2 | T2 S2 R2 | X3 W3 Y3 (output 3) |
| top-left | D | Input 3 | T3 S3 R3 | X5 W5 Y5 (output 5) |
| top-right | E | Input 4 | T4 S4 R4 | X7 W7 Y7 (output 7) |

**Thermocouple wiring: TC+ → R, TC− (red lead) → S. T unused for a TC.** Input spec: >20 MΩ, 3 µA open-sensor detection.
Which loop = "upper cutting head": **VERIFY** on the Syntegon drawing (photo hint suggested loop 1 / slot A).

### Bottom connector (slot C, every module)
Positions: 98, 99 (24 V power — do not touch), **CF (Standard Bus common), CD (T−/R−, "A"), CE (T+/R+, "B")**, CZ/CX/CY (inter-module backplane — do not use).

---

## 2. Event log

- **2026-09-04** Upper cutting head reading **1700**. Diagnosis: not a real temperature; open/high-resistance TC circuit *or* controller input fault. (EZ-ZONE pulls an open lead to sensor over-range; ~15 kΩ series resistance on a type J adds ~+1400°F without an "open" flag.)
- Johnathan swapped in the RMC from the other Syntegon wrapper → reading normal. **Root cause = failed RMC input (slot A card), not the thermocouple.**
- **2026-09-07** Radwell RMC1U1U1U1UAAAA installed in place of the borrowed module. Machine runs and reads correctly with no manual configuration. Syntegon claims their units are "programmed"; the field system evidently loaded/accepted the config on its own. Mechanism **unknown** — see §4.
- Metal detectors (3× Mettler-Toledo Safeline) were unplugged over the weekend of Sep 5–6; verdict: harmless one-off; leave powered 24/7 going forward (§7).

---

## 3. Spares compatibility (drop-in rules)

- **RMC1U1U1U1UAAAA** — exact match. Radwell (values 8/27/2026): New $1,295; Never Used Orig Pkg $985; Never Used Radwell Pkg $855; **Refurbished $623.69 (5 in stock)**; 2-yr Radwell warranty; Radwell is not an authorized Watlow distributor. Instrumart (authorized) configured price **$1,061**, call for availability; Thermal Devices and Valin also authorized.
- **RMC1E1E1E1EAAAA** (on hand) — drop-in superset. E = output 1 switched DC/OC **plus** output 2 switched DC (adds W2/Y2, W4/Y4, W6/Y6, W8/Y8 in the positions blank on the U). Leave extras unwired; they default Off. Same inputs, same X/W/Y outputs, same connector, same comm.
- General rule: any RMC with **1** in positions 4/6/8/10 and **U, D, E, F, or G** in 5/7/9/11 and **A** in position 13 works electrically. D/F/G put relay contacts on the spare terminals (fine if unwired). **5** (limit) or **7** (CT) in an input position, or **1** in position 13 (Modbus RTU), is not a match.
- Firmware: RM modules need **≥ 9.0** for Composer. Configurator works with older. Check "Software Release Version" (Factory › Diagnostics) on any spare.
- RMA auto-clone/restore requires **identical part number** at the same zone address. A different-part-number spare (e.g., the E) must be configured via Configurator/Composer or by hand.

---

## 4. Open question: how did the blank Radwell module get its config?

Three candidates, most likely first:
1. **RMA Auto-Clone** — RMA Restore set to "Change"; RMA saw new serial number, same part number, zone 1, and restored its stored image (15–45 min per module).
2. **PLC writes parameters** over EtherNet/IP at power-up / recipe load.
3. **Watlow defaults happen to run** (type J TC, loop1→input1, heat on output 1) — works but untuned, default limits, no alarms.

### Test A — read the RMA's backup registers (Modbus TCP, relative addresses)
| Register | Parameter | Values |
|---|---|---|
| 1270 | Setup › Backup › **Save** | 62 Off, 1646 Now (write 1646 to start a backup) |
| 1272 | Setup › Backup › **Restore** | 62 Off, 1646 Now, **1647 Change** (= auto-clone armed) |
| 1274 | Operations › **Backup Status** | 62 Off, 1644 Save, 1645 Restore, **1187 Monitor**, 18 Complete, 28 Error |
| 1276 | Operations › **Backup Zone** | 1–16 (zone last saved/restored) |
| 1280 (+6 per zone) | Operations › **Zone n backup status** | 61 None, **1644 OK**, 1637 No Memory, 1664 No Module, **1665 No Image**, 28 Error |

Interpretation: Restore = 1647 **and** zone-1 status = 1644 → the RMA cloned it. Restore = 62 or zone 1 = 1665 → config came from the PLC or it's on defaults.
If Restore is Off: set it to Change (write 1647 to 1272) and run a Save (write 1646 to 1270) while a good module is installed.

```python
# pip install pymodbus   (Modbus TCP to the RMA's IP; laptop on same subnet via COM20801)
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient("RMA_IP"); c.connect()
print(c.read_holding_registers(1272, 5).registers)   # [restore, -, status, -, zone]
print(c.read_holding_registers(1280, 1).registers)   # zone 1 image status
```
Address note: Watlow "relative" = zero-based protocol address; tools using 4xxxx style need +40001 (1272 → 41273).

### Test B — compare loop settings to the other wrapper
Read loop 1–4: proportional band / integral / derivative, set point high/low limits, alarm set points, sensor type.
Watlow defaults (**VERIFY** against RMC manual) ≈ Pb 25°F / Ti 180 s / Td 0 s, SP high limit 300°F. Defaults present → case 3 → load the config.

---

## 5. Tools to read/write configuration

### Path 1 — Modbus TCP over the machine network (nothing to buy)
Laptop into a free port on COM20801, same subnet as the RMA (get IP from PLC Ethernet/IP config or RMA Factory › Diagnostics iP.A1–4). Any Modbus client (QModMaster, Modbus Poll, pymodbus). Reads are harmless.

### Path 2 — RS-485 + Watlow free software (ordered/ordering)
- Converter: **Advantech BB-485USBTB-2W-A** (ex-B&B; Watlow part 0847-0326-0000). ~$99–108 (DigiKey, RS, CompSource, Radwell). Includes 3 ft USB A-to-B cable. Port-powered; FTDI VCP driver auto-installs.
- Wire (3 ft of Cat5 scrap): **CE → converter B(+)**, **CD → converter A(−)**, **CF → converter GND**. Any module's slot C; bus is shared on the backplane. Keep converter plugged into the PC while wired in.
- Software (Windows, free):
  - EZ-ZONE Configurator v6.1 — https://www.watlow.com/en/products/controllers/software/ez-zone-configurator-software (any firmware)
  - COMPOSER v3.22.44 — https://www.watlow.com/products/controllers/Software/COMPOSER-Software (firmware ≥ 9.0; system image = whole rail in one file; warns but allows import into a different part number at the same zone)
- Scan runs at 38,400 baud, lists zone J (RMA) and zone 1 (RMC). Save the RMC config file → attach to the wrapper's asset record in Aptean EAM.

### Hand-entry fallback (if no image loads)
Per loop (×4): sensor type, units, set point low/high limits, PID (Pb/Ti/Td), output function + instance (heat power → loop n), alarm type/set points, input error failure mode. ~15 parameters × 4 loops, under an hour side-by-side with the good module.

### Useful RMC Modbus registers (Map 1, per input; +90 per instance)
- 360 Analog Input Value (float; returns last known value if an error exists)
- 362 Input Error: 61 None, 65 Open, 127 Shorted, 140 Measurement Error, 139 Bad Cal, 9 Ambient, 141 RTD, 32 Fail

---

## 6. Action list

1. [ ] Run Test A (registers) and Test B (PID compare) on the Radwell module.
2. [ ] If Restore ≠ Change or no image: set Restore = Change, Save backup with the good module installed.
3. [ ] Return the borrowed RMC to the other wrapper; verify that wrapper.
4. [ ] Buy converter (BB-485USBTB-2W-A); save a Configurator/Composer image for **each** wrapper → EAM.
5. [ ] Buy one more spare RMC1U1U1U1UAAAA (Radwell refurb $623.69 or Instrumart new $1,061). Keep the RMC1E1E1E1EAAAA as backup-backup.
6. [ ] Write the swap SOP: same part number → zone 1 → auto-restore 15–45 min → verify PID/limits → PVR/seal check.
7. [ ] Bench-check the failed RMC (slot A input) — Radwell repair estimate ~$580; probably not worth it vs. refurb.

---

## 7. Metal detectors (Mettler-Toledo Safeline) — side notes

- "V3 / V4" = electronics platform generation (round buttons = V3, upgradable to V4 Touch LS; square buttons = V1/V2), not coil generations.
- Coils are a low-power, high-frequency copper coil system (10 kHz–1 MHz, whole detector ≈100 VA). Continuous power does **not** wear them. Hour-driven parts: display backlight (~50,000 h) and PSU electrolytics (decades at 45°C). Cycling (inrush, thermal cycle, relays normally energized, condensation) does more harm than 24/7 running.
- Verdict: leave powered 24/7; isolate only for LOTO. Keep electronics enclosure cool/dry; head cable gland 5 Nm; dedicated low-power feed, not shared with VFDs.
- After a power-off: warm 30 min in a cold room, check date/time, Condition Monitoring green (EW-01 Power Drive, EW-02 Balance, EW-03/04 self-check), full Fe/NFe/SS test before product. Internal battery 10 yr typical — photograph settings on old units before powering off.

---

## 8. Sources
- Watlow EZ-ZONE RMC User's Guide 0600-0070-0000 — https://www.watlow.com/-/media/documents/user-manuals/rmc-rev-e.ashx
- Watlow EZ-ZONE RMA User's Guide 0600-0072-0000 Rev B — https://www.watlow.com/-/media/documents/user-manuals/rma-rev-b.ashx
- Radwell RMC1U1U1U1UAAAA — https://www.radwell.com/Buy/WATLOW/WATLOW/RMC1U1U1U1UAAAA
- Instrumart RMC configurator (authorized) — https://www.instrumart.com/products/35845/watlow-ez-zone-rm-control-module-rmc-multi-function-controller
- Watlow Composer FAQ / spec — https://www.watlow.com/-/media/documents/specification-sheets/rma-plus-faq.ashx
- Mettler-Toledo Safeline Profile manual (2009) — https://ppnfiles.s3-ap-southeast-2.amazonaws.com/22125-0070-1648595663710.pdf
- Mettler-Toledo upgrade page (V1–V4) — https://www.mt.com/us/en/home/products/Product-Inspection_1/service/performance/upgrade-and-refurbishment/Performance-and-Compliance.html
- Watlow tech support: +1 (507) 494-5656, wintechsupport@watlow.com (Winona, MN)
