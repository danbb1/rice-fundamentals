class Person:
    def __init__(self, first_name, last_name, birth_year):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year

    def __str__(self):
        return self.first_name + " " + self.last_name + " was born in " + str(self.birth_year)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def age(self, current_year):
        return current_year - self.birth_year


class Student:
    def __init__(self, person, password):
        self.person = person
        self.password = password
        self.projects = []

    def get_name(self):
        return self.person.full_name()

    def check_password(self, password):
        return self.password == password

    def get_projects(self):
        return self.projects

    def add_project(self, project_name):
        self.projects = [project_name]


def assign(students, student_full_name, password, project):
    for student in students:
        if student.full_name() == student_full_name and student.password == password:
            if project not in student.projects:
                student.projects.append(project)


def average_age(people):
    total_ages = 0
    for person in people:
        total_ages += person.age

    return total_ages / len(people)
