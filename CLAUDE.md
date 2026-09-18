# WORK — project memory

Maintenance / controls notes for Buddy's Kitchen (Burnsville, MN). Each project gets a
directory with a `HANDOFF.md` as its living record.

## Projects

| Directory | Subject | Status |
|---|---|---|
| `syntegon-wrapper-watlow/` | Syntegon wrapper, Watlow EZ-ZONE RM temperature control | Open — see the action list in its `HANDOFF.md` §6 |
| `air-compressor-intake/` | New plant air compressor — missing intake filter, spec + food-air review | Open — see the action list in its `HANDOFF.md` §7 |

## Conventions

- **`HANDOFF.md` is the source of truth** for a project. Read it before acting; update it
  when facts change. It carries hardware inventory, an event log, open questions, and an
  action list.
- **`**VERIFY**` marks a claim that is not confirmed.** Treat it as a hypothesis, not a
  fact. When one is confirmed or disproved, replace the marker with the finding and cite
  where it came from (manual + page, drawing number, or a reading taken off the machine).
- **Cite sources.** Part numbers, register addresses, and prices come from OEM manuals or
  distributor listings — keep the link in §8 so the next person can re-check it.
- **Date the event log.** Anything done to a machine goes in the project's event log with
  the date and the observed result, not just the intent.
- Prices and stock levels go stale; re-check before purchasing.

## Safety

These notes describe live 24 VDC control panels and food-production equipment. Nothing
here authorizes work on a running machine — follow site LOTO and PVR/seal-check
procedures. Configuration reads (Modbus, Configurator scans) are harmless; writes change
machine behavior and belong to a planned window.
