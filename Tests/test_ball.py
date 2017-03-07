import pygame


class TestBall(object):
	"""
		A ball with "simple" aerodynamics concept.
	"""
	import os
	filename = os.path.join(os.getcwd(), 'Resources', 'images', 'doge.png')
	image = pygame.image.load(filename)

	del os

	def __init__(self, director):
		self._director = director
		import colorsys
		import random
		self.__color = tuple(
			int(i * 255) for i in colorsys.hsv_to_rgb(random.random(), 1, 1))

		self.__surf = TestBall.image.convert_alpha()
		self.__surf.fill(self.__color, None, pygame.BLEND_RGB_MULT)
		self.__size = self.__surf.get_size()

		surf = self._director.get_screen().get_rect()
		self.__acceleration = [200 * random.random(), 200 * random.random()]
		self.__real_x = random.randrange(0, surf.width - self.__size[0])
		self.__real_y = random.randrange(0, surf.height - self.__size[1])

	def top(self):
		return self.__real_y

	def bottom(self):
		return self.__real_y + self.__size[1]

	def left(self):
		return self.__real_x

	def right(self):
		return self.__real_x + self.__size[0]

	def check_bound(self, x, y):
		surf = self._director.get_screen().get_rect()

		if (self.top() + y) <= 0 or (self.bottom() + y) >= surf.height:
			self.__acceleration[1] = -self.__acceleration[1]
			self.__real_y -= y
		if (self.left() + x) <= 0 or (self.right() + x) >= surf.width:
			self.__acceleration[0] = -self.__acceleration[0]
			self.__real_x -= x

	def on_update(self, dtime):
		offset_x = self.__acceleration[0] * dtime
		offset_y = self.__acceleration[1] * dtime
		self.check_bound(offset_x, offset_y)
		self.__real_x += offset_x
		self.__real_y += offset_y

	def on_draw(self, screen):
		screen.blit(self.__surf, (int(self.__real_x), int(self.__real_y)))