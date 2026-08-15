import csv
from datetime import datetime
import os
import sys

CSV_FILE = "utilization_log.csv"
OUTPUT_PLOT = "gym_utilization_analysis.png"


def load_data(filepath):
    timestamps = []
    percentages = []
    levels = []

    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return timestamps, percentages, levels

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                pct = float(row["percentage"])
                timestamps.append(dt)
                percentages.append(pct)
                levels.append(row.get("level", "UNKNOWN"))
            except (ValueError, KeyError):
                continue

    return timestamps, percentages, levels


def plot_with_matplotlib(timestamps, percentages):
    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend for headless plotting
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle("Gym Utilization Tracker Analysis", fontsize=16, fontweight="bold")

        # Plot 1: Time Series (15-min Granularity)
        ax1.plot(timestamps, percentages, marker="o", color="#2563eb", linewidth=2, label="Utilization %")
        ax1.fill_between(timestamps, percentages, color="#3b82f6", alpha=0.2)
        ax1.set_title("Gym Utilization Over Time (15-Minute Intervals)", fontsize=12)
        ax1.set_ylabel("Utilization (%)")
        ax1.set_ylim(0, 100)
        ax1.grid(True, linestyle="--", alpha=0.6)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        fig.autofmt_xdate()

        # Plot 2: Average Utilization by Hour of Day
        hourly_data = {}
        for dt, pct in zip(timestamps, percentages):
            hour = dt.hour
            hourly_data.setdefault(hour, []).append(pct)

        hours = sorted(hourly_data.keys())
        avg_pcts = [sum(hourly_data[h]) / len(hourly_data[h]) for h in hours]

        bars = ax2.bar(hours, avg_pcts, color="#10b981", edgecolor="#047857", alpha=0.85)
        ax2.set_title("Average Utilization by Hour of Day", fontsize=12)
        ax2.set_xlabel("Hour of Day (0 - 23)")
        ax2.set_ylabel("Average Utilization (%)")
        ax2.set_xticks(range(0, 24))
        ax2.set_ylim(0, 100)
        ax2.grid(True, linestyle="--", alpha=0.6)

        # Highlight values on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.annotate(
                    f"{height:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

        plt.tight_layout()
        plt.savefig(OUTPUT_PLOT, dpi=300)
        print(f"Successfully generated plot: {OUTPUT_PLOT}")

    except ImportError:
        print("matplotlib is not installed. To generate PNG charts, run: pip install matplotlib")
        print("\n--- Summary Statistics ---")
        if percentages:
            print(f"Total Entries Recorded: {len(percentages)}")
            print(f"Latest Utilization: {percentages[-1]}%")
            print(f"Max Utilization: {max(percentages)}%")
            print(f"Average Utilization: {sum(percentages)/len(percentages):.2f}%")


def main():
    timestamps, percentages, levels = load_data(CSV_FILE)
    if not timestamps:
        print(f"No valid data found in {CSV_FILE}. Run tracker.py first to accumulate logs.")
        sys.exit(0)

    print(f"Loaded {len(timestamps)} records from {CSV_FILE}.")
    plot_with_matplotlib(timestamps, percentages)


if __name__ == "__main__":
    main()
