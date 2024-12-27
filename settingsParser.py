from os import getcwd
from os.path import isfile
import os
import re



class SettingsParser():
    def __init__(self, settingsFile='http_server.config', check=False):
        self._settings = {}
        self.__check = check
        self.__settingsFile = settingsFile
        self._init_settings()
        self.__loadSettingsFile()

    def _init_settings(self):
        # OVERRIDE THIS METHOD

        # int setting
        #self._settings['setting1'] = 222222

        # float setting

        #self._settings['setting2'] = 33333.44
        # string setting

        #self._settings['setting3'] = 'abcde'
        # bool setting

        #self._settings['setting4'] = true | false
        # Tuple setting

        #self._settings['setting5'] = ('key', 'abcde')
        # List setting

        #self._settings['setting6'] = [('key1', 555555), ('key2', 'xxxxxx')]
        pass

    def __getattr__(self, attr):
        return self._settings[attr]
    
    def __loadSettingsFile(self):
        filePath = None
        
        if isfile(self.__settingsFile):
            filePath = self.__settingsFile
        elif isfile(self.__settingsFile):
            filePath = os.getcwd() + '/http_server.config'
        
        if filePath:
            with open(filePath, 'r', encoding='utf-8') as fd:
                settings = fd.readlines()

            self.__parseSettings(settings)

    def __parseSettings(self, settings):
        line_number = 1
        for line in settings:
            line = line.strip('\n').strip()

            if not len(line) or line[0] == '#':
                line_number += 1
                continue

            line = re.sub('#+.*', '', line)

            if line.find('=') < 0:
                raise SettingsParserError(f"Settings parser error: line {line_number}, unrecognized setting.")

            line = line.lower()
            setting, value = line.split('=', 1)
            if len(value) == 0:
                raise SettingsParserError(f"Settings parser error: line {line_number}, no value found for '{setting}'.")

            setting, value = setting.strip(), value.strip()
            if not setting in self._settings:
                raise SettingsParserError(f"Settings parser error: line {line_number}, config '{setting}' not valid.")

            defaultSettingType = type(self._settings[setting])
            newValue = self.__getLoadedSetting( value, defaultSettingType )
            
            if not self.__check:
                if defaultSettingType.__name__ == 'list':
                    self._settings[setting].append(newValue)
                else:
                    self._settings[setting] = newValue
            else:
                print(setting, '=', newValue)

            line_number += 1

        if self.__check:
            print(f'\nSettings file is valid: {self.__settingsFile}')

    def __getLoadedSetting(self, value, defaultSettingType):
        defaultSettingType = defaultSettingType.__name__

        if defaultSettingType == 'tuple' or defaultSettingType == 'list':
            if value == '()':
                return tuple()
            
            value = value.replace(' ', ',', 1)
            values = [x.strip() for x in value.split(',')]

            for index, val in enumerate(values):
                if val.isdecimal():
                    values[index] = int(val)
                elif val.replace('.', '', 1).isdigit():
                    values[index] = float(val)
                else:
                    values[index] = val

            value = tuple( filter(None, values) )

        elif defaultSettingType == 'list':
            k, v = value.split(':', 1)
            return (k.strip(), v.strip())

        elif value in ('true', 'false'):
            value = eval( value.capitalize() )

        elif value.isdecimal():
            value = int(value)

        elif value.replace('.','',1).isdigit():
            value = float(value)

        else:
            value = value.strip("'")

        return value
        
            



class SettingsParserError(Exception):
    def __init__(self, message):
        super().__init__(message)



if __name__ == '__main__':
    pass