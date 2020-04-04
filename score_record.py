from constants import *

class ScoreRecord():

	def __init__(self, score=STARTING_SCORE, name="Very bad player"):
		self.score = score
		self.name = name

	def get_name(self):
		return self.name

	def get_score(self):
		return self.score

	def increase_score(self):
		self.score += SCORE_BONUS

	def set_name(self, name):
		self.name = name

	def reset(self):
		self.score = STARTING_SCORE