#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import configparser
import requests
import os

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
    resp = requests.get(picture_url, stream=True)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)

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

def on_fetch():
    try:
       with open("apikey.txt", "r") as f:
           key = f.read().strip()
    except IOError:
        messagebox.showerror("Error", "Could not open apikey.txt - make sure it exists")
        return 
    game   = entry_game.get().strip()
    mod_id = entry_id.get().strip()

    if not key or not game or not mod_id:
        messagebox.showwarning("Missing Data", "Please fill in all three fields.")
        return

    try:
        mod_id_int = int(mod_id)
    except ValueError:
        messagebox.showerror("Invalid ID", "Mod ID must be an integer.")
        return

    try:
        status.set("Fetching metadata…")
        root.update_idletasks()

        mod = fetch_mod(key, game, mod_id_int)

        pic_url = mod.get("picture_url")
        if pic_url:
            status.set("Downloading screenshot…")
            root.update_idletasks()
            download_screenshot(pic_url)
        else:
            # no picture_url
            pass

        status.set("Writing modinfo.ini…")
        root.update_idletasks()
        write_modinfo(mod, game, mod_id_int)

        status.set("Done!")
        messagebox.showinfo("Success", "Created modinfo.ini and screenshot.png")
    except requests.HTTPError as e:
        status.set("Error")
        messagebox.showerror("HTTP Error", str(e))
    except Exception as e:
        status.set("Error")
        messagebox.showerror("Error", str(e))

# --- build the UI ---
root = tk.Tk()
root.title("NexusMods Fetch")
root.iconbitmap("resources/icon.ico")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack()

""" in case you want to have the api key being entered manually for security
tk.Label(frm, text="API Key:").grid(row=0, column=0, sticky="e")
entry_key  = tk.Entry(frm, width=40)
entry_key.grid(row=0, column=1, pady=2) """

tk.Label(frm, text="Game Name:").grid(row=1, column=0, sticky="e")
entry_game = tk.Entry(frm, width=40)
entry_game.grid(row=1, column=1, pady=2)

tk.Label(frm, text="Mod ID:").grid(row=2, column=0, sticky="e")
entry_id   = tk.Entry(frm, width=40)
entry_id.grid(row=2, column=1, pady=2)

btn = tk.Button(frm, text="Fetch", command=on_fetch)
btn.grid(row=3, column=0, columnspan=2, pady=8)

status = tk.StringVar(value="Ready")
status_lbl = tk.Label(root, textvariable=status, anchor="w")
status_lbl.pack(fill="x", padx=10, pady=(0,10))

root.mainloop()