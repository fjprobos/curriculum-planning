import json


class Course:
    def __init__(self, id, name, utility):
        self.id = id
        self.name = name
        self.utility = utility
        self.edges = []

    def __str__(self):
        return "id: {}, name: {}, utility: {}, prerequisites: {}\n".format(self.id, self.name, self.utility, self.edges)

    def __repr__(self):
        return str(self)


class CourseCatalog:
    def __init__(self, jsonFile):
        with open(jsonFile, 'r') as f:
            self.courseList = []
            self.courseDict = {}
            input = json.load(f)
            self.coursesRequired = input['k']
            for c in input['courses']:
                prerequisites = c['prerequisites']
                course = Course(c['courseId'], c['name'], c['utility'])
                for i in prerequisites:
                    course.edges.append(i)
                self.courseList.append(course)
                self.courseDict[course.id] = course

    def __str__(self):
        return str(self.courseList)
