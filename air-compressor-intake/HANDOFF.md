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
   3 µm. A purpose-built compressor intake element is **99 %+ to 5 µm (polyester)** or **99 %+ to 2 µm (paper)**
   — Solberg published spec. Better than half of the abrasive dust in the damaging size range would pass. The
   particles that score cylinder walls, valve plates and screw rotors are exactly the ones this pad lets through.

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

## 3. First thing to check — is the filter actually missing?

Before buying anything, confirm the machine really shipped without intake filtration. Common cases:

- Intake filter shipped **loose in the crate or in the parts/literature bag**, not installed.
- A **red plastic shipping plug** in the inlet port that is meant to be removed and replaced with the filter.
- On an enclosed rotary screw, the visible opening is the **enclosure louver**; the actual airend intake filter
  lives inside the canopy. What looks like a bare inlet may not be one.

Check the crate, the parts bag, and the parts list in the O&M manual. **VERIFY** — cheapest possible fix.

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

**Preferred: the OEM intake filter.** Look the part number up against the model/serial and order it. Typically
$15–60 and stocked. This is the answer that keeps the warranty clean.

**Acceptable interim: a threaded intake filter-silencer** that screws directly into the inlet port — metal
housing, pleated paper or polyester element, integral silencer. Selection criteria:

| Criterion | Target |
|---|---|
| Connection | Match the measured inlet thread exactly (1/2"–2" NPT are the common sizes) |
| Flow rating | ≥ compressor inlet CFM. **Oversizing is good** — lower ΔP, longer service interval |
| Filtration | 5 µm @ 99 %+ minimum; 2 µm paper preferred. Polyester if the air is humid, oily or greasy (washable) |
| Housing | Metal, not plastic — it sits on a hot machine |
| Silencer | Include it; intake noise is real in a plant space |

Known sources (prices 2026-09-18, re-check before purchase):
- Generic 3/4" NPT metal filter-silencer w/ element — Compressor Source, **$14.95**; replacement element FE-01X.
  Housing 3" tall × 5" wide, element 2.75" dia × 1.625".
- Solberg F / FT series — the industrial standard. FT = compact, exposed element, low restriction; F = fully
  drawn weatherhood. Carbon steel, powder coat. Continuous service −15 °F to 220 °F.
- Also Donaldson, Nugent. Grainger/Zoro stock equivalents.

**Service trigger:** Solberg specifies element change-out at **15–20" H₂O over initial ΔP**. A cheap intake
vacuum gauge or restriction indicator turns the filter PM from a calendar guess into a measurement.

---

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
4. [ ] Order the OEM intake filter against model/serial. If lead time is unacceptable, order a correctly sized
       threaded filter-silencer as the interim — **not** the McMaster pad.
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
- Solberg F/FT Series inlet filters (efficiency, temp range, change-out ΔP) — https://www.solbergmfg.com/collections/f-ft-series
- Solberg polyester element ratings (99 %+ to 5 µm) — https://www.solbergmfg.com/collections/polyester-elements
- Solberg 2-micron paper element — https://www.solbergmfg.com/products/14
- 3/4" NPT intake filter-silencer, $14.95, element FE-01X — https://compressor-source.com/products/3-4-npt-air-compressor-intake-filter-silencer-metal-housing-and-element
- Donaldson, intake filter restriction vs. energy — https://www.donaldson.com/en-us/compressor/technical-articles/filter-ecosystem-energy-consumption/
- ISO 8573-1 for food production — https://www.hengst.com/en/solutions/know-how/iso-8573-1-guide-to-the-quality-of-compressed-air-for-food-production
- Food-safe compressed air standards (Atlas Copco) — https://www.atlascopco.com/en-us/compressors/industry-solutions/pneumatic-conveying-systems/compressed-air-standards-food-industry
- Compressed air rules of thumb (1 psi ΔP ≈ 0.5 % bhp) — https://www.air-compressor-guide.com/knowledge-base/compressed-air-basics/rules-of-thumb
