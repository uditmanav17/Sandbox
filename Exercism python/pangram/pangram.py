def is_pangram(sentence):
    s0 = set(list("abcdefghijklmnopqrstuvwxyz"))
    s1 = set(list(sentence.lower()))
    return not (s0 - s1)

