import random, string

"""
Casino game, Baccarat:
    there are three choices for users, Player, Tie and Banker. If users choose either player or banker and win
        their money will be doubled. if the rep goes Tie and they had chosen P or B they get a refund.
        otherwise they lose their money. E.g: Kevin bets on player, but Banker wins, he loses his money.
        Kevin bets 100$ on Banker and he wins, he gets 200$.
        Kevin bets on player or banker, bet goes Tie, he gets his 100$ back.
        Kevin bets 100$ on Tie, bet goes Tie, he will get 800$.
    player and banker recieve two cards, if the sum is <= 5, they recieve another card.
        9 is the biggest number in baccarat. if users get a 9, and dealer has 8 or lower number, users win the game.
"""

# list of cards

card_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# value of each card

card_value = {"A": 1,
              "2": 2,
              "3": 3,
              "4": 4,
              "5": 5,
              "6": 6,
              "7": 7,
              "8": 8,
              "9": 9,
              "10": 0,
              "J": 0,
              "Q": 0,
              "K": 0}

# the range of money that players can bet

money_range = 100000000000000000000000000000000000000


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


player = "p"
banker = "b"
tie = "t"



print( "Guide:\ntype p for Player, t for Tie and b for Banker and q to quit the game" )
print()

player_cards = random.sample(card_list,2)
banker_cards = random.sample(card_list,2)




ferst_card_p = player_cards[0]
second_card_p = player_cards[1]

ferst_card_b = banker_cards[0]
second_card_b = banker_cards[1]

a=card_value[ferst_card_p] + card_value[second_card_p]
b=card_value[ferst_card_b] + card_value[second_card_b]
player_cost=a%10
banker_cost=b%10

if player_cost < 6:
    add_player_card = random.choice(card_list)
    player_cards.append(add_player_card)
    third_card_p=player_cards[2]
    a=card_value[third_card_p]+card_value[ferst_card_p] + card_value[second_card_p]
    player_cost=a%10
if banker_cost < 6:
    add_banker_card = random.choice(card_list)
    banker_cards.append(add_banker_card)
    third_card_b=banker_cards[2]
    b=card_value[third_card_b]+card_value[ferst_card_b] + card_value[second_card_b]
    banker_cost=b%10


while True:
    chosen_input = input("Bet on Player / Tie / Banker: ")
    if chosen_input in ("p", "P"):
        print("you bet on Player")
        break
    elif chosen_input in ("t", "T"):
        print("you bet on Tie")
        break
    elif chosen_input in ("b", "B"):
        print("you bet on Banker")
        break
    elif chosen_input in ("q", "Q"):
        print("Thanks for playing Baccarat.")
        break
    else:
        print(color.RED + "Please type P for Player, T for Tie or B for Banker" + color.END)
    



def bet_amount():
    while True:
        betamount_input = int(input("How much money do you want to bet on:" ))
        if 1 <= betamount_input <= 1000000000:
            print("You bet {} on {}".format(betamount_input, chosen_input))
            print("Player's cards", player_cards)
            print("Player's cost:", player_cost)
            print("Banker's cards", banker_cards)
            print("Banker's cost:", banker_cost)
            break


        elif betamount_input > money_range or betamount_input < 1:
            print("please type a number between 1 and 10000")
            break
        elif betamount_input in ("q", "Q"):
            print("Thanks for playing Baccarat.")
            break
    a=0  
    
    while a<1:
        if player_cost>banker_cost and chosen_input == "p":
            print("Вы выйграли!!!")
            a+=1
        elif player_cost<banker_cost and chosen_input == "p":
            print("Вы проиграли :(")
            a+=1
        break
    while a<1:
        if player_cost<banker_cost and chosen_input == "b":
           print("Вы выйграли!!!")
           a+=1
        elif player_cost>banker_cost and chosen_input == "b":
            print("Вы проиграли :(")
            a+=1
        break
    while a<1:
        if player_cost==banker_cost and chosen_input == "t":
            print("Вы выйграли!!!")
            a+=1
        else:
            print("Вы проиграли :(")
            a+=1
            
bet_amount()


