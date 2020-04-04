from score_record import ScoreRecord
from constants import *
import pygame
from pygame import K_LEFT, K_RIGHT


#This class is data-object class, representing the player
class Player(pygame.sprite.Sprite):
	name = ""

	def __init__(self):
		super(Player, self).__init__()
		self.character = pygame.image.load("resources\\boat.png").convert_alpha()
		self.character.set_colorkey(WHITE, pygame.locals.RLEACCEL)
		self.rect = self.character.get_rect(
			center=(SCREEN_WIDTH - BOAT_WIDTH/2, SEA_LEVEL)
		)
		self.lives = STARTING_LIVES
		self.score_record = ScoreRecord()

	def get_pos(self):
		return self.rect.left, self.rect.right

	def get_character_and_position(self):
		return self.character, self.rect

	#State setter with validation
	def update_state(self, pressed_keys):
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-5,0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(5,0)
		if self.rect.left<0:
			self.rect.left = 0
		if self.rect.right> SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH

	def set_name(self, name):
		self.name = name
		self.score_record.set_name(name)

	def get_name(self):
		return self.score_record.get_name()

	def get_score(self):
		return self.score_record.get_score()

	def get_lives(self):
		return self.lives

	#Setter
	def reset(self):
		self.lives = STARTING_LIVES
		self.score_record.reset()

	#Setter and getter
	#Assumption: this func is called when lives>0
	def decrease_life_and_get(self):
		self.lives -= 1
		return self.lives

	#Setter
	def increase_score(self):
		self.score_record.increase_score()

	def get_score_record(self):
		return self.score_record

