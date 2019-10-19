import random

# random.shuffle
# random.sample
# list.remove
# itertools.combinations

_NAME2RANK = {"A":14, "K":13, "Q":12, "J":11, "T":10}
_RANKO2NAME = {14:"A", 13:"K", 12:"Q", 11:"J", 10:"T"}

class Card:
    def __init__(self, rank_and_suit):
        rank, suit = tuple(rank_and_suit)
        if rank in _NAME2RANK.keys():
            self.rank = _NAME2RANK[rank]
        else:
            self.rank = int(rank)
        self.suit = suit

    def __repr__(self):
        if self.rank in [14, 13, 12, 11, 10]:
            return str(_RANKO2NAME[self.rank]) + self.suit
        else:
            return str(self.rank) + self.suit

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

_FULL_DECK = [Card(c) for c in _FULL_DECK_RAW]

def deal_cards(deck = _FULL_DECK, number_of_cards = 1):
    """
    Randomly selects number_of_cards and removes them from the deck.
    """
    player_hand = random.sample(deck, number_of_cards)
    for c in player_hand:
        deck.remove(c) # modify outer deck, because the function gets a reference to a (mutable) list
    return player_hand

deck = _FULL_DECK
player1_hand = deal_cards(deck, 2)
print("player1:", player1_hand)
player2_hand = deal_cards(deck, 2)
print("player2:", player2_hand)
flop = deal_cards(deck, 3)
turn = deal_cards(deck, 1)
river = deal_cards(deck, 1)
print("board:", flop, turn, river)

# who has what?
# who wins?

def identify_holdem_hand(board, hole_cards):
    pass

def identify_3card_holdem_hand(board, hole_cards):
    pass

def identify_omaha_hand(board, hole_cards):
    pass