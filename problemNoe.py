class Project:
	def __init__(self, name, duration, score, end, roles):
		self.name = name
		self.duration = int(duration)
		self.score = int(score)
		self.end = int(end)
		self.roles = roles
		self.contributors = []

	def getContributors(self, contributors):
		for role in self.roles:
			for contributor in contributors:
				if not contributor.working:
					if contributor.get_skill(role[0]) >= role[1]:
						if contributor.get_skill(role[0]) == role[1]:
							contributor.impoveSkill(role[0])
						self.contributors.append(contributor)
						contributor.working = True
						break
			else:
				return False
		return True

	def __str__(self):
		# return str(self.name)+" "+str(self.duration)+" "+str(self.score)+" "+str(self.end)+" "+str(self.roles)
		return "Score: " + str(self.score) + " End: " + str(self.end)


class Contributor:
	def __init__(self, name, skills):
		self.name = name
		self.skills = skills  # dictionary: key=skill, value=level
		self.working = False

	def get_skill(self, skill) -> bool:
		if skill in self.skills.keys():
			return self.skills[skill]
		return 0

	def __str__(self):
		return str(self.name) + " " + str(self.skills)

	def check_project(self, project: Project) -> bool:
		for i in project.roles.keys():
			if i in self.skills.keys():
				if self.skills[i] >= project.roles[i]:
					return i
		return False

	def improveSkill(self, skill):
		if skill in self.skills.keys():
			self.skills[skill] += 1
		else:
			self.skills[skill] = 1


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
				skills[skill] = int(level)

			contributors.append(Contributor(name, skills))

		for x in range(int(p)):
			name, d, s, e, r = f.readline().split()
			roles = []
			for y in range(int(r)):
				role, level = f.readline().split()
				roles.append((role, int(level)))

			projects.append(Project(name, d, s, e, roles))

	return contributors, projects


def sortProjects(projects):
	newProjects = sorted(projects, key=lambda x: (x.score, x.end), reverse=True)
	return newProjects


def assignContributors(projects):
	working = []
	for project in projects:
		if not project.getContributors(contributors):
			continue
		working.append(project)
		projects.remove(project)

	return working


def completeProject(working):
	global day, score

	working = sorted(working, key=lambda x: x.duration - day)
	currentProject = working.pop()
	day += currentProject.duration - day
	score += max(currentProject.score - (currentProject.end - day), 0)
	for c in currentProject.contributors:
		c.working = False

	return currentProject


def write_submission(done, filename):
	with open(filename, "w") as file:
		file.write(str(len(done)))
		for project in done:
			file.write("\n" + project.name)
			tmp = "\n"
			for contributor in project.contributors:
				tmp += contributor.name + " "
			file.write(tmp)


# Main code
day = 0
score = 0

filename = "a_an_example.in.txt"
# filename = "b_better_start_small.in.txt"
contributors, projects = readInput(filename)
numberOfProjects = len(projects)
projects = sortProjects(projects)
done = []

while True:
	working = assignContributors(projects)
	if working == []:
		break
	done.append(completeProject(working))
	if len(done) == numberOfProjects:
		break

write_submission(done, "a_submission.txt")
