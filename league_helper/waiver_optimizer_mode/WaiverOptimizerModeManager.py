

from pathlib import Path
from waiver_optimizer_mode.WaiverOptimizerConfigManager import WaiverOptimizerConfigManager

class WaiverOptimizerModeManager:

    def __init__(self, config_folder : Path):
        self.config = WaiverOptimizerConfigManager(config_folder)