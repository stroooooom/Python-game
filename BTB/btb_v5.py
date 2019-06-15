import pygame
from pygame import Surface
from random import choice
from os import path

sounds_dir = path.join(path.dirname(__file__), 'sounds')

#MENU EVENTS
buttonStartPressed = pygame.event.Event(pygame.USEREVENT + 1)
buttonExitPressed = pygame.event.Event(pygame.USEREVENT + 2)
#PLAY EVENTS
rightAnswerGiven = pygame.event.Event(pygame.USEREVENT + 3)
wrongAnswerGiven = pygame.event.Event(pygame.USEREVENT + 4)
countdown_event_id = pygame.USEREVENT + 5
buttonOkPressed = pygame.event.Event(pygame.USEREVENT + 6)

special_colors = {
	'white': (255, 255, 255)
}

colors = {
	'black': (0, 0, 0),
	'red': (244, 65, 65),
	'pink': (244, 66, 131),
	'purple': (214, 65, 244),
	'blue': (65, 76, 244),
	'cyan': (65, 229, 244),
	'yellow': (255, 231, 17),
	'green': (7, 175, 26),
	'brown': (175, 81, 8),
	'orange': (255, 140, 33)
}

def left_click():
	if pygame.mouse.get_pressed()[0] == 1:
		coord = pygame.mouse.get_pos()
		return coord[0], coord[1]

class Level:
	def __init__(self, numberOfCubes = 4):
		self.numberOfCubes = numberOfCubes
		self.color_names = []
		for key in colors:
			self.color_names.append(key)

	def generate(self):
		unselectedColors = self.color_names.copy()
		pickedColors = []
		for i in range(self.numberOfCubes):
			color = choice(unselectedColors)
			pickedColors += [color]
			unselectedColors.remove(color)
		return pickedColors

class Play:
	def __init__(self, gameWindow):
		self.parent = gameWindow

		self.width = 800
		self.height = 600

		self.button_width = 400
		self.button_height = 100

		self.msPerStep = 500
		self.numberOfCubes = 4
		self.points = 0

		font_name = pygame.font.match_font('comicsansms')
		self.font = pygame.font.SysFont(font_name, 200)

		font_name = pygame.font.match_font('Copperplate')
		self.font2 = pygame.font.SysFont(font_name, 100)

	def resetScore(self):
		self.msPerStep = 500
		self.points = 0

	def load(self):
		self.level = Level(self.numberOfCubes)
		self.current_time = 5
		self.text = None
		self.timer = None
		self.cubes = []
		if self.numberOfCubes == 4:
			self.size = 100
			self.offset = 100
			self.delta = 65
		elif self.numberOfCubes == 5:
			self.size = 60
			self.offset = 150
			self.delta = 50
		elif self.numberOfCubes == 6:
			self.size = 50
			self.offset = 125
			self.delta = 50
		elif self.numberOfCubes == 7:
			self.size = 50
			self.offset = 75
			self.delta = 50

		for i in range(self.numberOfCubes):
			self.cubes += [Surface((self.size, self.size))]

		self.nextLevel()

	def nextLevel(self):
		self.current_time = 5

		if self.text:
			rect = self.text.get_rect()
			surf = Surface(rect.size)
			surf.fill(special_colors['white'])

			self.parent.surface.blit(surf,
			(0.5*(self.width - self.text.get_width()), 
			0.3*(self.height - self.text.get_height())))

		self.cubes_rect = []
		picked_colors = self.level.generate()
		self.word = choice(picked_colors) # (рандомно) выбирается слово
		color = colors[choice(picked_colors)] # выбирается цвет слова

		self.text = self.font.render(self.word, True, color)
		self.parent.surface.blit(self.text,
			(0.5*(self.width - self.text.get_width()), 
			0.3*(self.height - self.text.get_height())))

		for i in range(self.numberOfCubes):
			self.cubes[i].fill(colors[picked_colors[i]])
			self.cubes_rect += [self.parent.surface.blit(self.cubes[i],
				(self.offset + (self.size+self.delta)*i, 400))]
			if picked_colors[i] == self.word:
				self.rightCubeID = i # квадрат того цвета, которое обозначает слово

		self.updateTimer()
		pygame.mouse.set_pos((self.width/2, self.height/2))

	def updateTimer(self):
		if self.timer:
			rect = self.timer.get_rect()
			surf = Surface(rect.size)
			surf.fill(special_colors['white'])
			self.parent.surface.blit(surf, (0.5*(self.width - self.timer.get_width()), 50))

		self.timer = self.font2.render(str(self.current_time), True, colors['black'])
		self.parent.surface.blit(self.timer, (0.5*(self.width - self.timer.get_width()), 50))
		pygame.time.set_timer(countdown_event_id, self.msPerStep)

	def checkCubes(self):
		click = left_click()
		if click != None:
			for i in range(self.numberOfCubes):
				if self.cubes_rect[i].collidepoint(click):
					if i == self.rightCubeID:
						pygame.event.post(rightAnswerGiven)
					else:
						pygame.event.post(wrongAnswerGiven)

	def showScore(self):
		self.text = self.font.render("Your score:", True, colors['black'])
		self.score = self.font.render(str(self.points), True, colors['black'])
		self.parent.surface.blit(self.text, (0.5*(self.width - self.text.get_width()), 50))
		self.parent.surface.blit(self.score, (0.5*(self.width - self.score.get_width()), 200))

		self.button_ok = Surface((self.button_width, self.button_height))
		self.button_ok.fill(colors['purple'])

		button_ok_text = self.font.render("Good", True, colors['yellow'])

		self.button_ok.blit(button_ok_text, 
			(0.5*(self.button_width - button_ok_text.get_width()), 
			0.5*(self.button_height - button_ok_text.get_height())))

		self.button_ok_rect = self.parent.surface.blit(self.button_ok, (200, 400))
		pygame.mouse.set_pos((self.width/2, self.height/2))

	def cleanScore(self):
		rect = self.text.get_rect()
		surf = Surface(rect.size)
		surf.fill(special_colors['white'])
		self.parent.surface.blit(surf, (0.5*(self.width - self.text.get_width()), 50))

		rect = self.score.get_rect()
		surf = Surface(rect.size)
		surf.fill(special_colors['white'])
		self.parent.surface.blit(surf, (0.5*(self.width - self.score.get_width()), 400))

	def checkOkButton(self):
		click = left_click()
		if click != None:
			if self.button_ok_rect.collidepoint(click):
				pygame.event.post(buttonOkPressed)


class Menu:
	def __init__(self, gameWindow):
		self.parent = gameWindow

		self.width = 800
		self.height = 600

		self.button_width = 400
		self.button_height = 100

		self.createButtons()

	def createButtons(self):
		self.button_start = Surface((self.button_width, self.button_height))
		self.button_exit = Surface((self.button_width, self.button_height))
		self.button_start.fill(colors['purple'])
		self.button_exit.fill(colors['purple'])

		self.font = pygame.font.SysFont("comicsansms", 80)

		button_start_text = self.font.render("Start", True, colors['yellow']) 
		button_exit_text = self.font.render("Exit", True, colors['yellow'])

		self.button_start.blit(button_start_text, 
			(0.5*(self.button_width - button_start_text.get_width()), 
			0.5*(self.button_height - button_start_text.get_height())))
		self.button_exit.blit(button_exit_text, 
			(0.5*(self.button_width - button_exit_text.get_width()), 
			0.5*(self.button_height - button_exit_text.get_height())))

	def blit(self):
		self.button_start_rect = self.parent.surface.blit(self.button_start, (200, 100))
		self.button_exit_rect = self.parent.surface.blit(self.button_exit, (200, 300))

	def checkButtons(self):
		if left_click() != None:
			if self.button_start_rect.collidepoint(left_click()):
				pygame.event.post(buttonStartPressed)
			if self.button_exit_rect.collidepoint(left_click()):
				pygame.event.post(buttonExitPressed)

class GameWindow:
	def __init__(self):
		self.state = 'Menu'
		self.width = 800
		self.height = 600

		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		self.surface = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
		self.surface.fill(special_colors['white'])

		self.rightAnswerSounds = []
		for sound in ['rightAnswer1.wav', 'rightAnswer3.wav']:
			self.rightAnswerSounds.append(pygame.mixer.Sound(path.join(sounds_dir, sound)))
		self.wrongAnswerSound = pygame.mixer.Sound(path.join(sounds_dir, 'wrongAnswer.wav'))
		self.menuMusic = pygame.mixer.Sound(path.join(sounds_dir, 'menu.wav'))
		pygame.mixer.music.load(path.join(sounds_dir, 'background.wav'))
		pygame.mixer.music.set_volume(0.05)
		self.menuMusicChannel = pygame.mixer.Channel(0)

		pygame.display.set_caption('Game')
		pygame.display.update()

		self.play = Play(self)
		self.menu = Menu(self)
		self.menu.blit()
		self.menuMusicChannel.play(self.menuMusic, loops = -1, fade_ms = 5)

		self.updateWindow()

	def updateWindow(self):
		pygame.display.update()

	def clear(self):
		self.surface.fill(special_colors['white'])

	def handleMenuEvents(self):
		self.menu.checkButtons()

		for event in pygame.event.get():
			if event == buttonStartPressed:
				self.clear()
				self.state = 'Play'
				self.play.numberOfCubes = 4
				self.play.load()
				self.updateWindow()
				self.menuMusicChannel.pause()
				pygame.mixer.music.play()
			elif event == buttonExitPressed:
				self.wrongAnswerSound.play()
				pygame.time.delay(500)
				exit()

	def goToScore(self):
		self.waitCountdown()
		self.clear()
		self.state = 'Score'
		self.play.showScore()

	def returnToMenu(self):
		self.play.resetScore()
		self.play.cleanScore()
		self.clear()
		pygame.mixer.music.stop()
		self.state = 'Menu'
		self.menu.blit()
		pygame.mouse.set_pos((self.width/2, 250))
		self.menuMusicChannel.unpause()

	def waitCountdown(self):
		while True:
			if not pygame.event.peek(countdown_event_id):
				break
			for event in pygame.event.get():
				if event.type == countdown_event_id:
					break

	def handlePlayEvents(self):
		self.play.checkCubes()

		for event in pygame.event.get():
			if event == rightAnswerGiven:
				if self.play.points > 0:
					self.waitCountdown()
				self.play.points += 1
				if self.play.points < 5:
					self.play.nextLevel()
				elif self.play.points < 10:
					if self.play.numberOfCubes == 5:
						self.play.nextLevel()
					else:
						self.clear()
						self.play.numberOfCubes = 5
						self.play.load()
				elif self.play.points < 20:
					if self.play.numberOfCubes == 6:
						self.play.nextLevel()
					else:
						self.clear()
						self.play.numberOfCubes = 6
						self.play.load()
				else:
					if self.play.numberOfCubes == 7:
						self.play.nextLevel()
					else:
						self.clear()
						self.play.numberOfCubes = 7
						self.play.load()
				self.play.msPerStep -= 10
				choice(self.rightAnswerSounds).play()
			elif event == wrongAnswerGiven:
				self.wrongAnswerSound.play()
				self.goToScore()
			elif event.type == countdown_event_id:
				if self.play.current_time > 1:
					self.play.current_time -= 1
					pygame.time.set_timer(countdown_event_id, self.play.msPerStep)
					self.play.updateTimer()
				else:
					self.wrongAnswerSound.play()
					self.goToScore()

			self.updateWindow()

	def handleScoreEvents(self):
		self.play.checkOkButton()

		for event in pygame.event.get():
			if event == buttonOkPressed:
				self.returnToMenu()
				self.updateWindow()

	def hande_events(self):
		while 1:
			if self.state == 'Menu': self.handleMenuEvents()
			if self.state == 'Play': self.handlePlayEvents()
			if self.state == 'Score': self.handleScoreEvents()
			if pygame.event.get(pygame.QUIT):
				self.wrongAnswerSound.play()
				exit()

gw = GameWindow()
gw.hande_events()
