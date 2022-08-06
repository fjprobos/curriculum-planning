import model

file = open('test/test1.json')
catalog = model.CourseCatalog(file)

print(catalog)