# Garden Manager - Project Instructions

## Project Overview
A CLI tool to manage two raised garden beds. Track planting, watering, pest/disease
issues, and harvests. The source of truth is `garden.json` — never overwrite it,
only update specific fields or append new records.

## My Garden

### Bed 1 — 2ft wide x 5ft long x 2ft deep
- Full sun most of the day
- Located by the house
- **Contents (as of May 8, 2026):**
  - Lettuce (variety TBD — spring planting Mar 15)
  - Beet — Detroit Dark Red Medium Top (Mar 15)
  - Beet — Detroit Supreme (Mar 15; first beet harvested May 2026, remaining plants in bed)
  - Onion — Walla Walla (Mar 15)
  - Onion — Bunching Onion Flavor King (Mar 15)
  - Kale — Dwarf Blue Curled (seeded Apr 5)
  - Tomato — Big Red, 3 plants (transplanted Apr 18)
  - Broccoli starts — 3 plants (transplanted early May)
  - Cauliflower starts — some plants (transplanted early May)
  - Green Bean — Bush Blue Lake 274 / Provider Bush / Contender Organic (direct sown May 8)

### Bed 2 — 3ft wide x 3ft long x 1ft deep
- Full sun most of the day
- Located by the house
- Has a trellis on one side: ~5ft tall, 8 rungs
- **Contents (as of May 8, 2026):**
  - Lettuce — Igloo, Giant Caesar, Gourmet Blend (spring planting Mar 15; still growing)
  - Lettuce — Black Seeded Simpson (Mar 15; **harvested May 2026**)
  - Kale — Dwarf Blue Curled (seeded Apr 5)
  - Cucumber — Straight Eight, 1 plant (transplanted Apr 18; now climbing trellis)
  - Broccoli — 1 start (transplanted early May)

### Containers
- **Blue container:** 1 broccoli start (planted early May)
- **Galvanized containers (2):** 2 pepper plants (planted early May); some cauliflower starts

## Summer Crop Plan

### Tomato — Big Red (Ferry Morse Organic)
- **Started indoors:** April 5, 2026
- **Transplanted:** April 18, 2026 to Bed 1 (3 plants)
- **Days to maturity:** 85 days from transplant (~July 12 from Apr 18)
- **Status:** Growing in Bed 1
- **Notes:** Will need cages; original plan was max 2 plants — 3 were transplanted, monitor spacing

### Cucumber — Straight Eight (Ferry Morse Organic)
- **Started indoors:** April 5, 2026
- **Transplanted:** April 18, 2026 to Bed 2 near trellis (1 plant)
- **Days to maturity:** 60 days from transplant (~June 17 from Apr 18)
- **Status:** Growing in Bed 2, climbing trellis

### Green Beans (new — direct sown May 8, 2026)
- **Bush Blue Lake 274 (Burpee):** ~52 days → ready ~June 29
- **Provider Bush (Ferry Morse):** 50 days → ready ~June 27
- **Contender Organic (Ferry Morse):** 55 days → ready ~July 2
- **Location:** Direct sown in empty Bed 1 squares May 8

### Squash (variety TBD)
- **Status:** Still to be seeded
- **Planned location:** Container (not a raised bed)

## Bed Transition Plans

### Bed 1
- Harvest spring crops (lettuce, beets, onions) May–June
- Transplant tomatoes (Big Red) into Bed 1 after spring crops are cleared
- Max 2 tomato plants

### Bed 2
- Cucumbers on trellis all summer
- Spring lettuce harvested as cucumbers fill in

## Location & Climate
- Orlinda, Tennessee (Zone 6b)
- Spring planting season — cool weather crops appropriate for current timing

## CLI Commands (build toward these)
- `status` — overview of all beds, current plant health, days since watering
- `water-check` — should I water today? (use Open-Meteo API, no key required)
- `log harvest` — record what was picked, from which bed, date, quantity
- `add-pest` — log a pest or disease observation with bed, description, date
- `schedule` — show upcoming tasks based on planting dates and crop timelines

## Data File — garden.json
- Single source of truth for all beds, plants, logs
- Never overwrite the whole file — always read first, update specific fields, write back
- Schema should include:
  - beds (static info: dimensions, location, trellis)
  - plants (per bed: variety, date planted, status, notes)
  - watering_log (date, bed, method, notes)
  - harvest_log (date, bed, plant, quantity, notes)
  - pest_log (date, bed, description, action_taken)

## Build Order
1. `garden.json` schema + seed with current bed/plant data
2. `status` command
3. `log harvest` and `add-pest` commands
4. `schedule` command based on days-to-maturity for each variety
5. `water-check` using Open-Meteo weather API

## Notes
- Prefer simple, readable Python
- Days-to-maturity reference:
  - Beet Detroit Dark Red: ~60 days from Mar 15 (ready ~May 14)
  - Beet Detroit Supreme: ~55 days from Mar 15 (ready ~May 9; first harvested May 2026)
  - Onion Walla Walla: ~90 days from Mar 15 (ready ~June 13)
  - Bunching Onion Flavor King: ~65 days from Mar 15 (ready ~May 19)
  - Lettuce Igloo: ~45 days from Mar 15 (ready ~April 29)
  - Lettuce Giant Caesar: ~70 days from Mar 15 (ready ~May 24)
  - Lettuce Black Seeded Simpson: ~45 days from Mar 15 (harvested May 2026)
  - Lettuce Gourmet Blend: ~45 days from Mar 15 (ready ~April 29)
  - Kale Dwarf Blue Curled: ~55 days from Apr 5 (ready ~June 3)
  - Tomato Big Red: ~85 days from Apr 18 transplant (ready ~July 12)
  - Cucumber Straight Eight: ~60 days from Apr 18 transplant (ready ~June 17)
  - Broccoli (starts): ~60 days from ~May 1 transplant (ready ~June 30; variety unknown)
  - Cauliflower (starts): ~65 days from ~May 1 transplant (ready ~July 5; variety unknown)
  - Pepper: ~75 days from ~May 1 transplant (ready ~July 15; variety unknown)
  - Green Bean Bush Blue Lake 274: ~52 days from May 8 (ready ~June 29)
  - Green Bean Provider Bush: ~50 days from May 8 (ready ~June 27)
  - Green Bean Contender Organic: ~55 days from May 8 (ready ~July 2)
- Some seedling loss is noted — Claude should ask before marking any plant as dead
- Days-to-maturity for summer crops are counted from transplant date, not indoor start date
