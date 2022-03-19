import argparse

class Project:
	def __init__(self, name, duration, score, end, roles):
		self.name = name
		self.duration = int(duration)
		self.score = int(score)
		self.end = int(end)
		self.roles = roles
		self.contributors = []
		self.working = False
		self.done = False

	def findContributors(self):
		# Takes a dictionary with contributors
		# and tries to fill all the roles for the current project
		# if we cant fill all the roles then it return False
		# else it return True
		# TO DO: make the use of the findMentor function
		for role in self.roles:
			mentee = self.findMentor(role[0], role[1])
			if mentee != None:
				self.contributors.append(mentee)
				mentee.working = True
				continue
			for contributor in Contributor.contributorIndex[role[0]]:
				if not contributor.working:
					if contributor.skills[role[0]] >= role[1]:
						self.contributors.append(contributor)
						contributor.working = True
						break
			else:
				for c in self.contributors:
					c.working = False
				self.contributors.clear()
				return False
		return True

	def findMentor(self, cur_role: str, level: int):
		# Take the contributor assigned in the current project
		for contributor in self.contributors:
			# when a contributor inside the projects is assigned who knows the role
			# at an adequate level then find a mentee
			# if the required level for the role is 1
			# then anyone can be assigned to the project
			# return false if not mentee or mentor is found
			if cur_role in contributor.skills.keys() and contributor.skills[cur_role] >= level:
				if level == 1:
					for mentee in Contributor.contributorList:
						if cur_role in mentee.skills.keys():
							continue
						if not mentee.working:
							return mentee
				for mentee in Contributor.contributorIndex[cur_role]:
					if not mentee.working and mentee.skills[cur_role] == level - 1:
						return mentee
		return None

	def __str__(self):
		# return str(self.name)+" "+str(self.duration)+" "+str(self.score)+" "+str(self.end)+" "+str(self.roles)
		return "Score: " + str(self.score) + " End: " + str(self.end)


class Contributor:
	contributorList = []
	contributorIndex = {}

	def __init__(self, name, skills):
		self.name = name
		self.skills = skills  # dictionary: key=skill, value=level
		self.working = False

	def __str__(self):
		return str(self.name) + " " + str(self.skills)

	# Below function not use
	# Probably we can delete it
	def checkProject(self, project: Project) -> bool:
		for i in project.roles.keys():
			if i in self.skills.keys():
				if self.skills[i] >= project.roles[i]:
					return i
		return False

	# If the skill needs to be improved then we add one to it
	# else we add the current skill to the skills dictionary and
	# assign 1 to it
	def improveSkill(self, skill:list):
		if skill[0] in self.skills.keys():
			if self.skills[skill[0]] <= skill[1]:
				self.skills[skill[0]] += 1
				return False
		else:
			self.skills[skill[0]] = 1
			return True

# Simple function to read all the projects
# and contributors and add them to the corresponding
# list


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

# Function to sort the projects list
# TO DO: find better key to sort the projects
# current best option is:
# (x.score , x.end) reverse = True


def sortProjects(projects):
	# newProjects = sorted(projects, key=lambda x: (x.end-x.duration, x.end, x.score, len(x.roles)))
	# newProjects = sorted(projects, key=lambda x: (x.end, x.score), reverse=True) # score=112410
	newProjects = sorted(projects, key=lambda x: (x.score, x.end), reverse=True) # score=146850
	# newProjects = sorted(projects, key=lambda x: (x.score+x.end), reverse=True) # score=157715
	# newProjects = sorted(projects, key=lambda x: (x.end/x.score), reverse=False)
	return newProjects


def assignContributors(projects):
	working = []
	# projectsCopy = projects.copy()
	for project in projects:
		if project.working or project.done:
			continue
		if not project.findContributors():
			continue
		project.working = True
		working.append(project)
		# Probably this method takes a lot of time
		# TO DO: find a better way to do this
		# Possible idea to add an attribute to projects
		# so we can mark them that are done
		# so we dont need to make a copy of the projects list
		# and then remove it
		# projectsCopy.remove(project)

	return working

# Function to progress time and free up the working contributors


def completeProjects(working):
	# This is horrible but nevermind
	global day, score, nonScoringProjects
	# Sort bases the least ammount of time to work
	# and the progress for that time
	working = sorted(working, key=lambda x: x.duration)

	done = [working.pop(0)]
	done[0].done = True
	day += done[0].duration
	for project in working:
		if project.done:
			continue
		project.duration -= done[0].duration
		if project.duration <= 0:
			project.done = True
			done.append(project)
			working.remove(project)

	for project in done:
		for i, c in enumerate(project.contributors):
			# This probably works even if the contributor is a mentee
			# not checked yet
			if c.improveSkill(project.roles[i]):
				Contributor.contributorIndex[project.roles[i][0]].insert(0, c)
		# Calculate the score
		scorePenalty = day - project.end if day > project.end else 0
		score += max(project.score - scorePenalty, 0)
		if project.score - scorePenalty < 0:
			nonScoringProjects += 1
		# Free up the working contributors
		for c in project.contributors:
			c.working = False

	return done, working

# Method to write a txt needed for the hashcode
# submission


def writeSubmission(done, filename):
	with open(filename, "w") as file:
		file.write(str(len(done)))
		for project in done:
			file.write("\n" + project.name)
			tmp = "\n"
			for contributor in project.contributors:
				tmp += contributor.name + " "
			file.write(tmp)

# Make an index using the contributors list


def makeIndex(contributors: list):
	roleindex = {}
	for contributor in contributors:
		for role in contributor.skills.keys():
			if role in roleindex.keys():
				roleindex[role].append(contributor)
			else:
				roleindex[role] = [contributor]
	return roleindex

# Sort the index from lower to higher skill


def sort_index(contributors_index):
	for key in contributors_index.keys():
		# print([str(x) for x in contributors_index[key]])
		contributors_index[key] = sorted(
			contributors_index[key], key=lambda x: x.skills[key])
		# print([str(x) for x in contributors_index[key]])
	return contributors_index


# Main code
day = 0
score = 0
nonScoringProjects = 0



parser = argparse.ArgumentParser(description="Hashcode 2022")
parser.add_argument("--file","-f" , action="store" , help="choose the file to run" , type = str)
args = parser.parse_args()
match args.file:
	case "a":
		filename = "a_an_example.in.txt"
	case "b":
		filename = "b_better_start_small.in.txt"
	case "c":
		filename = "c_collaboration.in.txt"
	case "d":
		filename = "d_dense_schedule.in.txt"
	case "e":
		filename = "e_exceptional_skills.in.txt"
	case "f":
		filename = "f_find_great_mentors.in.txt"
	case _:
		filename = "f_find_great_mentors.in.txt"
# Get contributors and projects
Contributor.contributorList, projects = readInput(filename)
projects = sortProjects(projects)
# Used for checking
numberOfProjects = len(projects)
done = []
working = []
# Make index
Contributor.contributorIndex = makeIndex(Contributor.contributorList)
Contributor.contributorIndex = sort_index(Contributor.contributorIndex)

# Main loop to calculate our solution
try:
	while True:
		newWorking = assignContributors(projects)
		# We need to extend working in the case there are some remaining
		# projects to be done
		working.extend(newWorking)
		# if working is empty that means that we couldnt assign anymore
		# contributors to a project so we end our while True loop
		if working == []:
			break
		# take the working projects and forward time in order
		# to free up some contributors
		newDone, working = completeProjects(working)
		done.extend(newDone)
		# if the done list has as many projects as the
		# numberOfProjects then we are done
		if len(done) == numberOfProjects:
			break

		print(f"{len(done)=}")

finally:
	writeSubmission(done, filename[0]+"_submission.txt")
	# Debugging
	print("\n")
	print(f"{day=}")
	print(f"{score=}")
	print(f"{nonScoringProjects=}")
	print(f"{len(done)=}")
	print(f"{len(working)=}")
