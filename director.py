import pygame

import Scenes
from configuration import Config


class Director(object):
	"""
		The Director manage the updates, the draws and events of the game.
	"""

	def __init__(self):
		self.config = Config()
		self.__running = True
		import os
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		self.__screen = pygame.display.set_mode(
			self.config.get(self.config.RESOLUTION))
		if self.config.get(self.config.FULLSCREEN):
			self.toggle_fullscreen()
		pygame.display.set_caption("ISN Project")
		self.__clock = pygame.time.Clock()
		self.__dtime = 0
		self.__scene = Scenes.test_scene.SceneTest(self)

	def get_screen(self):
		return self.__screen

	def toggle_fullscreen(self):
		flags = self.__screen.get_flags()
		if flags & pygame.FULLSCREEN is False:
			flags |= pygame.FULLSCREEN
			pygame.display.set_mode(self.config.get(self.config.RESOLUTION),
			                        flags)
		else:
			flags ^= pygame.FULLSCREEN
			pygame.display.set_mode(self.config.get(self.config.RESOLUTION),
			                        flags)
		self.config.set(Config.FULLSCREEN, (flags & pygame.FULLSCREEN) is
		                not 0)

	def mainloop(self):
		while self.__running:
			self.__dtime = self.__clock.tick() / 1000
			# events
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.quit()
				if event.type == pygame.KEYDOWN:
					# key = event.dict['unicode'].encode()
					key = event.unicode
					keye = key.encode()
					if keye == b'\x1b':
						self.quit()
					elif pygame.key.get_mods() & pygame.KMOD_ALT and keye == \
							b'\r':
						self.toggle_fullscreen()

			# Detect events
			self.__scene.on_event(events, self.__dtime)

			# Update scene
			self.__scene.on_update(self.__dtime)

			# Draw the screen
			self.__scene.on_draw(self.__screen)
			pygame.display.update()

	def quit(self):
		self.config.write_config()
		self.__running = False
