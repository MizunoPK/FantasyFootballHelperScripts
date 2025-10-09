

from pathlib import Path
from starter_helper_mode.StarterHelperConfigManager import StarterHelperConfigManager

class StarterHelperModeManager:

    def __init__(self, config_folder : Path):
        self.config = StarterHelperConfigManager(config_folder)