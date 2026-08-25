from datetime import datetime, timedelta, timezone
import json
import os
import sys
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:
    requests = None

# Supabase REST API Configuration
SUPABASE_URL = "https://vnsqquagjxgjteuvypwo.supabase.co/rest/v1/gym_utilization"
SUPABASE_KEY = "sb_publishable_pKmBZFPN2bcGOEA3l7yrjA_tpusw3Pl"
OUTPUT_PLOT = "gym_utilization_analysis.png"

COLORS = [
    "#2563eb",  # Blue
    "#10b981",  # Emerald Green
    "#f59e0b",  # Amber/Orange
    "#8b5cf6",  # Purple
    "#ec4899",  # Pink
    "#06b6d4",  # Cyan
    "#f43f5e",  # Red
    "#84cc16",  # Lime
]


def clean_studio_name(name):
    if not name:
        return "General Gym"
    import re

    cleaned = re.sub(r"^(ai\s*[-_]?\s*fitness\s*)", "", name, flags=re.IGNORECASE).strip()
    if cleaned == "Bielefeld Eckendorfer":
        cleaned = "Bielefeld City"
    return cleaned if cleaned else name


def parse_timestamp(ts_str):
    if not ts_str:
        return None
    try:
        # If standard ISO timestamp
        ts_clean = ts_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts_clean)
        # Convert to Germany timezone for plotting
        try:
            berlin_tz = ZoneInfo("Europe/Berlin")
            dt = dt.astimezone(berlin_tz)
        except Exception:
            pass
        return dt
    except Exception:
        # Fallback to string matching
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
    return None


def fetch_data_from_supabase(days=7):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Range-Unit": "items",
    }

    since_dt = datetime.now(timezone.utc) - timedelta(days=days)
    since_str = urllib.parse.quote(since_dt.isoformat())

    rows = []
    limit_per_page = 1000
    max_pages = 5

    for page in range(max_pages):
        offset = page * limit_per_page
        url = (
            f"{SUPABASE_URL}?select=timestamp,studio,percentage,level"
            f"&timestamp=gte.{since_str}&order=timestamp.desc&limit={limit_per_page}&offset={offset}"
        )
        batch = []
        try:
            if requests is not None:
                res = requests.get(url, headers=headers, timeout=20)
                res.raise_for_status()
                batch = res.json()
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as response:
                    batch = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"Error fetching page {page} from Supabase: {e}")
            break

        if not batch:
            break
        rows.extend(batch)
        if len(batch) < limit_per_page:
            break

    # Reverse rows to restore chronological order (oldest to newest) for plotting
    rows.reverse()

    studio_data = {}
    for r in rows:
        studio = clean_studio_name(r.get("studio"))
        ts = parse_timestamp(r.get("timestamp"))
        if not ts:
            continue
        try:
            pct = float(r.get("percentage", 0))
        except (ValueError, TypeError):
            pct = 0.0
        level = r.get("level", "UNKNOWN")

        if studio not in studio_data:
            studio_data[studio] = []
        studio_data[studio].append((ts, pct, level))

    return studio_data


def plot_with_matplotlib(studio_data):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
        import numpy as np

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9))
        fig.suptitle("Gym Utilization Tracker - Germany-Wide Studio Analysis", fontsize=16, fontweight="bold")

        # Select top active studios for chart clarity
        sorted_studios = sorted(
            studio_data.keys(),
            key=lambda s: max([r[1] for r in studio_data[s]]) if studio_data[s] else 0,
            reverse=True,
        )

        display_studios = sorted_studios[:8]

        # Plot 1: Time Series per Studio
        for i, studio in enumerate(display_studios):
            records = studio_data[studio]
            color = COLORS[i % len(COLORS)]
            timestamps = [r[0] for r in records]
            percentages = [r[1] for r in records]

            ax1.plot(
                timestamps,
                percentages,
                marker="o",
                markersize=4,
                linewidth=2,
                label=studio,
                color=color,
                alpha=0.85,
            )

        ax1.set_title(f"Utilization Over Time (Top {len(display_studios)} Active Studios)", fontsize=12)
        ax1.set_ylabel("Utilization (%)")
        ax1.set_ylim(0, 100)
        ax1.grid(True, linestyle="--", alpha=0.6)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax1.legend(loc="upper left", fontsize=9)
        fig.autofmt_xdate()

        # Plot 2: Hourly Averages per Studio
        all_hours = range(0, 24)
        x = np.arange(len(all_hours))
        num_studios = len(display_studios)
        width = 0.8 / max(1, num_studios)

        for i, studio in enumerate(display_studios):
            records = studio_data[studio]
            color = COLORS[i % len(COLORS)]
            hour_dict = {h: [] for h in all_hours}
            for dt, pct, _ in records:
                hour_dict[dt.hour].append(pct)

            avg_list = [sum(hour_dict[h]) / len(hour_dict[h]) if hour_dict[h] else 0 for h in all_hours]
            offset = (i - num_studios / 2 + 0.5) * width
            ax2.bar(x + offset, avg_list, width, label=studio, color=color, alpha=0.85)

        ax2.set_title("Average Utilization by Hour of Day", fontsize=12)
        ax2.set_xlabel("Hour of Day (0 - 23)")
        ax2.set_ylabel("Average Utilization (%)")
        ax2.set_xticks(x)
        ax2.set_xticklabels([f"{h:02d}:00" for h in all_hours], rotation=45, fontsize=8)
        ax2.set_ylim(0, 100)
        ax2.grid(True, linestyle="--", alpha=0.6)
        ax2.legend(loc="upper left", fontsize=9)

        plt.tight_layout()
        plt.savefig(OUTPUT_PLOT, dpi=300)
        print(f"Successfully generated plot: {OUTPUT_PLOT}")

    except ImportError:
        print("matplotlib is not installed. To generate PNG charts, run: pip install matplotlib")


def main():
    studio_data = fetch_data_from_supabase(days=7)
    if not studio_data:
        print("No valid data found in Supabase. Run tracker.py to log utilization records.")
        sys.exit(0)

    total_records = sum(len(v) for v in studio_data.values())
    print(f"Loaded {total_records} records across {len(studio_data)} studio(s) directly from Supabase.")
    plot_with_matplotlib(studio_data)


if __name__ == "__main__":
    main()
