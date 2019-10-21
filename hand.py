import itertools
import collections
import string

from deck import Card

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

    def __eq__(self, other):
        return self.cards == other.cards

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
                return self.cards < other.cards
            elif self_type in [QUADS, FULL_HOUSE, TRIPS, TWO_PAIR, PAIR]:
                if self_howHigh < other_howHigh:
                    return True
                elif self_howHigh > other_howHigh:
                    return False
                else:
                    # Same howHigh --> compare kickers
                    if self_kickers:
                        assert(len(self_kickers) == len(other_kickers))
                        return self_kickers < other_kickers
                    else:
                        return False

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

STRAIGHT_FLUSH = 8
QUADS = 7
FULL_HOUSE = 6
FLUSH = 5
STRAIGHT = 4
TRIPS = 3
TWO_PAIR = 2
PAIR = 1
HIGH_CARD = 0


def rank5(hand, loud = False):
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
        if(loud): print(hand, "is a straight flush", Card.rank2name[howHigh], "high")

    elif rank_count_values == [4, 1]:
        handType = QUADS
        howHigh = rank_count_items[0][0]
        kickers = [rank_count_items[1][0]]
        if(loud): print(hand, "is quad", Card.rank2name[howHigh], "with", kickers, "kicker")

    elif rank_count_values == [3, 2]:
        handType = FULL_HOUSE
        howHigh = rank_count_items[0][0], rank_count_items[1][0]
        kickers = None
        if(loud): print(hand, "is a full house", Card.rank2name[howHigh[0]], "full of", Card.rank2name[howHigh[1]])
 
    elif isFlush:
        handType = FLUSH
        howHigh = hand
        kickers = hand
        if(loud): print(hand, "is a flush", howHigh) 

    elif isStraight:
        handType = STRAIGHT
        howHigh = list(hand)[0].rank # Cards in Hand are in descending order by rank
        kickers = hand
        if(loud): print(hand, "is a straight", Card.rank2name[howHigh], "high")
 
    elif rank_count_values == [3, 1, 1]:
        handType = TRIPS
        howHigh = rank_count_items[0][0]
        kickers = [c for c in hand if c.rank != howHigh]
        assert(len(kickers) == 2)
        if(loud): print(hand, "is trips", howHigh, "with", kickers)
 
    elif rank_count_values == [2, 2, 1]:
        handType = TWO_PAIR
        a = rank_count_items[0][0]
        b = rank_count_items[1][0]
        pair1 = max(a, b)
        pair2 = min(a, b)
        howHigh = pair1, pair2
        kickers = [rank_count_items[2][0]]
        if(loud): print(hand, "is two pair", Card.rank2name[pair1], "and", Card.rank2name[pair2], "with", kickers, "kicker")
 
    elif rank_count_values == [2, 1, 1, 1]:
        handType = PAIR
        howHigh = rank_count_items[0][0]
        kickers = list(map(lambda x: x[0], rank_count_items[1:]))
        if(loud): print(hand, "is one pair", Card.rank2name[howHigh], "with", kickers, "kickers")
 
    elif rank_count_values == [1, 1, 1, 1, 1]:
        handType = HIGH_CARD
        howHigh = None
        kickers = hand
        if(loud): print(hand, "is a high card hand", hand)
    return handType, howHigh, kickers

def best5plus2(board, hole_cards):
    """
    Finds the best 5 card combination
      taken from 7 Cards (5 board Cards + 2 player Cards)
    
    Expected arguments: lists of Cards
    """
    # list of tuples of Cards
    possible_combinations = itertools.combinations(board + hole_cards, 5)
    possible_hands = [Hand(list(toc)) for toc in possible_combinations]
    best = possible_hands.pop()
    while(possible_hands):
        challenger = possible_hands.pop()
        if best < challenger:
            best = challenger
    return best

def best5plus3(board, hole_cards):
    best = Hand(board)
    # test using 1 card
    combos = itertools.combinations(hole_cards, 1)
    combos = list(map(lambda x: list(x), combos))
    assert(len(combos) == 3)
    for c in combos:
        challenger = best5plus2(board, c)
        if best < challenger:
            best = challenger
    # test using 2 cards
    combos = itertools.combinations(hole_cards, 2)
    combos = list(map(lambda x: list(x), combos))
    assert(len(combos) == 3)
    for c in combos:
        challenger = best5plus2(board, c)
        if best < challenger:
            best = challenger
    return best