# Author:   Kevin Santschi
# Class:    MA465-01 Spring 2024
# Final Project:
# The purpose of this program is to create a Monte Carlo simulation to explore different strategies
# for the game blackjack, in order to find which ones, given very simple strategies, return a higher net positive.

import random

# Global vars to track win/loss, what number deck the program is on, and the list of outcomes.
bankRoll = 0
deckNum = 1
resultList = []


# Class to define the deck of cards
class DeckOfCards:

    # Constructor function with a list for cards
    def __init__(self):
        self.cards = []

    # Function to fill the list with a double deck of playing cards
    def createDeck(self):

        # Create list of card values/"faces"
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

        # Normally there are 4 of each in a deck of cards, but we are playing with double decks so append 8 of each
        for i in range(8):
            for rank in ranks:
                self.cards.append(rank)

        # Shuffle the deck
        random.shuffle(self.cards)

    # Function to deal the top card of the deck to a hand
    def dealCard(self):

        # If there are no cards left in the deck
        if len(self.cards) == 0:
            global deckNum
            global bankRoll

            # Print the result from that double deck, instantiate the next deck and start from 0
            print(f"Result from deck number {deckNum}: {bankRoll}")
            deckNum += 1
            resultList.append(bankRoll)
            bankRoll = 0
            self.createDeck()

        # Remove and return the first card in the deck
        return self.cards.pop(0)


# Global function to calculate the value of a hand of cards
def calculateHandValue(hand):
    value = 0
    num_aces = 0

    # Take the base value of each card
    for card in hand:
        if card.isdigit():
            value += int(card)
        elif card in ['Jack', 'Queen', 'King']:
            value += 10
        else:  # Ace
            num_aces += 1
            value += 11

    # If the hand includes an ace and would bust normally, count the ace as a 1
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1

    return value


# Function to determine the winner of a round. Uses bool finalEval to determine if it's a bust or the end of the round
def determineWinner(pHandVal, dHandVal, finalEval):
    global bankRoll

    # If it is not the end of the round and this function is being called, then someone went over 21
    if not finalEval:

        # Player busted; player loses their bet amount
        if pHandVal > 21:
            bankRoll -= 2
            return "Player Bust"

        # Dealer busted; player gains their bet amount
        if dHandVal > 21:
            bankRoll += 2
            return "Dealer Bust"

    # If it is the end of the round and neither hand went over 21, determine the winner normally
    elif finalEval:

        # Hands tied; no bet is gained nor lost
        if pHandVal == dHandVal:
            return "Tied"

        # Player won; player gains their bet amount
        if pHandVal > dHandVal:
            bankRoll += 2
            return "Won"

        # Player lost; player loses their bet amount
        if dHandVal > pHandVal:
            bankRoll -= 2
            return "Lost"


# Class to define the game of blackjack and its methods
class Blackjack:

    # Constructor function. Includes a DeckOfCards object, and two lists to track the player and dealer hands
    def __init__(self):
        self.deck = DeckOfCards()
        self.playerHand = []
        self.dealerHand = []

    # Function to simulate the start of the game
    def dealInitCards(self):
        # Empty player and dealer hands
        self.playerHand.clear()
        self.dealerHand.clear()

        # Deal two cards to each hand
        self.playerHand.append(self.deck.dealCard())
        self.dealerHand.append(self.deck.dealCard())
        self.playerHand.append(self.deck.dealCard())
        self.dealerHand.append(self.deck.dealCard())

    # Function to check for a blackjack at the start of the round
    def checkBlackjack(self):
        global bankRoll

        # Calculate the value of each hand
        pHandVal = calculateHandValue(self.playerHand)
        dHandVal = calculateHandValue(self.dealerHand)

        # If either hand got a blackjack,
        if pHandVal == 21 or dHandVal == 21:

            # If both hands got a blackjack, continue to the next hand with no winner
            if pHandVal == dHandVal:
                return "Continue"

            # If the player got the blackjack, win 1.5x bet amount and continue to the next hand
            elif pHandVal > dHandVal:
                bankRoll += 3
                return "Continue"

            # If the dealer got the blackjack, lose bet amount and continue to the next hand
            else:
                bankRoll -= 2
                return "Continue"

        # Otherwise, continue with the round like normal
        else:
            return "No blackjack"

    # Function to simulate the player's turn
    def playerTurn(self, strategy):

        # Hand check loop
        while True:

            # Calculate value of the player's hand and check if they have an ace
            pHandVal = calculateHandValue(self.playerHand)
            hasAce = any(card == "Ace" for card in self.playerHand)

            # If the player has gone over 21, player busts and loses automatically
            if pHandVal > 21:
                return determineWinner(pHandVal, 0, False)

            # Depending on the player's strategy.

            # Strategy 1: The player copies the dealer's strategy and stands on a 17 or higher hand.
            if strategy == "Copy Dealer":
                if pHandVal >= 17:
                    return "Stand"
                else:
                    self.playerHand.append(self.deck.dealCard())

            # Strategy 2: The player plays it safe and stands if they have 14+ without an ace, or 17+ with an ace
            elif strategy == "Safe Plays":
                if (not hasAce and pHandVal >= 14) or (hasAce and pHandVal >= 17):
                    return "Stand"
                else:
                    self.playerHand.append(self.deck.dealCard())

            # Strategy 3: Similar to 2 but riskier, player stands if they have 17+ without an ace, or 19+ with an ace
            elif strategy == "Risky Plays":
                if (not hasAce and pHandVal >= 17) or (hasAce and pHandVal >= 19):
                    return "Stand"
                else:
                    self.playerHand.append(self.deck.dealCard())

    # Function to simulate the dealer's turn
    def dealerTurn(self):

        # Hand check loop
        while True:

            # Calculate value of the dealer's hand
            dHandVal = calculateHandValue(self.dealerHand)

            # If the dealer has gone over 21, dealer busts and loses automatically
            if dHandVal > 21:
                return determineWinner(0, dHandVal, False)

            # The dealer stands on a 17 or higher, hits otherwise.
            if dHandVal >= 17:
                return "Stand"
            else:
                self.dealerHand.append(self.deck.dealCard())

    # Function to simulate the actual game
    def game(self, strategy):
        global deckNum
        global bankRoll
        self.deck.createDeck()

        print(f"Strategy: {strategy}")

        # Play through 12 decks. This number may be changed to increase the sample size
        while deckNum <= 12:

            # Deal the initial cards
            self.dealInitCards()

            # Check for a blackjack. If there has been a blackjack, continue to the next round
            if self.checkBlackjack() == "Continue":
                continue

            # The player's turn. If the player busts, continue to the next round
            if self.playerTurn(strategy) == "Player Bust":
                continue

            # The dealer's turn. If the dealer busts, continue to the next round
            if self.dealerTurn() == "Dealer Bust":
                continue

            # Otherwise, determine the winner of the round normally
            determineWinner(calculateHandValue(self.playerHand), calculateHandValue(self.dealerHand), True)

        # After all decks are run out, set the deck number back to 1 and print the results of the decks
        deckNum = 1
        print("Results:", resultList)
        print("Average:", round(sum(resultList) / len(resultList), 2))
        resultList.clear()


# Instantiate the Blackjack object and play 3 games of 12 decks, 1 for each strategy
blackjackGame = Blackjack()
blackjackGame.game("Copy Dealer")
print()
blackjackGame.game("Safe Plays")
print()
blackjackGame.game("Risky Plays")
