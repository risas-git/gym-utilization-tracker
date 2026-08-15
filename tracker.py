import concurrent.futures
from datetime import datetime
import json
import os
from zoneinfo import ZoneInfo

try:
    import requests
except ImportError:
    requests = None

STUDIO_DIRECTORY_URL = "https://www.ai-fitness.de/connect/v2/studio"
UTILIZATION_URL_TEMPLATE = "https://www.ai-fitness.de/connect/v1/studio/{id}/utilization"
CSV_FILE = "utilization_log.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_url_json(url):
    if requests is not None:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return res.json()
    else:
        import urllib.request

        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)


def get_all_studios():
    try:
        studios_data = fetch_url_json(STUDIO_DIRECTORY_URL)
        studios = []
        for s in studios_data:
            sid = s.get("id")
            name = s.get("studioName", "").strip()
            city = s.get("address", {}).get("city", "").strip() if s.get("address") else ""

            if sid:
                # Standardize studio name format
                clean_name = name if name else f"Studio {sid}"
                if city and city.lower() not in clean_name.lower():
                    clean_name = f"{clean_name} ({city})"
                studios.append({"id": sid, "name": clean_name})
        return studios
    except Exception as e:
        print(f"Error fetching studio directory: {e}")
        # Fallback to local default studios if directory fetch fails
        return [
            {"id": "1468963780", "name": "Bielefeld Schildesche"},
            {"id": "1316633090", "name": "Bielefeld Sieker"},
            {"id": "1321967250", "name": "Bielefeld City"},
        ]


def fetch_studio_utilization(studio, timestamp):
    sid = studio["id"]
    name = studio["name"]
    url = UTILIZATION_URL_TEMPLATE.format(id=sid)

    try:
        data = fetch_url_json(url)
        items = data.get("items", []) if data else []
        current_slot = next((item for item in items if item.get("isCurrent")), None)

        if current_slot:
            return (
                f"{timestamp},{name},{current_slot['startTime']},{current_slot['endTime']},{current_slot['percentage']},{current_slot['level']}\n"
            )
        else:
            return f"{timestamp},{name},closed,closed,0,CLOSED\n"
    except Exception as e:
        return f"{timestamp},{name},closed,closed,0,CLOSED\n"


def ensure_csv_header():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.write("timestamp,studio,slot_start,slot_end,percentage,level\n")


def log_utilization():
    ensure_csv_header()

    try:
        germany_tz = ZoneInfo("Europe/Berlin")
        now = datetime.now(germany_tz).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    studios = get_all_studios()
    print(f"[{now}] Discovering & fetching utilization for {len(studios)} studios in Germany...")

    # Fetch all studio utilization data in parallel using ThreadPoolExecutor
    log_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_studio_utilization, s, now) for s in studios]
        for future in concurrent.futures.as_completed(futures):
            log_rows.append(future.result())

    # Write all fetched records to CSV in a single batch
    with open(CSV_FILE, "a", encoding="utf-8") as f:
        f.writelines(log_rows)

    print(f"[{now}] Successfully logged {len(log_rows)} studio records into {CSV_FILE}.")


if __name__ == "__main__":
    log_utilization()