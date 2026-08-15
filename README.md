# Gym Utilization Tracker

Automated 15-minute gym capacity tracker and visualization system for AI Fitness studios.

📊 **[View Interactive Dashboard (Live Web App)](https://risas-git.github.io/gym-utilization-tracker/)** | **[HTML Preview Link](https://htmlpreview.github.io/?https://github.com/risas-git/gym-utilization-tracker/blob/main/index.html)** | **[Source index.html](index.html)**

---

## Features

- **Germany-Wide Studio Tracking**: Automatically discovers and tracks all **200+ All Inclusive / AI Fitness studios across Germany**.
- **Interactive Search & Filter**: Search and select any city or studio (e.g. Bielefeld City, Schildesche, Sieker, Bonn, Berlin, Munich) to compare capacity side-by-side.
- **15-Minute Automated Parallel Scraping**: Runs via GitHub Actions (`.github/workflows/scrape.yml`) on a 15-minute cron schedule (`*/15 * * * *`), leveraging multithreaded requests to fetch 200+ studios in ~5 seconds.
- **Resilient Logging**: Records capacity statistics into `utilization_log.csv`.
- **Plotting & Analytics**: Includes `plot_utilization.py` to generate comparative multi-line charts and hourly average plots saved as PNG.
- **Interactive Dashboard**: Includes `index.html` with real-time search & studio selector filters.

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
You can jump directly to the visualization using any of the following links:
- **Live Dashboard (GitHub Pages)**: [https://risas-git.github.io/gym-utilization-tracker/](https://risas-git.github.io/gym-utilization-tracker/)
- **Instant HTML Preview**: [View on HTMLPreview](https://htmlpreview.github.io/?https://github.com/risas-git/gym-utilization-tracker/blob/main/index.html)
- **Local / Repository File**: Open [index.html](index.html) directly in your browser or repository.

## Automated Scheduling

The GitHub Actions workflow runs every 15 minutes (`:00`, `:15`, `:30`, `:45`). When new data is fetched, it automatically commits and pushes the updated `utilization_log.csv` back to your repository.