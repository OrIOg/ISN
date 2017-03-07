import configparser
from pathlib import Path


def is_bool(var):
	if isinstance(var, bool):
		if var in [0, 1]:
			return bool
	return False


class Config(object):
	"""
		Manage the configuration of the game.
	"""
	# CONSTANTS
	VIDEO = 'VIDEO'
	RESOLUTION = 'RESOLUTION'
	FULLSCREEN = 'FULLSCREEN'

	AUDIO = 'AUDIO'
	VOLUME = 'VOLUME'

	CUSTOM = 'CUSTOM'
	NAME = 'NAME'

	PATH = 'Settings.ini'

	def __init__(self):
		"""
			Reading settings from file. If doesn't exist, create the default
			file.
		"""
		file = Path(Config.PATH)
		self.__settings = {}
		self.__default_ini = \
			{
				Config.VIDEO:
					{
						Config.RESOLUTION: (1280, 720),
						Config.FULLSCREEN: False
					},
				Config.AUDIO:
					{
						Config.VOLUME: 100
					},
				Config.CUSTOM:
					{
						Config.NAME: 'Örlog'
					}
			}
		self.__config = configparser.ConfigParser()
		if not file.is_file(): self.write_default_config()
		self.__settings = self.read_config()
		self.__default_settings = self.read_config(True)

	def get(self, setting):
		if setting in self.__settings.keys():
			return self.__settings[setting]
		elif setting in self.__default_settings.keys():
			return self.__default_settings[setting]
		else:
			raise NameError(
				'No settings named "{}", please tell it to the stupid thing '
				'who made this shit'.format(setting))

	def set(self, setting, value):
		if setting in self.__settings.keys():
			if type(self.__settings[setting]) == is_bool(value):
				self.__settings[setting] = value
			elif isinstance(self.__settings[setting], type(value)):
				self.__settings[setting] = value
			else:
				raise NameError(
					"The type of the new value({}) "
					"isn't equal to the one alreadyest({})"
						.format(type(self.__settings[setting]), type(value)))
		else:
			raise NameError(
				'No settings named "{}", please tell it to the stupid thing '
				'who made this shit'.format(setting))

	def read_config(self, default=False):
		self.__config.read_dict(self.__default_ini)
		if not default: self.__config.read(Config.PATH)

		local_settings = {}

		# Video
		local_settings[Config.RESOLUTION] = tuple(map(int, self.__config.get(
			Config.VIDEO, Config.RESOLUTION)[1:-1].split(',')))
		local_settings[Config.FULLSCREEN] = self.__config.getboolean(
			Config.VIDEO, Config.FULLSCREEN)

		# Audio
		local_settings[Config.VOLUME] = self.__config.getint(
			Config.AUDIO, Config.VOLUME)

		# Custom
		local_settings[Config.NAME] = self.__config.get(
			Config.CUSTOM, Config.NAME)

		return local_settings

	def write_default_config(self):
		self.__config.read_dict(self.__default_ini)
		with open(Config.PATH, 'w') as configfile:
			self.__config.write(configfile)
		print('Default config writed')

	def write_config(self):
		new_config = dict(self.__default_ini)
		new_config[Config.VIDEO][Config.RESOLUTION] = self.__settings[
			Config.RESOLUTION]
		new_config[Config.VIDEO][Config.FULLSCREEN] = self.__settings[
			Config.FULLSCREEN]
		new_config[Config.AUDIO][Config.VOLUME] = self.__settings[
			Config.VOLUME]
		new_config[Config.CUSTOM][Config.NAME] = self.__settings[Config.NAME]
		parser = configparser.ConfigParser()
		parser.read_dict(new_config)
		with open(Config.PATH, 'w') as configfile:
			parser.write(configfile)
