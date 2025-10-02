# NFL Scores Fetcher - Beginner's Guide

A simple Python script to download NFL game scores from ESPN and save them to Excel files.

## What This Script Does

- Fetches NFL game scores from ESPN's free API
- Saves data to Excel files with detailed game information
- Works for any NFL week or season
- No ESPN account or API key required!

## What You Need

1. **Python 3.12 or higher** installed on your computer
2. **Internet connection** to download scores from ESPN
3. **Basic text editor** to modify configuration (Notepad, TextEdit, etc.)

---

## Installation

### Step 1: Install Python

**If you don't have Python installed:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.12 or newer
3. **Important:** During installation, check the box that says "Add Python to PATH"
4. Complete the installation

**To check if Python is installed:**
- Open Command Prompt (Windows) or Terminal (Mac/Linux)
- Type: `python --version`
- You should see something like: `Python 3.12.0`

### Step 2: Install Required Libraries

Open Command Prompt or Terminal and run these commands one at a time:

```bash
pip install httpx
pip install pydantic
pip install tenacity
pip install pandas
pip install openpyxl
```

**What these do:**
- `httpx` - Downloads data from ESPN
- `pydantic` - Validates the data
- `tenacity` - Retries if ESPN is slow
- `pandas` - Organizes data into tables
- `openpyxl` - Creates Excel files

---

## Setup

### Step 1: Download the Script

Save the `fetch_nfl_scores.py` file to a folder on your computer.

### Step 2: Configure What Data to Fetch

Open `fetch_nfl_scores.py` in a text editor and find the **CONFIGURATION** section at the top:

```python
# NFL Season Settings
SEASON = 2025                    # NFL season year
SEASON_TYPE = 2                  # 1=preseason, 2=regular, 3=postseason, 4=off-season
CURRENT_WEEK = 5                 # NFL week number (1-18), or None for recent games
ONLY_COMPLETED_GAMES = False     # True = only final scores, False = include live/upcoming

# Output Settings
OUTPUT_DIRECTORY = "./data"      # Where to save Excel files
CREATE_NORMAL_EXCEL = True       # Create detailed Excel with multiple sheets
CREATE_CONDENSED_EXCEL = True    # Create condensed team-comparison Excel
```

**What to change:**

- `SEASON` - Change to the NFL season year you want (e.g., `2025`)
- `CURRENT_WEEK` - Change to the week you want (e.g., `7` for week 7)
  - Set to `None` to get recent games from the last 10 days
- `ONLY_COMPLETED_GAMES` - Set to `True` if you only want finished games
- `CREATE_NORMAL_EXCEL` - Keep `True` for detailed game data
- `CREATE_CONDENSED_EXCEL` - Keep `True` for simple team comparison

### Step 3: Save Your Changes

After editing the configuration, save the file.

---

## Usage

### Running the Script

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the folder with the script:
   ```bash
   cd path/to/your/folder
   ```
3. Run the script:
   ```bash
   python fetch_nfl_scores.py
   ```

### What Happens

The script will:
1. Connect to ESPN's API
2. Download the game scores
3. Create Excel files in the `./data` folder
4. Print a summary to your screen

**Example output:**
```
============================================================
NFL SCORES FETCHER - Standalone Version
============================================================
Season: 2025
Week: 5
Output Directory: ./data
============================================================

Fetching NFL scores from ESPN...
Making request to ESPN API...
Request successful
Processing 14 games
Successfully parsed 14 games

Exporting data to Excel...
Created normal Excel: nfl_scores_week5_2025-10-01_15-30-45.xlsx
Created condensed Excel: nfl_scores_condensed_week5_2025-10-01_15-30-45.xlsx

============================================================
NFL SCORES COLLECTION COMPLETE
============================================================
...
```

---

## Output Files

The script creates two types of Excel files in the `./data` folder:

### 1. Normal Excel File (`nfl_scores_week5_*.xlsx`)

Contains multiple sheets:
- **All Games** - Every game with full details (scores, venue, weather, etc.)
- **Completed Games** - Only finished games
- **Summary** - Statistics like average points, overtime games, etc.
- **High Scoring Games** - Games with 50+ total points

### 2. Condensed Excel File (`nfl_scores_condensed_week5_*.xlsx`)

Simple format with one row per team showing:
- Team name
- Opponent
- Points scored
- Points allowed

Perfect for quick comparisons!

---

## Troubleshooting

### Error: "Python is not recognized"

**Problem:** Python is not in your system PATH

**Solution:**
1. Reinstall Python and check "Add Python to PATH" during installation
2. OR manually add Python to your PATH:
   - Windows: Search "Environment Variables" → Edit PATH → Add Python folder
   - Mac/Linux: Add to `~/.bashrc` or `~/.zshrc`: `export PATH="/usr/local/bin/python3:$PATH"`

### Error: "No module named 'httpx'"

**Problem:** Required libraries not installed

**Solution:**
Run the installation commands again:
```bash
pip install httpx pydantic tenacity pandas openpyxl
```

### Error: "Network error" or "ESPN server error"

**Problem:** Cannot connect to ESPN or ESPN is down

**Solution:**
1. Check your internet connection
2. Try again in a few minutes (ESPN may be temporarily down)
3. Verify the ESPN API is working by visiting [espn.com](https://www.espn.com)

### Error: "This script requires Python 3.12 or higher"

**Problem:** Your Python version is too old

**Solution:**
1. Check your version: `python --version`
2. Download Python 3.12+ from [python.org](https://www.python.org/downloads/)
3. Uninstall old Python first (optional but recommended)

### No Games Found

**Problem:** Script runs but says "No games found"

**Solution:**
1. Check your `SEASON` and `CURRENT_WEEK` settings
2. Make sure you're requesting a week that has already been played
3. If requesting future weeks, set `ONLY_COMPLETED_GAMES = False`

### Rate Limited by ESPN

**Problem:** ESPN tells you to slow down

**Solution:**
- The script automatically waits and retries
- If it keeps happening, increase `RATE_LIMIT_DELAY` in the configuration (try `0.5` or `1.0`)

### Permission Denied Creating Files

**Problem:** Can't create the `./data` folder or files

**Solution:**
1. Make sure you have write permissions in the script folder
2. Try running Command Prompt/Terminal as Administrator
3. Change `OUTPUT_DIRECTORY` to a folder where you have permissions (e.g., `C:/Users/YourName/Documents/nfl_data`)

### Script Hangs or Takes Too Long

**Problem:** Script seems frozen

**Solution:**
1. ESPN API might be slow - wait up to 60 seconds
2. Check `REQUEST_TIMEOUT` setting (default is 30 seconds)
3. Press Ctrl+C to cancel and try again

---

## File Details

### Filename Format

Files are named with a timestamp:
- `nfl_scores_week5_2025-10-01_15-30-45.xlsx`
  - `week5` - The NFL week
  - `2025-10-01` - Date created
  - `15-30-45` - Time created (3:30:45 PM)

### Data Retention

- The script creates new files each time it runs
- Old files are NOT deleted automatically
- You can manually delete old files from the `./data` folder

---

## Tips

1. **Weekly Routine**: Run the script after games finish each week to collect scores
2. **Backup Data**: Copy Excel files to another location if you want to keep them long-term
3. **Multiple Weeks**: Change `CURRENT_WEEK` and run again to get different weeks
4. **Recent Games**: Set `CURRENT_WEEK = None` to automatically get the last 10 days of games

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Make sure all dependencies are installed: `pip list | grep -E "httpx|pydantic|tenacity|pandas|openpyxl"`
3. Verify your Python version: `python --version` (must be 3.12+)
4. Check your internet connection

---

## License

This script uses ESPN's free public API. Use responsibly and don't make excessive requests.

---

**Last Updated:** October 2025
