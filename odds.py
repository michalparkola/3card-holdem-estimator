import random
import itertools
import collections
import string

class Card:
    name2rank = {"A":14, "K":13, "Q":12, "J":11, "T":10}
    rank2name = {14:"A", 13:"K", 12:"Q", 11:"J", 10:"T"}
    def __init__(self, rank_and_suit):
        rank, suit = tuple(rank_and_suit)
        if rank in self.name2rank.keys():
            self.rank = self.name2rank[rank]
        else:
            self.rank = int(rank)
        self.suit = suit

    def __repr__(self):
        if self.rank in [14, 13, 12, 11, 10]:
            return str(self.rank2name[self.rank]) + self.suit
        else:
            return str(self.rank) + self.suit

    def __lt__(self, other):
        return self.rank < other.rank

def compareUnpairedCards(cards1, cards2):
    # make sure both have an equal amount of cards
    assert(len(cards1) == len(cards2))
    # make sure both are sorted
    cards1.sort()
    cards2.sort()

    while (cards1 and cards2):
        c1 = cards1.pop()
        c2 = cards2.pop()
        if (c1.rank < c2.rank):
            return True # cards1 < cards2
        if (c1.rank > c2.rank):
            return False
        else:
            continue

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
        selfRank = rank5(self)
        otherRank = rank5(other)
        if (selfRank < otherRank):
            return True
        elif (selfRank > otherRank):
            return False
        else:
            assert(selfRank == otherRank)
            # str8 flush, flush, str8, high-card --> compare card by card
            if (selfRank in [8, 5, 4, 0]):
                return compareUnpairedCards(self.cards, other.cards)
            # quads --> compare rank of quads, then kicker
            if (selfRank == 7):
                selfCnt = collections.Counter([c.rank for c in self])
                otherCnt = collections.Counter([c.rank for c in other])
                for r in selfCnt.keys():
                    if (selfCnt[r] == 4):
                        selfQuadRank = r
                
                for r in otherCnt.keys():
                    if (otherCnt[r] == 4):
                        otherQuadRank = r

                if (selfQuadRank < otherQuadRank):
                    return True
                elif (selfQuadRank > otherQuadRank):
                    return False
                else:
                    for r in selfCnt.keys():
                        if (selfCnt[r] == 1):
                            selfKicker = selfCnt[r]
                    for r in otherCnt.keys():
                        if (otherCnt[r] == 1):
                            otherKicker = otherCnt[r]
                    return selfKicker < otherKicker

                return True
            # full --> rank of thrips then rank of pair
            if (selfRank == 6):
                return True
            # trips --> rank of trips then kickers
            if (selfRank == 3):
                return True
            # twopair --> rank of higher pair, then rank of lowe pair, then kicker
            if (selfRank == 2):
                return True
            # pair --> rank of pair then kickers
            if (selfRank == 1):
                return True

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

def deal_cards(deck, number_of_cards = 1):
    """
    Randomly selects number_of_cards from deck.
    Modifies outer deck by removing dealt cards.
    """
    player_hand = random.sample(deck, number_of_cards)
    for c in player_hand:
        deck.remove(c)
    return player_hand

royal = Hand.fromString('As Ks Qs Js Ts')
quads = Hand.fromString('As Ah Ad Ac 2c')
full = Hand.fromString('As Ah Ad Ks Kh')
trips = Hand.fromString('As Kh 2d 2s 2c')
twop = Hand.fromString('As 2c Ks Ah Kc')
pear = Hand.fromString('As Ah 9s 6d 2c')
hi = Hand.fromString('As Kh 9s 6d 2c')

# TODO: who has what?
# TODO: who wins?
# TODO: generate frequency histogram for different ranks of hands
# TODO: compare hands within a category

# the functions below take Hand's but would also work for lists of Cards
def isHighCard(hand):
    cnt = collections.Counter([c.rank for c in hand])
    return sorted(cnt.values()) == [1,1,1,1,1]

def isPair(hand):
    cnt = collections.Counter([c.rank for c in hand])
    return sorted(cnt.values()) == [1,1,1,2]

def isTwoPair(hand):
    cnt = collections.Counter([c.rank for c in hand])
    return sorted(cnt.values()) == [1,2,2]

def isTrips(hand):
    cnt = collections.Counter([c.rank for c in hand])
    return sorted(cnt.values()) == [1,1,3]

def isStraight(hand):
    h = list(hand)
    return all((h[i].rank == 1 + h[i+1].rank) for i in range(4))

def isFlush(hand):
    return len(set([c.suit for c in hand])) == 1

def isFullHouse(hand):
    cnt = collections.Counter([c.rank for c in hand])
    return sorted(cnt.values()) == [2,3]

def isQuads(hand):
    cnt = collections.Counter([c.rank for c in hand])
    return sorted(cnt.values()) == [1,4]

def isStraightFlush(hand):
    return isStraight(hand) and isFlush(hand)

def rank5(hand):
    rank = 0
    if isStraightFlush(hand):
        print(hand, "is a straight flush")
        rank = 8
    elif isQuads(hand):
        print(hand, "is quads")
        rank = 7
    elif isFullHouse(hand):
        print(hand, "is a full house")
        rank = 6
    elif isFlush(hand):
        print(hand, "is a flush")
        rank = 5
    elif isStraight(hand):
        print(hand, "is a straight")
        rank = 4
    elif isTrips(hand):
        print(hand, "is trips")
        rank = 3
    elif isTwoPair(hand):
        print(hand, "is two pair")
        rank = 2
    elif isPair(hand):
        print(hand, "is one pair")
        rank = 1
    elif isHighCard(hand):
        print(hand, "is a high card hand")
        rank = 0
    else:
        rank = -1
    return rank

# Warning: hand can mean an instance of class Hand or a list of Cards
# rank5plus2 sends
def rank5plus2(board, hole_cards):
    """
    Calculates the (integer) rank of the best 5 card combination
      taken from 7 Cards (5 board Cards + 2 player Cards)
    
    Expected arguments: lists of Cards
    Returns: int
    """

    # list of tuples of Cards
    possible_combinations = itertools.combinations(board + hole_cards, 5)
    # list of Hands
    possible_hands = [Hand(list(toc)) for toc in possible_combinations]
    return max(rank5(h) for h in possible_hands)

def rank5plus3(board, hole_cards):
    pass

# d = _FULL_DECK.copy()
# b = deal_cards(d, 5)
# h = deal_cards(d, 2)
# rank5plus2(b, h)

# rank5(royal)
# rank5(quads)
# rank5(full)
# rank5(trips)
# rank5(twop)
# rank5(pear)
# rank5(hi)

# print(royal > hi)
print(Hand.fromString('AhAcAsAd3c') > Hand.fromString('AhAsAdAc2c'))