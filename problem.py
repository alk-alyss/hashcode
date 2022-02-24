class Project:
	def __init__(self, name, duration, score, end, roles):
		self.name = name
		self.duration = duration
		self.score = score
		self.end = end
		self.roles = roles

class Contributor:
	def __init__(self, name, skills):
		self.name = name
		self.skills = skills
