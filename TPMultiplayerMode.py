# Extra playable mode that allows you to have 2 human players if you pass the 
# laptop on each turn

from cmu_112_graphics import *
from tkinter import *
import math, copy, random
from TPClasses import *
class MultiplayerMode(Mode):
    def appStarted(self):
        self.font = "system"
        self.setupImages()
        self.isFirstTurn = True
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
        self.isAskingChallenge = False
        self.isShowingLostCard = False
        self.isIncorrectChallenge = False
        self.isCorrectChallenge = False
        self.switchPlayer = False
        self.nextTurn = False
        self.playerViewing = 0
        self.loseCardButtons = None
        self.lostCard = None
        self.isChoosingLostCard = False
        self.currentChallenge = ""
        self.currentMove = ""
    def setupImages(self):
        path = "cards"
        # Copied from: http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html
        # and http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#spritesheetsWithCropping
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
        self.players.append(HumanPlayer("P1", card1, card2, self.app.width/2, self.app.height*(5/6), True))
        card1, card2 = self.deck.removeCards(2)
        self.players.append(HumanPlayer("P2", card1, card2, self.app.width/2, self.app.height*(1/6), False))
    def mousePressed(self, event):
        #do action at end of sequence in pressed
        # checks if pressing help
        if self.isPressingButton(event.x, event.y, self.help):
            self.app.setActiveMode(self.app.helpMode)
        #elif self.turn == 0:
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
        elif self.isAskingChallenge:
            # "Yes"
            button = self.challengeButtons.L[0]
            if self.isPressingButton(event.x, event.y, button):
                self.currentChallenge = button.text
            # "No"
            button = self.challengeButtons.L[1]
            if self.isPressingButton(event.x, event.y, button):
                self.currentChallenge = button.text
        elif self.isChoosingPlayer:
            # self.isChoosingAction = False
            target = None
            while(target == None):
                target = self.pickPlayer(event)
            self.doAction(target)
        elif self.isExchangingCards:
            self.players[self.turn].card1, self.players[self.turn].card2 = self.pickCard(event)
            self.doAction()
        elif self.isChoosingLostCard:
            for button in self.loseCardButtons.L:
                if self.isPressingButton(event.x, event.y, button):
                    cardName = button.text
                    self.lostCard = self.players[self.playerViewing].loseInfluence(cardName)
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
                if self.players[self.turn].numCards == 2:
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
        k = self.players[self.turn].numCards
        numButtons = int(math.factorial(n)/(math.factorial(k)*math.factorial(n - k)))
        increment = (endy - starty)/numButtons
        buttonTexts = [ ]
        if self.players[self.turn].numCards == 2:
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
        # "Take Income"
        if self.currentMove == self.moves[0]:
            self.isChoosingAction = False
            self.players[self.turn].takeIncome()
        # "Take Foreign Aid"
        elif self.currentMove == self.moves[1]:
            self.isChoosingAction = False
            self.players[self.turn].takeForeignAid()
        # "Tax"
        elif self.currentMove == self.moves[2]:
            self.isChoosingAction = False
            self.players[self.turn].tax()
        # "Steal"
        elif self.currentMove == self.moves[3]:
            self.players[self.turn].steal(target)
            self.isChoosingPlayer = False
        # "Swap Influence"
        elif self.currentMove == self.moves[4]:
            self.isExchangingCards = False
        # "Assassinate"
        elif self.currentMove == self.moves[5]:
            self.players[self.turn].assassinate(target)
            self.isChoosingPlayer = False
        # "Coup"
        elif self.currentMove == self.moves[6]:
            self.players[self.turn].coup(target)
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
        if self.isChoosingAction:
            # check challenge
            if self.currentMove != "":
                generalMoves = ["Take Income", "Take Foreign Aid", "Coup"]
                if self.currentMove not in generalMoves:
                    # ask next player to challenge
                    self.changePlayer()
                # if not challengable move
                else:
                    self.continueAction() 
        elif self.isAskingChallenge:
            if self.currentChallenge == "Yes":
                player = self.players[self.turn]
                # incorrect challenge - player loses card
                if player.canDoAction(self.currentMove):
                    self.isIncorrectChallenge = True
                    playerLosing = self.players[self.playerViewing]
                    L = self.makeCardList(playerLosing)
                    self.loseCardButtons = self.createButtons(L)
                    self.currentChallenge == ""
                    ##### new situation
                    self.isCorrectChallenge = False
                    # prompt player to choose a card to be rid of
                    self.isChoosingLostCard = True
                    self.isAskingChallenge = False
                    
                # correct challenge 
                else:
                    self.isCorrectChallenge = True
                    self.changePlayer()
                    self.isAskingChallenge = False
            # if no challenge     
            elif self.currentChallenge == "No":
                self.currentChallenge = ""
                self.isAskingChallenge = False
                self.continueAction()         
        elif self.isChoosingLostCard:

            self.isChoosingLostCard = False
            self.isShowingLostCard = True
            
            self.endTurn()
    def changePlayer(self):
        self.switchPlayer = True
        self.playerViewing = (self.playerViewing + 1)%2
        for player in self.players:
            player.show = False
    def makeCardList(self, player):
        L = []
        if player.card2 != None and player.card1 != None:
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
        # "Steal"
        elif self.currentMove == self.moves[3]:
            self.changePlayer()
        # "Swap Influence" 
        elif self.currentMove == self.moves[4]:
            self.changePlayer()
        # "Assassinate"
        elif self.currentMove == self.moves[5]:
            self.changePlayer()            
        elif self.currentMove == self.moves[6]:
            self.isChoosingAction = False
            self.isChoosingPlayer = True

    def keyPressed(self, event):
        ### these are shortcuts to the winscreen and lose screen
        if event.key == "q":
            self.app.setActiveMode(self.app.winScreen)
        elif event.key == "w":
            self.app.setActiveMode(self.app.loseScreen)
        if event.key == "Enter":
            if self.isFirstTurn:
                self.isFirstTurn = False            
            self.players[self.playerViewing].show = True
            if self.nextTurn:
                self.isChoosingAction = True
                self.nextTurn = False
            elif self.switchPlayer:
                self.players[self.playerViewing].show = True
                if self.isChoosingAction:
                    self.isChoosingAction = False
                    self.isAskingChallenge = True
                elif self.isCorrectChallenge:
                    self.isChoosingLostCard = True
                    playerLosing = self.players[self.playerViewing]
                    L = self.makeCardList(playerLosing)
                    self.loseCardButtons = self.createButtons(L)
                    self.isAskingChallenge = False
                    self.currentChallenge == ""
                    self.isCorrectChallenge = False
                # "Steal"
                elif self.currentMove == self.moves[3]:
                    self.isChoosingAction = False
                    self.isChoosingPlayer = True  
                # "Swap Influence"
                elif self.currentMove == self.moves[4]: 
                    self.isChoosingAction = False
                    self.cardsToShow = self.deck.removeCards(self.players[self.turn].numCards) + [self.players[self.turn].card1, self.players[self.turn].card2]
                    self.createCardButtons()
                    self.isExchangingCards = True
                # "Assassinate"
                elif self.currentMove == self.moves[5]:
                    self.isChoosingAction = False
                    self.isChoosingPlayer = True
                self.switchPlayer = False
            else:
                self.isChoosingAction = True
    def endTurn(self):
        for player in self.players:
            player.show = False
        self.nextTurn = True
        self.checkGameOver()
        self.turn = (self.turn + 1)%len(self.players)
        self.playerViewing = self.turn
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.app.width, self.app.height, 
            fill="#969696", width=0)
        self.drawDeckAndBank(canvas)
        canvas.create_text(50, self.app.height/2, text=f"Turn:\n{self.players[self.turn].name}")
        for player in self.players:
           self.drawPlayer(canvas, player)
        self.drawHelp(canvas) 
        if self.isFirstTurn:
            canvas.create_text(self.app.width/2, self.app.height/2, 
                font=f"{self.font} 15 bold", fill="black",
                text="Press 'Enter' to go")
        elif self.nextTurn:
            if self.currentChallenge == "No":
                canvas.create_text(self.app.width/2, self.app.height*(5/8), 
                    font=f"{self.font} 15 bold", fill="black",
                    text=f"{self.players[(self.turn+1)%2].name} did {self.currentMove}'")
            elif self.isShowingLostCard:
                canvas.create_text(self.app.width/2, self.app.height*(5/8), 
                    font=f"{self.font} 15 bold", fill="black",
                    text=f"{self.players[(self.turn+1)%2].name} lost {self.lostCard.name}'")
            canvas.create_text(self.app.width/2, self.app.height/2, 
                font=f"{self.font} 15 bold", fill="black",
                text=f"End of turn: give the laptop to {self.players[self.turn].name}\nPress 'Enter' ")
        elif self.switchPlayer:
            if self.isCorrectChallenge:
                canvas.create_text(self.app.width/2, self.app.height*(3/8), 
                    font=f"{self.font} 15 bold", fill="black",
                    text=f"You challenged correctly!")
            if self.currentMove != "":
                canvas.create_text(self.app.width/2, self.app.height*(5/16), 
                    font=f"{self.font} 15 bold", fill="black",
                    text=f"{self.players[self.turn].name} wants to {self.currentMove}")
            canvas.create_text(self.app.width/2, self.app.height/2, 
                font=f"{self.font} 15 bold", fill="black",
                text=f"Give the laptop to {self.players[self.playerViewing].name}\nPress 'Enter' ")
        elif self.isChoosingAction or self.isChoosingPlayer or self.isExchangingCards:
            self.drawChoicesPanel(canvas)
        elif self.isChoosingLostCard:
            self.drawChoicesPanel(canvas)
        elif self.isAskingChallenge:
                self.drawChoicesPanel(canvas)
        else:
            canvas.create_text(self.app.width/2, self.app.height/2, 
                font=f"{self.font} 15 bold", fill="black",
                text=f"Give the laptop to {self.players[(self.turn+1)%2].name}\nPress 'Enter' ")
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
        startx = panelx1 + (1/50)*self.app.width
        starty = panely1 + (5/50)*self.app.height
        endx = panelx2 - (1/50)*self.app.width
        endy = panely2 - (3/50)*self.app.height
        textx = self.app.width/2
        texty = (1/6+2/50)*self.app.height
        if self.isChoosingPlayer:
            canvas.create_text(textx, texty, anchor="c", text="Who do you choose?")
            self.drawPlayerChoices(canvas, startx, starty, endx, endy)
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
            if self.isCorrectChallenge:
                text = f"{self.players[(self.turn+1)%2]} has successfully challenged you.\nWhich card do you lose?"
            elif self.isIncorrectChallenge:
                text = f"You have failed to challenge.\nWhich card do you lose?"
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