def convert( number ):
    answer = 'Pling' if not number % 3 else ""
    answer += 'Plang' if not number % 5 else ""
    answer += 'Plong' if not number % 7 else ""
    return answer or str(number)
