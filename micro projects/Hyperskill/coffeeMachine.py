# https://hyperskill.org/projects/68
class coffeeMachine:
    water = 400
    milk = 540
    beans = 120
    disp_cups = 9
    money = 550
    coffees = {
        "1": [250, 0, 16, 4],  # espresso
        "2": [350, 75, 20, 7],  # latte
        "3": [200, 100, 12, 6],  # cupp
    }

    def __init__(self):
        self.process()

    def process(self):
        inp = ""
        while inp != "exit":
            inp = input("Write action (buy, fill, take, remaining, exit):\n> ")
            print()
            if inp == "take":
                self.take()
            elif inp == "fill":
                self.fill()
            elif inp == "buy":
                self.buy()
            elif inp == "remaining":
                self.display_info()

    def display_info(self):
        print(
            f"""The coffee machine has:
{self.water} of water
{self.milk} of milk
{self.beans} of coffee beans
{self.disp_cups} of disposable cups
${self.money} of money\n"""
        )

    def buy(self):
        resources = ["water", "milk", "beans"]
        remaining_res = [self.water, self.milk, self.beans]
        min_req = [min(a, b, c) for a, b, c in zip(*self.coffees.values())][:-1]
        # print(min_req)
        # print(remaining_res)
        check = [a <= b for a, b in zip(min_req, remaining_res)]
        # print(check)

        if not all(check):
            print(f"Sorry, not enough {resources[check.index(False)]}!\n")
            return

        option = input(
            "What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu::\n> "
        )
        if option == "back":
            return
        curr_val = self.coffees[option]
        self.water = self.water - curr_val[0]
        self.milk = self.milk - curr_val[1]
        self.beans = self.beans - curr_val[2]
        # made coffee
        self.money += curr_val[3]
        self.disp_cups -= 1
        print("I have enough resources, making you a coffee!\n")

    def fill(self):
        self.water += int(input("Write how many ml of water do you want to add:\n> "))
        self.milk += int(input("Write how many ml of milk do you want to add:\n> "))
        self.beans += int(
            input("Write how many grams of coffee beans do you want to add:\n> ")
        )
        self.disp_cups += int(
            input("Write how many disposable cups of coffee do you want to add:\n> ")
        )
        print()

    def take(self):
        print(f"I gave you ${self.money}\n")
        self.money = 0


coffee = coffeeMachine()
