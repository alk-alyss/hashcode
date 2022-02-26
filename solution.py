class Project:
	def __init__(self, name, duration, score, end, roles):
		self.name = name
		self.duration = int(duration)
		self.score = int(score)
		self.end = int(end)
		self.roles = roles
		self.contributors = []

	def findContributors(self, contributors):
		for role in self.roles:
			for contributor in contributors:
				if not contributor.working:
					if contributor.getSkill(role[0]) >= role[1]:
						self.contributors.append(contributor)
						contributor.working = True
						break
			else:
				for c in self.contributors:
					c.working = False
				self.contributors.clear()
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

	def getSkill(self, skill) -> bool:
		if skill in self.skills.keys():
			return self.skills[skill]
		return 0

	def __str__(self):
		return str(self.name) + " " + str(self.skills)

	def checkProject(self, project: Project) -> bool:
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
	projectsCopy = projects.copy()
	for project in projects:
		if not project.findContributors(contributors):
			continue
		working.append(project)
		projectsCopy.remove(project)

	return working, projectsCopy


def completeProjects(working):
	global day, score

	working = sorted(working, key=lambda x: x.duration)
	done = [working.pop(0)]

	day += done[0].duration
	for project in working:
		project.duration -= done[0].duration
		if project.duration <= 0:
			done.append(project)
			working.remove(project)


	for project in done:
		for i, c in enumerate(project.contributors):
			if c.skills[project.roles[i][0]] <= project.roles[i][1]:
				c.improveSkill(project.roles[i][0])

		scorePenalty = day - project.end if day >= project.end else 0
		score += max(project.score - scorePenalty, 0)

		for c in project.contributors:
			c.working = False

	return done, working


def writeSubmission(done, filename):
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

# filename = "a_an_example.in.txt"
filename = "b_better_start_small.in.txt"
# filename = "c_collaboration.in.txt"
# filename = "d_dense_schedule.in.txt"
# filename = "e_exceptional_skills.in.txt"
# filename = "f_find_great_mentors.in.txt"

contributors, projects = readInput(filename)
numberOfProjects = len(projects)
projects = sortProjects(projects)
done = []
working = []

while True:
	newWorking, projects = assignContributors(projects)
	working.extend(newWorking)
	if working == []:
		break
	newDone, working = completeProjects(working)
	done.extend(newDone)
	if len(done) == numberOfProjects:
		break

writeSubmission(done, filename[0]+"_submission.txt")
print(f"{day=}")
print(f"{score=}")
print(f"{len(done)=}")
