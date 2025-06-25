#!/usr/bin/env python3
import argparse
import configparser
import requests
import sys
import os
from io import BytesIO
from PIL import Image

API_BASE = "https://api.nexusmods.com/v1/games"

def fetch_mod(api_key: str, gamename: str, mod_id: int) -> dict:
    url = f"{API_BASE}/{gamename}/mods/{mod_id}.json"
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def download_screenshot(picture_url: str, out_path: str = "screenshot.png"):
    """
    Download the image via requests, then re-save it through Pillow
    to guarantee a clean, standards-compliant PNG.
    """
    resp = requests.get(picture_url)
    resp.raise_for_status()

    # Load into PIL and re‐save
    img = Image.open(BytesIO(resp.content))
    # (optional) convert to RGBA to ensure alpha is correct:
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")

    img.save(out_path, format="PNG", optimize=True)

def write_modinfo(data: dict, gamename: str, mod_id: int, out_path: str = "modinfo.ini"):
    cfg = configparser.ConfigParser()
    cfg["ModInfo"] = {
        "name":        data.get("name", "UNKNOWN"),
        "version":     data.get("version", "1.0"),
        "description": data.get("summary", "").replace("\n", " "),
        "author":      data.get("author", "UNKNOWN"),
        "category":    "costumes",
        "homepage":    f"https://www.nexusmods.com/{gamename}/mods/{mod_id}"
    }
    with open(out_path, "w") as f:
        cfg.write(f)

def main():
    p = argparse.ArgumentParser(
        description="Fetch NexusMods mod JSON and emit modinfo.ini + screenshot.png"
    )
    p.add_argument("apikey", help="Your NexusMods API key")
    p.add_argument("gamename", help="Game domain name (e.g. skyrim, fallout4, etc.)")
    p.add_argument("mod_id", type=int, help="Numeric ID of the mod")
    args = p.parse_args()

    try:
        print(f"→ Fetching mod #{args.mod_id} for “{args.gamename}”…")
        mod = fetch_mod(args.apikey, args.gamename, args.mod_id)

        pic = mod.get("picture_url")
        if pic:
            print("→ Downloading screenshot.png …")
            download_screenshot(pic, "screenshot.png")
        else:
            print("No picture_url found; skipping screenshot download.")

        print("→ Writing modinfo.ini …")
        write_modinfo(mod, args.gamename, args.mod_id, "modinfo.ini")

        print("\n All done! Files created:")
        for fn in ("modinfo.ini", "screenshot.png"):
            if os.path.exists(fn):
                print("   •", fn)
    except requests.HTTPError as e:
        sys.exit(f"HTTP error: {e}")
    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()
