# This file deals with the animations/graphics of the game

# Copied from: http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

from tkinter import *
import math, copy, random
from TPClasses import *
from TPMultiplayerMode import *
class SplashScreen(Mode):
    def appStarted(self):
        cx = self.app.width/2
        cy = self.app.height*(3/4)
        marginFromCenter = 30
        margin1 = 40
        margin2 = 20
        buttonWidth = 100
        buttonHeight = 40
        x1Multi, y1Multi = cx - marginFromCenter - buttonWidth, cy
        x2Multi, y2Multi =  x1Multi + buttonWidth, y1Multi+ buttonHeight
        x1CPU, y1CPU = cx + marginFromCenter, y1Multi
        x2CPU, y2CPU = x1CPU + buttonWidth, y1CPU + buttonHeight
        self.multiplayerButton = Button("Multiplayer", x1Multi, y1Multi, x2Multi, y2Multi)
        self.computerButton = Button("Computer", x1CPU, y1CPU, x2CPU, y2CPU)
    def mousePressed(self, event):
        if self.isPressingButton(event.x, event.y, self.multiplayerButton):
            self.app.setActiveMode(self.app.multiplayerMode)
        elif self.isPressingButton(event.x, event.y, self.computerButton):
            self.app.setActiveMode(self.app.gameMode)
    def redrawAll(self, canvas):
        margin1 = 40
        margin2 = 20
        canvas.create_rectangle(margin2, margin2, 
            self.app.width-margin2, self.app.height-margin2, 
            fill="#969696", width=0)
        canvas.create_rectangle(margin1, margin1, 
            self.app.width-margin1, self.app.height-margin1, 
            fill="#323232", width=0)
        canvas.create_text(self.app.width/2, self.app.height/8,
            anchor="ne", font="system 30", fill="white",
            text="Welcome to...")
        canvas.create_text(self.app.width/2, self.app.height/3,
            anchor="c", font="system 80 bold", fill="white",
            text="COUP")
        canvas.create_text(self.app.width/2, self.app.height*(5/8),
            anchor="c", width=400, font="system 25", fill="white",
            text="Goal: Make the other players lose their influence (cards)")
        self.drawButton(canvas, self.multiplayerButton)
        self.drawButton(canvas, self.computerButton)
    def drawButton(self, canvas, button):
        canvas.create_rectangle(button.x1, button.y1, 
            button.x2, button.y2, fill="white")
        canvas.create_text(button.textx, button.texty, 
            anchor="c", fill="black", font="system 20",
            text=button.text)
    def isPressingButton(self, x, y, button):
        return ((button.x1 <= x <= button.x2) and
            (button.y1 <= y <= button.y2))

class WinScreen(Mode):
    def redrawAll(self, canvas):
        margin1 = 40
        margin2 = 20
        canvas.create_rectangle(margin2, margin2, 
            self.app.width-margin2, self.app.height-margin2, 
            fill="#969696", width=0)
        canvas.create_rectangle(margin1, margin1, 
            self.app.width-margin1, self.app.height-margin1, 
            fill="#323232", width=0)
        canvas.create_text(self.app.width/2, self.app.height/3,
            anchor="c", font="system 80 bold", fill="#497f15",
            text="YOU WIN")
class LoseScreen(Mode):
    def redrawAll(self, canvas):
        margin1 = 40
        margin2 = 20
        canvas.create_rectangle(margin2, margin2, 
            self.app.width-margin2, self.app.height-margin2, 
            fill="#969696", width=0)
        canvas.create_rectangle(margin1, margin1, 
            self.app.width-margin1, self.app.height-margin1, 
            fill="#323232", width=0)
        canvas.create_text(self.app.width/2, self.app.height/3,
            anchor="c", font="system 80 bold", fill="#a33a3a",
            text="YOU LOSE")
class HelpMode(Mode):
    def appStarted(self):
        self.isPage1 = True
        self.isPage2 = False
        marginx = (1/50)*self.app.width
        marginy = (1/50)*self.app.height
        sidey = (3/50)*self.app.height
        sidex = (6/50)*self.app.width
        topLeftx = self.app.width - sidex - marginx
        topLefty = self.app.height - sidey - marginy
        self.page1Button = Button("Next", topLeftx, topLefty, 
            topLeftx + sidex, topLefty + sidey)
        x1, y1 = marginx, topLefty
        x2, y2 = x1 + sidex, y1 + sidey
        self.page2Button = Button("Back", x1, y1, x2, y2)
        self.text1 = "This is Coup, a game of lying and deception. \nThe goal of the game\
is to get rid of the other player's influence. \nThere is a list of actions \
you can take to achieve this goal. The twist is that you can take actions \
that are not associated with the cards you have. This is why there is a \
challenge option in which you can make the opponent lose influence. \
However, if you are wrong you will have to lose influence."
        self.text2 = "Here are the roles and their possible actions:\n\n\
General Actions:\n\
Take Income - Get 1 coins\n\
Take Foreign Aid - Get 2 coins\n\
Coup - Pay 7 coins to make opponent lose influence\n\
\n\
Roles:\n\
Duke\t\tTax - Get 3 coins\n\
Captain\t\tSteal - Take 2 coins from opponent\n\
Ambassador\tSwap Influence - Look at 2 cards in\n\
\t\tthe deck and swap them if you want\n\
Assassin\t\tAssassinate - Pay 3 coins to make\n\
\t\topponent lose influence\n\
Contessa\t\tNo Special Action"
    def redrawAll(self, canvas):
        margin1 = 40
        margin2 = 20
        textWidth = 410
        x1 = (self.app.width - textWidth)/2
        y1 = 50
        canvas.create_rectangle(margin2, margin2, 
            self.app.width-margin2, self.app.height-margin2, 
            fill="#969696", width=0)
        canvas.create_rectangle(margin1, margin1, 
            self.app.width-margin1, self.app.height-margin1, 
            fill="#323232", width=0)
        if self.isPage1:
            canvas.create_text(x1, y1,
                anchor="nw", font="system 15 ", 
                fill="white", width=textWidth,
                text=self.text1)
            self.drawButton(canvas, self.page1Button)
        elif self.isPage2:
            canvas.create_text(x1, y1,
                anchor="nw", font="system 15", 
                fill="white", width=textWidth,
                text=self.text2)
            self.drawButton(canvas, self.page2Button)
        
        canvas.create_text(self.app.width/2, self.app.height*(5/6),
            anchor="c", font="system 15 ", 
            fill="white", width=textWidth,
            text="Press 'Enter' to go back to your game")
    def mousePressed(self, event):
        if self.isPage1:
            if self.isPressingButton(event.x, event.y, self.page1Button):
                self.isPage1 = False
                self.isPage2 = True
        elif self.isPage2:
            if self.isPressingButton(event.x, event.y, self.page2Button):
                self.isPage2 = False
                self.isPage1 = True
    def drawButton(self, canvas, button):
        canvas.create_rectangle(button.x1, button.y1, 
            button.x2, button.y2, fill="black")
        canvas.create_text(button.textx, button.texty, 
            anchor="c", fill="white", font="system 25",
            text=button.text)

    def isPressingButton(self, x, y, button):
        return ((button.x1 <= x <= button.x2) and
            (button.y1 <= y <= button.y2))
    def keyPressed(self, event):
        if event.key == "Enter":
            self.app.setActiveMode(self.app.gameMode)

class GameMode(Mode):
    def appStarted(self):
        self.font = "system"
        self.setupImages()
        self.isGameOver = False
        self.timerDelay = 2000
        self.turn = 0 
        self.moves = ["Take Income", "Take Foreign Aid", "Tax", "Steal", "Swap Influence", "Assassinate", "Coup"]
        self.blocks = ["Block Foreign Aid", "Block Steal", "Block Assassination", "Challenge"]
        self.deck = Deck()
        self.deck.shuffle()
        numPlayers = 2
        self.createHelp()
        self.setUpGame(numPlayers)
        self.isChoosingAction = False
        self.choiceButtons = self.createButtons(self.moves)
        self.isChoosingPlayer = False
        playerNames = [ ]
        for player in self.players:
            playerNames.append(player.name)
        self.playerButtons = self.createButtons(playerNames)
        self.isExchangingCards = False
        self.cardButtons = ButtonList(False, [])
        L = ["Yes", "No"]
        self.challengeButtons = self.createButtons(L)
        self.isShowingComputerAction = False
        self.isAskingChallenge = False
        self.isShowingLostCard = False
        self.isCPChallenge = False
        self.loseCardButtons = None
        self.lostCard = None
        self.isChoosingLostCard = False
        self.currentChallenge = ""
        self.currentState = GameState(self.players, self.deck, self.turn)
        ComputerPlayer.addState(self.currentState)
        self.currentMove = ""
    def setupImages(self):
        path = "cards"
        # Copied from: http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
        # and http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#spritesheetsWithCropping
        # with edits
        for filename in os.listdir(path):
            if ".jpg" in filename:
                image = self.loadImage(path + os.sep + filename)
                image = self.scaleImage(image, 1/2)
                if filename == "cardBack.jpg":
                    Card.assignCardBack(image)
                elif filename == "ambassador.jpg":
                    Ambassador.assignCardFront(image)
                elif filename == "assassin.jpg":
                    Assassin.assignCardFront(image)
                elif filename == "captain.jpg":
                    Captain.assignCardFront(image)
                elif filename == "contessa.jpg":
                    Contessa.assignCardFront(image)
                elif filename == "duke.jpg":
                    Duke.assignCardFront(image)
    def checkGameOver(self):
        if self.players[0].numCards == 0:
            self.app.setActiveMode(self.app.loseScreen)
        elif self.players[1].numCards == 0:
            self.app.setActiveMode(self.app.winScreen)
    def createButtons(self, L): 
        buttons = [ ]
        startx = (1/6 + 1/50)*self.app.width
        starty = (1/6 + 5/50)*self.app.height
        endx = (5/6 - 1/50)*self.app.width
        endy = (5/6 - 3/50)*self.height
        increment = (endy - starty)/len(L)
        for i in range(len(L)):
            y1 = starty+increment*i
            y2 = starty+increment*(i+1)
            newButton = Button(L[i], startx, y1, endx, y2)
            buttons.append(newButton)
        return ButtonList(False, buttons)
    def createHelp(self):
        marginx = (1/50)*self.app.width
        marginy = (1/50)*self.app.height
        sidey = (3/50)*self.app.height
        sidex = (6/50)*self.app.width
        topLeftx = self.app.width - sidex - marginx
        topLefty = self.app.height - sidey - marginy
        self.help = Button("Help", topLeftx, topLefty, 
            topLeftx + sidex, topLefty + sidey)
    def setUpGame(self, numPlayers):
        self.players = [ ]
        card1, card2 = self.deck.removeCards(2)
        self.players.append(HumanPlayer("You", card1, card2, self.app.width/2, self.app.height*(5/6), True))
        card1, card2 = self.deck.removeCards(2)
        self.players.append(ComputerPlayer("CP1", card1, card2, self.app.width/2, self.app.height*(1/6), False))
    def mousePressed(self, event):
        # do action at end of sequence in pressed
        # checks if pressing help
        if self.isPressingButton(event.x, event.y, self.help):
            self.app.setActiveMode(self.app.helpMode)
        elif self.turn == 0:
            if self.isChoosingAction:
                # self.moves = ["Take Income", "Take Foreign Aid", "Tax", "Steal", "Swap Influence", "Assassinate", "Coup"]
                # "Take Income"
                move = self.moves[0]
                button = self.choiceButtons.L[0]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
                # "Take Foreign Aid"
                move = self.moves[1]
                button = self.choiceButtons.L[1]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
                # "Tax"
                move = self.moves[2]
                button = self.choiceButtons.L[2]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
                # "Steal"
                move = self.moves[3]
                button = self.choiceButtons.L[3]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
                # "Swap Influence"
                move = self.moves[4]
                button = self.choiceButtons.L[4]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
                # "Assassinate"
                move = self.moves[5]
                button = self.choiceButtons.L[5]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
                # "Coup"
                move = self.moves[6]
                button = self.choiceButtons.L[6]
                if self.isPressingButton(event.x, event.y, button):
                    if self.isValidMove(move):
                        self.currentMove = move
            elif self.isChoosingPlayer:
                # self.isChoosingAction = False
                target = None
                while(target == None):
                    target = self.pickPlayer(event)
                self.doAction(target)
            elif self.isExchangingCards:
                self.players[0].card1, self.players[0].card2 = self.pickCard(event)
                self.doAction()
            elif self.isChoosingLostCard:
                for button in self.loseCardButtons.L:
                    if self.isPressingButton(event.x, event.y, button):
                        cardName = button.text
                        self.players[0].loseInfluence(cardName)
        elif self.turn == 1:
            if self.isAskingChallenge:
                # "Yes"
                button = self.challengeButtons.L[0]
                if self.isPressingButton(event.x, event.y, button):
                    self.currentChallenge = button.text
                # "No"
                button = self.challengeButtons.L[1]
                if self.isPressingButton(event.x, event.y, button):
                    self.currentChallenge = button.text
            elif self.isChoosingLostCard:
                for button in self.loseCardButtons.L:
                    if self.isPressingButton(event.x, event.y, button):
                        cardName = button.text
                        self.players[0].loseInfluence(cardName)

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
            if currentPlayer.coins < 10:
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
####make while loop and return list of cards
    def pickCard(self, event):
        result = set()
        cardNames = []
        for card in self.cardsToShow:
            if card != None:
                cardNames.append(card.name)
        for i in range(len(self.cardButtons.L)):
            button = self.cardButtons.L[i]
            if self.isPressingButton(event.x, event.y, button):
                if self.players[0].numCards == 2:
                    name1, name2 = button.text.split(", ")
                    card1 = self.cardsToShow[cardNames.index(name1)]
                    card2 = self.cardsToShow[cardNames.index(name2)]
                    L = [card1, card2]
                else:
                    name = button.text
                    card = self.cardsToShow[cardNames.index(name)]
                    L = [card, None]
        return L
    def createCardButtons(self):
        cardButtons = [ ]
        startx = (1/6 + 1/50)*self.app.width
        starty = (1/6 + 3/50)*self.app.height
        endx = (5/6 - 1/50)*self.app.width
        endy = (5/6 - 3/50)*self.height
        n = len(self.cardsToShow)
        k = self.players[0].numCards
        numButtons = int(math.factorial(n)/(math.factorial(k)*math.factorial(n - k)))
        increment = (endy - starty)/numButtons
        buttonTexts = [ ]
        if self.players[0].numCards == 2:
            for i in range(len(self.cardsToShow)-1):
                for j in range(i+1, len(self.cardsToShow)):
                    text = self.cardsToShow[i].name + ", " + self.cardsToShow[j].name
                    buttonTexts.append(text)
        else:
            for i in range(len(self.cardsToShow)):
                if self.cardsToShow[i] != None:
                    text = self.cardsToShow[i].name
                    buttonTexts.append(text)
                else:
                    numButtons -= 1
        for i in range(numButtons):
            y1 = starty+increment*i
            y2 = starty+increment*(i+1)
            newButton = Button(buttonTexts[i], startx, y1, endx, y2)
            cardButtons.append(newButton)
        self.cardButtons = ButtonList(False, cardButtons)
    ### ends turn at the end of doAction
    def doAction(self, target=None):
        # self.moves = ["Take Income", "Take Foreign Aid", "Tax", "Steal", "Swap Influence", "Assassinate", "Coup"]
        ComputerPlayer.prevMoves["Player"].append(self.currentMove)
        # "Take Income"
        if self.currentMove == self.moves[0]:
            self.isChoosingAction = False
            self.players[0].takeIncome()
        # "Take Foreign Aid"
        elif self.currentMove == self.moves[1]:
            self.isChoosingAction = False
            self.players[0].takeForeignAid()
        # "Tax"
        elif self.currentMove == self.moves[2]:
            self.isChoosingAction = False
            self.players[0].tax()
        # "Steal"
        elif self.currentMove == self.moves[3]:
            self.players[0].steal(target)
            self.isChoosingPlayer = False
        # "Swap Influence"
        elif self.currentMove == self.moves[4]:
            self.isExchangingCards = False
        # "Assassinate"
        elif self.currentMove == self.moves[5]:
            self.players[0].assassinate(target)
            self.isChoosingPlayer = False
        # "Coup"
        elif self.currentMove == self.moves[6]:
            self.players[0].coup(target)
            self.isChoosingPlayer = False
        self.endTurn()
    def pickPlayer(self, event):
        for i in range(len(self.players)):
            button = self.playerButtons.L[i]
            if button.text != self.players[self.turn].name:
                if self.isPressingButton(event.x, event.y, button):
                    name = button.text
                    for p in self.players:
                        if name == p.name:
                            return p 
    def isPressingButton(self, x, y, button):
        return ((button.x1 <= x <= button.x2) and
            (button.y1 <= y <= button.y2))
    def mouseReleased(self, event):
        if self.turn == 0:
            if self.isChoosingAction:
                # check to see if the computers if any want to challenge
                generalMoves = ["Take Income", "Take Foreign Aid", "Coup"]
                if self.currentMove not in generalMoves:
                    challengingCP = [ ]
                    for cp in self.players[1:]:
                        isChallenging = cp.challenge(self.currentMove)
                        if isChallenging:
                            self.isCPChallenge = isChallenging
                            challengingCP.append(cp)
                    # yes, computer player is challenging
                    if self.isCPChallenge:
                        index = random.randint(0, len(self.players)-2)
                        cpPlayers = self.players[1:]
                        self.challengingCP = cpPlayers[index]
                        # if player can do the action
                        if self.players[0].canDoAction(self.currentMove):
                            self.lostCard = self.challengingCP.loseInfluence()
                            self.continueAction()
                            self.isShowingLostCard = True
                        # if player cant do the action
                        else:
                            self.isChoosingAction = False
                            L = self.makeCardList(self.players[0])
                            self.loseCardButtons = self.createButtons(L)
                            self.isChoosingLostCard = True
                    # if no challenge, continue
                    else:
                        self.continueAction()
                # if its a general move continue
                else:
                    self.continueAction()
            elif self.isExchangingCards:
                pass
            elif self.isChoosingLostCard:
                self.isChoosingLostCard = False
                self.endTurn()
        if self.turn == 1:
            if self.isAskingChallenge:
                if self.currentChallenge == "Yes":
                    cp = self.players[self.turn]
                    # incorrect challenge - player loses card, computer
                    if cp.canDoAction(self.currentMove):
                        # prompt player to choose a card to be rid of
                        self.isChoosingLostCard = True
                        player = self.players[0]
                        L = self.makeCardList(player)
                        self.loseCardButtons = self.createButtons(L)
                        self.isAskingChallenge = False
                    # correct challenge - computer loses card
                    else:
                        self.lostCard = cp.loseInfluence()
                        self.isAskingChallenge = False
                        ##### new situation
                        self.isShowingLostCard = True
                        
                elif self.currentChallenge == "No":
                    self.isAskingChallenge = False
                    target = self.players[0]
                    self.doComputerAction(target)
                    ###end of cp turn
                    self.endTurn()
                    #### redrawall say press enter to move on
            elif self.isChoosingLostCard:
                self.isChoosingLostCard = False
                self.endTurn()
    def makeCardList(self, player):
        L = []
        if player.card2 != None:
            L = [player.card1.name, player.card2.name]
        else:
            L = [player.card1.name]
        return L
    def continueAction(self):
        if self.currentMove == self.moves[0]:
            self.doAction()
        elif self.currentMove == self.moves[1]:
            self.doAction()
        elif self.currentMove == self.moves[2]:
            self.doAction()
        elif self.currentMove == self.moves[3]:
            self.isChoosingAction = False
            self.isChoosingPlayer = True
        # "Swap Influence"
        elif self.currentMove == self.moves[4]:
            self.isChoosingAction = False
            self.cardsToShow = self.deck.removeCards(self.players[0].numCards) + [self.players[0].card1, self.players[0].card2]
            self.createCardButtons()
            self.isExchangingCards = True
        elif self.currentMove == self.moves[5]:
            self.isChoosingAction = False
            self.isChoosingPlayer = True
        elif self.currentMove == self.moves[6]:
            self.isChoosingAction = False
            self.isChoosingPlayer = True

    def keyPressed(self, event):
        ### these are shortcuts to the winscreen and lose screen
        if event.key == "q":
            self.app.setActiveMode(self.app.winScreen)
        elif event.key == "w":
            self.app.setActiveMode(self.app.loseScreen)
        if self.turn == 0:
            if event.key == "Enter":
                self.isChoosingAction = True
                self.isShowingComputerAction = False
        elif self.turn == 1:
            if event.key == "Enter":
                if self.isShowingComputerAction:
                    pass
                elif self.isAskingChallenge:
                    pass
                else:
                    #computer does its actions
                    cp = self.players[self.turn]
                    self.currentMove = cp.getAction()       
    def keyReleased(self, event):
        if self.turn == 0:
            self.isShowingComputerAction = False
        elif self.turn == 1:
            if event.key == "Enter":
                if self.isShowingLostCard:
                    self.endTurn()
                    self.isShowingLostCard = False
                elif self.isShowingComputerAction:
                    self.isShowingComputerAction = False
                    self.isAskingChallenge = True
                else:
                    self.isShowingComputerAction = True
    def doComputerAction(self, target=None):
        # self.moves = ["Take Income", "Take Foreign Aid", "Tax", "Steal", "Swap Influence", "Assassinate", "Coup"]
        ComputerPlayer.prevMoves["CP1"].append(self.currentMove)
        # "Take Income"
        if self.currentMove == self.moves[self.turn]:
            self.players[self.turn].takeIncome()
        # "Take Foreign Aid"
        elif self.currentMove == self.moves[1]:
            self.players[self.turn].takeForeignAid()
        # "Tax"
        elif self.currentMove == self.moves[2]:
            self.players[self.turn].tax()
        # "Steal"
        elif self.currentMove == self.moves[3]:
            self.players[self.turn].steal(target)
        # "Swap Influence"
        elif self.currentMove == self.moves[4]:
            self.cardsToShow = self.deck.removeCards(self.players[1].numCards) + [self.players[1].card1, self.players[1].card2]
            cp = self.players[self.turn]
            cp.chooseCards(self.cardsToShow)
        # "Assassinate"
        elif self.currentMove == self.moves[5]:
            target.card2 = None
            target.numCards -= 1
            self.players[self.turn].coins -= 3
        # "Coup"
        elif self.currentMove == self.moves[6]:
            self.players[self.turn].coup(target)
    def endTurn(self):
        self.challengingCP = False
        self.isCPChallenge = False
        universalMoves = {"Take Income", "Take Foreign Aid", "Coup"}
        if self.turn == 0:
            if self.currentMove not in universalMoves:
                self.players[1].updatePlayerCards(self.currentMove)
        self.currentMove = ""
        newState = GameState(self.players, self.deck, self.turn)
        ComputerPlayer.addState(newState)
        self.checkGameOver()
        self.turn = (self.turn + 1)%len(self.players)
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.app.width, self.app.height, 
            fill="#969696", width=0)
        self.drawDeckAndBank(canvas)
        for player in self.players:
           self.drawPlayer(canvas, player)
        self.drawHelp(canvas) 
        if self.turn == 0:
            if self.isChoosingAction or self.isChoosingPlayer or self.isExchangingCards:
                self.drawChoicesPanel(canvas)
            elif self.isChoosingLostCard:
                self.drawChoicesPanel(canvas)
            else:
                canvas.create_text(self.app.width/2, self.app.height/2, 
                    font=f"{self.font} 15 bold", fill="black",
                    text="Press 'Enter' to go")
        elif self.turn == 1:
            if self.isShowingComputerAction:
                canvas.create_text(self.app.width/2, self.app.height/2, 
                    font=f"{self.font} 15 bold", fill="black",
                    text="Press 'Enter'")
                text = f"{self.players[1].name} wants to do action: {self.currentMove}"
                canvas.create_text(self.app.width/2, self.app.height*(5/8), 
                    text=text)
            elif self.isAskingChallenge:
                self.drawChoicesPanel(canvas)
            elif self.isChoosingLostCard:
                self.drawChoicesPanel(canvas)
            elif self.isShowingLostCard:
                canvas.create_text(self.app.width/2, self.app.height/2, 
                    font=f"{self.font} 15 bold", fill="black",
                    text="Press 'Enter'")
                if self.isCPChallenge:
                    text = f"{self.challengingCP.name} was wrong, they got rid of {self.lostCard.name}"
                else:
                    text = f"You were right! {self.players[1].name} got rid of {self.lostCard.name}"
                canvas.create_text(self.app.width/2, self.app.height*(5/8), 
                    font=f"{self.font} 15 bold", fill="black",
                    text=text)
            else:
                canvas.create_text(self.app.width/2, self.app.height/2, 
                font=f"{self.font} 15 bold", fill="black",
                text="Press 'Enter' to make the next player go")
    def drawDeckAndBank(self, canvas):
        cx = self.app.width/2
        cy = self.app.height/2
        marginFromCenter = (1/25)*self.app.width
        deckImage = self.deck.cards[0].cardBack
        deckImage = self.scaleImage(deckImage, 1/2)
        cardWidth, cardHeight = deckImage.size
        canvas.create_image(cx-cardWidth/2-marginFromCenter, cy,
            anchor="c",
            image=ImageTk.PhotoImage(deckImage))
        canvas.create_text(cx-cardWidth/2-marginFromCenter, cy-cardHeight/2-marginFromCenter,
            anchor="c", font=f"{self.font} 10 bold", 
            text="Deck")
        r = 25
        
        canvas.create_oval(cx+marginFromCenter, cy-r, 
            cx+marginFromCenter+r*2, cy+r, 
            width=0, fill="yellow")
        canvas.create_text(cx+marginFromCenter+r, cy-marginFromCenter-r, 
            anchor="c", fill="black", font=f"{self.font} 10 bold",
            text="Bank")
    def drawChoicesPanel(self, canvas):
        # creates general choice panel
        panelx1 = (1/6)*self.app.width
        panely1 = (1/6)*self.app.height
        panelx2 = (5/6)*self.app.width
        panely2 = (5/6)*self.app.height
        canvas.create_rectangle(panelx1, panely1,
            panelx2, panely2, 
            fill="white", outline="black", width=5)
        ### dont need this
        startx = panelx1 + (1/50)*self.app.width
        starty = panely1 + (5/50)*self.app.height
        endx = panelx2 - (1/50)*self.app.width
        endy = panely2 - (3/50)*self.app.height
        textx = self.app.width/2
        texty = (1/6+2/50)*self.app.height
        # is in the choosing player state
        if self.isChoosingPlayer:
            canvas.create_text(textx, texty, anchor="c", text="Who do you choose?")
            self.drawPlayerChoices(canvas,startx, starty, endx, endy)
        # is in choosing action state
        elif self.isChoosingAction:
            canvas.create_text(textx, texty, anchor="c", text="What do you do?")
            self.drawActionChoices(canvas, startx, starty, endx, endy)
        elif self.isExchangingCards:
            canvas.create_text(textx, texty, anchor="c", text="What is your new hand?")
            self.drawCardChoices(canvas, startx, starty, endx, endy)
        elif self.isAskingChallenge:
            canvas.create_text(textx, texty, anchor="c", text="Do you want to challenge?")
            self.drawChallengeChoices(canvas, startx, starty, endx, endy)
        elif self.isChoosingLostCard:
            if self.isCPChallenge:
                text = "CP1 has successfully challenged you\nWhich card do you lose?"
            else:
                text = "Which card do you lose?"
            canvas.create_text(textx, texty, anchor="c", text=text)
            self.drawLoseCardChoices(canvas, startx, starty, endx, endy)
    def drawLoseCardChoices(self, canvas, startx, starty, endx, endy):
        increment = (endy - starty)/len(self.loseCardButtons.L)
        for i in range(len(self.loseCardButtons.L)):
            button = self.loseCardButtons.L[i]
            canvas.create_rectangle(button.x1, button.y1,
                button.x2, button.y2, fill="yellow" )
            canvas.create_text(button.textx, button.texty, 
                anchor="c", text=button.text)
    def drawChallengeChoices(self, canvas, startx, starty, endx, endy):
        increment = (endy - starty)/len(self.challengeButtons.L)
        for i in range(len(self.challengeButtons.L)):
            button = self.challengeButtons.L[i]
            canvas.create_rectangle(button.x1, button.y1,
                button.x2, button.y2, fill="yellow" )
            canvas.create_text(button.textx, button.texty, 
                anchor="c", text=button.text) 
    def drawCardChoices(self, canvas, startx, starty, endx, endy):
        increment = (endy - starty)/len(self.cardButtons.L)
        for i in range(len(self.cardButtons.L)):
            button = self.cardButtons.L[i]
            canvas.create_rectangle(button.x1, button.y1,
                button.x2, button.y2, fill="yellow" )
            canvas.create_text(button.textx, button.texty, 
                anchor="c", text=button.text) 
    def drawPlayerChoices(self, canvas, startx, starty, endx, endy):
        increment = (endy - starty)/len(self.players)
        for i in range(len(self.playerButtons.L)):
            if self.playerButtons.L[i].text != self.players[self.turn].name:
                button = self.playerButtons.L[i]
                canvas.create_rectangle(button.x1, button.y1,
                    button.x2, button.y2, fill="yellow" )
                canvas.create_text(button.textx, button.texty, 
                    anchor="c", text=button.text) 
    def drawActionChoices(self, canvas, startx, starty, endx, endy):
        increment = (endy - starty)/len(self.moves)
        for i in range(len(self.choiceButtons.L)):
            button = self.choiceButtons.L[i]
            canvas.create_rectangle(button.x1, button.y1,
                button.x2, button.y2, fill="yellow" )
            canvas.create_text(button.textx, button.texty, 
                anchor="c", text=button.text) 
    def drawHelp(self, canvas):
        canvas.create_rectangle(self.help.x1, self.help.y1, 
            self.help.x2, self.help.y2, fill="red")
        canvas.create_text(self.help.textx, self.help.texty, 
            anchor="c", fill="white", font="system 25",
            text=self.help.text)
    def drawPlayer(self,canvas, player):
        marginFromCenterx = (1/25)*self.app.width
        marginFromCentery = 30
        if player.cy < self.app.height/2:
            namey = player.cy - marginFromCentery
            coinsy = player.cy - 2*marginFromCentery
        else:
            namey = player.cy + marginFromCentery
            coinsy = player.cy + 2*marginFromCentery
        canvas.create_text(player.cx, namey, 
            anchor="c", font=f"{self.font} 15 bold", fill="white",
            text=player.name)
        canvas.create_text(player.cx, coinsy, 
            anchor="c", width=marginFromCenterx*2, 
            font=f"{self.font} 15 bold", fill="black",
            text=f"{player.coins} coins")
        if player.card1 != None:
            if player.show:
                image = player.card1.cardFront
                cardWidth, cardHeight = image.size
                canvas.create_image(player.cx-cardWidth/2-marginFromCenterx, player.cy,
                    anchor="c",
                    image=ImageTk.PhotoImage(image))
            else:
                image = player.card1.cardBack
                cardWidth, cardHeight = image.size
                
                canvas.create_image(player.cx-cardWidth/2-marginFromCenterx, player.cy,
                    anchor="c",
                    image=ImageTk.PhotoImage(image))

        if player.card2 != None:
            if player.show:
                image = player.card2.cardFront
                cardWidth, cardHeight = image.size
                canvas.create_image(player.cx+marginFromCenterx+cardWidth/2, 
                    player.cy, anchor="c", 
                    image=ImageTk.PhotoImage(image))
            else:
                image = player.card2.cardBack
                cardWidth, cardHeight = image.size
                canvas.create_image(player.cx+marginFromCenterx+cardWidth/2, 
                    player.cy, anchor="c",
                    image=ImageTk.PhotoImage(image))
class MyModalApp(ModalApp):
    def appStarted(self):
        self.gameMode = GameMode()
        self.helpMode = HelpMode()
        self.winScreen = WinScreen()
        self.loseScreen = LoseScreen()
        self.splashScreen = SplashScreen()
        self.multiplayerMode = MultiplayerMode()
        self.setActiveMode(self.splashScreen)
MyModalApp(width=500, height=500)
