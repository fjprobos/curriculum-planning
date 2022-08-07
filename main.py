import model
import algorithms

file = open('test/test1.json')
catalog = model.CourseCatalog(file)

order, utility = algorithms.exhaustiveSearch(catalog)
print("Solution:")
print(order)
print("Utility")
print(str(utility))