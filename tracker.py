from datetime import datetime
import json
import os
from zoneinfo import ZoneInfo
import requests

URL = "https://www.ai-fitness.de/connect/v1/studio/1321967250/utilization"
CSV_FILE = "utilization_log.csv"

# Polite headers mimicking standard web traffic
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def log_utilization():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Explicitly get the current time in Germany (handles CET/CEST automatically)
        germany_tz = ZoneInfo("Europe/Berlin")
        now = datetime.now(germany_tz).strftime("%Y-%m-%d %H:%M:%S")

        # Find the active hour slot or save all slots
        items = data.get("items", [])
        current_slot = next((item for item in items if item.get("isCurrent")), None)

        file_exists = os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("timestamp,slot_start,slot_end,percentage,level\n")

            if current_slot:
                f.write(
                    f"{now},{current_slot['startTime']},{current_slot['endTime']},{current_slot['percentage']},{current_slot['level']}\n"
                )
            else:
                # If gym is closed or no slot is active, record a 0% entry
                f.write(f"{now},closed,closed,0,CLOSED\n")

        print(f"[{now}] Logged successfully.")
    except Exception as e:
        print(f"Error fetching data: {e}")


if __name__ == "__main__":
    log_utilization()