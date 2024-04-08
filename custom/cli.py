import logging
import os

from legendary.cli import LegendaryCLI as LegendaryCLI_old
from legendary.core import LegendaryCore


class LegendaryCLI(LegendaryCLI_old):
    def __init__(self, api_timeout=10):
        self._path = os.path.join(os.getcwd(), 'legendary')
        self.core = LegendaryCore(os.path.join(self._path, 'config.ini'), timeout=api_timeout)
        self.logger = logging.getLogger('cli')
        self.logging_queue = None

    def list_installed(self, *args, **kwargs):
        message = ''
        # logger.info('Logging in to check for updates...')
        try:
            if not self.core.login():
                message = '[ERROR] Login failed! Not checking for updates.'
                # logger.error('Login failed! Not checking for updates.')
            else:
                # Update assets for all platforms currently installed
                for app_platform in self.core.get_installed_platforms():
                    self.core.get_assets(True, platform=app_platform)
        except ValueError as e:
            if e.args and e.args[0] == 'No saved credentials':
                print()
                return {'data': [], 'message': 'No saved credentials'}

        games = sorted(self.core.get_installed_list(include_dlc=True),
                       key=lambda x: x.title.lower())

        versions = dict()
        for game in games:
            try:
                versions[game.app_name] = self.core.get_asset(game.app_name, platform=game.platform).build_version
            except ValueError:
                if message:
                    message += '\n'
                message += f'[ERROR] Metadata for "{game.app_name}" is missing, the game may have been removed from ' \
                           'your account or not be in legendary\'s database yet.'

        return {'data': [vars(g) for g in games], 'message': message}
