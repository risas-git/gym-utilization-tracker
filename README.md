# Gym Utilization Tracker

Automated 15-minute gym capacity tracker and visualization system for AI Fitness studios.

## Features

- **15-Minute Automated Scraping**: Runs via GitHub Actions (`.github/workflows/scrape.yml`) on a 15-minute cron schedule (`*/15 * * * *`).
- **Resilient Logging**: Scrapes real-time crowd percentage data and appends timestamped logs to `utilization_log.csv`.
- **Plotting & Analytics**: Includes `plot_utilization.py` to generate time-series trend lines and hourly average charts saved as PNG.
- **Interactive Dashboard**: Includes `index.html` with Chart.js to visualize logs directly in any web browser.

## Quick Start

### 1. Manual Scrape
To run the tracker manually and log current utilization:
```bash
python tracker.py
```

### 2. Generate Plot / Graph
To analyze the logged data and output high-resolution PNG charts:
```bash
python plot_utilization.py
```
This generates `gym_utilization_analysis.png`.

### 3. Open Interactive Web Dashboard
Open `index.html` in your web browser to view the interactive 15-minute graphs, peak utilization stats, and hourly heatmaps.

## Automated Scheduling

The GitHub Actions workflow runs every 15 minutes (`:00`, `:15`, `:30`, `:45`). When new data is fetched, it automatically commits and pushes the updated `utilization_log.csv` back to your repository.