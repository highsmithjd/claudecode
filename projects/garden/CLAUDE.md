# Garden Manager - Project Instructions

## Project Overview
A CLI tool to manage two raised garden beds. Track planting, watering, pest/disease
issues, and harvests. The source of truth is `garden.json` — never overwrite it,
only update specific fields or append new records.

## My Garden

### Bed 1 — 2ft wide x 5ft long x 2ft deep
- Full sun most of the day
- Located by the house
- **Planted:** March 15, 2026
- **Contents:** Mix of lettuce, beets, and onions
  - Lettuce (variety TBD — likely one of: Igloo, Giant Caesar, Black Seeded Simpson,
    or Gourmet Blend)
  - Beet — Detroit Dark Red Medium Top
  - Beet — Detroit Supreme
  - Onion — Walla Walla
  - Onion — Bunching Onion Flavor King
- **Status:** Some seedlings ~2 inches tall; some germinated and died

### Bed 2 — 3ft wide x 3ft long x 1ft deep
- Full sun most of the day
- Located by the house
- Has a trellis on one side: ~5ft tall, 8 rungs
- **Planted:** March 15, 2026
- **Contents:** All lettuce
  - Lettuce varieties: Igloo, Giant Caesar, Black Seeded Simpson, Gourmet Blend
- **Status:** Some seedlings ~2 inches tall; some germinated and died

## Summer Crop Plan

### Tomato — Big Red (Ferry Morse Organic)
- **Started indoors:** April 5, 2026
- **Transplant to:** Bed 1 (after May 1)
- **Days to maturity:** 85 days from transplant
- **Notes:** Will need a cage; max 2 plants; takes over Bed 1 after spring harvest

### Cucumber — Straight Eight (Ferry Morse Organic)
- **Started indoors:** April 5, 2026
- **Transplant to:** Bed 2 near trellis (after May 1)
- **Days to maturity:** 60 days from transplant
- **Notes:** Will climb the Bed 2 trellis; primary summer crop for Bed 2

### Peppers (variety TBD)
- **Status:** Still to be seeded
- **Planned location:** Bed 1 (alongside or after tomatoes)

### Squash (variety TBD)
- **Status:** Still to be seeded
- **Planned location:** Container (not a raised bed)

## Bed Transition Plans

### Bed 1
- Harvest spring crops (lettuce, beets, onions) May–June
- Transplant tomatoes (Big Red) into Bed 1 after spring crops are cleared
- Max 2 tomato plants; peppers may share space if room allows

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
  - Beet Detroit Dark Red: ~60 days (ready ~May 14)
  - Beet Detroit Supreme: ~55 days (ready ~May 9)
  - Onion Walla Walla: ~90 days (ready ~June 13)
  - Bunching Onion Flavor King: ~65 days (ready ~May 19)
  - Lettuce Igloo: ~45 days (ready ~April 29)
  - Lettuce Giant Caesar: ~70 days (ready ~May 24)
  - Lettuce Black Seeded Simpson: ~45 days (ready ~April 29)
  - Lettuce Gourmet Blend: ~45 days (ready ~April 29)
  - Tomato Big Red: ~85 days from transplant (if transplanted May 1, ready ~July 25)
  - Cucumber Straight Eight: ~60 days from transplant (if transplanted May 1, ready ~June 30)
- Some seedling loss is noted — Claude should ask before marking any plant as dead
- Days-to-maturity for summer crops are counted from transplant date, not indoor start date
