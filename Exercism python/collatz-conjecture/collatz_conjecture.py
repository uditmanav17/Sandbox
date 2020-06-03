def steps(number):
    if number <= 0:
        raise ValueError("Error")
    count = 0
    while number != 1:
        count += 1
        if not number%2:
            number //= 2
        else:
            number = 3*number + 1
    return count
