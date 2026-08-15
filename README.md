# Gym Utilization Tracker

Automated 15-minute gym capacity tracker and visualization system for AI Fitness studios.

📊 **[View Interactive Dashboard (Live Web App)](https://risas-git.github.io/gym-utilization-tracker/)** | **[HTML Preview Link](https://htmlpreview.github.io/?https://github.com/risas-git/gym-utilization-tracker/blob/main/index.html)** | **[Source index.html](index.html)**

---

## Features

- **Multi-Studio Comparison**: Automatically tracks and compares multiple AI Fitness locations:
  - **Bielefeld Schildesche** (`1468963780`)
  - **Bielefeld Sieker** (`1316633090`)
  - **Bielefeld City** (`1321967250`)
- **15-Minute Automated Scraping**: Runs via GitHub Actions (`.github/workflows/scrape.yml`) on a 15-minute cron schedule (`*/15 * * * *`).
- **Resilient Logging**: Scrapes real-time crowd percentage data for all locations into `utilization_log.csv`.
- **Plotting & Analytics**: Includes `plot_utilization.py` to generate comparative multi-line charts and hourly average plots saved as PNG.
- **Interactive Dashboard**: Includes `index.html` with studio selector filters & side-by-side Chart.js visualizations.

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