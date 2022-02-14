import random
from time import sleep

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 0}

# set min players to 0 for dealer debug
min_players = 1
max_players = 3


class Card:

    def __init__(self, suit, rank):
        self.suit = suit.title()
        self.rank = rank.title()
        self.value = VALUES[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.all_cards = []

        for suit in SUITS:
            for rank in RANKS:
                self.all_cards.append(Card(suit, rank))

        self.aces = [ace_card for ace_card in self.all_cards if ace_card.rank == 'Ace']

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        try:
            return self.all_cards.pop()
        except IndexError:
            pass

    def return_card(self, cards: list):
        self.all_cards.extend(cards)


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bet = 0
        self.score = 0
        self.soft = 0
        if name == 'Dealer':
            self.money = float('inf')
        else:
            self.money = 1000

    def add_cards(self, new_cards):
        if isinstance(new_cards, list):
            self.hand.extend(new_cards)
        else:
            self.hand.append(new_cards)

    def take_bet(self):
        """
        validates bet amount
        """
        while True:
            try:
                bet_amount = int(input(f"{self.name} enter a bet amount (max: {self.money}): "))
                if 1 <= bet_amount <= self.money:
                    self.bet = bet_amount
                    break
                elif bet_amount < 1:
                    print("Please enter a bet that involves money.")
                else:
                    print("Please enter a bet that you can afford.")
            except ValueError:
                print("Please enter a valid number.")

    def ace_check(self):
        ace_index = [idx for idx, c in enumerate(self.hand) if c.value == 0]

        if self.name == 'Dealer':
            return ace_index

        for idx in ace_index:
            while True:
                ace_choice = int(input("An ace! Do you want it to be worth 1 or 11 points?: "))
                if ace_choice in [1, 11]:
                    if ace_choice == 11 and self.score + 11 > 21:
                        print("Well it has to equal 1, since 11 will make you bust!\n")
                        self.hand[idx].value = 1
                        break
                    if ace_choice == 11:
                        self.soft = 1
                    self.hand[idx].value = ace_choice
                    break
                else:
                    print("Enter a valid choice.")

    def play(self):
        while True:
            for c in player.hand:
                print(c)
            self.update_score()
            self.ace_check()
            self.update_score()
            if self.score > 21:
                print(f"{player.name} busts!\n")
                return
            if self.score == 21:
                print("Blackjack!\n")
                break
            choice = input(f"{self.name} do you want to hit or stand? (Score: {self.score}): ")
            if choice.lower() in ['h', 'hit', 'hit me']:
                self.add_cards(deck.deal())
            elif choice.lower() in ['s', 'stand']:
                print("You stand\n")
                break
            self.update_score()

    def update_score(self):
        self.score = sum([c.value for c in self.hand])
        if self.soft == 1 and self.score > 21:
            self.score -= 10
            self.soft = 0


def determine_players(player_max, player_min):
    player_names = []
    while True:
        try:
            player_amount = int(input(f"How many players are playing? ({player_min}-{player_max}): "))
            if player_min <= player_amount <= player_max:
                break
            else:
                print("Enter a valid amount.")
        except ValueError:
            print("Please enter a valid number.")
    for player_number in range(player_amount):
        while True:
            name = input(f"Player {player_number + 1}, please enter your name: ")
            if name.lower() != 'dealer':
                break
            else:
                print("You can't be the dealer.")
        player_names.append(name)
    return [Player(_) for _ in player_names]


dealer = Player('Dealer')
players = determine_players(max_players, min_players)
table = players + [dealer]

while True:
    # restart logic
    for player in table:
        player.hand = []
        player.bet = 0
        player.soft = 0
        player.score = 0

    deck = Deck()
    deck.shuffle()

    for ace in deck.aces:
        ace.value = 0

    # start of round
    for player in players:
        player.take_bet()
        print(f"{player.name} bets {player.bet}\n")

    # deal cards
    for x in range(2):
        for player in table:
            player.add_cards(deck.deal())

    # deal dealer
    print("Dealer")
    print(dealer.hand[0])
    print("Face down card")

    # play loop
    for player in players:
        print(f"\n{player.name}'s turn")
        player.play()
        sleep(2)

    # dealer loop
    print("\nDealer's turn")

    aces = dealer.ace_check()
    if len(aces) == 1:
        dealer.hand[aces[0]].value = 11
        dealer.soft = 1
    elif len(aces) == 2:
        dealer.hand[aces[0]].value = 11
        dealer.hand[aces[1]].value = 1
        dealer.soft = 1

    dealer.update_score()

    print(dealer.hand[0])
    print(f"{dealer.hand[1]} (Score: {dealer.score})")

    while dealer.score < 17:
        print('Dealer hits.')
        dealer.add_cards(deck.deal())
        if dealer.hand[-1].value == 0:
            if (dealer.score + 11) > 21:
                dealer.hand[-1].value = 1
            else:
                dealer.hand[-1].value = 11
                dealer.soft = 1
        dealer.update_score()
        print(f"{dealer.hand[-1]} (Score: {dealer.score})")
        sleep(1)
        if dealer.score > 21:
            print("Dealer busts!")
            dealer.score = 0
            sleep(2)
            break
        elif dealer.score == 21:
            print('Blackjack!')
            sleep(2)

    # win logic
    losers = []
    for player in players:
        if dealer.score < player.score < 22:
            print(f"{player.name} wins!")
            player.money += player.bet
        elif dealer.score == player.score < 22:
            print(f"{player.name} ties!")
        else:
            print(f"{player.name} lost!")
            player.money -= player.bet
        if player.money == 0:
            print(f"{player.name} is broke and has to leave the table!")
            losers.append(player)

    for loser in losers:
        players.remove(loser)

    if len(players) == 0 and min_players > 0:
        print('your bad')
        exit()

    while True:
        play_again = input("Do you wish to play again? (Yes or no)")
        if play_again.lower() in ['y', 'yes']:
            break
        if play_again.lower() in ['n', 'no']:
            print('ok bye :)')
            sleep(1)
            exit()
