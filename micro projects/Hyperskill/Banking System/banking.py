import os
import random
import sqlite3
from sqlite3.dbapi2 import Cursor, Connection

DATABSE_PATH = r"./card.s3db"


####################### DATABASE #######################
def createDatabase() -> Connection:
    conn = sqlite3.connect(DATABSE_PATH)
    c = conn.cursor()
    # create an employee table
    c.execute(
        """
    CREATE TABLE card (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        pin TEXT, 
        balance INTEGER DEFAULT 0
        )
    """
    )
    conn.commit()
    # returns conn to database
    return conn


def connect2Database() -> Connection:
    if not os.path.exists(DATABSE_PATH):
        conn = createDatabase()
    else:
        conn = sqlite3.connect(DATABSE_PATH)
    return conn


# connection to DB
conn = connect2Database()
cursor = conn.cursor()

# fetch all cards and save locally as set for fast access
all_cards = cursor.execute("SELECT number from card").fetchall()
all_cards = set([card[0] for card in all_cards])


def add2db(cardNo, pin):
    cursor.execute("INSERT INTO card (number, pin) values (?, ?)", (cardNo, pin))
    conn.commit()


def do_transfer(cardNo, balance):
    print("Transfer")
    receiver_cardNo = input("Enter card number: \n>")
    if receiver_cardNo == cardNo:
        print("You can't transfer money to the same account!\n")

    elif createChecksm(receiver_cardNo[:-1]) != int(receiver_cardNo[-1]):
        print("Probably you made mistake in the card number. Please try again!\n")

    elif receiver_cardNo not in all_cards:
        print("Such a card does not exist.\n")

    else:
        transfer_amount = int(input("Enter how much money you want to transfer:\n>"))
        print(balance, transfer_amount)
        if transfer_amount > balance:
            print("Not enough money!\n")
        else:
            with conn:
                cursor.execute(
                    "UPDATE card set balance=(balance-:transfer_amount) WHERE number=:cardNo",
                    {"cardNo": cardNo, "transfer_amount": transfer_amount},
                )
                cursor.execute(
                    "UPDATE card set balance=(balance+:transfer_amount) WHERE number=:receiver_cardNo",
                    {
                        "receiver_cardNo": receiver_cardNo,
                        "transfer_amount": transfer_amount,
                    },
                )
            balance = balance - transfer_amount
    return balance


####################### CREATE ACCOUNT #######################
def createCardNumber():
    IIN = "400000"
    acc = str(random.randint(100000000, 999999999))
    chkSum = str(createChecksm(IIN + acc))  # str(random.randint(0, 9))
    return IIN + acc + chkSum


def createChecksm(incompleteCardNo: str) -> int:
    cardNo = list(map(int, list(incompleteCardNo)))
    # multiply odd place digits by 2,  indexed from 1
    cardNo = [num * 2 if ind % 2 == 0 else num for ind, num in enumerate(cardNo)]
    # print(f"double it - {cardNo}")
    cardNo = [num - 9 if num > 9 else num for num in cardNo]
    # print(f"-9 - {cardNo}")
    mod = sum(cardNo) % 10
    # print(f"mod - {mod}")
    chkSum = (10 - mod) if mod != 0 else 0
    # print(sum(cardNo), chkSum)
    return chkSum


def createPIN():
    return str(random.randint(1000, 9999))


def createAccount():
    print("""Your card has been created\nYour card number:""")
    cardNo = createCardNumber()
    while cardNo in all_cards:
        cardNo = createCardNumber()
    print(cardNo)
    print("Your card PIN:")
    cardPIN = createPIN()
    print(cardPIN)

    # commit to db
    add2db(cardNo, cardPIN)
    all_cards.add(cardNo)
    print()


####################### LOGIN #######################
def login():
    cardNo = input("Enter your card number:\n")
    PIN = input("Enter your PIN:\n")
    print()
    # check credentials
    valid_user = False
    cursor.execute(
        "SELECT * from card where number=:cardNo and pin=:PIN",
        {"cardNo": cardNo, "PIN": PIN},
    )
    result = cursor.fetchall()
    if len(result) == 1:
        # print(result)
        valid_user = True
        _, cardNo, _, balance = result[0]

    if valid_user:
        print("You have successfully logged in!\n")
    else:
        print("Wrong card number or PIN!\n")
        return

    # keep printing menu after login
    while True:
        option = input(
            """1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n> """
        )
        print()
        if option == "0":
            return 0
        elif option == "1":
            print(f"Balance: ", balance, "\n")
        elif option == "2":
            income = int(input("Enter income: \n>"))
            with conn:  # using context manager we won't need to commit explicitly
                cursor.execute(
                    "UPDATE card set balance=(balance+:income) WHERE number=:cardNo",
                    {"cardNo": cardNo, "income": income},
                )
            balance += income
            print("Income was added!\n")
        elif option == "3":
            balance = do_transfer(cardNo, balance)
        elif option == "4":
            with conn:
                cursor.execute(
                    "DELETE from card where number=:cardNo", {"cardNo": cardNo}
                )
            print("The account has been closed!")
        elif option == "5":
            print("You have successfully logged out!\n")
            return
        else:
            print("Try Again!\n")


####################### DRIVER #######################
def mainMenu():
    print("""1. Create an account\n2. Log into account\n0. Exit""")
    return input("> ")


def main():
    # keep printing menu till exit
    option = None
    while option != 0:
        option = mainMenu()
        print()

        if option == "0":
            break
        elif option == "1":
            createAccount()
        elif option == "2":
            option = login()
        else:
            print("Try Again!")
    print("Bye!")


if __name__ == "__main__":
    main()
