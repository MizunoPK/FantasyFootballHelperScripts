// NFL Fantasy Data Exporter - Popup Script

let allPlayers = [];
let isExtracting = false;

const statusEl = document.getElementById('status');
const playerCountEl = document.getElementById('playerCount');
const extractBtn = document.getElementById('extractBtn');
const extractAllBtn = document.getElementById('extractAllBtn');
const downloadBtn = document.getElementById('downloadBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

// Position tabs to extract: Offense, Kickers, Defense
const POSITION_TABS = [
  { id: 'posO', name: 'Offense', selector: '#posO a' },
  { id: 'pos7', name: 'Kickers', selector: '#pos7 a' },
  { id: 'pos8', name: 'Defense', selector: '#pos8 a' }
];

function setStatus(message, type = '') {
  statusEl.textContent = message;
  statusEl.className = 'status ' + type;
}

function updatePlayerCount() {
  playerCountEl.textContent = allPlayers.length;
  downloadBtn.disabled = allPlayers.length === 0;
}

function showProgress(show) {
  progressContainer.style.display = show ? 'block' : 'none';
}

function updateProgress(text, percent) {
  progressFill.style.width = percent + '%';
  progressText.textContent = text;
}

async function injectContentScript(tabId) {
  try {
    await chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['content.js']
    });
    return true;
  } catch (e) {
    console.error('Failed to inject content script:', e);
    return false;
  }
}

async function extractFromCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab.url.includes('fantasy.nfl.com')) {
    setStatus('Please navigate to fantasy.nfl.com', 'error');
    return null;
  }

  // Inject content script
  await injectContentScript(tab.id);

  // Small delay to ensure script is loaded
  await new Promise(resolve => setTimeout(resolve, 100));

  return new Promise((resolve) => {
    chrome.tabs.sendMessage(tab.id, { action: 'extractPlayers' }, (response) => {
      if (chrome.runtime.lastError) {
        setStatus('Error: Could not access page. Try refreshing.', 'error');
        resolve(null);
        return;
      }
      resolve(response);
    });
  });
}

async function navigateToNextPage(tabId) {
  return new Promise((resolve) => {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      func: () => {
        const nextLink = document.querySelector('.next a');
        if (nextLink) {
          nextLink.click();
          return true;
        }
        return false;
      }
    }, (results) => {
      resolve(results && results[0] && results[0].result);
    });
  });
}

async function navigateToPositionTab(tabId, selector) {
  return new Promise((resolve) => {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      func: (sel) => {
        const link = document.querySelector(sel);
        if (link) {
          link.click();
          return true;
        }
        return false;
      },
      args: [selector]
    }, (results) => {
      resolve(results && results[0] && results[0].result);
    });
  });
}

async function waitForPageLoad(tabId, expectedOffset) {
  return new Promise((resolve) => {
    const checkInterval = setInterval(async () => {
      try {
        const results = await chrome.scripting.executeScript({
          target: { tabId: tabId },
          func: () => {
            const paginationTitle = document.querySelector('.paginationTitle');
            if (paginationTitle) {
              const match = paginationTitle.textContent.match(/(\d+)\s*-\s*(\d+)\s*of\s*(\d+)/);
              if (match) {
                return parseInt(match[1]);
              }
            }
            return 1;
          }
        });

        if (results && results[0] && results[0].result >= expectedOffset) {
          clearInterval(checkInterval);
          // Wait a bit more for content to fully load
          setTimeout(resolve, 500);
        }
      } catch (e) {
        // Page might be loading, continue waiting
      }
    }, 300);

    // Timeout after 10 seconds
    setTimeout(() => {
      clearInterval(checkInterval);
      resolve();
    }, 10000);
  });
}

async function waitForTabChange(tabId, positionId) {
  return new Promise((resolve) => {
    const checkInterval = setInterval(async () => {
      try {
        const results = await chrome.scripting.executeScript({
          target: { tabId: tabId },
          func: (posId) => {
            const selectedTab = document.querySelector(`#${posId}.selected`);
            return selectedTab !== null;
          },
          args: [positionId]
        });

        if (results && results[0] && results[0].result) {
          clearInterval(checkInterval);
          // Wait a bit more for content to fully load
          setTimeout(resolve, 800);
        }
      } catch (e) {
        // Page might be loading, continue waiting
      }
    }, 300);

    // Timeout after 10 seconds
    setTimeout(() => {
      clearInterval(checkInterval);
      resolve();
    }, 10000);
  });
}

async function extractAllPagesForCurrentPosition(tabId) {
  const players = [];

  // Get first page
  await injectContentScript(tabId);
  await new Promise(resolve => setTimeout(resolve, 100));

  const firstResponse = await new Promise((resolve) => {
    chrome.tabs.sendMessage(tabId, { action: 'extractPlayers' }, (response) => {
      if (chrome.runtime.lastError) {
        resolve(null);
        return;
      }
      resolve(response);
    });
  });

  if (!firstResponse || !firstResponse.players) {
    return players;
  }

  players.push(...firstResponse.players);

  const totalPlayers = firstResponse.pageInfo.totalPlayers;
  const totalPages = Math.ceil(totalPlayers / 25);

  // Extract remaining pages
  for (let page = 2; page <= totalPages; page++) {
    const navigated = await navigateToNextPage(tabId);
    if (!navigated) break;

    await waitForPageLoad(tabId, (page - 1) * 25 + 1);

    await injectContentScript(tabId);
    await new Promise(resolve => setTimeout(resolve, 100));

    const response = await new Promise((resolve) => {
      chrome.tabs.sendMessage(tabId, { action: 'extractPlayers' }, (response) => {
        if (chrome.runtime.lastError) {
          resolve(null);
          return;
        }
        resolve(response);
      });
    });

    if (response && response.players) {
      players.push(...response.players);
    }
  }

  return players;
}

extractBtn.addEventListener('click', async () => {
  if (isExtracting) return;

  isExtracting = true;
  extractBtn.disabled = true;
  extractAllBtn.disabled = true;

  setStatus('Extracting players...');
  allPlayers = [];
  updatePlayerCount();

  const response = await extractFromCurrentTab();

  if (response && response.players) {
    allPlayers = response.players;
    updatePlayerCount();
    setStatus(`Extracted ${allPlayers.length} players from current page`, 'success');
  }

  isExtracting = false;
  extractBtn.disabled = false;
  extractAllBtn.disabled = false;
});

extractAllBtn.addEventListener('click', async () => {
  if (isExtracting) return;

  isExtracting = true;
  extractBtn.disabled = true;
  extractAllBtn.disabled = true;

  allPlayers = [];
  updatePlayerCount();

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab.url.includes('fantasy.nfl.com')) {
    setStatus('Please navigate to fantasy.nfl.com', 'error');
    isExtracting = false;
    extractBtn.disabled = false;
    extractAllBtn.disabled = false;
    return;
  }

  showProgress(true);

  // Extract from each position tab (Offense, Kickers, Defense)
  for (let i = 0; i < POSITION_TABS.length; i++) {
    const posTab = POSITION_TABS[i];
    const progressPercent = Math.round(((i) / POSITION_TABS.length) * 100);

    updateProgress(`Extracting ${posTab.name}...`, progressPercent);
    setStatus(`Extracting ${posTab.name}...`);

    // Navigate to the position tab
    const navigated = await navigateToPositionTab(tab.id, posTab.selector);
    if (!navigated) {
      console.error(`Failed to navigate to ${posTab.name} tab`);
      continue;
    }

    // Wait for tab to change
    await waitForTabChange(tab.id, posTab.id);

    // Extract all pages for this position
    const players = await extractAllPagesForCurrentPosition(tab.id);
    allPlayers.push(...players);
    updatePlayerCount();

    updateProgress(`Extracted ${posTab.name}: ${players.length} players`,
                   Math.round(((i + 1) / POSITION_TABS.length) * 100));
  }

  showProgress(false);
  setStatus(`Extracted ${allPlayers.length} total players (Offense + K + DEF)`, 'success');

  isExtracting = false;
  extractBtn.disabled = false;
  extractAllBtn.disabled = false;
});

downloadBtn.addEventListener('click', () => {
  if (allPlayers.length === 0) return;

  // Format as CSV
  const csvContent = allPlayers.map(p => `${p.playerString},${p.owner}`).join('\n');

  // Create and download file
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'drafted_data.csv';
  a.click();
  URL.revokeObjectURL(url);

  setStatus('Downloaded drafted_data.csv', 'success');
});

// Check if we're on the right page when popup opens
(async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.url) {
    if (!tab.url.includes('fantasy.nfl.com')) {
      setStatus('Navigate to fantasy.nfl.com to use this extension', 'error');
      extractBtn.disabled = true;
      extractAllBtn.disabled = true;
    } else if (tab.url.includes('/players')) {
      setStatus('Ready - on Players page');
    } else {
      setStatus('Navigate to Players list for best results');
    }
  }
})();
