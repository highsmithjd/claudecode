#!/usr/bin/env python3
"""Garden Manager CLI — track beds, plants, watering, harvests, and pests."""

import json
import sys
import urllib.request
import urllib.error
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).parent / "garden.json"

# Orlinda, TN coordinates
LATITUDE = 36.638
LONGITUDE = -86.710
TIMEZONE = "America/Chicago"


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved to {DATA_FILE.name}")


def days_since(date_str):
    """Return days elapsed since a date string (YYYY-MM-DD)."""
    if not date_str:
        return None
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (date.today() - d).days


def days_until_maturity(date_planted_str, days_to_maturity):
    """Return days remaining until maturity (negative = already past)."""
    planted = datetime.strptime(date_planted_str, "%Y-%m-%d").date()
    ready = planted + timedelta(days=days_to_maturity)
    return (ready - date.today()).days


def maturity_date(date_planted_str, days_to_maturity):
    planted = datetime.strptime(date_planted_str, "%Y-%m-%d").date()
    return planted + timedelta(days=days_to_maturity)


def ask(prompt, default=None):
    """Prompt user for input, with optional default."""
    if default:
        val = input(f"  {prompt} [{default}]: ").strip()
        return val if val else default
    val = input(f"  {prompt}: ").strip()
    return val


def choose_bed(data):
    """Prompt user to select a bed by number."""
    beds = data["beds"]
    for i, b in enumerate(beds, 1):
        print(f"  {i}. {b['name']} ({b['id']})")
    while True:
        choice = input("  Choose bed (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(beds):
            return beds[int(choice) - 1]["id"]
        print("  Invalid choice, try again.")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def cmd_status():
    data = load_data()

    plants_by_bed = {}
    for plant in data["plants"]:
        plants_by_bed.setdefault(plant["bed_id"], []).append(plant)

    last_watered = {}
    for entry in data["watering_log"]:
        bid = entry["bed"]
        existing = last_watered.get(bid)
        if existing is None or entry["date"] > existing:
            last_watered[bid] = entry["date"]

    print(f"\n{'='*52}")
    print(f"  GARDEN STATUS  —  {date.today().strftime('%B %d, %Y')}")
    print(f"{'='*52}")

    for bed in data["beds"]:
        bid = bed["id"]
        dims = bed.get("dimensions")
        trellis = " [trellis]" if bed.get("trellis") else ""
        if dims:
            size_str = f"{dims['width_ft']}x{dims['length_ft']}x{dims['depth_ft']} ft"
        else:
            size_str = bed.get("type", "container")
        print(f"\n{bed['name']}  ({size_str}){trellis}")
        print(f"  {bed['sun']} — {bed['location']}")

        lw = last_watered.get(bid)
        if lw:
            ds = days_since(lw)
            print(f"  Last watered: {lw}  ({ds} day{'s' if ds != 1 else ''} ago)")
        else:
            print(f"  Last watered: not recorded")

        plants = plants_by_bed.get(bid, [])
        if not plants:
            print("  No plants recorded.")
            continue

        print(f"  {'Variety':<35} {'Status':<12} {'Days In':<9} {'Ready In'}")
        print(f"  {'-'*35} {'-'*12} {'-'*9} {'-'*10}")
        for p in plants:
            days_in = days_since(p["date_planted"])
            dtm = p.get("days_to_maturity")
            if dtm is not None:
                remaining = days_until_maturity(p["date_planted"], dtm)
                ready_str = f"{remaining}d" if remaining > 0 else f"READY ({abs(remaining)}d ago)"
            else:
                ready_str = "unknown"
            status = p["status"]
            variety = p["variety"]
            if len(variety) > 34:
                variety = variety[:31] + "..."
            print(f"  {variety:<35} {status:<12} {days_in:<9} {ready_str}")
            if p.get("notes"):
                print(f"    ^ {p['notes']}")

    if data["pest_log"]:
        recent_pests = sorted(data["pest_log"], key=lambda x: x["date"], reverse=True)[:3]
        print(f"\n  Recent pest/disease notes:")
        for entry in recent_pests:
            print(f"    [{entry['date']}] {entry['bed']}: {entry['description']}")

    print()


# ---------------------------------------------------------------------------
# water-check
# ---------------------------------------------------------------------------

def cmd_water_check():
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=precipitation_sum,precipitation_probability_max,temperature_2m_max"
        f"&past_days=3&forecast_days=2"
        f"&timezone={TIMEZONE}"
    )

    print(f"\n  Fetching weather for Orlinda, TN...")
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            weather = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"  Error fetching weather: {e}")
        sys.exit(1)

    daily = weather["daily"]
    dates = daily["time"]
    precip = daily["precipitation_sum"]
    rain_prob = daily["precipitation_probability_max"]
    temp_max = daily["temperature_2m_max"]

    today_str = date.today().isoformat()
    tomorrow_str = (date.today() + timedelta(days=1)).isoformat()

    print(f"\n  {'Date':<12} {'Rain (mm)':<12} {'Rain Prob%':<12} {'High (°F)'}")
    print(f"  {'-'*11} {'-'*11} {'-'*11} {'-'*10}")
    for i, d in enumerate(dates):
        label = ""
        if d == today_str:
            label = " ← today"
        elif d == tomorrow_str:
            label = " ← tomorrow"
        temp_f = round(temp_max[i] * 9 / 5 + 32, 1) if temp_max[i] is not None else "N/A"
        p = precip[i] if precip[i] is not None else 0
        rp = rain_prob[i] if rain_prob[i] is not None else 0
        print(f"  {d:<12} {p:<12.1f} {rp:<12} {temp_f}{label}")

    # Decision logic
    # Past 3 days precipitation
    past_rain = sum(
        (precip[i] or 0)
        for i, d in enumerate(dates)
        if d < today_str
    )
    today_idx = dates.index(today_str) if today_str in dates else None
    today_rain = precip[today_idx] or 0 if today_idx is not None else 0
    today_prob = rain_prob[today_idx] or 0 if today_idx is not None else 0

    print()
    if past_rain >= 10:
        print(f"  SKIP WATERING — {past_rain:.1f}mm rain in the last 3 days. Soil should be moist.")
    elif today_prob >= 60:
        print(f"  SKIP WATERING — {today_prob}% chance of rain today ({today_rain:.1f}mm forecast). Wait and see.")
    elif past_rain >= 5:
        print(f"  MAYBE WATER — Only {past_rain:.1f}mm in the last 3 days. Check soil moisture first.")
    else:
        print(f"  WATER TODAY — Only {past_rain:.1f}mm in the last 3 days. Seedlings need consistent moisture.")

    print()


# ---------------------------------------------------------------------------
# log water
# ---------------------------------------------------------------------------

def cmd_log_water():
    data = load_data()

    print(f"\n  Log Watering")
    print(f"  {'-'*30}")

    today_str = date.today().isoformat()
    water_date = ask("Date", today_str)

    print("  Which bed(s) did you water?")
    print("  1. Bed 1")
    print("  2. Bed 2")
    print("  3. Both beds")
    choice = input("  Choice: ").strip()

    if choice == "3":
        bed_ids = ["bed1", "bed2"]
    elif choice == "1":
        bed_ids = ["bed1"]
    elif choice == "2":
        bed_ids = ["bed2"]
    else:
        print("  Invalid choice.")
        sys.exit(1)

    method = ask("Method (e.g. hand watered, drip, rain)", "hand watered")
    notes = ask("Notes (optional)", "")

    for bid in bed_ids:
        entry = {
            "date": water_date,
            "bed": bid,
            "method": method,
            "notes": notes,
        }
        data["watering_log"].append(entry)
        print(f"  + Logged watering for {bid}")

    save_data(data)
    print()


# ---------------------------------------------------------------------------
# log harvest
# ---------------------------------------------------------------------------

def cmd_log_harvest():
    data = load_data()

    print(f"\n  Log Harvest")
    print(f"  {'-'*30}")

    today_str = date.today().isoformat()
    harvest_date = ask("Date", today_str)

    print("  Which bed?")
    bed_id = choose_bed(data)

    bed_plants = [p for p in data["plants"] if p["bed_id"] == bed_id]
    if not bed_plants:
        print("  No plants in that bed.")
        sys.exit(1)

    print("  Which plant?")
    for i, p in enumerate(bed_plants, 1):
        print(f"  {i}. {p['variety']} ({p['type']})")
    while True:
        choice = input("  Choice (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(bed_plants):
            plant = bed_plants[int(choice) - 1]
            break
        print("  Invalid choice, try again.")

    quantity = ask("Quantity (e.g. '3 heads', '200g', '2 beets')")
    notes = ask("Notes (optional)", "")

    entry = {
        "date": harvest_date,
        "bed": bed_id,
        "plant": plant["id"],
        "variety": plant["variety"],
        "quantity": quantity,
        "notes": notes,
    }
    data["harvest_log"].append(entry)
    print(f"  + Logged harvest: {quantity} of {plant['variety']} from {bed_id}")

    save_data(data)
    print()


# ---------------------------------------------------------------------------
# add-pest
# ---------------------------------------------------------------------------

def cmd_add_pest():
    data = load_data()

    print(f"\n  Log Pest / Disease Observation")
    print(f"  {'-'*30}")

    today_str = date.today().isoformat()
    obs_date = ask("Date", today_str)

    print("  Which bed?")
    bed_id = choose_bed(data)

    description = ask("Describe what you observed (pest, disease, damage)")
    action = ask("Action taken (or 'none')", "none")
    notes = ask("Additional notes (optional)", "")

    entry = {
        "date": obs_date,
        "bed": bed_id,
        "description": description,
        "action_taken": action,
        "notes": notes,
    }
    data["pest_log"].append(entry)
    print(f"  + Logged observation for {bed_id}: {description}")

    save_data(data)
    print()


# ---------------------------------------------------------------------------
# schedule
# ---------------------------------------------------------------------------

def cmd_schedule():
    data = load_data()
    today = date.today()

    print(f"\n{'='*52}")
    print(f"  HARVEST SCHEDULE  —  {today.strftime('%B %d, %Y')}")
    print(f"{'='*52}")

    # Build sorted list of (ready_date, plant, bed_name)
    beds_by_id = {b["id"]: b["name"] for b in data["beds"]}
    items = []
    for p in data["plants"]:
        if p["status"] in ("harvested", "removed"):
            continue
        ready = maturity_date(p["date_planted"], p["days_to_maturity"])
        items.append((ready, p, beds_by_id.get(p["bed_id"], p["bed_id"])))
    items.sort(key=lambda x: x[0])

    def section(label, entries):
        if not entries:
            return
        print(f"\n  {label}")
        print(f"  {'-'*48}")
        for ready, p, bed_name in entries:
            days_left = (ready - today).days
            if days_left <= 0:
                timing = f"READY ({abs(days_left)}d ago)"
            elif days_left == 1:
                timing = "TOMORROW"
            else:
                timing = f"in {days_left} days  ({ready.strftime('%b %d')})"
            variety = p["variety"]
            if len(variety) > 30:
                variety = variety[:27] + "..."
            print(f"  {variety:<32} {bed_name:<8} {timing}")

    ready_now   = [(r, p, b) for r, p, b in items if (r - today).days <= 0]
    week        = [(r, p, b) for r, p, b in items if 1 <= (r - today).days <= 7]
    two_weeks   = [(r, p, b) for r, p, b in items if 8 <= (r - today).days <= 14]
    month       = [(r, p, b) for r, p, b in items if 15 <= (r - today).days <= 30]
    later       = [(r, p, b) for r, p, b in items if (r - today).days > 30]

    section("READY TO HARVEST", ready_now)
    section("THIS WEEK (next 7 days)", week)
    section("NEXT 2 WEEKS", two_weeks)
    section("THIS MONTH", month)
    section("LATER", later)

    # Watering reminder
    last_watered = {}
    for entry in data["watering_log"]:
        bid = entry["bed"]
        existing = last_watered.get(bid)
        if existing is None or entry["date"] > existing:
            last_watered[bid] = entry["date"]

    print(f"\n  WATERING STATUS")
    print(f"  {'-'*48}")
    for bed in data["beds"]:
        bid = bed["id"]
        lw = last_watered.get(bid)
        if lw:
            ds = days_since(lw)
            warn = "  *** WATER SOON" if ds >= 2 else ""
            print(f"  {bed['name']:<10} last watered {ds}d ago ({lw}){warn}")
        else:
            print(f"  {bed['name']:<10} no watering recorded  *** LOG A WATERING")

    print()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

USAGE = """Usage: garden.py <command>

Commands:
  status          Overview of all beds and plant health
  water-check     Should I water today? (uses Open-Meteo weather API)
  log water       Record a watering event
  log harvest     Record a harvest
  add-pest        Log a pest or disease observation
  schedule        Upcoming harvest dates and watering status
"""

def main():
    args = sys.argv[1:]

    if not args:
        print(USAGE)
        sys.exit(1)

    command = args[0]

    if command == "status":
        cmd_status()
    elif command == "water-check":
        cmd_water_check()
    elif command == "log":
        if len(args) < 2:
            print("Usage: garden.py log <water|harvest>")
            sys.exit(1)
        sub = args[1]
        if sub == "water":
            cmd_log_water()
        elif sub == "harvest":
            cmd_log_harvest()
        else:
            print(f"Unknown log subcommand: {sub}")
            print("Usage: garden.py log <water|harvest>")
            sys.exit(1)
    elif command == "add-pest":
        cmd_add_pest()
    elif command == "schedule":
        cmd_schedule()
    else:
        print(f"Unknown command: {command}\n")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
