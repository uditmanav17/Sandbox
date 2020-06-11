import json
import random
import time
import sys

# sys.setExecutionLimit(300000) # let this take up to 10 minutes
from player_classes import WOFHumanPlayer, WOFComputerPlayer

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VOWELS = "AEIOU"
VOWEL_COST = 250

# Repeatedly asks the user for a number between min & max (inclusive)
def getNumberBetween(prompt, minimum, maximum):
    userinp = input(prompt)  # ask the first time
    while True:
        try:
            n = int(userinp)  # try casting to an integer
            if n < minimum:
                errmessage = f"Must be at least {minimum}"
            elif n > maximum:
                errmessage = f"Must be at most {maximum}"
            else:
                return n
        except ValueError:  # The user didn't enter a number
            errmessage = f"{userinp} is not a number."

        # If we haven't gotten a number yet, add the error message
        # and ask again
        userinp = input(f"{errmessage}\n{prompt}")


# Spins the wheel of fortune wheel to give a random prize
# Examples:
#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
def spinWheel():
    with open("wheel.json", "r") as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)


# Returns a category & phrase (as a tuple) to guess
# Example:
#     ("Artist & Song", "Whitney Houston's I Will Always Love You")
def getRandomCategoryAndPhrase():
    with open("phrases.json", "r") as f:
        phrases = json.loads(f.read())
        category = random.choice(list(phrases.keys()))
        phrase = random.choice(phrases[category])
    return category, phrase.upper()


# Given a phrase and a list of guessed letters, returns an obscured version
# Example:
#     guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
#     phrase:  "GLACIER NATIONAL PARK"
#     returns> "_L___ER N____N_L P_RK"
def obscurePhrase(phrase, guessed):
    rv = ""
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv + "_"
        else:
            rv = rv + s  # + " "
    return rv


# Returns a string representing the current state of the game
def showBoard(category, obscuredPhrase, guessed):
    return f"""
Category: {category}
Phrase:   {obscuredPhrase}
Guessed:  {', '.join(sorted(guessed))}"""


def requestPlayerMove(player, category, guessed, phrase):
    # we're going to keep asking the player for a move until they give a valid one
    while True:
        # added so that any feedback is printed out before the next prompt
        time.sleep(0.1)

        move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
        move = move.upper()  # convert whatever the player entered to UPPERCASE
        if move == "EXIT" or move == "PASS":
            return move
        elif len(move) == 1:  # they guessed a character
            # the user entered an invalid letter (such as @, #, or $)
            if move not in LETTERS:
                print("Guesses should be letters. Try again.")
                continue
            # this letter has already been guessed
            elif move in guessed:
                print(f"{move} has already been guessed. Try again.")
                continue
            # if it's a vowel, we need to be sure the player has enough
            elif move in VOWELS and player.prizeMoney < VOWEL_COST:
                print(f"Need ${VOWEL_COST} to guess a vowel. Try again.")
                continue
            else:
                return move
        else:  # they guessed the phrase
            return move


def get_players():
    num_human = getNumberBetween("How many human players?: ", 0, 10)

    # Create the human player instances
    human_players = [
        WOFHumanPlayer(input(f"Enter the name for human player #{i+1}: "))
        for i in range(num_human)
    ]

    num_computer = getNumberBetween("How many computer players?: ", 0, 10)

    # If there are computer players, ask how difficult they should be
    if num_computer >= 1:
        difficulty = getNumberBetween("Computers Difficulty? (1-10): ", 1, 10)

    # Create the computer player instances
    computer_players = [
        WOFComputerPlayer(f"Computer {i+1}", difficulty) for i in range(num_computer)
    ]
    players = human_players + computer_players

    # No players, no game :(
    if len(players) == 0:
        print("We need players to play!")
        sys.exit()
        # raise Exception("Not enough players")

    return players


def print_board(player, phrase, guessed, wheelPrize, category):
    print("")
    print("-" * 15)
    print(showBoard(category, obscurePhrase(phrase, guessed), guessed))
    print("")
    print(f"{player.name} spins...")
    time.sleep(2 / 2)  # pause for dramatic effect!
    print(f"{wheelPrize['text']}!")
    time.sleep(1 / 2)  # pause again for more dramatic effect!


def check_winner(winner, phrase):
    if winner:
        # In your head, you should hear this as being announced by a game show host
        print(f"{winner.name} wins! The phrase was {phrase}")
        print(f"{winner.name} won ${winner.prizeMoney}")
        if len(winner.prizes) > 0:
            print(f"{winner.name} also won:")
            for prize in winner.prizes:
                print(f"    - {prize}")
    else:
        print(f"Nobody won. The phrase was {phrase}")


# GAME LOGIC CODE
def main():
    print("=" * 15)
    print("WHEEL OF PYTHON")
    print("=" * 15)
    print("")

    players = get_players()

    # category and phrase are strings.
    category, phrase = getRandomCategoryAndPhrase()
    # guessed is a list of the letters that have been guessed
    guessed = []

    # playerIndex keeps track of the index (0 to len(players)-1) of the player whose turn it is
    playerIndex = 0

    # will be set to the player instance when/if someone wins
    winner = False

    while True:
        player = players[playerIndex]
        wheelPrize = spinWheel()

        print_board(player, phrase, guessed, wheelPrize, category)

        if wheelPrize["type"] == "bankrupt":
            player.goBankrupt()
        elif wheelPrize["type"] == "loseturn":
            pass  # do nothing; just move on to the next player
        elif wheelPrize["type"] == "cash":
            move = requestPlayerMove(player, category, guessed, phrase)
            if move == "EXIT":  # leave the game
                print("Until next time!")
                break
            elif move == "PASS":  # will just move on to next player
                print(f"{player.name} passes")
            # elif len
            elif len(move) == 1:  # they guessed a letter
                guessed.append(move)
                print(f'{player.name} guesses "{move}"')

                if move in VOWELS:
                    player.prizeMoney -= VOWEL_COST

                count = phrase.count(move)
                # returns an integer with how many times this letter appears
                if count > 0:
                    if count == 1:
                        print(f"There is one {move}")
                    else:
                        print(f"There are {count} {move}'s")

                    # Give them the money and the prizes
                    player.addMoney(count * wheelPrize["value"])
                    if wheelPrize["prize"]:
                        player.addPrize(wheelPrize["prize"])

                    # all of the letters have been guessed
                    if obscurePhrase(phrase, guessed) == phrase:
                        winner = player
                        break

                    continue  # this player gets to go again

                elif count == 0:
                    print(f"There is no {move}")
            else:  # they guessed the whole phrase or words
                if move == phrase:  # they guessed the full phrase correctly
                    winner = player
                    # Give them the money and the prizes
                    player.addMoney(wheelPrize["value"])
                    if wheelPrize["prize"]:
                        player.addPrize(wheelPrize["prize"])
                    break
                else:
                    print(f"{move} was not the phrase")

        # Move on to the next player (or go back to player[0] if we reached the end)
        playerIndex = (playerIndex + 1) % len(players)

    check_winner(winner, phrase)


if __name__ == "__main__":
    main()
