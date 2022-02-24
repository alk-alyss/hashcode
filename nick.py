# creating a generator
f = open('a_an_example.in.txt')
number_of_people_and_projects = list(map(int, next(f).strip('\n').split()))

people = [next(f) for i in range(number_of_people_and_projects[0])]
projects = [next(f) for i in range(number_of_people_and_projects[1])]

