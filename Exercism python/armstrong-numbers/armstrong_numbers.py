def is_armstrong_number(number):
    n = len(str(number))
    return sum([i**n for i in map(int, list(str(number)))]) == number

