from os.path import isfile

class SettingsParser():
    def __init__(self, settingsFile=''):
        self._settings = {}
        self._configFile = settingsFile
        self._init_settings()

    def _init_settings(self):
        pass

    def __getattr__(self, attr):
        return self._settings[attr]
    
    def __readSettingsFile():
        
        pass


class SettingsParserError(Exception):
    pass