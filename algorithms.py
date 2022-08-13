# Script with functions representing different algorithms to solve the problem
import math
import itertools
from model import CourseCatalog, Course

class Solution:
    def solve(self, catalog: CourseCatalog) -> tuple:
        raise Exception("solve function not implemented")

class ExhaustiveSearchSolution(Solution):

    def __init__(self):
        self.solutionName = "exhaustive search"

    def solve(self, catalog):
        """
        :param catalog: CourseCatalog object representing the graph with the entire course offering.
        :return: Tuple with: List with the id of courses in order and integer representing the utility of
        that order.
        """
        def checkSolutionFeasibility(solution):
            """
            Helper funciton to check if a given ordered list of courses to take is feasible.
            :param solution:
            :return:
            """
            coursesTaken = []

            # Check over all courses if prerequisites are met
            for c in solution:
                # Check that all prerequisites of a given course have already been taken.
                for p in c.edges:
                    if p not in coursesTaken:
                        return False
                coursesTaken.append(c.id)

            return True

        # Get the required data from the catalog
        coursesRequired = catalog.coursesRequired
        courseList = catalog.courseList

        # Generate a brute force solution by generating all permutations and then filtering out those
        # that are not feasible in terms of prerequisites
        possiblePermutations = itertools.permutations(courseList, coursesRequired)
        feasiblePermutarions = [p for p in possiblePermutations if checkSolutionFeasibility(p)]

        # Finally, whe select the order yielding the max utility
        maxUtility = math.inf * -1
        order = []

        for p in feasiblePermutarions:
            # print([c.id for c in p], [c.utility for c in p], sum([c.utility for c in p]))
            utility = sum([c.utility for c in p])
            if utility > maxUtility:
                maxUtility = utility
                order = p

        return [c.id for c in order], maxUtility


class GreedySolution(Solution):

    def __init__(self):
        self.catalog = None
        self.mergedUtility = {}
        self.chosenCourses = []
        self.solutionName = "greedy"

    def solve(self, catalog):
        self.catalog = catalog
        self.mergedUtility = {}
        self.chosenCourses = []

        while len(self.chosenCourses) < self.catalog.coursesRequired:
            self.__mergeUtility__()
            avgUtilityList = []
            for id in self.mergedUtility:
                if self.mergedUtility[id][0] != 0:
                    avgUtilityList.append([id] + self.mergedUtility[id])

            avgUtilityList = sorted(avgUtilityList, key=lambda x: - x[1] / x[2])

            for mergedCourseTuple in avgUtilityList:
                courseId = mergedCourseTuple[0]
                mergedNum = mergedCourseTuple[2]

                if len(self.chosenCourses) + mergedNum <= self.catalog.coursesRequired:
                    self.__pickCourse__(courseId)
                    break

            # print("chosen", self.chosenCourses)

        totalUtility = 0
        for chosenId in self.chosenCourses:
            totalUtility += self.catalog.courseDict[chosenId].utility

        return self.chosenCourses, totalUtility

    def __pickCourse__(self, courseId):
        self.chosenCourses.append(courseId)
        # self.mergedUtility[courseId][0] = 0
        for preId in self.catalog.courseDict[courseId].edges:
            if preId not in self.chosenCourses:
                self.__pickCourse__(preId)

    # merge course utilities
    def __mergeUtility__(self):
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
                preMerged, preCount = dfsMerge(pre)
                merged += preMerged
                count += preCount

            self.mergedUtility[courseId] = [merged, count]
            return merged, count

        for course in self.catalog.courseList:
            if not visited[course.id]:
                merged, count = dfsMerge(course.id)
                self.mergedUtility[course.id] = [merged, count]