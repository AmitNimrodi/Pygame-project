from constants import *
import pygame

#This class is data-object class, representing the plane
class Plane(pygame.sprite.Sprite):

	def __init__(self):
		super(Plane, self).__init__()
		self.character = pygame.image.load("resources\plane.png").convert_alpha()
		self.character.set_colorkey(WHITE, pygame.locals.RLEACCEL)
		self.rect = self.character.get_rect(
						center=(SCREEN_WIDTH-PLANE_WIDTH/2, SKY_LEVEL)
		)

	#State setter with validation
	def update_state(self):
		self.rect.move_ip(-1,0)
		if self.rect.right<0:
			self.respawn()

	#State setter
	def respawn(self):
		self.rect.left=SCREEN_WIDTH

	#State setter
	def reset(self):
		self.rect = self.character.get_rect(
						center=(SCREEN_WIDTH-PLANE_WIDTH/2, SKY_LEVEL)
		)

	def get_horizontal_pos(self):
		return self.rect.x

	def get_character_and_position(self):
		return self.character, self.rect




