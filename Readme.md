# Nexusmods Information Fetcher (N.I.F)

`Nexusmods information fetcher` is a simple python+gui program that allows the user to specify a game name and a mod id and automatically get its information from [nexusmods](https://www.nexusmods.com/) for use in conjunction with [fluffy mod manager](https://www.nexusmods.com/site/mods/818)

~~A program to allow automatically creating mods with multiple options is under development.~~ 
The program can be found [here](https://github.com/Motor-k/Fluffy-Automated-Option-Generator)

This document explains the libraries used by the NexusMods Information Fetcher program and how to install and run it.

GUI Version:

![Image of the gui version of nexusmods information fetcher](https://i.imgur.com/L2ZSeQj.png)

---

## Libraries Used

- **requests**
  - HTTP library for Python, used to make GET requests to the NexusMods API and to download the mod `picture_url` image.
  - Installed via `pip install requests`.

- **tkinter**
  - Standard Python GUI toolkit, used to build the simple graphical interface for entering the Mod ID and Game Name (the API key can be read from `apikey.txt`).
  - Included with most Python distributions; no additional installation needed.

- **configparser**
  - Part of the Python standard library; used to generate the `modinfo.ini` file with the requested fields.


---

## Requirements

Make sure you have Python 3.6+ installed. Then install the third-party dependency:

```bash
pip install -r requirements.txt
```
or `install requirements.bat`

The provided **requirements.txt** should contain:

```text
requests>=2.25.1
```

---

## Files

- `apikey.txt` - A plain text file containing your NexusMods API key (no newline or extra characters).
- `run_GUI.bat` - A simple batch file to launch the gui.
- `fetch_nexus_mod_GUI.py` - The main Python script with GUI, fetch logic and file output.
- `install requirements.bat` - A simple batch file to install the requirements listed on the requirements.txt.
- `requirements.txt` - Lists the `requests` dependency.
- `NoGui\run.bat` - A simple configurable batch file to run the no GUI version of the program with pre-set variables.
- `NoGui\fetch_nexus_mod.py` - A simple configurable batch file to run the no GUI version of the program with pre-set variables.
---

## How to Run

1. Make sure you have python installed (get from microft store to avoid anoying config issues) and run `install requirements.bat`
2. Create/edit a file named `apikey.txt` containing only your API key.
3. Launch the GUI by running `run_GUI.bat`
4. In the GUI window, enter:
   - **Game Name** (e.g. `skyrim`, `fallout4`)
   - **Mod ID** (integer)
5. Click **Fetch**.

On success, you will see two new files in the folder:

- `modinfo.ini` - Contains:
  ```ini
  [ModInfo]
  name        = <mod name>
  version     = <mod version>
  description = <mod summary>
  author      = <mod author>
  category    = costumes
  homepage    = https://www.nexusmods.com/<gamename>/mods/<id>
  ```

- `screenshot.png` - The mod's `picture_url` image.

---

## Troubleshooting

- **`requests.exceptions.HTTPError`**: Check your API key, Game Name, and Mod ID for typos.
- **No `picture_url`**: The program will skip screenshot download if the API response lacks a `picture_url` field.
- **`tkinter` missing**: On some Linux installs you may need to install `python3-tk` via your package manager.

Developed by : Gustavo Bule