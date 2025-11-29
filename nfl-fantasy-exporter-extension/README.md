# NFL Fantasy Data Exporter - Chrome Extension

A Chrome extension that extracts player ownership data from NFL Fantasy and exports it to CSV format compatible with the Fantasy Football Helper Scripts.

## Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top right corner)
3. Click **Load unpacked**
4. Select the `nfl-fantasy-exporter-extension` folder
5. The extension icon should appear in your browser toolbar

## Usage

### Step 1: Navigate to NFL Fantasy

1. Go to [fantasy.nfl.com](https://fantasy.nfl.com)
2. Log in to your account
3. Navigate to your league
4. Go to **Players** → Select **All Taken Players** from the status dropdown

### Step 2: Extract Data

1. Click the extension icon in your browser toolbar
2. You'll see two extraction options:
   - **Extract Current Page**: Extracts only the players visible on the current page
   - **Extract All Pages**: Extracts all owned players across all positions (Offense, Kickers, Defense)

3. Click **Extract All Pages** for a complete export
4. The extension will automatically:
   - Click through the Offense, K, and DEF position tabs
   - Navigate through all pagination pages for each position
   - Collect all player data

### Step 3: Download CSV

1. Once extraction is complete, click **Download CSV**
2. The file `drafted_data.csv` will be downloaded
3. Move this file to the `data/` folder in your Fantasy Football Helper Scripts directory

## Output Format

The exported CSV matches the format expected by the league helper:

```
Player Name Position - Team [View News],Owner Name
```

Examples:
```
A.J. Brown WR - PHI View News,Pidgin
Patrick Mahomes QB - KC,Sea Sharp
Chicago Bears DEF,Annihilators
Brandon Aubrey K - DAL,The Eskimo Brothers
```

### Data Extracted

| Field | Description | Example |
|-------|-------------|---------|
| Player Name | Full player name | `A.J. Brown` |
| Position | Player position (QB, RB, WR, TE, K, DEF) | `WR` |
| Team | NFL team abbreviation | `PHI` |
| View News | Indicator if player has news (optional) | `View News` |
| Owner | Fantasy team name that owns the player | `Pidgin` |

### Note on Injury Status

The extension does not capture injury status codes (Q, O, IR, IA) from the page. This is intentional and does not affect functionality - the league helper's `DraftedRosterManager` normalizes these codes out during player matching anyway.

## Troubleshooting

### "Error: Could not access page. Try refreshing."
- Refresh the NFL Fantasy page and try again
- Make sure you're on a `fantasy.nfl.com` page

### "Navigate to fantasy.nfl.com to use this extension"
- The extension only works on NFL Fantasy pages
- Navigate to your league's player list first

### Extension not appearing in toolbar
- Go to `chrome://extensions/` and verify the extension is enabled
- Click the puzzle piece icon in Chrome and pin the extension

### Missing players in export
- Ensure you're on the "All Taken Players" view (not "All Available" or a specific team)
- Use "Extract All Pages" to get all positions including K and DEF

## Files

| File | Description |
|------|-------------|
| `manifest.json` | Chrome extension configuration (Manifest V3) |
| `popup.html` | Extension popup UI |
| `popup.js` | Popup logic - handles extraction and download |
| `content.js` | Content script - extracts data from page DOM |
| `icon16.png` | Extension icon (16x16) |
| `icon48.png` | Extension icon (48x48) |
| `icon128.png` | Extension icon (128x128) |

## Technical Details

- **Manifest Version**: 3 (Chrome's latest extension format)
- **Permissions**: `activeTab`, `scripting` (minimal permissions required)
- **Host Permissions**: `https://fantasy.nfl.com/*`

### How It Works

1. The popup script (`popup.js`) injects the content script into the active tab
2. The content script (`content.js`) queries the DOM for player table rows
3. For each row, it extracts:
   - Player name from `.playerName` element
   - Position/Team from the `<em>` tag
   - Owner from `.teamName` element
   - News indicator from `.playerNote` presence
4. The popup navigates through position tabs (O, K, DEF) and pagination
5. All data is collected and formatted as CSV for download

## Compatibility

- **Browser**: Chrome (or Chromium-based browsers like Edge, Brave)
- **NFL Fantasy**: Works with the 2024-2025 NFL Fantasy interface
- **Output**: Compatible with Fantasy Football Helper Scripts `DraftedRosterManager`
