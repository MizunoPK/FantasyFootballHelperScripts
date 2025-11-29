// NFL Fantasy Data Exporter - Content Script
// Extracts player data from NFL Fantasy player list pages

function extractPlayersFromPage() {
  const players = [];
  const rows = document.querySelectorAll('tr[class*="player-"]');

  rows.forEach(row => {
    try {
      // Get player name
      const nameEl = row.querySelector('.playerName');
      if (!nameEl) return;

      const playerName = nameEl.textContent.trim();

      // Get position and team from the <em> element
      const infoCell = row.querySelector('.playerNameAndInfo');
      if (!infoCell) return;

      const posTeamEl = infoCell.querySelector('em');
      let posTeam = '';

      if (posTeamEl) {
        posTeam = posTeamEl.textContent.trim();
        // Position/Team format: "WR - PHI" or "QB - KC Q" (with injury status)
        // For DEF: just "DEF"
        // For K: "K - DAL"
      }

      // Check for news indicator
      const hasNews = row.querySelector('.playerNote') !== null;

      // Get owner/manager
      const ownerEl = row.querySelector('.teamName');
      const owner = ownerEl ? ownerEl.textContent.trim() : 'Free Agent';

      // Build the player string in the expected format
      let playerString;

      // Check if this is a defense (posTeam is just "DEF")
      if (posTeam === 'DEF') {
        // Defense format: "Team Name DEF" (e.g., "Chicago Bears DEF")
        playerString = `${playerName} DEF`;
      } else {
        // Regular player format: "Player Name Position - Team [Status] [View News]"
        playerString = `${playerName} ${posTeam}`;
      }

      if (hasNews) {
        playerString += ' View News';
      }

      players.push({
        playerString: playerString,
        owner: owner
      });

    } catch (e) {
      console.error('Error parsing player row:', e);
    }
  });

  return players;
}

function formatAsCSV(players) {
  return players.map(p => `${p.playerString},${p.owner}`).join('\n');
}

function getPageInfo() {
  // Get pagination info
  const paginationTitle = document.querySelector('.paginationTitle');
  let currentPage = 1;
  let totalPlayers = 0;
  let hasNextPage = false;

  if (paginationTitle) {
    const match = paginationTitle.textContent.match(/(\d+)\s*-\s*(\d+)\s*of\s*(\d+)/);
    if (match) {
      const start = parseInt(match[1]);
      const end = parseInt(match[2]);
      totalPlayers = parseInt(match[3]);
      currentPage = Math.ceil(start / 25);
      hasNextPage = end < totalPlayers;
    }
  }

  // Check for next page link
  const nextLink = document.querySelector('.next a');
  hasNextPage = hasNextPage && nextLink !== null;

  return { currentPage, totalPlayers, hasNextPage };
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractPlayers') {
    const players = extractPlayersFromPage();
    const pageInfo = getPageInfo();
    sendResponse({
      players: players,
      pageInfo: pageInfo
    });
  } else if (request.action === 'getPageInfo') {
    const pageInfo = getPageInfo();
    sendResponse({ pageInfo: pageInfo });
  }
  return true; // Keep message channel open for async response
});
