import math 
def factors(value):
    if value < 2:
        return []
    factors_list = []
    while not value%2:
        factors_list.append(2)
        value = value/2
    for i in range(3, int(math.sqrt(value)) + 1, 2):
        while not value%i:
            factors_list.append(i)
            value = value/i
    if value>2:
        factors_list.append(value)
    return factors_list