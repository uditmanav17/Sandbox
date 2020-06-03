def classify(number):
    if number < 1:
        raise ValueError("Number should be greater than 0")
    pair_factors = [
        (x, number // x) for x in range(1, int(number**0.5) + 1) if not number % x
    ]
    factors = {item for sublist in pair_factors for item in sublist}
    factors = sorted(list(factors))[:-1]
    return (
        "perfect"
        if sum(factors) == number
        else "abundant"
        if sum(factors) > number
        else "deficient"
    )
