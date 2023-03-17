import random

class Tarot():
    def __init__(self):
        with open('tarot.txt', 'r') as tarot_file:
            tarot = tarot_file.readlines()
        self.tarot = [t.strip() for t in tarot]

    def reading(self, n):
        return random.sample(self.tarot, n)
