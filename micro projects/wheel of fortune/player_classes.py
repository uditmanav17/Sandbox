import random


class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def addMoney(self, amt):
        self.prizeMoney += amt

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self, prize):
        self.prizes.append(prize)

    def __str__(self):
        return f"{self.name} (${self.prizeMoney})"


class WOFHumanPlayer(WOFPlayer):
    def getMove(self, category, obscuredPhrase, guessed):
        print(f"{self.name} has ${self.prizeMoney}\n")
        print(
            f"Category: {category}\nPhrase:  {obscuredPhrase}\nGuessed: {', '.join(sorted(guessed))}\n"
        )
        move = input("Guess a letter, phrase, or type 'exit' or 'pass': ")
        return move


class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = "ZQXJKVBPYGFWMUCLDRHSNIOATE"
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    VOWELS = "AEIOU"
    VOWEL_COST = 250

    def __init__(self, name, difficulty):
        self.difficulty = difficulty
        super().__init__(name)

    def smartCoinFlip(self):
        """use to decide whether to select charater based on their frequencies in English"""
        rand_number = random.randint(1, 10)
        return True if rand_number > self.difficulty else False

    def getPossibleLetters(self, guessed):
        possible = [l for l in self.LETTERS if l not in guessed]
        if self.prizeMoney < self.VOWEL_COST:
            possible = [l for l in possible if l not in self.VOWELS]
        return possible

    def getMove(self, category, obscuredPhrase, guessed):
        valid_choices = [char for char in self.LETTERS if char not in guessed]
        if self.prizeMoney < 250:
            valid_choices = [char for char in valid_choices if char not in self.VOWELS]
        if not valid_choices:
            return "pass"
        if self.smartCoinFlip():
            for char in self.SORTED_FREQUENCIES:
                if char in valid_choices:
                    return char
        else:
            return random.choice(valid_choices)
