def is_isogram(string):
    s = set()
    for ele in [char for char in string.lower() if char.isalpha()]:
        if ele not in s:
            s.add(ele)
        else:
            return False
    return True
