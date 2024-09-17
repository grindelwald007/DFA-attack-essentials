from solution_set import MatrixOperations

set_1 = {}
set_2 = {}
set_3 = {}
set_4 = {}

mo = MatrixOperations()
set_1 = mo.compute_set(2, "E7")
set_2 = mo.compute_set(1, "51")
set_3 = mo.compute_set(1, "47")
set_4 = mo.compute_set(3, "99")

print(len(set_1))
intersection = set_1.intersection(set_2, set_3, set_4)
print("S: ", sorted(intersection))




