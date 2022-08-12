# Script with functions representing different algorithms to solve the problem
import math
import itertools


def exhaustiveSearch(catalog):
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

    return order, maxUtility
