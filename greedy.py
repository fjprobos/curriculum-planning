import model

class GreedyPlanner:

    def __init__(self, catalog):
        self.catalog = catalog
        self.mergedUtility = {}
        self.chosenCourses = []

    # merge course utilities
    def mergeUtility(self):

        visited = [False] * (len(self.catalog.courseList) + 1)
        for chosenId in self.chosenCourses:
            visited[chosenId] = True
            self.mergedUtility[chosenId] = [0, 0]

        def dfsMerge(courseId):
            if visited[courseId]:
                return self.mergedUtility[courseId]
            visited[courseId] = True

            merged = self.catalog.courseDict[courseId].utility
            count = 1
            for pre in self.catalog.courseDict[courseId].edges:
                # preMerged, preCount = dfsMerge(self.catalog.courseDict[pre].id)
                preMerged, preCount = dfsMerge(pre)
                merged += preMerged
                count += preCount

            self.mergedUtility[courseId] = [merged, count]
            return merged, count
        
        for course in self.catalog.courseList:
            if not visited[course.id]:
                merged, count = dfsMerge(course.id)
                self.mergedUtility[course.id] = [merged, count]

        # print("merged:", self.mergedUtility)

    def planCourses(self):
        while len(self.chosenCourses) < self.catalog.coursesRequired:
            self.mergeUtility()
            avgUtilityList = []
            for id in self.mergedUtility:
                if self.mergedUtility[id][0] != 0:
                    avgUtilityList.append([id] + self.mergedUtility[id])

            avgUtilityList = sorted(avgUtilityList, key=lambda x: - x[1] / x[2])

            for mergedCourseTuple in avgUtilityList:
                courseId = mergedCourseTuple[0]
                mergedNum = mergedCourseTuple[2]

                if len(self.chosenCourses) + mergedNum <= self.catalog.coursesRequired:
                    self.pickCourse(courseId)
                    break

        totalUtility = 0
        for chosenId in self.chosenCourses:
            totalUtility += self.catalog.courseDict[chosenId].utility
        
        return sorted(self.chosenCourses), totalUtility

    def pickCourse(self, courseId):
        self.chosenCourses.append(courseId)
        # self.mergedUtility[courseId][0] = 0
        for preId in self.catalog.courseDict[courseId].edges:
            self.pickCourse(preId)

file = open('test/test2.json')
catalog = model.CourseCatalog(file)

solver = GreedyPlanner(catalog)
print(solver.planCourses())