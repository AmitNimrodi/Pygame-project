from constants import *
import pygame


#This class is data-object class, representing the parachutists
class Parachutist(pygame.sprite.Sprite):

	def __init__(self, horizontal_pos):
		super(Parachutist,self).__init__()
		self.character = pygame.image.load("resources\parachutist.png").convert_alpha()
		self.character.set_colorkey(WHITE,pygame.locals.RLEACCEL)
		self.rect = self.character.get_rect(
			center=(
				horizontal_pos, SKY_LEVEL+50
			)
		)

	def update(self):
		self.decrease_height()

	def get_character_and_position(self):
		return self.character, self.rect

	def decrease_height(self):
		self.rect.move_ip(0, 1)
		return self.get_height()

	def decrease_height_and_get(self):
		self.decrease_height()
		return self.get_height()

	def get_height(self):
		return self.rect.y

	def get_horizontal_pos(self):
		return self.rect.x
