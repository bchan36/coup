# General object classes written here for use in TPAnimations.py and 
# TPMultiPlayerMode.py

# Taken from: http://www.cs.cmu.edu/~112/notes/hw11.html
from cmu_112_graphics import *
from tkinter import *
import math, copy, random

### Card Class
### subclass the 5 different cards
### each has actions
class Deck(object):
    def __init__(self):
        self.cards = [ ]
        for _ in range(3):
            card = Duke()
            self.cards.append(card)
        for _ in range(3):
            card = Captain()
            self.cards.append(card)
        for _ in range(3):
            card = Ambassador()
            self.cards.append(card)
        for _ in range(3):
            card = Contessa()
            self.cards.append(card)
        for _ in range(3):
            card = Assassin()
            self.cards.append(card)
    def shuffle(self):
        for i in range(len(self.cards)):
            index = random.randint(0,len(self.cards)-1)
            temp = self.cards[index]
            self.cards[index] = self.cards[i]
            self.cards[i] = temp
    def addCard(self, cards):
        self.cards.extend(cards)
        self.shuffle()
    def removeCards(self, number):
        c = [ ]
        for _ in range(number):
            c.append(self.cards.pop(0))
        return c
class Card(object):
    actions = { }
    @staticmethod
    def assignCardBack(image):
        Card.cardBack = image
# subclassed cards
class Duke(Card):
    name = "Duke"
    actions = {"Tax"}
    @staticmethod
    def assignCardFront(image):
        Duke.cardFront = image
    @staticmethod
    def canDoAction(actionName):
        if actionName in Duke.actions:
            return True
        else:
            return False
class Captain(Card):
    name = "Captain"
    actions = {"Steal"}
    @staticmethod
    def assignCardFront(image):
        Captain.cardFront = image
    @staticmethod
    def canDoAction(actionName):
        if actionName in Captain.actions:
            return True
        else:
            return False

class Ambassador(Card):
    name = "Ambassador"
    actions = {"Swap Influence"}
    @staticmethod
    def assignCardFront(image):
        Ambassador.cardFront = image
    @staticmethod
    def canDoAction(actionName):
        if actionName in Ambassador.actions:
            return True
        else:
            return False

class Assassin(Card):
    name = "Assassin"
    actions = {"Assassinate"}
    @staticmethod
    def assignCardFront(image):
        Assassin.cardFront = image
    @staticmethod
    def canDoAction(actionName):
        if actionName in Assassin.actions:
            return True
        else:
            return False

class Contessa(Card):
    name = "Contessa"
    @staticmethod
    def assignCardFront(image):
        Contessa.cardFront = image
    @staticmethod
    def canDoAction(actionName):
        if actionName in Contessa.actions:
            return True
        else:
            return False

### Player Class
class Player(object):
    width = 80
    height= 110
    def __init__(self, name, card1, card2, cx, cy, show):
        self.show = show
        self.name = name
        self.cx = cx
        self.cy = cy
        self.x1, self.y1 = self.cx - Player.width/2, self.cy - Player.height/2
        self.x2, self.y2 = self.cx + Player.width/2, self.cy + Player.height/2
        self.numCards = 2
        self.card1 = card1
        self.card2 = card2
        self.coins = 2
    def canDoAction(self, move):
        if ((self.card1 != None and self.card1.canDoAction(move)) or 
            (self.card2!= None and self.card2.canDoAction(move))):
            return True
        else:
            return False
    def takeIncome(self):
        if self.coins < 10:
            self.coins += 1
    def takeForeignAid(self):
        if self.coins < 10:
            self.coins += 2
    def tax(self):
        if self.coins<10:
            self.coins += 3
    def steal(self, target):
        if target.coins > 0 and self.coins < 10:
            self.coins += 2
            target.coins -= 2
    def blindCards(self):
        self.card1 = None
        self.card2 = None
    def swapInfluence(self):
        self.blindCards()
    def assassinate(self, target):
        if self.coins >= 3:
            self.coins -= 3
            target.card1 = None
            target.numCards -= 1
    def coup(self, target):
        if self.coins >= 7:
            self.coins -= 7
            target.card1 = None
            target.numCards -= 1
    def chooseCards(self, cards):
        self.card1 = cards[0]
        self.card2 = cards[1]
    
### Human Player Class
class HumanPlayer(Player):
    def loseInfluence(self, name):
        self.numCards -= 1
        if self.card1.name == name:
            card = self.card1
            self.card1 = None
        else:
            card = self.card2
            self.card2 = None
        return card
        
### Computer Class
class ComputerPlayer(Player):
    ### Predicts 5 steps ahead
    prevMoves = {"Player" : [ ],
                "CP1" : [ ] }
    gameStatesSeen = []
    cardProbabilities = {"Duke": 0,
                        "Captain": 0,
                        "Ambassador": 0,
                        "Assassin": 0,
                        "Contessa": 0
                        }
    playerCard1 = ""
    playerCard2 = ""
    def loseInfluence(self):
        if self.numCards == 1:
            card = self.card1
            self.card1 = None
            self.numCards -= 1
            return card
        else:
            index = random.randint(0,1)
            if index == 0:
                card = self.card1
                self.card1 = self.card2
                self.card2 = None
                self.numCards -= 1
                return card
            else:
                card = self.card2 
                self.card2 = None
                self.numCards -= 1
                return card
    def updatePlayerCards(self, move):
        # keeps track of what they think the player has
        # apply this whenever player turn ends
        if move == "Swap Influence":
            ComputerPlayer.cardProbabilities = {"Duke": 0,
                                                "Captain": 0,
                                                "Ambassador": 0,
                                                "Assassin": 0,
                                                "Contessa": 0
                                                }
            ComputerPlayer.playerCard1 = ""
            ComputerPlayer.playerCard2 = ""
        else:
            if Duke.canDoAction(move):
                ComputerPlayer.cardProbabilities["Duke"] += 1
            elif Captain.canDoAction(move):
                ComputerPlayer.cardProbabilities["Captain"] += 1
            elif Ambassador.canDoAction(move):
                ComputerPlayer.cardProbabilities["Ambassador"] += 1
            elif Assassin.canDoAction(move):
                ComputerPlayer.cardProbabilities["Assassin"] += 1
            elif Contessa.canDoAction(move):
                ComputerPlayer.cardProbabilities["Contessa"] += 1
            max1 = 0
            max1Key = ""
            max2 = 0
            max2Key = ""
            for key in ComputerPlayer.cardProbabilities:
                if key != self.card1 and key != self.card2:
                    val = ComputerPlayer.cardProbabilities[key] 
                    if val > max1:
                        max2 = max1
                        max1 = val
                        max2Key = max1Key
                        max1Key = key
                    elif val > max2:
                        max2 = val
                        max2Key = key
            ComputerPlayer.playerCard1 = max1Key
            ComputerPlayer.playerCard2 = max2Key
    @staticmethod
    def addState(state):
        ComputerPlayer.gameStatesSeen.append(state)
    def getAction(self):
        depth = 4
        tree = self.gameStatesSeen[-1]
        self.makeTree(tree, depth)
        moves, payoff = self.minimax(tree, True, depth)
        index = random.randint(0,len(moves)-1)
        return moves[index]
    def minimax(self, tree, isMax, depth):
        # for minimax -> cp1 wants max, p1 wants min
        if depth == 0:
            result = ([tree.move], tree.overallPayoff)
        else:
            if isMax:
                maximumMoves = [ ]
                maximum = None
                for state in tree.potentialStates:
                    moves, payoff = self.minimax(state, not isMax, depth-1)
                    if maximum == None or payoff > maximum:
                        maximumMoves = [state.move]
                        maximum = payoff
                    elif payoff == maximum:
                        maximumMoves.append(state.move)
                result = (maximumMoves, maximum)
            elif not isMax:
                minimumMoves = [ ]
                minimum = None
                for state in tree.potentialStates:
                    moves, payoff = self.minimax(state, not isMax, depth-1)
                    if minimum == None or payoff < minimum:
                        mimimumMoves = [state.move]
                        minimum = payoff
                    elif payoff == minimum:
                        minimumMoves.append(state.move)
                result = (minimumMoves, minimum)
        return result
    def makeTree(self, state0, depth):
        if depth==0:
            return None
        else:
            state0.createPotentialStates()
            for state1 in state0.potentialStates:
                self.makeTree(state1, depth - 1)
    def challenge(self, move):
        # bases challenges on what probability says the other player has
        if Duke.canDoAction(move):
            if ((ComputerPlayer.playerCard1 == "Duke" or ComputerPlayer.playerCard2 == "Duke") or
                (ComputerPlayer.playerCard1 == "" or ComputerPlayer.playerCard2 == "")):
                return False
        elif Captain.canDoAction(move):
            if ((ComputerPlayer.playerCard1 == "Captain" or ComputerPlayer.playerCard2 == "Captain") or
                (ComputerPlayer.playerCard1 == "" or ComputerPlayer.playerCard2 == "")) :
                return False
        elif Ambassador.canDoAction(move):
           if ((ComputerPlayer.playerCard1 == "Ambassador" or ComputerPlayer.playerCard2 == "Ambassador") or
                (ComputerPlayer.playerCard1 == "" or ComputerPlayer.playerCard2 == "")) :
                return False
        elif Assassin.canDoAction(move):
            if ((ComputerPlayer.playerCard1 == "Assassin" or ComputerPlayer.playerCard2 == "Assassin") or
                (ComputerPlayer.playerCard1 == "" or ComputerPlayer.playerCard2 == "")) :
                return False
        elif Contessa.canDoAction(move):
            if ((ComputerPlayer.playerCard1 == "Contessa" or ComputerPlayer.playerCard2 == "Contessa") or
                (ComputerPlayer.playerCard1 == "" or ComputerPlayer.playerCard2 == "")) :
                return False
        return True 
class Button(object):
    def __init__(self, text, x1, y1, x2, y2):
        self.textx, self.texty = (x1+x2)/2, (y1+y2)/2
        self.text = text
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.isActive = True
    def __hash__(self):
        return hash(self.text)
    def __eq__(self, other):
        return isinstance(other, Button) and self.text == other.text
class ButtonList(object):
    def __init__(self, isActive, L):
        self.isActive = isActive
        self.L = L
class GameState(object):
    moves = ["Take Income", "Take Foreign Aid", "Tax", "Steal", "Swap Influence", "Assassinate", "Coup"]
    def __init__(self, players, deck, turn, move=None):
        ### the turn that does the move if inputted
        self.turn = (turn-1)%2
        self.move = move
        ### the turn that is going to go next
        self.nextTurn = turn
        self.players = copy.deepcopy(players)
        self.player1 = copy.copy(players[0])
        self.player1.blindCards()
        self.CP1 = copy.copy(players[1])
        self.deck = copy.copy(deck)
        self.processMove(move)
        self.calcPayoff()
    def __repr__(self):
        return f"{self.nextTurn} and {self.overallPayoff}"
        
    def calcPayoff(self):
        if self.move == None:
            return
        else:
            payoffP1 = self.player1.coins + 10*self.player1.numCards
            payoffCP1 = self.CP1.coins + 10*self.CP1.numCards
            self.overallPayoff = payoffCP1 - payoffP1
            if self.turn == 1:
                if not self.CP1.canDoAction(self.move):
                    self.overallPayoff -= 75
                if self.move == "Swap Influence":
                    self.overallPayoff += 50
    def processMove(self, move):
        if self.turn == 0:
            activePlayer = self.player1
            target = self.CP1
        else:
            activePlayer = self.CP1
            target = self.player1
        # "Take Income"
        if move == self.moves[0]:
            activePlayer.takeIncome()
        # "Take Foreign Aid"
        elif move == self.moves[1]:
            activePlayer.takeForeignAid()
        # "Tax"
        elif move == self.moves[2]:
            activePlayer.tax()
        # "Steal"
        elif move == self.moves[3]:
            activePlayer.steal(target)
        # "Swap Influence"
        elif move == self.moves[4]:
            activePlayer.swapInfluence()
        # "Assassinate"
        elif move == self.moves[5]:
            activePlayer.assassinate(target)
        # "Coup"
        elif move == self.moves[6]:
            activePlayer.coup(target)
    def isValidMove(self, move):
        # "Take Income"
        currentPlayer = self.players[self.turn]
        if move == self.moves[0]:
            if currentPlayer.coins < 10:
                return True
        # "Take Foreign Aid"
        elif move == self.moves[1]:
            if currentPlayer.coins < 10:
                return True
        # "Tax"
        elif move == self.moves[2]:
            if currentPlayer.coins < 10:
                return True
        # "Steal"
        elif move == self.moves[3]:
            if currentPlayer.coins < 10 and self.CP1.coins >= 2:
                return True
        # "Swap Influence"
        elif move == self.moves[4]:
            return True
        # "Assassinate"
        elif move == self.moves[5]:
            if currentPlayer.coins >= 3:
                return True
        # "Coup"
        elif move == self.moves[6]:
            if currentPlayer.coins >= 7:
                return True
        return False
    def createPotentialStates(self):
        self.potentialStates = [ ]
        for move in GameState.moves:
            if self.isValidMove(move):
                newState = GameState([self.player1, self.CP1], self.deck, self.nextTurn, move)
                self.potentialStates.append(newState)
    
