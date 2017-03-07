import Tests
from Scenes.scene import Scene


class SceneTest(Scene):
	"""
		A Test scene for testing lel ( ͡° ͜ʖ ͡°)
	"""

	def __init__(self, director):
		super().__init__(director)
		self.__balls = [Tests.TestBall(self._director) for i in range(2000)]

	def on_update(self, dtime):
		for ball in self.__balls:
			ball.on_update(dtime)

	def on_event(self, events, dtime):
		pass

	def on_draw(self, screen):
		screen.fill((0, 0, 0))
		for ball in self.__balls:
			ball.on_draw(screen)
