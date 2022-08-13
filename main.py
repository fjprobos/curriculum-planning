import model
from algorithms import Solution, ExhaustiveSearchSolution, GreedySolution
from verifier import Verifier
import os

if __name__ == "__main__":
    greedy = GreedySolution()
    exhaustiveSearch = ExhaustiveSearchSolution()
    verifier = Verifier()

    print("Correctness Check") 
    testFolder = "test/"
    passCnt = 0
    total = 0
    for f in os.listdir(testFolder):
        if f.endswith('.json'):
            testFile = os.path.join(testFolder, f)
            result = verifier.compareSolution(testFile, greedy, exhaustiveSearch)
            print(f, "Pass" if result else "Fail")

            if result:
                passCnt += 1
            total += 1

    print("Passed", passCnt, "/", total)


    print("Performance Benchmark") 
    testFolder = "test/"
    for f in os.listdir(testFolder):
        if f.endswith('.json'):
            testFile = os.path.join(testFolder, f)
            result1 = verifier.benchmarkTestCase(testFile, greedy)
            result2 = verifier.benchmarkTestCase(testFile, exhaustiveSearch)
            print(result1, result2)