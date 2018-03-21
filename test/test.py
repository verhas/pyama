a = {"A": 1, "B": 2, "C": 3}
b = {"A": 2, "D": 2, "E": 3}

print({**a, **b}.values())

for key, value in {**a, **b}.items():
    print(" {} {} \n ".format(key, value))

a = [2, 3, 4]

print(a[1:-1])
