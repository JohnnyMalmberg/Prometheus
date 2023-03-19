import random

class Tarot():
    def __init__(self):
        with open('data/text/tarot', 'r') as tarot_file:
            tarot = tarot_file.readlines()
        self.tarot = [t.strip() for t in tarot]

    def reading(self, n):
        def maybe_invert(card):
            return card if random.randint(0,1) == 0 else f'{card} (inverted)'
        return [maybe_invert(card) for card in random.sample(self.tarot, n)]

standard_deck = Tarot()
