import random
import time


color = ("RED","GREEN","BLUE","YELLOW")
rank = ("0","1","2","3","4","5","6","7","8","9","Skip","Reverse","Draw2","Draw4","Wild")
card_type = {"0":"number","1":"number","2":"number","3":"number","4":"number","5":"number","6":"number",
            "7":"number","8":"number","9":"number","Skip":"action","Reverse":"action","Draw2":"action",
            "Draw4":"action_nocolor","Wild":"action_nocolor"}

class Card:

    def __init__(self, color, rank):
        self.rank = rank
        if card_type[rank] == "number":
            self.color = color
            self.cardtype = "number"
        elif card_type[rank] == "action":
            self.color = color
            self.cardtype = "action"
        else:
            self.color = None
            self.cardtype = "action_nocolor"

    def __str__(self):
        if self.color == None:
            return self.rank
        else:
            return self.color + " " + self.rank


class Deck:

    def __init__(self):
        self.deck = []
        for self_color in color:
            for self_rank in rank:
                if card_type[self_rank] != "action_nocolor":
                    self.deck.append(Card(self_color, self_rank))
                    self.deck.append(Card(self_color, self_rank))
                else:
                    self.deck.append(Card(self_color, self_rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.cards = []
        self.cardsstr = []
        self.number_cards = 0
        self.action_cards = 0

    def add_card(self, card):
        self.cards.append(card)
        self.cardsstr.append(str(card))
        if card.cardtype == "number":
            self.number_cards += 1
        else:
            self.action_cards += 1

    def remove_card(self, place):
        self.cardsstr.pop(place - 1)
        return self.cards.pop(place - 1)

    def cards_in_hand(self):
        for i in range(len(self.cardsstr)):
            print(f" {i + 1}.{self.cardsstr[i]}")

    def single_card(self, place):
        return self.cards[place - 1]

    def no_of_cards(self):
        return len(self.cards)


#randomly selects who starts first
def choose_first():
    if random.randint(0,1)==0:
        return "Player"
    else:
        return "Donald Duck"


#Function to check if the card thrown by Player/Donald Duck is a valid card by comparing it with the top card
def single_card_check(top_card,card):
    if card.color==top_card.color or top_card.rank==card.rank or card.cardtype=="action_nocolor":
        return True
    else:
        return False


#FOR Donald Duck ONLY
#To check if Donald Duck has any valid card to throw
def full_hand_check(hand,top_card):
    for c in hand.cards:
        if c.color==top_card.color or c.rank == top_card.rank or c.cardtype=="action_nocolor":
            return hand.remove_card(hand.cardsstr.index(str(c))+1)
    else:
        return "no card"


#Function to check if either wins
def win_check(hand):
    if len(hand.cards)==0:
        return True
    else:
        return False


#Function to check if last card is an action card (GAME MUST END WITH A NUMBER CARD)
def last_card_check(hand):
    for c in hand.cards:
        if c.cardtype!="number":
            return True
        else:
            return False


#The gaming loop
while True:

    print("Uno! The best card game in the world! Defeat Donald Duck to win!")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    for i in range(7):
        player_hand.add_card(deck.deal())

    pc_hand = Hand()
    for i in range(7):
        pc_hand.add_card(deck.deal())

    top_card = deck.deal()
    if top_card.cardtype != "number":
        while top_card.cardtype != "number":
            top_card = deck.deal()
    print("\nStarting Card is: {}".format(top_card))
    time.sleep(1)
    playing = True

    turn = choose_first()
    print(turn + " will go first")

    while playing:

        if turn == "Player":
            print("\nTop card is: " + str(top_card))
            print("Your cards: ")
            player_hand.cards_in_hand()
            if player_hand.no_of_cards() == 1:
                if last_card_check(player_hand):
                    print("Last card can't be an action card \nAdding one card from deck")
                    player_hand.add_card(deck.deal())
                    print("Your cards: ")
                    player_hand.cards_in_hand()
            choice = input("\nHit or Pull? (h/p): ")
            if choice == "h" or "H" or "hit" or "Hit":
                pos = int(input("Enter index of card: "))
                temp_card = player_hand.single_card(pos)
                if single_card_check(top_card, temp_card):
                    if temp_card.cardtype == "number":
                        top_card = player_hand.remove_card(pos)
                        turn = "Donald Duck"
                    else:
                        if temp_card.rank == "Skip":
                            turn = "Player"
                            top_card = player_hand.remove_card(pos)
                        elif temp_card.rank == "Reverse":
                            turn = "Player"
                            top_card = player_hand.remove_card(pos)
                        elif temp_card.rank == "Draw2":
                            pc_hand.add_card(deck.deal())
                            pc_hand.add_card(deck.deal())
                            top_card = player_hand.remove_card(pos)
                            turn = "Player"
                        elif temp_card.rank == "Draw4":
                            for i in range(4):
                                pc_hand.add_card(deck.deal())
                            top_card = player_hand.remove_card(pos)
                            draw4color = input("Change color to (enter in caps): ")
                            if draw4color != draw4color.upper():
                                draw4color = draw4color.upper()
                            top_card.color = draw4color
                            turn = "Player"
                        elif temp_card.rank == "Wild":
                            top_card = player_hand.remove_card(pos)
                            wildcolor = input("Change color to (enter in caps): ")
                            if wildcolor != wildcolor.upper():
                                wildcolor = wildcolor.upper()
                            top_card.color = wildcolor
                            turn = "Donald Duck"
                else:
                    print("This card can't be used")
            elif choice == "p" or "P" or "pull" or "Pull":
                temp_card = deck.deal()
                print("You got: " + str(temp_card))
                time.sleep(1)
                if single_card_check(top_card, temp_card):
                    player_hand.add_card(temp_card)
                else:
                    print("Can't use this card")
                    player_hand.add_card(temp_card)
                    turn = "Donald Duck"
            if win_check(player_hand):
                print("\nPLAYER WON!!")
                playing = False
                break

        if turn == "Donald Duck":
            if pc_hand.no_of_cards() == 1:
                if last_card_check(pc_hand):
                    time.sleep(1)
                    print("Adding a card to Donald Duck's hand")
                    pc_hand.add_card(deck.deal())
            temp_card = full_hand_check(pc_hand, top_card)
            time.sleep(1)
            if temp_card != "no card":
                print(f"\nDonald Duck throws: {temp_card}")
                time.sleep(1)
                if temp_card.cardtype == "number":
                    top_card = temp_card
                    turn = "Player"
                else:
                    if temp_card.rank == "Skip":
                        turn = "Donald Duck"
                        top_card = temp_card
                    elif temp_card.rank == "Reverse":
                        turn = "Donald Duck"
                        top_card = temp_card
                    elif temp_card.rank == "Draw2":
                        player_hand.add_card(deck.deal())
                        player_hand.add_card(deck.deal())
                        top_card = temp_card
                        turn = "Donald Duck"
                    elif temp_card.rank == "Draw4":
                        for i in range(4):
                            player_hand.add_card(deck.deal())
                        top_card = temp_card
                        draw4color = pc_hand.cards[0].color
                        print("Color changes to", draw4color)
                        top_card.color = draw4color
                        turn = "Donald Duck"
                    elif temp_card.rank == "Wild":
                        top_card = temp_card
                        wildcolor = pc_hand.cards[0].color
                        print("Color changes to", wildcolor)
                        top_card.color = wildcolor
                        turn = "Player"
            else:
                print("\nDonald Duck pulls a card from deck")
                time.sleep(1)
                temp_card = deck.deal()
                if single_card_check(top_card, temp_card):
                    print(f"Donald Duck throws: {temp_card}")
                    time.sleep(1)
                    if temp_card.cardtype == "number":
                        top_card = temp_card
                        turn = "Player"
                    else:
                        if temp_card.rank == "Skip":
                            turn = "Donald Duck"
                            top_card = temp_card
                        elif temp_card.rank == "Reverse":
                            turn = "Donald Duck"
                            top_card = temp_card
                        elif temp_card.rank == "Draw2":
                            player_hand.add_card(deck.deal())
                            player_hand.add_card(deck.deal())
                            top_card = temp_card
                            turn = "Donald Duck"
                        elif temp_card.rank == "Draw4":
                            for i in range(4):
                                player_hand.add_card(deck.deal())
                            top_card = temp_card
                            draw4color = pc_hand.cards[0].color
                            print("Color changes to", draw4color)
                            top_card.color = draw4color
                            turn = "Donald Duck"
                        elif temp_card.rank == "Wild":
                            top_card = temp_card
                            wildcolor = pc_hand.cards[0].color
                            print("Color changes to", wildcolor)
                            top_card.color = wildcolor
                            turn = "Player"
                else:
                    print("Donald Duck doesn't have a card")
                    time.sleep(1)
                    pc_hand.add_card(temp_card)
                    turn = "Player"
            print("\nDonald Duck has {} cards remaining".format(pc_hand.no_of_cards()))
            time.sleep(1)
            if win_check(pc_hand):
                print("\nDonald Duck WON!")
                playing = False

    new_game = input("Would you like to play again? (y/n)")
    if new_game == "y":
        continue
    else:
        print("\nThanks for playing!")
        break
