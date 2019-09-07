import os
from player import Player
from card import Card
import random
import argparse
parser = argparse.ArgumentParser(description='Play a Game of modified Uno!')
parser.add_argument('-numplayers', type=int,
                    help='The number of players in the game')
parser.add_argument('-decksize', type=int, dest='decksize',
                    help=' The size of the deck in question')
parser.add_argument('-handsize', type=int, dest='handsize',
                    help=' The size of the intial hand in question')
args = parser.parse_args()
# Below are constants that we are defining for our game of UNO
ALLOWED_COLORS = set(["blue", "green", "red", "yellow"])
UNO_PENALTY = 5
CARD_TYPES = {0: "normal", 1: "add2", 2: "add4", 3: "changeColor"
              }
SPECIAL_CASES = set(["add4", "changeColor"])
NUM_CARD_TYPES = 4
MAX_NUM = 10
# Below is a class which defines our game and tracks all the state of the game


class Game():
    # Note the constructor arguements, you need to specify the direction of
    # the game 1 is clockwise, intialhandnum is how many cards everyone starts
    # with, and deck_size is obvious
    def __init__(self, numPlayers, direction, intialhandnum, deck_size):
        if intialhandnum * numPlayers > deck_size:
            raise ValueError(
                "Invalid Intial Configuration Chosen, not enough cards")
        self.current_player = 0
        # generate the cards for each player
        self.deck = self.generateDeck(deck_size)
        self.players = [Player(name="Player {}".format(i))
                        for i in range(numPlayers)]
        for player in self.players:
            for i in range(intialhandnum):
                player.add_card(self.draw())
        self.cards = []
        # a direction of 1 implies clockwise
        self.direction = 1
        # this function populates our deck with a weighted probability
        # distribution for the cards

    def generateDeck(self, deck_size):
        temporary_deck = []
        for index in range(deck_size):
            type_ = random.randint(0, NUM_CARD_TYPES * 20)
            # Weight Probability Distribution to generate Cards
            if type_ < 5:
                type_ = CARD_TYPES[2]
            elif type_ >= 5 and type_ <= 20:
                type_ = CARD_TYPES[3]
            elif type_ > 20 and type_ <= 40:
                type_ = CARD_TYPES[1]
            else:
                type_ = CARD_TYPES[0]
            if type_ == "add2" or type_ == "normal":
                generated_color = random.choice(list(ALLOWED_COLORS))
                if type_ == "normal":
                    type_ = random.randint(0, MAX_NUM)
                temporary_deck.append(Card(color=generated_color, type_=type_))
            else:
                temporary_deck.append(Card(color="TBD", type_=type_))
        return temporary_deck
    # shuffles our cards if we run out of our deck

    def shuffle(self):
        random.shuffle(self.deck)
    # lets us draw from the deck

    def draw(self):
        if not self.deck:
            self.deck = self.cards[:-1]
            self.shuffle()
        return self.deck.pop()
    # checks if the game is over

    def game_over(self):
        return not self.players[self.current_player].cards
    # starts the game

    def start_game(self):
        self.current_player = random.randint(0, len(self.players) - 1)
        self.add_card(
            self.players[self.current_player].cards[-1], self.players[self.current_player])
        # In case the computer starts the Uno Game, we pick blue to start with
        # if its a TBD card:
        if self.cards[-1].color == "TBD":
            self.cards[-1].color == "blue"
        return self.players[self.current_player]
    # increments us to the next turn

    def next_turn(self):
        self.current_player = (self.current_player +
                               self.direction) % len(self.players)
        return self.players[self.current_player]
    # adds a card to the stack of cards

    def add_card(self, card, player):
        if self.players[self.current_player] != player:
            raise ValueError("Invalid Call to this method")
        if not self.cards or card.color == self.cards[-1].color or card.type in SPECIAL_CASES:
            self.cards.append(card)
            self.cards[-1].color = self.evaluate_card(card)
            self.players[self.current_player].play_card(card)
            return True
        return False
    # ensures that a color is valid

    def isValid(self, color):
        return color.lower() in ALLOWED_COLORS
    # evaluates the different type of cards

    def evaluate_card(self, card):
        if card.type == "changeColor" or card.type == "add4":
            color = input(
                "Please specify what color you are changing the board to")
            if self.isValid(color):
                if card.type == "add4":
                    for i in range(4):
                        self.players[(self.current_player + self.direction) %
                                     len(self.players)].add_card(self.draw())
                if "blue" in color.lower():
                    return "blue"
                elif "green" in color.lower():
                    return "green"
                elif "red" in color.lower():
                    return "red"
                elif "yellow" in color.lower():
                    return "yellow"
                else:
                    raise ValueError("You requested to exit")
            else:
                print("You Provided an invalid color, I'll let you try again")
                evaluate_card(card)
        elif card.type == "add2":
            for i in range(4):
                self.players[(self.current_player + self.direction) %
                             len(self.players)].add_card(self.draw())
        return card.color
    # checks whether it is needed to draw a card from the deck

    def needs_draw(self):
        return self.players[self.current_player].colors.get(
            self.cards[-1].color, 0) == 0 and self.players[self.current_player].colors.get("TBD", 0) == 0
    # prints the data about the game so the player can make an informed choice

    def print_hands(self, currentPlayer):
        for player in self.players:
            print("{} has {} cards".format(player.name, len(player.cards)))
            if len(player.cards) == 1:
                # TODO replace this with a weighted random number generator
                # based on how long the user took to input this
                user_input = input('CHANCE FOR UNO! TYPE IT IN')
                val = random.randint(0, len(self.players))
                if val == 0:
                    print("No one pressed uno fast enough")
                else:
                    for i in range(UNO_PENALTY):
                        player.add_card(self.draw())
            self.print_my_hand(currentPlayer)
    # prints only the current players hand

    def print_my_hand(self, currentPlayer):
        print("You have the following cards, please choose one to play on the board")
        for index, card in enumerate(currentPlayer.cards):
            print(card, " ", index)
        print("You({}) need to play a card of color {}".format(
            currentPlayer.name, self.cards[-1].color))
# runs our game with our custom configurations


def main():
    myGame = Game(args.numplayers, 1, args.handsize, args.decksize)
    currentPlayer = myGame.start_game()
    while not myGame.game_over():
        while myGame.needs_draw():
            print("You don't have a matching card so please draw a card")
            currentPlayer.add_card(myGame.draw())
            print("You just drew {}".format(currentPlayer.cards[-1]))
        card_index = 0
        myGame.print_hands(currentPlayer)
        try:
            card_index = int(
                input("What card index do you pick, please note INDEX"))
            while not myGame.add_card(
                    currentPlayer.cards[card_index],
                    currentPlayer):
                print(
                    "YOU PICKED A CARD THAT WAS NOT THE SAME COLOR AS THE PREVIOUS CARD PICK ANOTHER ONE")
                card_index = int(
                    input("What card index do you pick, please note INDEX"))
        except BaseException:
            raise ValueError(
                "Please only provide indices as an input for picking a card")
        if not myGame.game_over():
            print(" WE ARE CHANGING TURNS PLEASE SWITCH TO THE OTHER PLAYER")
            os.system('cls' if os.name == 'nt' else 'clear')
            currentPlayer = myGame.next_turn()
    print(" VICTORY!!!!", "PLAYER {} WON THE GAME".format(currentPlayer.name))


if __name__ == "__main__":
    main()
