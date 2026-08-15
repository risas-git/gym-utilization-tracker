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

# Supabase Credentials
SUPABASE_URL = "https://vnsqquagjxgjteuvypwo.supabase.co/rest/v1/gym_utilization"
SUPABASE_KEY = "sb_publishable_pKmBZFPN2bcGOEA3l7yrjA_tpusw3Pl"

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


def clean_studio_name(name):
    if not name:
        return ""
    import re

    cleaned = re.sub(r"^(ai\s*[-_]?\s*fitness\s*)", "", name, flags=re.IGNORECASE).strip()
    return cleaned if cleaned else name


def get_all_studios():
    try:
        studios_data = fetch_url_json(STUDIO_DIRECTORY_URL)
        studios = []
        for s in studios_data:
            sid = s.get("id")
            name = s.get("studioName", "").strip()
            city = s.get("address", {}).get("city", "").strip() if s.get("address") else ""

            if sid:
                c_name = clean_studio_name(name) if name else f"Studio {sid}"
                if city and city.lower() not in c_name.lower():
                    c_name = f"{c_name} ({city})"
                studios.append({"id": sid, "name": c_name})
        return studios
    except Exception as e:
        print(f"Error fetching studio directory: {e}")
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
            return {
                "timestamp": timestamp,
                "studio": name,
                "slot_start": current_slot["startTime"],
                "slot_end": current_slot["endTime"],
                "percentage": current_slot["percentage"],
                "level": current_slot["level"],
            }
        else:
            return {
                "timestamp": timestamp,
                "studio": name,
                "slot_start": "closed",
                "slot_end": "closed",
                "percentage": 0,
                "level": "CLOSED",
            }
    except Exception:
        return {
            "timestamp": timestamp,
            "studio": name,
            "slot_start": "closed",
            "slot_end": "closed",
            "percentage": 0,
            "level": "CLOSED",
        }


def push_to_supabase(records):
    try:
        if requests is not None:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            }
            res = requests.post(SUPABASE_URL, json=records, headers=headers, timeout=15)
            res.raise_for_status()
            print(f"Successfully pushed {len(records)} records to Supabase Cloud Database.")
        else:
            import urllib.request

            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            }
            req = urllib.request.Request(
                SUPABASE_URL, data=json.dumps(records).encode("utf-8"), headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as res:
                print(f"Successfully pushed {len(records)} records to Supabase Cloud Database.")
    except Exception as e:
        print(f"Error pushing to Supabase: {e}")


def ensure_csv_header():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.write("timestamp,studio,slot_start,slot_end,percentage,level\n")


def log_utilization():
    ensure_csv_header()

    try:
        germany_tz = ZoneInfo("Europe/Berlin")
        dt_now = datetime.now(germany_tz)
    except Exception:
        import datetime as dt_module
        germany_tz = dt_module.timezone(dt_module.timedelta(hours=2))
        dt_now = datetime.now(germany_tz)

    now_str = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    iso_str = dt_now.isoformat()

    studios = get_all_studios()
    print(f"[{now_str}] Discovering & fetching utilization for {len(studios)} studios in Germany...")

    # Fetch all studio utilization data in parallel using ThreadPoolExecutor
    db_records = []
    csv_rows = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_studio_utilization, s, iso_str) for s in studios]
        for future in concurrent.futures.as_completed(futures):
            rec = future.result()
            db_records.append(rec)
            csv_rows.append(
                f"{now_str},{rec['studio']},{rec['slot_start']},{rec['slot_end']},{rec['percentage']},{rec['level']}\n"
            )

    # Batch insert into Supabase Cloud Database
    push_to_supabase(db_records)

    # Also log to local CSV backup
    with open(CSV_FILE, "a", encoding="utf-8") as f:
        f.writelines(csv_rows)

    print(f"[{now_str}] Logged {len(db_records)} studio records.")


if __name__ == "__main__":
    log_utilization()