import logging
import os

from legendary.cli import LegendaryCLI as LegendaryCLI_old
from legendary.core import LegendaryCore


class LegendaryCLI(LegendaryCLI_old):
    def __init__(self, override_config=None, api_timeout=10):
        self._path = os.path.join(os.getcwd(), 'legendary')
        self.core = LegendaryCore(os.path.join(self._path, 'config.ini'), timeout=api_timeout)
        self.logger = logging.getLogger('cli')
        self.logging_queue = None
