# New Plant Air Compressor — Intake Filtration: Handoff Notes

Prepared 2026-09-18 for Johnathan (Data Analyst / Maintenance Systems Planner, Buddy's Kitchen, Burnsville MN).
Purpose: project memory for Claude Code. Trigger: a newly purchased plant air compressor was observed with
**no filter at the air inlet**, and a McMaster HVAC filter pad (2173K133) was proposed as an interim fix held on
with magnets. Items marked **VERIFY** are unconfirmed.

---

## 1. Proposed part — McMaster 2173K133

Specs as listed by McMaster (read off the listing 2026-09-18):

| Attribute | Value |
|---|---|
| Form | **Pad** — cut-to-size media, sold individually |
| Trade size / thickness | 12 × 12 in, 1" thick |
| Material / construction | Fiberglass, **unpleated** |
| MERV rating | **6** |
| Efficiency @ 3 µm | **35 %** |
| Removes particle size down to | 3 µm |
| Max temperature | 250 °F |
| Reusable | No |
| Certification | UL Classified |
| Listing description | "Replace dirty HVAC filters with this media to collect large dust and debris. Cut this media to the size you need and attach it to…" |

**This is furnace/air-handler filter media, not a compressor intake filter.** Verdict: do not use it on the
compressor inlet. Reasoning in §2.

---

## 2. Why the pad-and-magnets plan should not be used

1. **Far too coarse.** MERV 6 captures 35–49.9 % of the 3–10 µm fraction (ASHRAE 52.2); McMaster lists 35 % at
   3 µm. A purpose-built compressor intake element is **99 %+ to 2 µm (paper)** or **99 %+ to 5–10 µm
   (polyester)** — Solberg published spec. Better than half of the abrasive dust in the damaging size range
   would pass. The particles that score cylinder walls, valve plates and screw rotors are exactly the ones this pad lets through.

2. **Unsealed media does not filter — it decorates.** Filtration is a sealing problem. A pad held by magnets has
   an open perimeter, and air takes the lowest-resistance path. As the pad loads, bypass around the edge
   *increases*, so effective efficiency trends toward zero. A filter that is not sealed to the inlet bore is not
   in the air path in any controlled sense.

3. **Local face velocity is ~10× what the media is built for, so it will shed fibers.** 1" fiberglass panel media
   is designed for a few hundred FPM across a supported frame. At a compressor inlet the flow converges on a small
   port. Worked example (assumptions stated, real numbers pending §4): 100 ACFM through a 2" inlet bore
   = 0.0218 ft², giving **≈ 4,600 FPM** at the bore and thousands of FPM in the media immediately around it.
   Unpleated fiberglass is adhesive-bonded loose fill; at that velocity, over a pulsating reciprocating suction,
   it will release glass fiber straight into the intake. Glass fiber is abrasive and ends up in the valves and
   the oil.

4. **Detached-part risk, and it is a food plant.** Magnets on a vibrating compressor walk. A dislodged pad in
   front of a live inlet gets ingested — on a rotary screw that is a destroyed airend, not a cleanup.
   Independently of the machine risk, loose fiberglass plus friction-held magnets near production is a foreign-
   material hazard; magnets used as fasteners generally have to be captive and accounted for in the FM/HACCP
   program. **VERIFY** with QA before anything magnetic goes on plant equipment.

5. **Warranty.** The unit is new. Dust-ingestion damage is trivially identified at teardown (scoring), and
   running without correct intake filtration is a clean warranty denial. This is a ~$20 part protecting the
   newest capital asset in the room.

---

## 3. Is the filter actually missing?

**2026-09-18: reported as genuinely absent — no filter came with the machine.** The checks below are a
two-minute confirmation, worth doing once before ordering, but the plan of record is now §5 (buy the correct
threaded filter-silencer). Common cases where one turns up after all:

- Intake filter shipped **loose in the crate or in the parts/literature bag**, not installed.
- A **red plastic shipping plug** in the inlet port that is meant to be removed and replaced with the filter.
- On an enclosed rotary screw, the visible opening is the **enclosure louver**; the actual airend intake filter
  lives inside the canopy. What looks like a bare inlet may not be one.

Check the crate, the parts bag, and the parts list in the O&M manual. If nothing turns up, go to §5 — a
Solberg FS (or equivalent) is the correct permanent answer, not a substitute for one.

---

## 4. Information needed to spec the correct part

Off the nameplate and the machine:

1. Make, model, serial.
2. HP and rated CFM — note **inlet/displacement CFM**, not just delivered FAD; size the filter to the larger.
3. Type: reciprocating vs. rotary screw; oil-lubricated vs. oil-free.
4. Inlet connection: thread size and whether male or female NPT (measure it — do not eyeball).
5. Where the inlet draws from: ambient temperature at that point, and whether the air there is greasy, steamy,
   or dusty.

---

## 5. What to install instead

**Key point: this is not "OEM or improvise."** A threaded inlet filter-silencer is the standard, universal,
off-the-shelf part for this job — it is what most compressors ship with from the factory. Buying one is the
correct permanent fix, not a stopgap. Solberg FS Series is the reference product; Donaldson and Nugent are
equivalents. Cost runs roughly $15–40 for small sizes, more as connection size grows.

### Solberg FS Series — published selection table

Source: Solberg FS Series catalogs US_FS-sm.pdf (1/4"–1") and US_FS-med.pdf (1/2"–6"), Rev US2506C2.
All male NPT unless noted. Stamped carbon steel, drawn weatherhood, tubular silencing.

| Outlet (MNPT) | SCFM rating | Paper element (2 µm) | Polyester element | Series |
|---|---|---|---|---|
| 1/4" | 4 | FS-04-025 | FS-05-025 | small |
| 3/8" | 8 | FS-04-038 / FS-06-038 | FS-05-038 / FS-07-038 | small |
| 1/2" | 8 | FS-04-050 | FS-05-050 | small |
| 1/2" | 12 | FS-06-050 / FS-10-050 | FS-07-050 / FS-11-050 | small |
| 1/2" | 10 | FS-14-050 | FS-15-050 | medium |
| 3/4" | 12 | FS-06-075 | FS-07-075 | small |
| 3/4" | 25 | FS-10-075 / FS-14-075 | FS-11-075 / FS-15-075 | small / medium |
| 1" | 35 | FS-10-100 / FS-14-100 | FS-11-100 / FS-15-100 | small / medium |
| 1" | 55 | FS-18P-100 | FS-19P-100 | medium |
| 1 1/4" | 70 | FS-18P-125 | FS-19P-125 | medium |
| 1 1/2" | 85 | FS-18P-150 | FS-19P-150 | medium |
| 2" | 135 | FS-30P-200 / FS-230P-200 | FS-31P-200 / FS-231P-200 | medium |
| 2 1/2" | 195 | FS-30P-250 / FS-230P-250 | FS-31P-250 / FS-231P-250 | medium |
| 3" | 300 | FS-230P-300 / FS-234P-300 / FS-274P-300 | FS-231P-300 / FS-235P-300 / FS-275P-300 | medium |
| 4" | 520 | FS-234P-400 / FS-274P-400 | FS-235P-400 / FS-275P-400 | medium |
| 5" | 800 | FS-244P-500 / FS-274P-500 | FS-245P-500 / FS-275P-500 | medium |
| 6" | 1100 | FS-274P-600 | FS-275P-600 | medium |

4"–6" are also available flanged (suffix **F**, e.g. FS-234P-400F).

### Media choice — matters here

| | Paper | Polyester |
|---|---|---|
| Efficiency | **99 %+ to 2 µm** | 99 %+ to **5 µm** (medium series) / **10 µm** (small stamped series) |
| Moisture / oil / humidity | Degrades and blinds when damp | Handles it; **washable and reusable** |
| Buddy's Kitchen call | Use if the compressor sits in a dry mechanical room | **Use if the intake sees kitchen humidity, steam or grease** |

Both are enormously better than the MERV 6 pad (35 % @ 3 µm). Note the small stamped FS series polyester is
10 µm, not 5 µm — only the medium series polyester is 5 µm.

### Common specs (both series)
- Continuous temp: −15 °F to 220 °F (−26 °C to 104 °C)
- Filter change-out differential: **15–20" H₂O over initial ΔP**
- Corrosion-resistant powder coat carbon steel; mounts vertically or horizontally
- Stainless construction and a pressure-drop indicator are listed options on the medium series

### Sizing rule
1. **Thread first.** Match the compressor's actual inlet thread. Oversizing the filter and adapting *up* with a
   nipple/bushing is fine and desirable; bushing *down* to a smaller filter is not.
2. **Then CFM.** Filter SCFM rating ≥ compressor inlet/displacement CFM. Round up — a larger filter means lower
   ΔP and a longer service interval.
3. If only HP is known, estimate inlet CFM ≈ **5 × HP** and round up, then confirm against the nameplate.
   Rough guide: 10 HP ≈ 50 CFM (FS-18P-100, 1"); 25 HP ≈ 125 CFM (FS-30P-200, 2"); 50 HP ≈ 250 CFM
   (FS-230P-300, 3"). **VERIFY** against the actual nameplate before ordering.

## 6. Related items worth raising while the machine is new

- **Intake air source drives capacity.** Compressor capacity scales with inlet air density, so warm intake air
  costs output directly: 70 °F → 90 °F is 530/550 °R ≈ **3.6 % less mass flow**, for nothing. Drawing from
  ceiling level, from beside an oven, or from the unit's own cooling-air discharge is a standing penalty. In a
  kitchen, also keep the intake out of grease- and steam-laden air — grease blinds an element fast and loads the
  oil. If the compressor room is hot or greasy, duct the intake to a cool clean source (or outside), with the
  filter at the duct inlet.
- **Intake piping.** If the intake is ducted, the pipe should be at least one size **larger** than the inlet
  port, with smooth wide-radius elbows and no corrugated hose. Rule of thumb: 1 psi of pressure drop ≈ 0.5 % of
  brake horsepower.
- **The intake filter does not make the air food-safe.** It protects the machine. Air that contacts product or
  product-contact surfaces is governed by ISO 8573-1:2010 purity classes [particles : water : oil]. BCAS
  food-and-beverage guidance for direct-contact air is commonly cited as **[2:2:1]**, with point-of-use
  filtration (coalescing + carbon + sterile membrane) at each contact point — compressor-room filtration alone
  does not satisfy it, and SQF expects periodic air-quality testing at contact points. **VERIFY** the exact
  requirement against our own scheme (SQF/BRCGS) with QA. If this compressor feeds any direct-contact air and is
  oil-lubricated, that belongs in the HACCP review now, not after the audit.
- **Heat rejection.** A compressor turns essentially all its input power into room heat: 1 HP ≈ 2,545 BTU/hr, so
  a 25 HP unit dumps ≈ 64,000 BTU/hr. Confirm the room's ventilation actually handles it.
- **Commissioning checklist** on a new unit: rotation direction verified at first start (a screw compressor run
  backwards even briefly can wreck the airend), oil level and correct oil type, safety relief valve, isolation/
  LOTO point identified and documented, vibration isolation/mounting, and condensate handling — oil-water
  separation before drain if it is oil-lubricated. **VERIFY** local discharge requirements.

---

## 7. Action list

1. [ ] Check crate, parts bag and O&M parts list for a shipped-loose intake filter or a shipping plug (§3).
2. [ ] Record nameplate data: make/model/serial, HP, inlet CFM, recip vs. screw, oil vs. oil-free (§4).
3. [ ] Measure the inlet thread size and gender.
4. [ ] Order a Solberg FS (or Donaldson/Nugent equivalent) sized off §5: thread match first, then SCFM ≥ inlet
       CFM, paper element if the room is dry / polyester if it sees humidity or grease. **Not** the McMaster pad.
       Order a spare element at the same time.
5. [ ] Do not run the compressor with an unfiltered inlet in the meantime; if it must run, keep it short and
       document it.
6. [ ] Add intake filter to the PM schedule; fit an intake restriction gauge and set change-out at
       15–20" H₂O over initial.
7. [ ] Confirm where the inlet draws from; evaluate ducting to cooler/cleaner air (§6).
8. [ ] Raise with QA: (a) magnets as fasteners under the FM program, (b) whether this compressor feeds any
       food-contact air and what ISO 8573-1 class applies.
9. [ ] Log the intake filter and element part numbers in Aptean EAM once confirmed.

---

## 8. Sources
- McMaster-Carr 2173K133 product listing (specs transcribed 2026-09-18) — https://www.mcmaster.com/2173K133/
- **Solberg FS Series catalog, 1/4"–1" (sizing table, Rev US2506C2)** — https://www.solbergmfg.com/cdn/shop/files/US_FS-sm.pdf
- **Solberg FS Series catalog, 1/2"–6" (sizing table, Rev US2506C2)** — https://www.solbergmfg.com/cdn/shop/files/US_FS-med.pdf
- Solberg FS/PS Series overview — https://www.solbergmfg.com/collections/fs-ps-series
- Solberg F/FT Series inlet filters (efficiency, temp range, change-out ΔP) — https://www.solbergmfg.com/collections/f-ft-series
- Solberg polyester element ratings (99 %+ to 5 µm) — https://www.solbergmfg.com/collections/polyester-elements
- Solberg 2-micron paper element — https://www.solbergmfg.com/products/14
- 3/4" NPT intake filter-silencer, $14.95, element FE-01X — https://compressor-source.com/products/3-4-npt-air-compressor-intake-filter-silencer-metal-housing-and-element
- Donaldson, intake filter restriction vs. energy — https://www.donaldson.com/en-us/compressor/technical-articles/filter-ecosystem-energy-consumption/
- ISO 8573-1 for food production — https://www.hengst.com/en/solutions/know-how/iso-8573-1-guide-to-the-quality-of-compressed-air-for-food-production
- Food-safe compressed air standards (Atlas Copco) — https://www.atlascopco.com/en-us/compressors/industry-solutions/pneumatic-conveying-systems/compressed-air-standards-food-industry
- Compressed air rules of thumb (1 psi ΔP ≈ 0.5 % bhp) — https://www.air-compressor-guide.com/knowledge-base/compressed-air-basics/rules-of-thumb
