def is_triangle(sides):
    sides.sort()
    return sum(sides[:2])>sides[2] and all(sides)
    

def equilateral(sides):
    return len(set(sides)) == 1 and is_triangle(sides)


def isosceles(sides):
    return len(set(sides)) <= 2 and is_triangle(sides)


def scalene(sides):
    return not isosceles(sides) and not equilateral(sides) and is_triangle(sides)

