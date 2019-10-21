from deck import Card, FULL_DECK, deal_cards
from hand import best5plus3

def estimateEquity2players3cards(heroCards, villainCards, numberOfRunouts = 1000, board = None):
    deck = FULL_DECK.copy()
    for h in heroCards + villainCards:
        deck.remove(h)
    if board:
        for h in board:
            deck.remove(h)

    heroWins, villainWins, tie = 0, 0, 0

    for i in range(numberOfRunouts):
        board = deal_cards(deck.copy(), 5)
        # print(board)
        b1 = best5plus3(board, heroCards)
        b2 = best5plus3(board, villainCards)
        if (b1 > b2):
            heroWins += 1
        elif (b1 < b2):
            villainWins += 1
        else:
            tie += 1

    return heroWins, villainWins, tie 

d = FULL_DECK.copy()
h1 = deal_cards(d, 3)
print("Hero has:", h1)
h2 = deal_cards(d, 3)
print("Villain has:", h2)

trials = 1000
heroWins, villainWins, ties = estimateEquity2players3cards(h1, h2, trials)
print("1k -- Hero wins:", heroWins/trials, "Villain wins:", villainWins/trials, "Ties:", ties/trials)

trials = 2000
heroWins, villainWins, ties = estimateEquity2players3cards(h1, h2, trials)
print("2k -- Hero wins:", heroWins/trials, "Villain wins:", villainWins/trials, "Ties:", ties/trials)

trials = 5000
heroWins, villainWins, ties = estimateEquity2players3cards(h1, h2, trials)
print("5k - Hero wins:", heroWins/trials, "Villain wins:", villainWins/trials, "Ties:", ties/trials)

trials = 10000
heroWins, villainWins, ties = estimateEquity2players3cards(h1, h2, trials)
print("10k - Hero wins:", heroWins/trials, "Villain wins:", villainWins/trials, "Ties:", ties/trials)