# Gym Utilization Tracker

Who also loves training in the gym but hates crowded ones where you have to wait for machines or ask *"How many sets do you have left?"*? 

With this app, you can view an overview of the business/occupancy of your nearest gyms to compare them and easily decide which one to go to!

📊 **[View Interactive Dashboard (Live Web App)](https://risas-git.github.io/gym-utilization-tracker/)**

---

## Features

- **Germany-Wide Studio Tracking**: Automatically discovers and tracks all **200+ All Inclusive / AI Fitness studios across Germany**.
- **Interactive Search & Filter**: Search and select any city or studio (e.g. Bielefeld City, Schildesche, Sieker, Bonn, Berlin, Munich) to compare capacity side-by-side.
- **15-Minute Automated Parallel Scraping**: Runs via GitHub Actions ([scrape.yml](.github/workflows/scrape.yml)) on a 15-minute cron schedule, leveraging multithreaded requests to fetch 200+ studios in ~5 seconds.
- **Cloud Database Storage**: Automatically logs all 15-minute capacity records into a Supabase PostgreSQL Cloud Database for long-term historical analytics.