import random

class Card:
    name2rank = {"A":14, "K":13, "Q":12, "J":11, "T":10, "9":9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2}
    rank2name = {14:"A", 13:"K", 12:"Q", 11:"J", 10:"T", 9:"9", 8:"8", 7:"7", 6:"6", 5:"5", 4:"4", 3:"3", 2:"2"}
    def __init__(self, rank_and_suit):
        rank, suit = tuple(rank_and_suit)
        self.rank = self.name2rank[rank]
        self.suit = suit

    def __repr__(self):
        return str(self.rank2name[self.rank]) + self.suit

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

_FULL_DECK_RAW = [
    'As', 'Ah', 'Ad', 'Ac',
    'Ks', 'Kh', 'Kd', 'Kc',
    'Qs', 'Qh', 'Qd', 'Qc',
    'Js', 'Jh', 'Jd', 'Jc',
    'Ts', 'Th', 'Td', 'Tc',
    '9s', '9h', '9d', '9c',
    '8s', '8h', '8d', '8c',
    '7s', '7h', '7d', '7c',
    '6s', '6h', '6d', '6c',
    '5s', '5h', '5d', '5c',
    '4s', '4h', '4d', '4c',
    '3s', '3h', '3d', '3c',
    '2s', '2h', '2d', '2c'
]

FULL_DECK = [Card(c) for c in _FULL_DECK_RAW]

def deal_cards(deck, number_of_cards = 1):
    """
    Randomly selects cards from a deck (without replacement).
    Modifies outer deck by removing dealt cards.
    Returns a list of Cards of length = number_of_cards
       in descending order
    """
    cards = random.sample(deck, number_of_cards)
    for c in cards:
        deck.remove(c)
    return sorted(cards, reverse = True)