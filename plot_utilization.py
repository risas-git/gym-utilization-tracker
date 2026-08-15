import csv
from datetime import datetime
import os
import sys

CSV_FILE = "utilization_log.csv"
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


def load_data(filepath):
    studio_data = {}  # {studio_name: [(timestamp, percentage, level)]}

    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return studio_data

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                pct = float(row["percentage"])
                studio = row.get("studio", "General Gym").strip()
                if not studio or studio == "Bielefeld Eckendorfer":
                    studio = "Bielefeld City"

                if studio not in studio_data:
                    studio_data[studio] = []
                studio_data[studio].append((dt, pct, row.get("level", "UNKNOWN")))
            except (ValueError, KeyError):
                continue

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

        # Select top active studios for chart clarity if there are many
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
    studio_data = load_data(CSV_FILE)
    if not studio_data:
        print(f"No valid data found in {CSV_FILE}. Run tracker.py first to accumulate logs.")
        sys.exit(0)

    total_records = sum(len(v) for v in studio_data.values())
    print(f"Loaded {total_records} records across {len(studio_data)} studio(s) from {CSV_FILE}.")
    plot_with_matplotlib(studio_data)


if __name__ == "__main__":
    main()
