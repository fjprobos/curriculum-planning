from model import CourseCatalog
from algorithms import Solution, ExhaustiveSearchSolution, DPSolution
from datetime import datetime

import os

class Verifier:

    def solveTestCase(self, caseFile, solution: Solution):
        catalog = CourseCatalog(caseFile)
        chosen, utility = solution.solve(catalog)
        return sorted(chosen), utility

    def compareSolution(self, caseFile, s1: Solution, s2: Solution) -> bool:
        r1Chosen, r1Utility = self.solveTestCase(caseFile, s1)
        r2Chosen, r2Utility = self.solveTestCase(caseFile, s2)
        return r1Chosen == r2Chosen and r1Utility == r2Utility

    def benchmarkTestCase(self, caseFile, solution: Solution):
        startTime = datetime.now()
        catalog = CourseCatalog(caseFile)
        for _ in range(10000):
            solution.solve(catalog)
        endTime = datetime.now()
        return {"algorithm": solution.solutionName, "test": os.path.basename(caseFile), "nodes": len(catalog.courseList), "edges": catalog.prerequisitesCount,"time": (endTime-startTime).total_seconds()}


if __name__ == "__main__":
    verifier = Verifier()
    # greedy = GreedySolution()
    # exhaustiveSearch = ExhaustiveSearchSolution()
    dp = DPSolution()
    # verifier.solveTestCase("test/test1.json", greedy)
    print(verifier.solveTestCase("test/test2.json", dp))
    # print(verifier.benchmarkTestCase("test/test1.json", greedy))
    # print(verifier.benchmarkTestCase("test/test1.json", exhaustiveSearch))