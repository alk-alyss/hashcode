class Project:
	def __init__(self, name, duration, score, end, roles):
		self.name = name
		self.duration = duration
		self.score = score
		self.end = end
		self.roles = roles
		self.contributors = []

	def __str__(self):
		return str(self.name)+" "+str(self.duration)+" "+str(self.score)+" "+str(self.end)+" "+str(self.roles)

class Contributor:
	def __init__(self, name, skills):
		self.name = name
		self.skills = skills # dictionary: key=skill, value=level
		self.working = False

	def check_project(self, project: Project) -> bool:
		for i in project.roles.keys():
			if i in self.skills.keys():
				if self.skills[i] >= project.roles[i]:
					return i
		return False

	def __str__(self):
		return str(self.name)+" "+str(self.skills)

def readInput(filename):
	contributors = []
	projects = []
	with open(filename, "r") as f:
		c, p = f.readline().split()
		for x in range(int(c)):
			name, n = f.readline().split()
			skills = {}
			for y in range(int(n)):
				skill, level = f.readline().split()
				skills.update({skill : level})
			
			contributors.append(Contributor(name, skills))

		for x in range(int(p)):
			name, d, s, e, r = f.readline().split()
			roles = {}
			for y in range(int(r)):
				role, level = f.readline().split()
				roles.update({role : level})
			
			projects.append(Project(name, d, s, e, roles))
	
	return contributors, projects

contributors, projects = readInput("a_an_example.in.txt")
for c in contributors:
	print(c)
for p in projects:
	print(p)