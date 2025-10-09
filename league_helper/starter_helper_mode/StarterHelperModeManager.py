

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from util.ConfigManager import ConfigManager

class StarterHelperModeManager:

    def __init__(self, config: ConfigManager):
        self.config = config