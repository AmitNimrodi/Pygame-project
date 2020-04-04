from plane import Plane
from parachutist import Parachutist
from player import Player
from score_record import ScoreRecord
import random
from constants import *
import pygame
from world import Background,Sea


#This class is in charge of managing the game:
#  the player state, plane state, parachutists state, scoreRecord state
class GameManager:
	parachutists = pygame.sprite.Group()
	all_sprites = pygame.sprite.Group()

	def __init__(self):
		self.top_scores = [ScoreRecord() for x in range(1,TOP_SCORES_LIST_LENGTH+1)]
		self.background = Background()
		self.sea = Sea()
		self.player = Player()
		self.plane = Plane()
		self.all_sprites.add(self.background)
		self.all_sprites.add(self.sea)
		self.all_sprites.add(self.player)
		self.all_sprites.add(self.plane)
		self.running = False
		pygame.mixer.init()
		pygame.mixer.music.load("resources\\backgroundMusic.mp3") 		  #Background music for the game
		pygame.mixer.music.play(loops=-1) #Run forever (or until game is closed)
		self.drop_parachutist_sound = pygame.mixer.Sound("resources\Airstrike.ogg")
		self.collision_sound = pygame.mixer.Sound("resources\collisionSound.ogg")
		self.miss_parachutist_sound = pygame.mixer.Sound("resources\Splash.ogg")
		self.drop_parachutist_sound.set_volume(LOW_VOLUME)
		self.collision_sound.set_volume(LOW_VOLUME)

	def get_parachutists(self):
		return self.parachutists

	#Deletes all parachutists (used at the end of the game to restart)
	def kill_parachutists(self):
		for parachutist in self.parachutists:
			parachutist.kill()

	#Draw whether a parachutist will drop or not
	def draw_parachutist(self):
		if (random.random()<PROBABILITY):
			new_para = self._drop_parachutist()
			self.parachutists.add(new_para)
			self.all_sprites.add(new_para)

	def _drop_parachutist(self):
		self.drop_parachutist_sound.play()
		return Parachutist(self.plane.get_horizontal_pos())

	#Update all parachutists positions and checks for collisions
	def update_paras_and_detect_collisions(self):
		self.parachutists.update()
		for parachutist in self.parachutists:
			if self.player.rect.colliderect(parachutist.rect):
				self.player.increase_score()
				self.collision_sound.play()
				parachutist.kill()
			elif parachutist.get_height() == SEA_LEVEL:
				parachutist.kill()
				self.miss_parachutist_sound.play()
				if not self.player.decrease_life_and_get() > 0:
					return False
		return True

	def stringify_score_record(self, record):
		name = record.get_name()
		score = record.get_score()
		return name + ": " + str(score)

	#Assumption: no parachutist in the list is at height 0
	def decrease_parachutists_level(self):
		player_left_end, player_right_end = self.player.get_pos()
		for parachutist in self.parachutists[:]:
			curr_parachutist_height = parachutist.decrease_height_and_get()
			curr_parachutist_x = parachutist.get_horizontal_pos()
			if curr_parachutist_height == SEA_LEVEL:
				self.parachutists.remove(parachutist)
				parachutist.kill()
				if player_left_end <= curr_parachutist_x <= player_right_end:
					self.player.increase_score()
				elif not self.player.decrease_life_and_get() > 0:
					return False
		return True

	def get_plane_char_and_pos(self):
		char, pos = self.plane.get_character_and_position()
		return char, pos

	def get_player_char_and_pos(self):
		char, pos = self.player.get_character_and_position()
		return char, pos

	def get_para_char_and_pos(self,para):
		char, pos = para.get_character_and_position()
		return char, pos

	def plane_is_in_screen_predicate(self):
		return 800 > self.plane.get_horizontal_pos()>0

	def move_player(self, pressed_keys):
		self.player.update_state(pressed_keys)

	def move_plane(self):
		self.plane.update_state()

	#Adds new top-10 highscore to the list
	def arrange_top_scores_list(self, player_score_record):
		for i in range(0, TOP_SCORES_LIST_LENGTH):
			curr_score_record = self.top_scores[i]
			if curr_score_record.get_score() > player_score_record.get_score():
				continue
			else:
				self.top_scores.remove(self.top_scores[TOP_SCORES_LIST_LENGTH-1])
				self.top_scores.insert(i, player_score_record)
				break

	def arrange_score(self):
		score_string = SCORE_DISPLAY_PREFIX_STRING + str(self.player.get_score())
		if self.player.get_score() >= self.top_scores[TOP_SCORES_LIST_LENGTH-1].get_score():
			player_score_record = ScoreRecord(self.player.get_score(), self.player.get_name())
			self.arrange_top_scores_list(player_score_record)
		return score_string



