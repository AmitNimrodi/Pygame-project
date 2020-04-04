import pygame
from game_manager import GameManager
from constants import *
from pygame.locals import (QUIT, K_BACKSPACE, K_RETURN, RLEACCEL)

#This class is in charge of setting and running the game:
#  That includes setup, run and post-run
class Game():
	running = False
	clock = pygame.time.Clock()

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
		self.screen.fill(WHITE)
		self.game_man = GameManager()

	#Helper function: draw text on screen
	def draw_text(self, str, size, color, x, y):
		font = pygame.font.Font(None, size)
		text_surface = font.render(str, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x,y)
		self.screen.blit(text_surface, text_rect)

	def refresh_display(self):
		for entity in self.game_man.all_sprites:
			self.screen.blit(entity.character, entity.rect)
		self.draw_player_state()
		pygame.display.flip()

	#Draws the high-score table at the end of the game
	def draw_score_list(self,score_list):
		x = SCREEN_WIDTH/2
		y = SCREEN_HEIGHT/3
		self.draw_text(SCORE_LIST_STRING,32,DARK_PURPLE,x, y)
		for line in score_list:
			y+=LINE_HEIGHT
			self.draw_text(line, 20 ,DARK_PURPLE,x, y)

	#Draws the player state while game runs
	def draw_player_state(self):
		self.draw_text(SCORE_STRING + str(self.game_man.player.get_score()),
					   15, BLACK, 2*LINE_HEIGHT, LINE_HEIGHT/2)
		self.draw_text(LIVES_STRING +str(self.game_man.player.get_lives()),
					   15,BLACK, 2*LINE_HEIGHT, LINE_HEIGHT)

	#Restarts the relevant game stats after game end
	def restart_game_stats(self):
		self.game_man.parachutists = pygame.sprite.Group()
		player_name = self.game_man.player.get_name()
		self.game_man.player.reset()
		self.game_man.player.set_name(player_name)
		self.game_man.plane.reset()

	#display post-game screen
	def display_game_over_screen(self, epilogue):
		start_screen_background=pygame.image.load("resources\\openScreenBackground.png").convert_alpha()
		start_screen_background.set_colorkey(WHITE,pygame.locals.RLEACCEL)
		start_screen_background_rect=start_screen_background.get_rect()
		self.screen.blit(start_screen_background,start_screen_background_rect)
		score_string=self.game_man.arrange_score()
		score_list=list(map(self.game_man.stringify_score_record,self.game_man.top_scores))
		self.draw_score_list(score_list)
		self.draw_text(score_string,48,LIGHT_GREEN,SCREEN_WIDTH/2,SCREEN_HEIGHT/7)
		self.draw_text(RESTART_STRING,36,LIGHT_GREEN,SCREEN_WIDTH/2,SCREEN_HEIGHT/4)
		pygame.display.flip()
		self.clock.tick(15) #slower render, waiting for user action
		while epilogue:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					epilogue = False
					self.running = False
					pygame.quit()
				if event.type == pygame.KEYUP:
					epilogue = False
					self.restart_game_stats()
					self.run_game()

	#Draws all text in start screen
	def draw_start_screen_text(self):
		start_screen_background = pygame.image.load("resources\\openScreenBackground.png").convert_alpha()
		start_screen_background.set_colorkey(WHITE,pygame.locals.RLEACCEL)
		start_screen_background_rect = start_screen_background.get_rect()
		self.screen.blit(start_screen_background,start_screen_background_rect)
		self.draw_text(START_SCREEN_STRING,48,WHITE,SCREEN_WIDTH/2,SCREEN_HEIGHT/7)
		self.draw_text(INSTRUCTIONS_STRING,22,WHITE,SCREEN_WIDTH/2,SCREEN_HEIGHT/5)
		self.draw_text(ENTER_NAME_STRING,22,WHITE,SCREEN_WIDTH/2,SCREEN_HEIGHT/4)
		self.draw_text(PRESS_KEY_STRING,22,WHITE,SCREEN_WIDTH/2,SCREEN_HEIGHT/3)

	def display_start_screen(self, prolog):
		self.draw_start_screen_text()
		font = pygame.font.Font(None, 28)
		input_box = pygame.Rect(SCREEN_WIDTH/2-1.5*LINE_HEIGHT,SCREEN_HEIGHT/3-LINE_HEIGHT,100, 26)
		username = ""
		while prolog:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					prolog=False
					self.running=False
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.unicode.isalpha():
						username += event.unicode
					elif event.key == K_BACKSPACE:
						username = username[:-1]
					elif event.key == K_RETURN:
						prolog=False
						self.game_man.player.set_name(username)
			self.draw_start_screen_text()
			username_surface = font.render(username, True, DARK_PURPLE)
			self.screen.blit(username_surface,(input_box.x+5, input_box.y+5))
			pygame.draw.rect(self.screen,DARK_PURPLE,input_box,2)
			pygame.display.flip()
			self.clock.tick(15)

	def run_game(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
			self.game_man.move_player(pygame.key.get_pressed())
			self.game_man.move_plane()
			if self.game_man.plane_is_in_screen_predicate():
				self.game_man.draw_parachutist()
			self.refresh_display()
			if running:
				running = self.game_man.update_paras_and_detect_collisions()
			self.clock.tick(150)
		self.game_man.kill_parachutists()
		self.display_game_over_screen(True)

def run_game():
	game = Game()
	game.display_start_screen(True)
	game.run_game()
	pygame.quit()


run_game()
