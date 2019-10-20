import random
import itertools
import collections
import string

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

class Hand:
    def __init__(self, cards):
        self.cards = sorted(cards, reverse = True)
        assert(len(self.cards) == 5)

    def __repr__(self):
        return repr(self.cards)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < 5:
            c = self.cards[self.i]
            self.i += 1
            return c
        else:
            raise StopIteration

    # TODO: equal

    # TODO
    def __lt__(self, other):
        self_type, self_howHigh, self_kickers = rank5(self)
        other_type, other_howHigh, other_kickers = rank5(other)
        if self_type < other_type:
            return True
        elif self_type > other_type:
            return False
        else:
            # Same hand type --> compare howHigh
            assert(self_type == other_type)
            if self_type in [STRAIGHT_FLUSH, FLUSH, STRAIGHT, HIGH_CARD]:
                return self < other
            elif self_type in [QUADS, FULL_HOUSE, TRIPS, TWO_PAIR, PAIR]:
                if self_howHigh < other_howHigh:
                    return True
                elif self_howHigh > other_howHigh:
                    return False
                else:
                    # Same howHigh --> compare kickers
                    assert(len(self_kickers) == len(other_kickers))
                    return self_kickers < other_kickers

    @classmethod
    def fromString(cls, s):
        s = ''.join(s.split())
        assert(len(s) == 10)

        cards = []
        while s:
            c = s[-2:]
            c = c[0].upper() + c[1].lower()
            cards.append(Card(c))
            s = s[:-2]

        return cls(cards)

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

STRAIGHT_FLUSH = 8
QUADS = 7
FULL_HOUSE = 6
FLUSH = 5
STRAIGHT = 4
TRIPS = 3
TWO_PAIR = 2
PAIR = 1
HIGH_CARD = 0

def rank5(hand):
    # group cards by rank
    rank_count_dict = collections.Counter([c.rank for c in hand])
    rank_count_values = sorted(rank_count_dict.values(), reverse = True)
    rank_count_items = sorted(rank_count_dict.items(), key = lambda x: x[1], reverse = True)

    h = list(hand)
    isStraight = all((h[i].rank == 1 + h[i+1].rank) for i in range(4))
    isFlush = len(set([c.suit for c in hand])) == 1
    
    if isFlush and isStraight:
        handType = STRAIGHT_FLUSH
        howHigh = list(hand)[0].rank # Cards in Hand are in descending order by rank
        kickers = None
        print(hand, "is a straight flush", Card.rank2name[howHigh], "high")

    elif rank_count_values == [4, 1]:
        handType = QUADS
        howHigh = rank_count_items[0][0]
        kickers = rank_count_items[1][0]
        print(hand, "is quad", Card.rank2name[howHigh], "with", kickers, "kicker")

    elif rank_count_values == [3, 2]:
        handType = FULL_HOUSE
        howHigh = rank_count_items[0][0], rank_count_items[1][0]
        kickers = None # TODO
        print(hand, "is a full house", Card.rank2name[howHigh[0]], "full of", Card.rank2name[howHigh[1]])
 
    elif isFlush:
        handType = FLUSH
        howHigh = hand
        kickers = hand
        print(hand, "is a flush", howHigh) 

    elif isStraight:
        handType = STRAIGHT
        howHigh = list(hand)[0].rank # Cards in Hand are in descending order by rank
        kickers = hand
        print(hand, "is a straight", Card.rank2name[howHigh], "high")
 
    elif rank_count_values == [3, 1, 1]:
        handType = TRIPS
        howHigh = rank_count_items[0][0]
        kickers = [c for c in hand if c.rank != howHigh]
        assert(len(kickers) == 2)
        print(hand, "is trips", howHigh, "with", kickers)
 
    elif rank_count_values == [2, 2, 1]:
        handType = TWO_PAIR
        a = rank_count_items[0][0]
        b = rank_count_items[1][0]
        pair1 = max(a, b)
        pair2 = min(a, b)
        howHigh = pair1, pair2
        kickers = rank_count_items[2][0]
        print(hand, "is two pair", Card.rank2name[pair1], "and", Card.rank2name[pair2], "with", kickers, "kicker")
 
    elif rank_count_values == [2, 1, 1, 1]:
        handType = PAIR
        howHigh = rank_count_items[0][0]
        kickers = list(map(lambda x: x[0], rank_count_items[1:]))
        print(hand, "is one pair", Card.rank2name[howHigh], "with", kickers, "kickers")
 
    elif rank_count_values == [1, 1, 1, 1, 1]:
        handType = HIGH_CARD
        howHigh = None
        kickers = hand
        print(hand, "is a high card hand", hand)
    return handType, howHigh, kickers

def rank5plus2(board, hole_cards):
    """
    Calculates the (integer) rank of the best 5 card combination
      taken from 7 Cards (5 board Cards + 2 player Cards)
    
    Expected arguments: lists of Cards
    """
    # list of tuples of Cards
    possible_combinations = itertools.combinations(board + hole_cards, 5)
    possible_hands = [Hand(list(toc)) for toc in possible_combinations]
    return max(rank5(h) for h in possible_hands)

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

# TODO: generate frequency histogram for different ranks of hands

# d = _FULL_DECK.copy()
# b = deal_cards(d, 5)
# h = deal_cards(d, 2)
# rank5plus2(b, h)

# for i in range(50):
#     rank5(deal_cards(_FULL_DECK.copy(),5))

royal = Hand.fromString('As Ks Qs Js Ts')
quads = Hand.fromString('3s 3h 3d 3c 2c')
full = Hand.fromString('As Ah Kd Ks Kh')
flush = Hand.fromString('3s 4s 7s 9s Js')
trip2sAK = Hand.fromString('As Kh 2d 2s 2c')
trip2sAQ = Hand.fromString('As Qh 2d 2s 2c')
str8 = Hand.fromString('Ad Ks Qs Js Ts')
twop = Hand.fromString('As 2c Ks Ah Kc')
pearA_962 = Hand.fromString('As Ah 9s 6d 2c')
pearA_952 = Hand.fromString('As Ah 9s 5d 2c')
hi = Hand.fromString('As Kh 9s 6d 2c')

# rank5(royal)
# rank5(quads)
# rank5(full)
# rank5(flush)
# rank5(str8)
# rank5(trip2sAK)
# rank5(trip2sAQ)
# rank5(twop)
# rank5(pearA)
# rank5(hi)

print(royal > quads)
print(trip2sAQ < trip2sAK)
print(pearA_952 > pearA_962)

# print(royal > hi)
# print(Hand.fromString('AhAcAsAd3c') > Hand.fromString('AhAsAdAc2c'))