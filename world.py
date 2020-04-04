from constants import *
import pygame

#This class is in charge of the graphical world the game runs on
class Background(pygame.sprite.Sprite):
	def __init__(self):
		super(Background,self).__init__()
		self.character=pygame.image.load(
			"resources\\background.png").convert_alpha()
		self.character.set_colorkey(WHITE,pygame.locals.RLEACCEL)
		self.rect = self.character.get_rect()


class Sea(pygame.sprite.Sprite):
	def __init__(self):
		super(Sea,self).__init__()
		self.character=pygame.image.load(
			"resources\sea.png").convert_alpha()
		self.character.set_colorkey(WHITE,pygame.locals.RLEACCEL)
		self.rect = self.character.get_rect(
			center=((SCREEN_WIDTH/2, SCREEN_HEIGHT-self.character.get_height()/3)))








