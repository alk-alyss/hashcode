class Project:
    def __init__(self, name: str, duration: int, score: int, end: int, roles: dict):
        self.name = name
        self.duration = duration
        self.score = score
        self.end = end
        self.roles = roles
        self.contributors = []


class Contributor:
    def __init__(self, name: str, skills: dict):
        self.name = name
        self.skills = skills

    def check_project(self, project: Project) -> bool:
        for i in project.roles.keys():
            if i in self.skills.keys():
                if self.skills[i] >= project.roles[i]:
                    return i
        return False


def main():
    return


if __name__ == "__main__":
    main()
