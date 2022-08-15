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


class DPSolution(Solution):

    def __init__(self):
        self.solutionName = "dynamic programming"

    # Use topological sort to generate a list of ids in order
    def __topologicalSort__(self, catalog: CourseCatalog):
        """
        :param catalog: CourseCatalog object representing the graph with the entire course offering.
        :return: a list of course ids after topological sort that follows the dependency order
        """
        topoSortedIds = []
        # track which node is visited
        visited = {}

        # recursively add node to the topoSortedIds list
        # Add all prerequisite nodes before adding current node
        def dfs(courseId):
            if courseId in visited:
                return
            visited[courseId] = True
            for preId in catalog.courseDict[courseId].edges:
                dfs(preId)
            topoSortedIds.append(courseId) 
            
        # for every node, we recursively add its prerequsites
        # if a node if visited, we can ignore it because it's already in the list 
        for cid in catalog.courseDict:
            dfs(cid)

        # return the topological sorted list
        return topoSortedIds
        

    # the main function to solve the problem
    def solve(self, catalog: CourseCatalog):
        """
        :param catalog: CourseCatalog object representing the graph with the entire course offering.
        :return: a list of course ids after topological sort that follows the dependency order
        """
        # get the number of required courses
        k = catalog.coursesRequired

        # acquire a list of course ids that follows the dependency order
        topoSortedIds = self.__topologicalSort__(catalog)

        # create a dp array
        # dp[x][s] means that taking x nodes, the utility value of combination s 
        dp = [{} for _ in range(k + 1)] 

        # base case
        # initialize dp with "taking 0 node" with "empty set" = 0 utility
        dp[0][()] = 0

        # iterate from 1 to k, because we need to pick k courses
        for iter in range(1, k+1):
            # for any set in the previous iteration
            for s in dp[iter-1]:
                # traverse through all ids
                for id in topoSortedIds:
                    if id not in s:
                        # a course is only valid to be expended into set s, if all
                        # the prerequisites courses are in s 
                        valid = True
                        for preId in catalog.courseDict[id].edges:
                            if preId not in s:
                                valid = False
                        
                        # state transition function
                        # from the previous iteration with set s we add new id to s
                        # update utility for the current iteration with s+(id)
                        if valid: 
                            dp[iter][s + (id,)] = dp[iter-1][s] + catalog.courseDict[id].utility
                    
        # Get the maximum possible utility and the corresponding combination
        maxComb = []
        maxUtility = -float('inf')
        for comb in dp[k]:
            if dp[k][comb] > maxUtility:
                maxUtility = dp[k][comb]
                maxComb = comb

        # return the result tuple
        return maxComb, maxUtility