import json


class Course:
    def __init__(self, id, name, utility):
        self.id = id
        self.name = name
        self.utility = utility
        self.edges = []

    def __str__(self):
        return "id: " + str(self.id) + ", name: " + str(self.name)


class CourseCatalog:
    def __init__(self, jsonFile):
        self.courseList = []
        self.courseDict = {}
        input = json.load(jsonFile)
        for c in input['courses']:
            prerequisites = c['prerequisites']
            course = Course(c['courseId'], c['name'], c['utility'])
            for i in prerequisites:
                course.edges.append(i)
            self.courseList.append(course)
            self.courseDict[course.id] = course

    def __str__(self):
        return str(self.courseList)
