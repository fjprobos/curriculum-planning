import model
from algorithms import Solution, ExhaustiveSearchSolution, DPSolution
from verifier import Verifier
import os
import json

if __name__ == "__main__":
    dp = DPSolution()
    exhaustiveSearch = ExhaustiveSearchSolution()
    verifier = Verifier()

    print("Correctness Check") 
    testFolder = "test/"
    passCnt = 0
    total = 0
    for f in os.listdir(testFolder):
        if f.endswith('.json'):
            testFile = os.path.join(testFolder, f)
            result = verifier.compareSolution(testFile, dp, exhaustiveSearch)
            print(f, "Pass" if result else "Fail")

            if result:
                passCnt += 1
            total += 1

    print("Passed", passCnt, "/", total)


    print("Performance Benchmark") 
    testFolder = "test/"
    results = []
    for f in os.listdir(testFolder):
        if f.endswith('.json'):
            testFile = os.path.join(testFolder, f)
            result1 = verifier.benchmarkTestCase(testFile, dp)
            result2 = verifier.benchmarkTestCase(testFile, exhaustiveSearch)
            print(result1, result2)
            results.append(result1)
            results.append(result2)

    # Write all results into a json file
    with open('results/results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
