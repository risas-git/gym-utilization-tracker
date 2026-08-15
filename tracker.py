from datetime import datetime
import json
import os
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:
    requests = None

STUDIOS = {
    "Bielefeld Schildesche": "https://www.ai-fitness.de/connect/v1/studio/1468963780/utilization",
    "Bielefeld Sieker": "https://www.ai-fitness.de/connect/v1/studio/1316633090/utilization",
    "Bielefeld City": "https://www.ai-fitness.de/connect/v1/studio/1321967250/utilization",
}

CSV_FILE = "utilization_log.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_studio_data(url):
    if requests is not None:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    else:
        import urllib.request

        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode("utf-8"))


def migrate_csv_header_if_needed():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.write("timestamp,studio,slot_start,slot_end,percentage,level\n")
        return

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.write("timestamp,studio,slot_start,slot_end,percentage,level\n")
        return

    first_line = lines[0].strip()
    if first_line == "timestamp,slot_start,slot_end,percentage,level":
        # Migrate old format to new format by inserting default studio name
        new_lines = ["timestamp,studio,slot_start,slot_end,percentage,level\n"]
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 5:
                # Insert 'Bielefeld City' as studio name
                new_lines.append(f"{parts[0]},Bielefeld City,{parts[1]},{parts[2]},{parts[3]},{parts[4]}\n")
            else:
                new_lines.append(line)

        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)


def log_utilization():
    migrate_csv_header_if_needed()

    try:
        germany_tz = ZoneInfo("Europe/Berlin")
        now = datetime.now(germany_tz).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for studio_name, url in STUDIOS.items():
        try:
            data = fetch_studio_data(url)
            items = data.get("items", []) if data else []
            current_slot = next((item for item in items if item.get("isCurrent")), None)

            with open(CSV_FILE, "a", encoding="utf-8") as f:
                if current_slot:
                    f.write(
                        f"{now},{studio_name},{current_slot['startTime']},{current_slot['endTime']},{current_slot['percentage']},{current_slot['level']}\n"
                    )
                else:
                    f.write(f"{now},{studio_name},closed,closed,0,CLOSED\n")

            print(f"[{now}] [{studio_name}] Logged successfully.")
        except Exception as e:
            print(f"[{now}] [{studio_name}] Error fetching data: {e}")


if __name__ == "__main__":
    log_utilization()