from odds import *


# TODO: generate frequency histogram for different ranks of hands

print("Hand:")
d = FULL_DECK.copy()
h1 = deal_cards(d, 2)
print("Hero has:", h1)
h2 = deal_cards(d, 2)
print("Villain has:", h2)
board = deal_cards(d, 5)
print("The board is:", board)

b1 = best5plus2(board, h1)
b2 = best5plus2(board, h2)

if (b1 > b2): print ("Hero wins with", b1, "vs.", b2)
elif (b1 < b2): print ("Villain wins with", b2, "vs.", b1)
else: print("It's a tie!")

# for i in range(50):
#     rank5(deal_cards(FULL_DECK.copy(),5))

# royal = Hand.fromString('As Ks Qs Js Ts')
# quads = Hand.fromString('3s 3h 3d 3c 2c')
# full = Hand.fromString('As Ah Kd Ks Kh')
# flush = Hand.fromString('3s 4s 7s 9s Js')
# trip2sAK = Hand.fromString('As Kh 2d 2s 2c')
# trip2sAQ = Hand.fromString('As Qh 2d 2s 2c')
# str8 = Hand.fromString('Ad Ks Qs Js Ts')
# twop = Hand.fromString('As 2c Ks Ah Kc')
# pearA_962 = Hand.fromString('As Ah 9s 6d 2c')
# pearA_952 = Hand.fromString('As Ah 9s 5d 2c')
# hi = Hand.fromString('As Kh 9s 6d 2c')

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

# print(royal > quads)
# print(trip2sAQ < trip2sAK)
# print(pearA_952 > pearA_962)

# print(royal > hi)
# print(Hand.fromString('AhAcAsAd3c') > Hand.fromString('AhAsAdAc2c'))