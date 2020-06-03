def find_anagrams(word, candidates):
    sort_word = lambda x : "".join(sorted(list(x)))
    li = [candidates[i] 
          for i in range(len(candidates)) 
          if sort_word(word.lower()) == sort_word(candidates[i].lower()) 
          and word.lower() != candidates[i].lower()]
    return li
