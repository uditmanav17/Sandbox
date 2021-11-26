import os


class PhoneBook:
    def __init__(self, cache_dir) -> None:
        self.numbers = {}
        # external resource
        self.filename = os.path.join(cache_dir, "phonebook.txt")
        self.cache = open(self.filename, "w")

    def clear(self):
        # clean up
        self.cache.close()
        os.remove(self.filename)

    def add(self, name, number) -> None:
        self.numbers[name] = number

    def lookup(self, name):
        return self.numbers[name]

    def is_consistent(self):
        for name1, number1 in self.numbers.items():
            for name2, number2 in self.numbers.items():
                if name1 == name2:
                    continue
                if number1.startswith(number2):
                    return False
        return True

    def get_names(self):
        return self.numbers.keys()

    def get_numbers(self):
        return self.numbers.values()
