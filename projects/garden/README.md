# Garden Manager

A simple CLI tool to manage two raised garden beds in Orlinda, Tennessee. Track plant health, watering, harvests, and pest observations — all stored in a local `garden.json` file.

## My Beds

| Bed | Size | Contents |
|-----|------|----------|
| Bed 1 | 2ft × 5ft × 2ft deep | Lettuce, Beets (Detroit Dark Red, Detroit Supreme), Onions (Walla Walla, Bunching Flavor King) |
| Bed 2 | 3ft × 3ft × 1ft deep | Lettuce (Igloo, Giant Caesar, Black Seeded Simpson, Gourmet Blend) — has a 5ft trellis |

Both beds are full sun, located by the house. Planted March 15, 2026.

## Requirements

- Python 3.8+
- No external dependencies — uses only the standard library
- Internet connection required for `water-check`

## Usage

```
python garden.py <command>
```

### `status`
Overview of all beds: plant varieties, current status, days since planting, and days until each crop is ready to harvest. Also shows the last recorded watering date and any recent pest activity.

```
python garden.py status
```

### `water-check`
Fetches real weather data from [Open-Meteo](https://open-meteo.com/) (free, no API key required) for Orlinda, TN. Shows precipitation over the past 3 days and the next 2 days, then gives a recommendation: water today, skip, or check soil first.

```
python garden.py water-check
```

### `log water`
Record that you watered one or both beds. Prompts for date, which bed(s), watering method, and optional notes. Updates the `Last watered` display in `status`.

```
python garden.py log water
```

### `log harvest`
Record a harvest. Prompts you to select the bed and plant, then enter quantity and notes. All entries are appended to the harvest log in `garden.json`.

```
python garden.py log harvest
```

### `add-pest`
Log a pest or disease observation. Prompts for bed, a description of what you saw, what action you took, and any additional notes. Recent entries show up in `status`.

```
python garden.py add-pest
```

### `schedule`
Shows all plants sorted by estimated harvest date, grouped into: Ready Now, This Week, Next 2 Weeks, This Month, and Later. Also shows watering status with a warning if no watering has been logged.

```
python garden.py schedule
```

## Data File

All data lives in `garden.json`. It is never overwritten — all log commands read the file first and append new entries. The schema includes:

- `beds` — static bed info (dimensions, location, trellis)
- `plants` — each variety with planting date, days-to-maturity, status, and notes
- `watering_log` — date, bed, method, notes
- `harvest_log` — date, bed, plant, quantity, notes
- `pest_log` — date, bed, description, action taken, notes

## Days-to-Maturity Reference

| Variety | Days | Est. Ready |
|---------|------|------------|
| Lettuce Igloo | 45 | Apr 29 |
| Lettuce Black Seeded Simpson | 45 | Apr 29 |
| Lettuce Gourmet Blend | 45 | Apr 29 |
| Beet Detroit Supreme | 55 | May 9 |
| Beet Detroit Dark Red | 60 | May 14 |
| Bunching Onion Flavor King | 65 | May 19 |
| Lettuce Giant Caesar | 70 | May 24 |
| Onion Walla Walla | 90 | Jun 13 |
