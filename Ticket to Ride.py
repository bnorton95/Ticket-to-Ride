"""
Ticket to Ride

Author : Brian Norton
"""

import pygame
import pygame.mouse as mouse
import pygame.draw as draw
import random
import networkx as nx
import math
import os
#import copy
pygame.init()

def mouseWithin(coordinates):
    if mouseX > coordinates[0][0] and mouseY > coordinates[0][1] and mouseX < coordinates[1][0] and mouseY < coordinates[1][1] :
        return True
    else:
        return False   
    
def sortHands(hand):
    sortedHand = [[0 for y in range(0,9)] for x in range(0,int(numPlayers))]
    for x in range(0,numPlayers):
        for y in range(0,9):
            sortedHand[x][y] = hand[x].count(colors[y])
    return sortedHand

def sortDisplay(display):
    sortedDisplay = [0,0,0,0,0]
    for x in range(0,5):
        for y in range(0,len(colors)):
            if display[x] == colors[y]:
                sortedDisplay[x] = y
    return sortedDisplay

def compactFunct(inputDeck):
    global colors
    compact = []
    for x in range(0,len(colors)):
        compact.append(inputDeck.count(colors[x]))
    return compact
    
def drawCard():
    global deck
    global discard
    if len(deck) == 0:
        deck = discard
        discard = []
        random.shuffle(deck)
    return deck.pop()
        

def nextPlayer():
    global option
    global finalTurn
    global room
    global turnPlayer
    option = 0
    if turnPlayer == finalTurn:
        room = 2
    if numTrains[turnPlayer] < 3 and finalTurn == -1:
        finalTurn = turnPlayer
    turnPlayer += 1
    if turnPlayer == numPlayers:
        turnPlayer = 0
    saveGame()
        
def saveGame():
    global gameSave
    global save1
    global save2
    global save3
    global name
    if gameSave == 1:
        if save1 == True:
            os.remove("save1.txt")
        f = open("save1.txt", "w+")
    if gameSave == 2:
        if save2 == True:
            os.remove("save2.txt")
        f = open("save2.txt", "w+")
    if gameSave == 3:
        if save3 == True:
            os.remove("save3.txt")
        f = open("save3.txt", "w+")                            
    f.write("Map "+fileName+"\n")
    f.write("Railroads\n")
    for u,v,k,info in totalGraph.edges(keys=True,data=True):
        f.write(str(u)+" "+str(v)+" "+str(k)+" "+str(info['owned'])+"\n")
    f.write("NumPlayers "+str(numPlayers)+"\n")
    f.write("Names ")
    for x in range(0,numPlayers):
        removeSpace = list(name[x])
        for y in range(0,len(removeSpace)):
            if removeSpace[y] == ' ':
                removeSpace = list(removeSpace)
                removeSpace[y] = '_'
            removeSpace = "".join(removeSpace)
        #name[x] = removeSpace   
        f.write(str(removeSpace)+" ")   
    f.write("\n")
    f.write("Turnplayer "+str(turnPlayer)+"\n")
    f.write("Trains ")
    for x in range(0,numPlayers):
        f.write(str(numTrains[x])+" ")
    f.write("\nPoints ")
    for x in range(0,numPlayers):
        f.write(str(points[x])+" ")
    f.write("\nRoutes")
    for x in range(0,numPlayers):
        for y in range(0,len(playerRoutes[x])):
            f.write("\n"+str(playerRoutes[x][y][0])+" "+str(playerRoutes[x][y][1])+" "+str(playerRoutes[x][y][2])+" "+str(playerRoutes[x][y][3]))
        if x != numPlayers-1:
            f.write("\nNext")
    f.write("\nDeck")
    for x in range(0,len(routes)):
        f.write("\n"+str(routes[x][0])+" "+str(routes[x][1])+" "+str(routes[x][2])+" "+str(routes[x][3]))
    sortedHand = sortHands(hand)
    f.write("\nHands\n")
    for x in range(0,numPlayers):
        for y in range(0,len(sortedHand[x])):
            f.write(str(sortedHand[x][y])+" ")
        f.write("\n")
    f.write("Draw ")
    compact = compactFunct(deck)
    for x in range(0,len(compact)):
        f.write(str(compact[x])+" ")
    f.write("\n")
    f.write("Discard ")
    compact = compactFunct(discard)
    for x in range(0,len(compact)):
        f.write(str(compact[x])+" ")
    f.write("\n")
    f.write("Display ")
    for x in range(0,len(display)):
        f.write(str(display[x])+" ")
    f.write("\nFinal "+str(finalTurn))
    f.close()
    
carnegieMode = True
background = True
    

"""Color definitions"""
black = (40,40,40)
white = (255,255,255)
red = (242,56,9)
green = (141,173,46)
blue = (46,131,173)
yellow = (255,204,0)
orange = (255,144,0)
pink = (242,152,203)
gray = (175,175,175)
tan = (237,202,137)
lightgray = (220,220,220) #Background color
medgray = (120,120,120)
darkgray = (60,60,60) #Background of hand color for black
brown = (104,65,35)
neongreen = (0,255,0)



"""TEMP VARIABLES THAT WILL BE IMPLEMENTED LATER"""
numPlayers = 5
name = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]



"""Loading images and fonts"""
trainLogo = pygame.image.load('train image.jpg')
miniTrain = pygame.image.load('miniTrain.jpg')
miniStar = pygame.image.load('miniStar.jpg')
wildCard = pygame.image.load('wildCard.jpg')
backg = pygame.image.load('US.png')
wildCardLarge = pygame.image.load('wildCardLarge.jpg')
nameFont = pygame.font.SysFont("Lucida Fax", 20)
cancelFont = pygame.font.SysFont("Lucida Fax", 18)
infoFont = pygame.font.SysFont("monospace",14)
smallNameFont = pygame.font.SysFont("Lucida Fax",12)
titleFont = pygame.font.SysFont("TW Cen MT", 64)
title = titleFont.render("Ticket to Ride", 1, black)
handTitle = smallNameFont.render("Hand",1,white)
routeTitle = smallNameFont.render("Routes",1,white)
actionTitle = smallNameFont.render("Actions",1,white)
routeDesc = smallNameFont.render("Obtain new routes",1,darkgray)
buyDesc = smallNameFont.render("Buy a railroad between two cities",1,darkgray)
buy1 = smallNameFont.render("Choose the first city to buy a railroad on",1,darkgray)
buy2 = smallNameFont.render("Choose a second city to select a railroad",1,darkgray)
buy3 = smallNameFont.render("Confirm to buy a railroad, or cancel",1,darkgray)
drawDesc = smallNameFont.render("Draw new cards",1,darkgray)
exitDesc = smallNameFont.render("Save and/or exit the game",1,darkgray)
routeFont = pygame.font.SysFont("Lucida Bright",12)
saveExit = cancelFont.render("Choose an option",1,darkgray)
routeConfirm = cancelFont.render("Are you sure you want to draw new routes?",1,darkgray)
drawInfo = cancelFont.render("Choose a card to add to your hand",1,darkgray)
drawSecond = cancelFont.render("Add another card to your hand",1,darkgray)
deckTitle = smallNameFont.render("Deck",1,white)
wildWarn = smallNameFont.render("Second card cannot be a face-up wild",1,darkgray)
saveTitleFont = pygame.font.SysFont("Lucida Fax",24)
startGame = cancelFont.render("Start",1,white)
startGameOn = cancelFont.render("Start",1,yellow)
newGame = cancelFont.render("New",1,white)
newGameOn = cancelFont.render("New",1,yellow)
startGameOn = cancelFont.render("Start",1,yellow)
numDisplay = smallNameFont.render("Number of players",1,white)
customDisplay1 = smallNameFont.render("Enter custom names",1,white)
customDisplay2 = smallNameFont.render("in console?",1,white)
customDisplay3 = cancelFont.render("Custom",1,white)
customDisplay3On = cancelFont.render("Custom",1,yellow)
finalFont = pygame.font.SysFont("Lucida Fax",16)
finalText = nameFont.render("Final Turn",1,red)
routeArrowFont = pygame.font.SysFont("Lucida Fax",20)
routeDesc2 = smallNameFont.render("Select 1, 2, or 3 railroads to add to your hand",1,darkgray)




"""Game display specs - can be changed"""
gameWidth = 640
gameHeight = 480
trainWidth = trainLogo.get_width()
nameCoord = (128,48) #size of the name boxes in the main game room
nameGap = (16,0) #space given in the upper left corner for the name to be written
trainGap = (16,26)
trainTextGap = (20+miniTrain.get_width(),27)
starGap = (84,26)
starTextGap = (88+miniStar.get_width(),27)
handDisplaySize = (240,52)
routeDisplaySize = (308,52)
handBoxSize = (24,32)
handGap = (5,3)
buttonBoxSize = (32,32)
buttonBg = (buttonBoxSize[0]*4+12,52)
optionWindow = (400,300)
exitWindow = (240,75)
routeConfirmBox = (420,95)
optionBorder = 3
cardSize = (64,82)
dotOuterSize = 7
dotInnerSize = 5
citySize = 15
buyBox = (300,300)
titleBox = (230,50)

"""Window Stuff"""
screen = pygame.display.set_mode((gameWidth,gameHeight))
pygame.display.set_caption('Ticket to Ride')
clock = pygame.time.Clock()

"""Dynamic variables - can be changed"""
colorTypes = 8
numColors = 8
numWilds = 4
colors = ["Red", "Blue", "Yellow", "Green", "White", "Black", "Orange", "Pink","Wild"]
colorPresets = [red,blue,yellow,green,white,black,orange,pink]
playerColor = [red,blue,orange,green,pink]
bgColor = [red,blue,orange,green,pink]
startTrains = 45
numTrains = [startTrains,startTrains,startTrains,startTrains,startTrains]
routesPerHand = 2
fileName = "USA Map.txt"
pointRewards = [1,2,4,7,10,15]

"""Loading files"""
if os.path.isfile('save1.txt'):
    save1 = True
else:
    save1 = False
if os.path.isfile('save2.txt'):
    save2 = True
else:
    save2 = False
if os.path.isfile('save3.txt'):
    save3 = True
else:
    save3 = False

"""Creating the Graphs"""
numCities = 0
p1Bought = nx.Graph()
p1Graph = nx.MultiGraph()
totalGraph = nx.MultiGraph()
scanSection = 1
routes = []
edgeSpace = 7
with open(fileName) as f:
    for line in f:
        inp = line.split()
        if inp[0] == "//":
            continue
        if inp[0] == "Paths":
            xCoords = nx.get_node_attributes(totalGraph,'x')
            yCoords = nx.get_node_attributes(totalGraph,'y')
            scanSection = 2
            continue
        if inp[0] == "Routes":
            scanSection = 3
            continue
        if scanSection == 1:
            removeUnderscore = list(inp[1])
            for x in range(0,len(removeUnderscore)):
                if removeUnderscore[x] == '_':
                    removeUnderscore[x] = ' '
            removeUnderscore = "".join(removeUnderscore)
            totalGraph.add_node(int(inp[0]),name=str(removeUnderscore),x=int(inp[2]),y=int(inp[3]))
            numCities += 1
        if scanSection == 2:
            if not totalGraph.has_edge(int(inp[0]),int(inp[1])):
                x1Inp = totalGraph.nodes[int(inp[0])]['x']
                y1Inp = totalGraph.nodes[int(inp[0])]['y']
                x2Inp = totalGraph.nodes[int(inp[1])]['x']
                y2Inp = totalGraph.nodes[int(inp[1])]['y']
                totalGraph.add_edge(int(inp[0]),int(inp[1]),key=1,weight=int(inp[3]),color=inp[2],owned=-1,x1=x1Inp,x2=x2Inp,y1=y1Inp,y2=y2Inp)
            else:
                p1 = (totalGraph.nodes[int(inp[0])]['x'],totalGraph.nodes[int(inp[0])]['y'])
                p2 = (totalGraph.nodes[int(inp[1])]['x'],totalGraph.nodes[int(inp[1])]['y'])
                angle = math.atan2(p2[1]-p1[1],p2[0]-p1[0])
                angle1 = (angle)-math.pi/2
                yL1 = edgeSpace*math.sin(angle1)
                xL1 = edgeSpace*math.cos(angle1)
                totalGraph.edges[int(inp[0]), int(inp[1]), 1]['x1'] = p1[0]+xL1
                totalGraph.edges[int(inp[0]), int(inp[1]), 1]['x2'] = p2[0]+xL1
                totalGraph.edges[int(inp[0]), int(inp[1]), 1]['y1'] = p1[1]+yL1
                totalGraph.edges[int(inp[0]), int(inp[1]), 1]['y2'] = p2[1]+yL1
                totalGraph.add_edge(int(inp[0]),int(inp[1]),key=2,weight=int(inp[3]),color=inp[2],owned=-1,x1=p1[0]-xL1,x2=p2[0]-xL1,y1=p1[1]-yL1,y2=p2[1]-yL1)
        if scanSection == 3:
           routes.append((int(inp[0]),int(inp[1]),int(inp[2]),0))
f.close()
p1Bought.add_nodes_from(range(1,numCities+1))
p5Bought = p1Bought.copy()
p4Bought = p1Bought.copy()
p3Bought = p1Bought.copy()
p2Bought = p1Bought.copy()
p5Graph = totalGraph.copy()
p4Graph = totalGraph.copy()
p3Graph = totalGraph.copy()
p2Graph = totalGraph.copy()
p1Graph = totalGraph.copy()

"""Distributing the routes"""
random.shuffle(routes)
playerRoutes = [[],[],[],[],[]]
for x in range(0,numPlayers):
        if routes:
            playerRoutes[x].append(routes.pop())
        if routes:
            playerRoutes[x].append(routes.pop())
routeNames = nx.get_node_attributes(totalGraph,'name')


"""Creating the deck and display cards"""
deck = []
display = [0,0,0,0,0]
discard = []
points = [0,0,0,0,0]
for x in range(0,colorTypes):
    for y in range(0,numColors):
        deck.append(colors[x])
for x in range(0,numWilds):
    deck.append("Wild")
random.shuffle(deck)
for x in range(0,5):
    display[x] = drawCard()
sortedDisplay = sortDisplay(display)

    
"""Hand setup"""
hand = [[],[],[],[],[]]
for x in range(0,numPlayers):
    hand[x].append(drawCard())
    hand[x].append(drawCard())
sortedHand = sortHands(hand)

#Cheat mode and stuff
if carnegieMode == True:
    for y in range(0,numPlayers):
        for x in range(0,numColors):
            while hand[y].count(colors[x]) < 9:
                hand[y].append(colors[x])
            while hand[y].count('Wild') < 9:
                hand[y].append('Wild')
    sortedHand = sortHands(hand)

"""Game variables - Do not change"""
room = 0
turnPlayer = 0
gameEnd = False
trainPos = gameWidth/2-70
gameBorder = 48
graphWindow = (gameBorder,gameBorder+nameCoord[1])
screenCheck = False
screenCheck2 = False
option = 0
click = False
leftClick = False
action = False
cardsTaken = 0
nearCity = -1
citySelect1 = -1
citySelect2 = -1
citiesChosen = 0
activeButton1 = False
activeButton2 = False
finalTurn = -1
routeScroller = [0,0,0,0,0]
takeRoute1 = False
takeRoute2 = False
takeRoute3 = False
anyCol = []

#Game previews
previewNum1 = -1
previewName1 = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]
previewScores1 = [0,0,0,0,0]
previewTrains1 = [0,0,0,0,0]
previewNum2 = -1
previewName2 = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]
previewScores2 = [0,0,0,0,0]
previewTrains2 = [0,0,0,0,0]
previewNum3 = -1
previewName3 = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]
previewScores3 = [0,0,0,0,0]
previewTrains3 = [0,0,0,0,0]
newNumPlayers = 2
inputNames = False

if save1 == True:
    with open("save1.txt") as f:
        for line in f:
            inp = line.split()
            if inp[0] == "NumPlayers":
                previewNum1 = int(inp[1])
            if inp[0] == "Names":
                for x in range(0,previewNum1):
                    removeSpace = list(inp[x+1])
                    for y in range(0,len(removeSpace)):
                        if removeSpace[y] == '_':
                            removeSpace = list(removeSpace)
                            removeSpace[y] = ' '
                        removeSpace = "".join(removeSpace)
                    previewName1[x] = removeSpace
            if inp[0] == "Points":
                for x in range(0,previewNum1):
                    previewScores1[x] = inp[x+1]
            if inp[0] == "Trains":
                for x in range(0,previewNum1):
                    previewTrains1[x] = inp[x+1]
    f.close()
if save2 == True:
    with open("save2.txt") as f:
        for line in f:
            inp = line.split()
            if inp[0] == "NumPlayers":
                previewNum2 = int(inp[1])
            if inp[0] == "Names":
                for x in range(0,previewNum1):
                    removeSpace = list(inp[x+1])
                    for y in range(0,len(removeSpace)):
                        if removeSpace[y] == '_':
                            removeSpace = list(removeSpace)
                            removeSpace[y] = ' '
                        removeSpace = "".join(removeSpace)
                    previewName1[x] = removeSpace
            if inp[0] == "Points":
                for x in range(0,previewNum1):
                    previewScores1[x] = inp[x+1]
            if inp[0] == "Trains":
                for x in range(0,previewNum2):
                    previewTrains2[x] = inp[x+1]
    f.close()
if save3 == True:
    with open("save3.txt") as f:
        for line in f:
            inp = line.split()
            if inp[0] == "NumPlayers":
                previewNum3 = int(inp[1])
            if inp[0] == "Names":
                for x in range(0,previewNum3):
                    removeSpace = list(inp[x+1])
                    for y in range(0,len(removeSpace)):
                        if removeSpace[y] == '_':
                            removeSpace = list(removeSpace)
                            removeSpace[y] = ' '
                        removeSpace = "".join(removeSpace)
                    previewName3[x] = removeSpace
            if inp[0] == "Points":
                for x in range(0,previewNum3):
                    previewScores3[x] = inp[x+1]
            if inp[0] == "Trains":
                for x in range(0,previewNum3):
                    previewTrains3[x] = inp[x+1]
    f.close()

    
"""Begin game loop"""
while not gameEnd:
    
    #Stuff that moves without event changes
    mouseX,mouseY = mouse.get_pos()
    mouseLeft,mouseCenter,mouseRight = mouse.get_pressed()
    if mouseLeft == False and action == True:
                action = False
    
    if room == 0:
        trainPos -= 2
        if trainPos < -trainWidth:
            trainPos = gameWidth
        screen.fill(tan)
        screen.blit(title,(gameWidth/2-132,gameHeight/2-170))
        screen.blit(trainLogo,(trainPos,gameHeight/2-105))
        
        draw.rect(screen,brown,(400,240,180,180))
        if option != 0:
            if (option == 1 and save1 == False) or (option == 2 and save2 == False) or (option == 3 and save3 == False):
                #Display for a new game
                draw.rect(screen,medgray,(455,380,70,30))
                if mouseWithin([(455,380),(525,410)]):
                    screen.blit(startGameOn,(465,383))
                else:
                    screen.blit(startGame,(465,383))
                screen.blit(numDisplay,(435,245))
                #Left arrow
                if newNumPlayers > 2:
                    draw.rect(screen,medgray,(455,265,22,26))
                    if mouseWithin([(455,265),(477,291)]):
                        leftArrow = routeArrowFont.render("<",1,yellow)
                    else:
                        leftArrow = routeArrowFont.render("<",1,white)
                else:
                    draw.rect(screen,darkgray,(455,265,22,26))
                    leftArrow = routeArrowFont.render("<",1,medgray)
                screen.blit(leftArrow,(459,264))
                #Right arrow
                if newNumPlayers < 5:
                    draw.rect(screen,medgray,(505,265,22,26))
                    if mouseWithin([(509,265),(531,291)]):
                        rightArrow = routeArrowFont.render(">",1,yellow)
                    else:
                        rightArrow = routeArrowFont.render(">",1,white)
                else:
                    draw.rect(screen,darkgray,(505,265,22,26))
                    rightArrow = routeArrowFont.render(">",1,medgray)
                screen.blit(rightArrow,(509,264))
                num = cancelFont.render(str(newNumPlayers),1,white)
                screen.blit(num,(485,266))
                
                #Custom button
                screen.blit(customDisplay1,(425,300))
                screen.blit(customDisplay2,(450,315))
                if inputNames == True:
                    draw.rect(screen,darkgray,(441,338,100,30))
                else:
                    draw.rect(screen,medgray,(441,338,100,30))
                if mouseWithin([(441,338),(541,368)]):
                    screen.blit(customDisplay3On,(455,340))
                else:
                    screen.blit(customDisplay3,(455,340))
                #inputNames = T/F
            else:
                #Display when a game is already started
                draw.rect(screen,medgray,(420,380,70,30))
                draw.rect(screen,medgray,(494,380,70,30))
                if mouseWithin([(420,380),(490,410)]):
                    screen.blit(startGameOn,(430,383))
                else:
                    screen.blit(startGame,(430,383))
                if mouseWithin([(494,380),(564,410)]):
                    screen.blit(newGameOn,(508,383))
                else:
                    screen.blit(newGame,(508,383))
                if option == 1:
                    if previewNum1 > 0:
                        p1 = smallNameFont.render(previewName1[0],1,white)
                        p1Score = smallNameFont.render(str(previewScores1[0]),1,white)
                        p1Train = smallNameFont.render(str(previewTrains1[0]),1,white)
                        screen.blit(p1,(410,275))
                        screen.blit(p1Score,(503,275))
                        screen.blit(p1Train,(548,275))
                        p2 = smallNameFont.render(previewName1[1],1,white)
                        p2Score = smallNameFont.render(str(previewScores1[1]),1,white)
                        p2Train = smallNameFont.render(str(previewTrains1[1]),1,white)
                        screen.blit(p2,(410,295))
                        screen.blit(p2Score,(503,295))
                        screen.blit(p2Train,(548,295))
                    if previewNum1 > 2:
                        p3 = smallNameFont.render(previewName1[2],1,white)
                        p3Score = smallNameFont.render(str(previewScores1[2]),1,white)
                        p3Train = smallNameFont.render(str(previewTrains1[2]),1,white)
                        screen.blit(p3,(410,315))
                        screen.blit(p3Score,(503,315))
                        screen.blit(p3Train,(548,315))
                    if previewNum1 > 3:
                        p4 = smallNameFont.render(previewName1[3],1,white)
                        p4Score = smallNameFont.render(str(previewScores1[3]),1,white)
                        p4Train = smallNameFont.render(str(previewTrains1[3]),1,white)
                        screen.blit(p4,(410,335))
                        screen.blit(p4Score,(503,335))
                        screen.blit(p4Train,(548,335))
                    if previewNum1 > 4:
                        p5 = smallNameFont.render(previewName1[4],1,white)
                        p5Score = smallNameFont.render(str(previewScores1[4]),1,white)
                        p5Train = smallNameFont.render(str(previewTrains1[4]),1,white)
                        screen.blit(p5,(410,355))
                        screen.blit(p5Score,(503,355))
                        screen.blit(p5Train,(548,355))
                if option == 2:
                    if previewNum2 > 0:
                        p1 = smallNameFont.render(previewName2[0],1,white)
                        p1Score = smallNameFont.render(str(previewScores2[0]),1,white)
                        p1Train = smallNameFont.render(str(previewTrains2[0]),1,white)
                        screen.blit(p1,(410,275))
                        screen.blit(p1Score,(503,275))
                        screen.blit(p1Train,(548,275))
                        p2 = smallNameFont.render(previewName2[1],1,white)
                        p2Score = smallNameFont.render(str(previewScores2[1]),1,white)
                        p2Train = smallNameFont.render(str(previewTrains2[1]),1,white)
                        screen.blit(p2,(410,295))
                        screen.blit(p2Score,(503,295))
                        screen.blit(p2Train,(548,295))
                    if previewNum2 > 2:
                        p3 = smallNameFont.render(previewName2[2],1,white)
                        p3Score = smallNameFont.render(str(previewScores2[2]),1,white)
                        p3Train = smallNameFont.render(str(previewTrains2[2]),1,white)
                        screen.blit(p3,(410,315))
                        screen.blit(p3Score,(503,315))
                        screen.blit(p3Train,(548,315))
                    if previewNum2 > 3:
                        p4 = smallNameFont.render(previewName2[3],1,white)
                        p4Score = smallNameFont.render(str(previewScores2[3]),1,white)
                        p4Train = smallNameFont.render(str(previewTrains2[3]),1,white)
                        screen.blit(p4,(410,315))
                        screen.blit(p4Score,(503,335))
                        screen.blit(p4Train,(548,335))
                    if previewNum2 > 4:
                        p5 = smallNameFont.render(previewName2[4],1,white)
                        p5Score = smallNameFont.render(str(previewScores2[4]),1,white)
                        p5Train = smallNameFont.render(str(previewTrains2[4]),1,white)
                        screen.blit(p5,(410,315))
                        screen.blit(p5Score,(503,355))
                        screen.blit(p5Train,(548,355))
                if option == 3:
                    if previewNum3 > 0:
                        p1 = smallNameFont.render(previewName3[0],1,white)
                        p1Score = smallNameFont.render(str(previewScores3[0]),1,white)
                        p1Train = smallNameFont.render(str(previewTrains3[0]),1,white)
                        screen.blit(p1,(410,275))
                        screen.blit(p1Score,(503,275))
                        screen.blit(p1Train,(548,275))
                        p2 = smallNameFont.render(previewName3[1],1,white)
                        p2Score = smallNameFont.render(str(previewScores3[1]),1,white)
                        p2Train = smallNameFont.render(str(previewTrains3[1]),1,white)
                        screen.blit(p2,(410,295))
                        screen.blit(p2Score,(503,295))
                        screen.blit(p2Train,(548,295))
                    if previewNum3 > 2:
                        p3 = smallNameFont.render(previewName3[2],1,white)
                        p3Score = smallNameFont.render(str(previewScores3[2]),1,white)
                        p3Train = smallNameFont.render(str(previewTrains3[2]),1,white)
                        screen.blit(p3,(410,315))
                        screen.blit(p3Score,(503,315))
                        screen.blit(p3Train,(548,315))
                    if previewNum3 > 3:
                        p4 = smallNameFont.render(previewName3[3],1,white)
                        p4Score = smallNameFont.render(str(previewScores3[3]),1,white)
                        p4Train = smallNameFont.render(str(previewTrains3[3]),1,white)
                        screen.blit(p4,(410,335))
                        screen.blit(p4Score,(503,335))
                        screen.blit(p4Train,(548,335))
                    if previewNum3 > 4:
                        p5 = smallNameFont.render(previewName3[4],1,white)
                        p5Score = smallNameFont.render(str(previewScores3[4]),1,white)
                        p5Train = smallNameFont.render(str(previewTrains3[4]),1,white)
                        screen.blit(p5,(410,355))
                        screen.blit(p5Score,(503,355))
                        screen.blit(p5Train,(548,355))
                nameLabel = smallNameFont.render("Name",1,white)
                scoreLabel = smallNameFont.render("Score",1,white)
                trainLabel = smallNameFont.render("Trains",1,white)
                screen.blit(nameLabel,(410,245))
                screen.blit(scoreLabel,(488,245))
                screen.blit(trainLabel,(533,245))
                draw.line(screen,lightgray,(405,265),(575,265))
                
                
        
        draw.rect(screen,brown,(105,235,titleBox[0],titleBox[1]))
        if save1 == False:
            if (mouseWithin([(105,235),(335,285)]) and option == 0) or option == 1:
                start1 = saveTitleFont.render("Start New Game",1, yellow)
            else:
                start1  = saveTitleFont.render("Start New Game",1, white)
            screen.blit(start1,(121,245))
        else:
            if (mouseWithin([(105,235),(335,285)]) and option == 0) or option == 1:
                start1 = saveTitleFont.render("Continue Game 1",1, yellow)
            else:
                start1  = saveTitleFont.render("Continue Game 1",1, white)
            screen.blit(start1,(113,245))
        
        draw.rect(screen,brown,(105,305,titleBox[0],titleBox[1]))
        if save2 == False:
            if (mouseWithin([(105,305),(335,355)]) and option == 0) or option == 2:
                start2 = saveTitleFont.render("Start New Game",1, yellow)
            else:
                start2  = saveTitleFont.render("Start New Game",1, white)
            screen.blit(start2,(121,315))
        else:
            if (mouseWithin([(105,305),(335,355)]) and option == 0) or option == 2:
                start2 = saveTitleFont.render("Continue Game 2",1, yellow)
            else:
                start2  = saveTitleFont.render("Continue Game 2",1, white)
            screen.blit(start2,(113,315))
        
        draw.rect(screen,brown,(105,375,titleBox[0],titleBox[1]))
        if save3 == False:
            if (mouseWithin([(105,375),(335,425)]) and option == 0) or option == 3:
                start2 = saveTitleFont.render("Start New Game",1, yellow)
            else:
                start2  = saveTitleFont.render("Start New Game",1, white)
            screen.blit(start2,(121,385))
        else:
            if (mouseWithin([(105,375),(335,425)]) and option == 0) or option == 3:
                start2 = saveTitleFont.render("Continue Game 3",1, yellow)
            else:
                start2  = saveTitleFont.render("Continue Game 3",1, white)
            screen.blit(start2,(113,385))
        
            
    
        
        
        
        
                
    if room == 1:
        #Initial changes to the room - happens only once
        if screenCheck == False:
            option = 0
            screenCheck = True
            if max(xCoords.values())+(gameBorder*2) < 700:
                gameWidth = 700
            else:
                gameWidth = max(xCoords.values())+(gameBorder*2)
            if max(yCoords.values()) + 164 < 464:
                gameHeight = 464
            else:
                gameHeight = max(yCoords.values())+(gameBorder*2)+nameCoord[1]+handDisplaySize[1]
            gameWidth = 1396
            gameHeight = 796
            r1Coord = [(gameWidth/2+66,gameHeight-38),(gameWidth/2+322,gameHeight-22)]
            r2Coord = [(gameWidth/2+66,gameHeight-20),(gameWidth/2+322,gameHeight-4)]
            screen = pygame.display.set_mode((gameWidth,gameHeight))
            handBoxLoc = [0 for x in range(0,9)]
            for x in range(0,9):
                handBoxLoc[x] = gameWidth/2-344+(x*(handBoxSize[0]+2))
        screen.fill(tan)
        if background == True:
            draw.rect(screen,medgray,(46,46,1304,704))
            screen.blit(backg,(48,48))
        draw.rect(screen,medgray,(gameWidth/2-348,gameHeight-75,696,75))
        draw.rect(screen,lightgray,(gameWidth/2-346,gameHeight-73,692,75))
        #Setting the points to dislay player rectangles and info
        if numPlayers == 2:
            base = [gameWidth/2-nameCoord[0],gameWidth/2]
        elif numPlayers == 3:
            base = [gameWidth/2-(nameCoord[0]*1.5),gameWidth/2-(nameCoord[0]/2),gameWidth/2+(nameCoord[0]/2)]
        elif numPlayers == 4:
            base = [gameWidth/2-(2*nameCoord[0]),gameWidth/2-nameCoord[0],gameWidth/2,gameWidth/2+nameCoord[0]]
        elif numPlayers == 5:
            base = [gameWidth/2-(nameCoord[0]*2.5),gameWidth/2-(nameCoord[0]*1.5),gameWidth/2-(nameCoord[0]/2),gameWidth/2+(nameCoord[0]/2),gameWidth/2+(nameCoord[0]*1.5)]
        #Blit player information and pictures to the screen
        for x in range(0,numPlayers):
            draw.rect(screen,playerColor[x],(base[x],0,nameCoord[0],nameCoord[1]))
            displayTrains = infoFont.render(str(numTrains[x]), 1, white)
            displayPoints = infoFont.render(str(points[x]),1,white)
            active = nameFont.render(name[x], 1, yellow)
            inactive = nameFont.render(name[x], 1, white)
            screen.blit(displayTrains,(base[x]+trainTextGap[0],trainTextGap[1]))
            screen.blit(displayPoints,(base[x]+starTextGap[0],starTextGap[1]))
            screen.blit(miniTrain,(base[x]+trainGap[0],trainGap[1]))
            screen.blit(miniStar,(base[x]+starGap[0],starGap[1]))
            if x == turnPlayer:
                screen.blit(active,(base[x]+nameGap[0],nameGap[1]))
            else:
                screen.blit(inactive,(base[x]+nameGap[0],nameGap[1]))
        #Hand display
        draw.rect(screen,bgColor[turnPlayer],(gameWidth/2-348,gameHeight-handDisplaySize[1],handDisplaySize[0],handDisplaySize[1]))
        draw.rect(screen,darkgray,(gameWidth/2-346,gameHeight-handDisplaySize[1]+14,236,36))
        screen.blit(handTitle,(gameWidth/2-240,gameHeight-52))
        screen.blit(wildCard,(handBoxLoc[8],gameHeight-36))
        displayHand = nameFont.render(str(sortedHand[turnPlayer][8]),1,black)
        screen.blit(displayHand,(handBoxLoc[8]+handGap[0],gameHeight-36+handGap[1]))
        for x in range(0,len(colorPresets)):
            draw.rect(screen,colorPresets[x],(handBoxLoc[x],gameHeight-36,handBoxSize[0],handBoxSize[1]))
            if colorPresets[x] != white:
                displayHand = nameFont.render(str(sortedHand[turnPlayer][x]),1,white)
            else:
                displayHand = nameFont.render(str(sortedHand[turnPlayer][x]),1,black)
            screen.blit(displayHand,(handBoxLoc[x]+handGap[0],gameHeight-36+handGap[1]))
            
        #Route display
        draw.rect(screen,bgColor[turnPlayer],(gameWidth/2+40,gameHeight-routeDisplaySize[1],routeDisplaySize[0],routeDisplaySize[1]))
        screen.blit(routeTitle,(gameWidth/2+170,gameHeight-52))
        draw.rect(screen,darkgray,(gameWidth/2+66,gameHeight-routeDisplaySize[1]+14,256,16))
        if len(playerRoutes[turnPlayer])- routeScroller[turnPlayer] != 1:
            draw.rect(screen,darkgray,(gameWidth/2+66,gameHeight-routeDisplaySize[1]+32,256,16))
            route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][1]]),1,white)
        if len(playerRoutes[turnPlayer]) - routeScroller[turnPlayer] <= 2:
            draw.rect(screen,medgray,(gameWidth/2+324,gameHeight-routeDisplaySize[1]+18,22,26))
            rightArrow = routeArrowFont.render(">",1,lightgray)
        else:
            draw.rect(screen,darkgray,(gameWidth/2+324,gameHeight-routeDisplaySize[1]+18,22,26))
            if mouseWithin([(gameWidth/2+324,gameHeight-34),(gameWidth/2+346,gameHeight-8)]) and (option == 0 or option == 3):
                rightArrow = routeArrowFont.render(">",1,yellow)
            else:
                rightArrow = routeArrowFont.render(">",1,white)
        if routeScroller[turnPlayer] == 0:
                draw.rect(screen,medgray,(gameWidth/2+42,gameHeight-routeDisplaySize[1]+18,22,26))
                leftArrow = routeArrowFont.render("<",1,lightgray)
        else:
            draw.rect(screen,darkgray,(gameWidth/2+42,gameHeight-routeDisplaySize[1]+18,22,26))
            if mouseWithin([(gameWidth/2+42,gameHeight-34),(gameWidth/2+64,gameHeight-8)]) and (option == 0 or option == 3):
                leftArrow = routeArrowFont.render("<",1,yellow)
            else:
                leftArrow = routeArrowFont.render("<",1,white)
        screen.blit(rightArrow,(gameWidth/2+329,gameHeight-35))
        screen.blit(leftArrow,(gameWidth/2+46,gameHeight-35))
        
        #Final Turn
        if finalTurn != -1:
            screen.blit(finalText,(gameWidth/2-50,50))
        
        #Graph display
        for u,v,info in totalGraph.edges(data=True):
            #Edges
            if info['owned'] == -1:
                displayCol = darkgray
                if (u == citySelect1 and v == citySelect2) or (v == citySelect1 and u == citySelect2):
                    if citiesChosen == 2:
                        draw.line(screen,neongreen,(info['x1']+gameBorder,info['y1']+gameBorder+nameCoord[1]),(info['x2']+gameBorder,info['y2']+gameBorder+nameCoord[1]),8)
                    else:
                        draw.line(screen,yellow,(info['x1']+gameBorder,info['y1']+gameBorder+nameCoord[1]),(info['x2']+gameBorder,info['y2']+gameBorder+nameCoord[1]),8)
                draw.line(screen,displayCol,(info['x1']+gameBorder,info['y1']+gameBorder+nameCoord[1]),(info['x2']+gameBorder,info['y2']+gameBorder+nameCoord[1]),4)
                #Background circles
                if info['weight'] == 1 or info['weight'] == 3 or info['weight'] == 5 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.5+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.5+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                if info['weight'] == 3 or info['weight'] == 5 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.4+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.4+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.6+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.6+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                if info['weight'] == 5 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.3+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.3+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.7+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.7+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                if info['weight'] == 2 or info['weight'] == 4 or info['weight'] == 6 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.45+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.45+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.55+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.55+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                if info['weight'] == 4 or info['weight'] == 6 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.35+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.35+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.65+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.65+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                if info['weight'] == 6 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.25+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.25+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.75+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.75+info['y1'])+gameBorder+nameCoord[1]),dotOuterSize)
                #Inner circles
                for a in range(0,len(colors)):
                    if info['color'] == colors[a]:
                        displayCol = colorPresets[a]
                        break
                if info['color'] == "Any":
                    displayCol = lightgray
                if info['weight'] == 1 or info['weight'] == 3 or info['weight'] == 5 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.5+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.5+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                if info['weight'] == 3 or info['weight'] == 5 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.4+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.4+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.6+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.6+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                if info['weight'] == 5 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.3+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.3+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.7+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.7+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                if info['weight'] == 2 or info['weight'] == 4 or info['weight'] == 6 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.45+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.45+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.55+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.55+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                if info['weight'] == 4 or info['weight'] == 6 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.35+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.35+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.65+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.65+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                if info['weight'] == 6 :
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.25+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.25+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
                    draw.circle(screen,displayCol,(int((info['x2']-info['x1'])*0.75+info['x1']+gameBorder),int((info['y2']-info['y1'])*0.75+info['y1'])+gameBorder+nameCoord[1]),dotInnerSize)
            else:
                draw.line(screen,darkgray,(info['x1']+gameBorder,info['y1']+gameBorder+nameCoord[1]),(info['x2']+gameBorder,info['y2']+gameBorder+nameCoord[1]),6)
                #if info['owned'] == turnPlayer:
                draw.line(screen,playerColor[info['owned']],(info['x1']+gameBorder,info['y1']+gameBorder+nameCoord[1]),(info['x2']+gameBorder,info['y2']+gameBorder+nameCoord[1]),4)
                
            
        for a in range(1,nx.number_of_nodes(totalGraph)+1):
            draw.circle(screen,black,(graphWindow[0]+xCoords[a],graphWindow[1]+yCoords[a]),15)
            #Route buttons
            if playerRoutes[turnPlayer][routeScroller[turnPlayer]][3] == 1:
                r1color = neongreen
            else:
                r1color = yellow
            if (mouseWithin(r1Coord) and (option == 0 or option == 3 or option == 5)):
                if (a==playerRoutes[turnPlayer][routeScroller[turnPlayer]][0] or a==playerRoutes[turnPlayer][routeScroller[turnPlayer]][1]):
                        draw.circle(screen,r1color,(graphWindow[0]+xCoords[a],graphWindow[1]+yCoords[a]),10)
                pts = routeFont.render(str(playerRoutes[turnPlayer][routeScroller[turnPlayer]][2])+" pts",1,r1color)
                route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]][1]]),1,r1color)
            else:
                if playerRoutes[turnPlayer][routeScroller[turnPlayer]][3] == 1:
                    pts = routeFont.render(str(playerRoutes[turnPlayer][routeScroller[turnPlayer]][2])+" pts",1,r1color)
                    route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]][1]]),1,r1color)
                else:
                    pts = routeFont.render(str(playerRoutes[turnPlayer][routeScroller[turnPlayer]][2])+" pts",1,white)
                    route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]][1]]),1,white)
            screen.blit(pts,(gameWidth/2+280,gameHeight-38))
            screen.blit(route,(gameWidth/2+69,gameHeight-38))
            if len(playerRoutes[turnPlayer]) - routeScroller[turnPlayer] != 1:
                if playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][3] == 1:
                    r2color = neongreen
                else:
                    r2color = yellow
                if (mouseWithin(r2Coord) and (option == 0 or option == 3 or option == 5)):
                    if(a==playerRoutes[turnPlayer][1][0] or a==playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][1]):
                        draw.circle(screen,r2color,(graphWindow[0]+xCoords[a],graphWindow[1]+yCoords[a]),10)   
                    pts = routeFont.render(str(playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][2])+" pts",1,r2color)
                    route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][1]]),1,r2color)
                else:
                    if playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][3] == 1:
                        pts = routeFont.render(str(playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][2])+" pts",1,r2color)
                        route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][1]]),1,r2color)
                    else:    
                        pts = routeFont.render(str(playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][2])+" pts",1,white)
                        route = routeFont.render(str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][0]])+" to "+str(routeNames[playerRoutes[turnPlayer][routeScroller[turnPlayer]+1][1]]),1,white)
                screen.blit(pts,(gameWidth/2+280,gameHeight-20))
                screen.blit(route,(gameWidth/2+69,gameHeight-20))
        
        
        #Mini hand display
        draw.rect(screen,bgColor[turnPlayer],(105,gameHeight-buttonBg[1],136,buttonBg[1]))
        displayTitle = smallNameFont.render("Display Cards",1,white)
        screen.blit(displayTitle,(132,gameHeight-52))
        draw.rect(screen,darkgray,(107,gameHeight-38,132,buttonBg[1]))
        for x in range(0,5):
            if sortedDisplay[x] != 8:
                draw.rect(screen,colorPresets[sortedDisplay[x]],(109+(26*x),gameHeight-36,handBoxSize[0],handBoxSize[1]))
            else:
                screen.blit(wildCard,(109+(26*x),gameHeight-36))
        #Actions display
        draw.rect(screen,bgColor[turnPlayer],(gameWidth/2-104,gameHeight-buttonBg[1],buttonBg[0],buttonBg[1]))
        if option == 1:
            draw.rect(screen,medgray,(gameWidth/2-buttonBoxSize[0]*2-37,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
        else:
            draw.rect(screen,darkgray,(gameWidth/2-buttonBoxSize[0]*2-37,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
        
        if option == 3:
            draw.rect(screen,medgray,(gameWidth/2-33,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
        else:
            draw.rect(screen,darkgray,(gameWidth/2-33,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
        if option == 4:
            draw.rect(screen,medgray,(gameWidth/2+buttonBoxSize[0]-31,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
        else:
            draw.rect(screen,darkgray,(gameWidth/2+buttonBoxSize[0]-31,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
        screen.blit(actionTitle,(gameWidth/2-56,gameHeight-52))
        #Draw (D) button
        if (mouseWithin([(gameWidth/2-101,gameHeight-36),(gameWidth/2-69,gameHeight-4)]) and option == 0) or option == 1:
            displayAction = nameFont.render("D",1,yellow)
            if option == 0:
                screen.blit(drawDesc,(gameWidth/2-50,gameHeight-70))
        else:
            displayAction = nameFont.render("D",1,white)
        screen.blit(displayAction,(gameWidth/2-93,gameHeight-34))
        if len(routes) == 0:
            draw.rect(screen,medgray,(gameWidth/2-buttonBoxSize[0]-35,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
            displayAction = nameFont.render("R",1,lightgray)
        else:
            if option == 2 or option == 5:
                draw.rect(screen,medgray,(gameWidth/2-buttonBoxSize[0]-35,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
            else:
                draw.rect(screen,darkgray,(gameWidth/2-buttonBoxSize[0]-35,gameHeight-36,buttonBoxSize[0],buttonBoxSize[1]))
            #New routes (R) button
            if ((mouseWithin([(gameWidth/2-67,gameHeight-36),(gameWidth/2-35,gameHeight-4)]) and option == 0) or option == 2 or option == 5 ):
                displayAction = nameFont.render("R",1,yellow)
                if option == 0:
                    screen.blit(routeDesc,(gameWidth/2-52,gameHeight-70))
            else:
                displayAction = nameFont.render("R",1,white)
        screen.blit(displayAction,(gameWidth/2-58,gameHeight-34))
        #Buy ($) button
        if (mouseWithin([(gameWidth/2-33,gameHeight-36),(gameWidth/2-1,gameHeight-4)]) and option == 0) or option == 3:
            displayAction = nameFont.render("$",1,yellow)
            if option == 0:
                screen.blit(buyDesc,(gameWidth/2-100,gameHeight-70))
        else:
            displayAction = nameFont.render("$",1,white)
        screen.blit(displayAction,(gameWidth/2-24,gameHeight-34))
        #Exit (E) button
        if (mouseWithin([(gameWidth/2+1,gameHeight-36),(gameWidth/2+34,gameHeight-4)]) and option == 0) or option == 4:
            displayAction = nameFont.render("E",1,yellow)
            if option == 0:
                screen.blit(exitDesc,(gameWidth/2-71,gameHeight-70))
        else:
            displayAction = nameFont.render("E",1,white)
        screen.blit(displayAction,(gameWidth/2+10,gameHeight-34))
        
        #Mouse-over city name display
        if option == 0 and nearCity == -1:
            for a in range(1,len(xCoords)+1):
                if (mouseX-(xCoords[a]+gameBorder))**2 + (mouseY-(yCoords[a]+gameBorder+48))**2 < citySize**2:
                    nearCity = a
        if nearCity != -1:
            if (mouseX-(xCoords[nearCity]+gameBorder))**2 + (mouseY-(yCoords[nearCity]+gameBorder+nameCoord[1]))**2 < 225:
                cityX, cityY = smallNameFont.size(totalGraph.node[nearCity]['name'])
                city = smallNameFont.render(totalGraph.node[nearCity]['name'],1,black)
                screen.blit(city,(gameWidth/2-cityX/2,gameHeight-70))
            else:
                nearCity = -1
        
        
        #Displayed options
        if option == 1: #Drawing cards
            draw.rect(screen,darkgray,(gameWidth/2-optionWindow[0]/2-optionBorder,gameHeight/2-optionWindow[1]/2-optionBorder,optionWindow[0]+optionBorder*2,optionWindow[1]+optionBorder*2))
            draw.rect(screen,tan,(gameWidth/2-optionWindow[0]/2,gameHeight/2-optionWindow[1]/2,optionWindow[0],optionWindow[1]))
            if cardsTaken == 0:
                draw.rect(screen,darkgray,(gameWidth/2-42,gameHeight/2+113,84,34))
                if mouseWithin([(gameWidth/2-44,gameHeight/2+108),(gameWidth/2+44,gameHeight/2+146)]):
                    cancel = cancelFont.render("Cancel",1,yellow)
                else:
                    cancel = cancelFont.render("Cancel",1,white)
                screen.blit(cancel,(gameWidth/2-32,gameHeight/2+118))
            if cardsTaken == 1:
                screen.blit(drawSecond,(gameWidth/2-140,gameHeight/2-126))
            else:
                screen.blit(drawInfo,(gameWidth/2-170,gameHeight/2-126))
            #Backgrounds
            if mouseWithin([(gameWidth/2-104,gameHeight/2-82),(gameWidth/2-36,gameHeight/2)]):
                draw.rect(screen,yellow,(gameWidth/2-cardSize[0]*1.5-8,gameHeight/2-82,cardSize[0]+4,cardSize[1]+4))
            else:
                draw.rect(screen,darkgray,(gameWidth/2-cardSize[0]*1.5-8,gameHeight/2-82,cardSize[0]+4,cardSize[1]+4))
            if mouseWithin([(gameWidth/2-34,gameHeight/2-82),(gameWidth/2+30,gameHeight/2)]) and (sortedDisplay[0] != 8 or cardsTaken == 0):
                draw.rect(screen,yellow,(gameWidth/2-cardSize[0]/2-2,gameHeight/2-82,cardSize[0]+4,cardSize[1]+4))
            else:
                if mouseWithin([(gameWidth/2-34,gameHeight/2-82),(gameWidth/2+30,gameHeight/2)]):
                    screen.blit(wildWarn,(gameWidth/2-110,gameHeight/2-103))
                draw.rect(screen,darkgray,(gameWidth/2-cardSize[0]/2-2,gameHeight/2-82,cardSize[0]+4,cardSize[1]+4))
            if mouseWithin([(gameWidth/2+36,gameHeight/2-82),(gameWidth/2+104,gameHeight/2)]) and (sortedDisplay[1] != 8 or cardsTaken == 0):
                draw.rect(screen,yellow,(gameWidth/2+cardSize[0]/2+4,gameHeight/2-82,cardSize[0]+4,cardSize[1]+4))
            else:
                if mouseWithin([(gameWidth/2+36,gameHeight/2-82),(gameWidth/2+104,gameHeight/2)]):
                    screen.blit(wildWarn,(gameWidth/2-110,gameHeight/2-103))
                draw.rect(screen,darkgray,(gameWidth/2+cardSize[0]/2+4,gameHeight/2-82,cardSize[0]+4,cardSize[1]+4))
            if mouseWithin([(gameWidth/2-104,gameHeight/2+6),(gameWidth/2-36,gameHeight/2+88)]) and (sortedDisplay[2] != 8 or cardsTaken == 0):
                draw.rect(screen,yellow,(gameWidth/2-cardSize[0]*1.5-8,gameHeight/2+6,cardSize[0]+4,cardSize[1]+4))
            else:
                if mouseWithin([(gameWidth/2-104,gameHeight/2+6),(gameWidth/2-36,gameHeight/2+88)]):
                    screen.blit(wildWarn,(gameWidth/2-110,gameHeight/2-103))
                draw.rect(screen,darkgray,(gameWidth/2-cardSize[0]*1.5-8,gameHeight/2+6,cardSize[0]+4,cardSize[1]+4))
            if mouseWithin([(gameWidth/2-34,gameHeight/2+6),(gameWidth/2+30,gameHeight/2+88)]) and (sortedDisplay[3] != 8 or cardsTaken == 0):
                draw.rect(screen,yellow,(gameWidth/2-cardSize[0]/2-2,gameHeight/2+6,cardSize[0]+4,cardSize[1]+4))
            else:
                if mouseWithin([(gameWidth/2-34,gameHeight/2+6),(gameWidth/2+30,gameHeight/2+88)]):
                    screen.blit(wildWarn,(gameWidth/2-110,gameHeight/2-103))
                draw.rect(screen,darkgray,(gameWidth/2-cardSize[0]/2-2,gameHeight/2+6,cardSize[0]+4,cardSize[1]+4))
            if mouseWithin([(gameWidth/2+36,gameHeight/2+6),(gameWidth/2+104,gameHeight/2+88)]) and (sortedDisplay[4] != 8 or cardsTaken == 0):
                draw.rect(screen,yellow,(gameWidth/2+cardSize[0]/2+4,gameHeight/2+6,cardSize[0]+4,cardSize[1]+4))
            else:
                if mouseWithin([(gameWidth/2+36,gameHeight/2+6),(gameWidth/2+104,gameHeight/2+88)]):
                    screen.blit(wildWarn,(gameWidth/2-110,gameHeight/2-103))
                draw.rect(screen,darkgray,(gameWidth/2+cardSize[0]/2+4,gameHeight/2+6,cardSize[0]+4,cardSize[1]+4))
            #Card inside fills
            draw.rect(screen,brown,(gameWidth/2-cardSize[0]*1.5-6,gameHeight/2-80,cardSize[0],cardSize[1]))
            if sortedDisplay[0] != 8:
                draw.rect(screen,colorPresets[sortedDisplay[0]],(gameWidth/2-cardSize[0]/2,gameHeight/2-80,cardSize[0],cardSize[1]))
            else:
                screen.blit(wildCardLarge,(gameWidth/2-cardSize[0]/2,gameHeight/2-80))
            if sortedDisplay[1] != 8:
                draw.rect(screen,colorPresets[sortedDisplay[1]],(gameWidth/2+cardSize[0]/2+6,gameHeight/2-80,cardSize[0],cardSize[1]))
            else:
                screen.blit(wildCardLarge,(gameWidth/2+cardSize[0]/2+6,gameHeight/2-80))
            if sortedDisplay[2] != 8:
                draw.rect(screen,colorPresets[sortedDisplay[2]],(gameWidth/2-cardSize[0]*1.5-6,gameHeight/2+8,cardSize[0],cardSize[1]))
            else:
                screen.blit(wildCardLarge,(gameWidth/2-cardSize[0]*1.5-6,gameHeight/2+8))
            if sortedDisplay[3] != 8:
                draw.rect(screen,colorPresets[sortedDisplay[3]],(gameWidth/2-cardSize[0]/2,gameHeight/2+8,cardSize[0],cardSize[1]))
            else:
                screen.blit(wildCardLarge,(gameWidth/2-cardSize[0]/2,gameHeight/2+8))
            if sortedDisplay[4] != 8:
                draw.rect(screen,colorPresets[sortedDisplay[4]],(gameWidth/2+cardSize[0]/2+6,gameHeight/2+8,cardSize[0],cardSize[1]))
            else:
                screen.blit(wildCardLarge,(gameWidth/2+cardSize[0]/2+6,gameHeight/2+8))
            screen.blit(deckTitle,(gameWidth/2-cardSize[0]*1.5+10,gameHeight/2-55))
            deckCount = smallNameFont.render(str(len(deck)),1,white)
            screen.blit(deckCount,(gameWidth/2-cardSize[0]*1.5+17,gameHeight/2-40))
            

            if cardsTaken >= 2:
                cardsTaken = 0
                option = 0
                nextPlayer()
            
        if option == 2:
            draw.rect(screen,darkgray,(gameWidth/2-routeConfirmBox[0]/2-optionBorder,gameHeight/2-routeConfirmBox[1]/2-optionBorder-10,routeConfirmBox[0]+optionBorder*2,routeConfirmBox[1]+optionBorder*2))
            draw.rect(screen,tan,(gameWidth/2-routeConfirmBox[0]/2,gameHeight/2-routeConfirmBox[1]/2-10,routeConfirmBox[0],routeConfirmBox[1]))
            draw.rect(screen,darkgray,(gameWidth/2+4,gameHeight/2,84,34))
            draw.rect(screen,darkgray,(gameWidth/2-88,gameHeight/2,84,34))
            screen.blit(routeConfirm,(gameWidth/2-208,gameHeight/2-50))
            if len(routes) == 2:
                routeWarn = smallNameFont.render("Warning: There are only 2 cards left that can be added",1,darkgray)
                screen.blit(routeWarn,(gameWidth/2-150,gameHeight/2-30))
            if len(routes) == 1:
                routeWarn = smallNameFont.render("Warning: There is only 1 card left that can be added",1,darkgray)
                screen.blit(routeWarn,(gameWidth/2-150,gameHeight/2-30))
            if mouseWithin([(gameWidth/2+4,gameHeight/2),(gameWidth/2+88,gameHeight/2+34)]):
                cancel = cancelFont.render("No",1,yellow)
            else:
                cancel = cancelFont.render("No",1,white)
            screen.blit(cancel,(gameWidth/2+35,gameHeight/2+6))
            if mouseWithin([(gameWidth/2-88,gameHeight/2),(gameWidth/2+-4,gameHeight/2+34)]):
                cancel = cancelFont.render("Yes",1,yellow)
            else:
                cancel = cancelFont.render("Yes",1,white)
            screen.blit(cancel,(gameWidth/2-64,gameHeight/2+6))
        if option == 5: #second part of route options
            draw.rect(screen,lightgray,(gameWidth/2-150,gameHeight-125,360,72))
            screen.blit(routeDesc2,(gameWidth/2-150,gameHeight-121))
            if len(routes) > 1:
                draw.rect(screen,darkgray,(gameWidth/2-128,gameHeight-88,256,16))
            if len(routes) > 2:
                draw.rect(screen,darkgray,(gameWidth/2-128,gameHeight-106,256,16))
            if takeRoute1 == False and takeRoute2 == False and takeRoute3 == False:
                draw.rect(screen,medgray,(gameWidth/2+132,gameHeight-96,74,34))
                add = cancelFont.render("Add",1,lightgray)
                screen.blit(add,(gameWidth/2+148,gameHeight-91))
            else:
                if mouseWithin([(gameWidth/2+132,gameHeight-96),(gameWidth/2+206,gameHeight-62)]):
                    add = cancelFont.render("Add",1,yellow)
                else:
                    add = cancelFont.render("Add",1,white)
                draw.rect(screen,playerColor[turnPlayer],(gameWidth/2+132,gameHeight-96,74,34))
                screen.blit(add,(gameWidth/2+148,gameHeight-91))
                
            draw.rect(screen,darkgray,(gameWidth/2-128,gameHeight-70,256,16))
            for a in range(1,nx.number_of_nodes(totalGraph)+1): #Lowest box - checks final route card
                if mouseWithin([(gameWidth/2-128,gameHeight-70),(gameWidth/2+128,gameHeight-54)]):
                    if (a==routes[len(routes)-1][0] or a==routes[len(routes)-1][1]):
                            draw.circle(screen,yellow,(graphWindow[0]+xCoords[a],graphWindow[1]+yCoords[a]),10)
                    pts = routeFont.render(str(routes[len(routes)-1][2])+" pts",1,yellow)
                    route = routeFont.render(str(routeNames[routes[len(routes)-1][0]])+" to "+str(routeNames[routes[len(routes)-1][1]]),1,yellow)
                else:
                    if takeRoute1 == True:
                        pts = routeFont.render(str(routes[len(routes)-1][2])+" pts",1,neongreen)
                        route = routeFont.render(str(routeNames[routes[len(routes)-1][0]])+" to "+str(routeNames[routes[len(routes)-1][1]]),1,neongreen)
                    else:
                        pts = routeFont.render(str(routes[len(routes)-1][2])+" pts",1,white)
                        route = routeFont.render(str(routeNames[routes[len(routes)-1][0]])+" to "+str(routeNames[routes[len(routes)-1][1]]),1,white)
                screen.blit(pts,(gameWidth/2+85,gameHeight-69))
                screen.blit(route,(gameWidth/2-126,gameHeight-69))
                if len(routes) > 1: #Button 2
                    if mouseWithin([(gameWidth/2-128,gameHeight-86),(gameWidth/2+128,gameHeight-70)]):
                        if (a==routes[len(routes)-2][0] or a==routes[len(routes)-2][1]):
                                draw.circle(screen,yellow,(graphWindow[0]+xCoords[a],graphWindow[1]+yCoords[a]),10)
                        pts = routeFont.render(str(routes[len(routes)-2][2])+" pts",1,yellow)
                        route = routeFont.render(str(routeNames[routes[len(routes)-2][0]])+" to "+str(routeNames[routes[len(routes)-2][1]]),1,yellow)
                    else:
                        if takeRoute2 == True:
                            pts = routeFont.render(str(routes[len(routes)-2][2])+" pts",1,neongreen)
                            route = routeFont.render(str(routeNames[routes[len(routes)-2][0]])+" to "+str(routeNames[routes[len(routes)-2][1]]),1,neongreen)
                        else: 
                            pts = routeFont.render(str(routes[len(routes)-2][2])+" pts",1,white)
                            route = routeFont.render(str(routeNames[routes[len(routes)-2][0]])+" to "+str(routeNames[routes[len(routes)-2][1]]),1,white)
                    screen.blit(pts,(gameWidth/2+85,gameHeight-87))
                    screen.blit(route,(gameWidth/2-126,gameHeight-87))
                if len(routes) > 2: #Button 3
                    if mouseWithin([(gameWidth/2-128,gameHeight-104),(gameWidth/2+128,gameHeight-88)]):
                        if (a==routes[len(routes)-3][0] or a==routes[len(routes)-3][1]):
                                draw.circle(screen,yellow,(graphWindow[0]+xCoords[a],graphWindow[1]+yCoords[a]),10)
                        pts = routeFont.render(str(routes[len(routes)-3][2])+" pts",1,yellow)
                        route = routeFont.render(str(routeNames[routes[len(routes)-3][0]])+" to "+str(routeNames[routes[len(routes)-3][1]]),1,yellow)
                    else:
                        if takeRoute3 == True:
                            pts = routeFont.render(str(routes[len(routes)-3][2])+" pts",1,neongreen)
                            route = routeFont.render(str(routeNames[routes[len(routes)-3][0]])+" to "+str(routeNames[routes[len(routes)-3][1]]),1,neongreen)
                        else:
                            pts = routeFont.render(str(routes[len(routes)-3][2])+" pts",1,white)
                            route = routeFont.render(str(routeNames[routes[len(routes)-3][0]])+" to "+str(routeNames[routes[len(routes)-3][1]]),1,white)
                    screen.blit(pts,(gameWidth/2+85,gameHeight-105))
                    screen.blit(route,(gameWidth/2-126,gameHeight-105))
                    
                    
                    
            
        if option == 3:
            draw.rect(screen,lightgray,(gameWidth-78,gameHeight-90,78,38))
            draw.rect(screen,darkgray,(gameWidth-76,gameHeight-88,74,34))
            if mouseWithin([(gameWidth-86,gameHeight-88),(gameWidth-2,gameHeight-54)]):
                cancel = cancelFont.render("Cancel",1,yellow)
            else:
                cancel = cancelFont.render("Cancel",1,white)
            screen.blit(cancel,(gameWidth-71,gameHeight-82))
            if citiesChosen == 0 :
                screen.blit(buy1,(gameWidth/2-120,gameHeight-70))
                if citySelect1 == -1:
                    for a in range(1,len(xCoords)+1):
                        if (mouseX-(xCoords[a]+gameBorder))**2 + (mouseY-(yCoords[a]+gameBorder+48))**2 < citySize**2:
                            citySelect1 = a
                else:
                    if (mouseX-(xCoords[citySelect1]+gameBorder))**2 + (mouseY-(yCoords[citySelect1]+gameBorder+nameCoord[1]))**2 < 225:
                        draw.circle(screen,yellow,(graphWindow[0]+xCoords[citySelect1],graphWindow[1]+yCoords[citySelect1]),10)
                    else:
                        citySelect1 = -1
            if citiesChosen == 1 :
                screen.blit(buy2,(gameWidth/2-120,gameHeight-70))
                draw.circle(screen,neongreen,(graphWindow[0]+xCoords[citySelect1],graphWindow[1]+yCoords[citySelect1]),10)
                if citySelect2 == -1 and citySelect2 != citySelect1:
                    for a in range(1,len(xCoords)+1):
                        if (mouseX-(xCoords[a]+gameBorder))**2 + (mouseY-(yCoords[a]+gameBorder+48))**2 < 225:
                            for b in nx.neighbors(totalGraph,citySelect1):
                                if b == a:
                                    citySelect2 = a
                else:
                    if (mouseX-(xCoords[citySelect2]+gameBorder))**2 + (mouseY-(yCoords[citySelect2]+gameBorder+nameCoord[1]))**2 < 225 and citySelect1 != citySelect2:
                        draw.circle(screen,yellow,(graphWindow[0]+xCoords[citySelect2],graphWindow[1]+yCoords[citySelect2]),10)
                    else:
                        citySelect2 = -1
            if citiesChosen == 2:
                """If 'any' color railroad is bought"""
                if totalGraph[citySelect1][citySelect2][1]['color'] == "Any":
                    if totalGraph[citySelect1][citySelect2][1]['owned'] == -1 and numTrains[turnPlayer] >= totalGraph[citySelect1][citySelect2][1]['weight']:
                        for x in range(0,len(colorPresets)):
                            if hand[turnPlayer].count(colors[x])+hand[turnPlayer].count("Wild") >= totalGraph[citySelect1][citySelect2][1]['weight']:
                                anyCol.append((colors[x],colorPresets[x]))
                    elif totalGraph.has_edge(citySelect1,citySelect2,key=2) and totalGraph[citySelect1][citySelect2][2]['owned'] == -1 and numTrains[turnPlayer] >= totalGraph[citySelect1][citySelect2][2]['weight']:
                        for x in range(0,len(colorPresets)):
                            if hand[turnPlayer].count(colors[x])+hand[turnPlayer].count("Wild") >= totalGraph[citySelect1][citySelect2][1]['weight']:
                                anyCol.append((colors[x],colorPresets[x]))
                    if len(anyCol) == 0:
                        draw.rect(screen,medgray,(gameWidth-76,gameHeight-124,74,34))
                        buyButton1= cancelFont.render("Buy",1,lightgray)
                        screen.blit(buyButton1,(gameWidth-55,gameHeight-118))
                    else:
                        draw.rect(screen,anyCol[0][1],(gameWidth-76,gameHeight-124,74,34))
                        if mouseWithin([(gameWidth-76,gameHeight-124),(gameWidth-2,gameHeight-90)]):
                            if anyCol[0][1] == yellow or anyCol[0][1] == white:
                                buyButton1 = cancelFont.render("Buy",1,black)
                            else:
                                buyButton1 = cancelFont.render("Buy",1,yellow)
                        else:
                            if anyCol[0][1] == yellow or anyCol[0][1] == white:
                                buyButton1 = cancelFont.render("Buy",1,medgray)
                            else:
                                buyButton1 = cancelFont.render("Buy",1,white)
                        screen.blit(buyButton1,(gameWidth-55,gameHeight-118))
                        if len(anyCol) > 1:
                            draw.rect(screen,anyCol[1][1],(gameWidth-76,gameHeight-160,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-160),(gameWidth-2,gameHeight-126)]):
                                if anyCol[1][1] == yellow or anyCol[1][1] == white:
                                    buyButton2 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton2 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[1][1] == yellow or anyCol[1][1] == white:
                                    buyButton2 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton2 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton2,(gameWidth-55,gameHeight-154))
                        if len(anyCol) > 2:
                            draw.rect(screen,anyCol[2][1],(gameWidth-76,gameHeight-196,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-196),(gameWidth-2,gameHeight-162)]):
                                if anyCol[2][1] == yellow or anyCol[1][1] == white:
                                    buyButton3 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton3 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[2][1] == yellow or anyCol[2][1] == white:
                                    buyButton3 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton3 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton3,(gameWidth-55,gameHeight-190))
                        if len(anyCol) > 3:
                            draw.rect(screen,anyCol[3][1],(gameWidth-76,gameHeight-232,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-232),(gameWidth-2,gameHeight-198)]):
                                if anyCol[3][1] == yellow or anyCol[3][1] == white:
                                    buyButton4 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton4 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[3][1] == yellow or anyCol[3][1] == white:
                                    buyButton4 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton4 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton4,(gameWidth-55,gameHeight-226))
                        if len(anyCol) > 4:
                            draw.rect(screen,anyCol[4][1],(gameWidth-76,gameHeight-268,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-268),(gameWidth-2,gameHeight-234)]):
                                if anyCol[4][1] == yellow or anyCol[4][1] == white:
                                    buyButton5 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton5 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[4][1] == yellow or anyCol[4][1] == white:
                                    buyButton5 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton5 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton5,(gameWidth-55,gameHeight-262))
                        if len(anyCol) > 5:
                            draw.rect(screen,anyCol[5][1],(gameWidth-76,gameHeight-304,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-304),(gameWidth-2,gameHeight-270)]):
                                if anyCol[5][1] == yellow or anyCol[5][1] == white:
                                    buyButton6 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton6 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[5][1] == yellow or anyCol[5][1] == white:
                                    buyButton6 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton6 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton6,(gameWidth-55,gameHeight-298))
                        if len(anyCol) > 6:
                            draw.rect(screen,anyCol[6][1],(gameWidth-76,gameHeight-340,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-340),(gameWidth-2,gameHeight-306)]):
                                if anyCol[6][1] == yellow or anyCol[6][1] == white:
                                    buyButton7 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton7 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[6][1] == yellow or anyCol[6][1] == white:
                                    buyButton7 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton7 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton7,(gameWidth-55,gameHeight-336))
                        if len(anyCol) > 7:
                            draw.rect(screen,anyCol[7][1],(gameWidth-76,gameHeight-376,74,34))
                            if mouseWithin([(gameWidth-76,gameHeight-376),(gameWidth-2,gameHeight-342)]):
                                if anyCol[7][1] == yellow or anyCol[7][1] == white:
                                    buyButton8 = cancelFont.render("Buy",1,black)
                                else:
                                    buyButton8 = cancelFont.render("Buy",1,yellow)
                            else:
                                if anyCol[7][1] == yellow or anyCol[7][1] == white:
                                    buyButton8 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton8 = cancelFont.render("Buy",1,white)
                            screen.blit(buyButton8,(gameWidth-55,gameHeight-370))
                else:
                    screen.blit(buy3,(gameWidth/2-110,gameHeight-70))
                    """ Displaying the lower button (key 1) when buying a railroad """
                    for a in range(0,len(colors)):
                        if totalGraph[citySelect1][citySelect2][1]['color'] == colors[a]:
                            if hand[turnPlayer].count(colors[a])+hand[turnPlayer].count("Wild") >= totalGraph[citySelect1][citySelect2][1]['weight']  and totalGraph[citySelect1][citySelect2][1]['owned'] == -1 and numTrains[turnPlayer] >= totalGraph[citySelect1][citySelect2][1]['weight']:
                                if totalGraph.has_edge(citySelect1,citySelect2,key=2) and totalGraph[citySelect1][citySelect2][2]['owned'] == turnPlayer:
                                        activeButton1 = False
                                        displayColor = medgray
                                else:
                                    activeButton1 = True
                                    displayColor = colorPresets[a]
                            else:
                                activeButton1 = False
                                displayColor = medgray
                    draw.rect(screen,displayColor,(gameWidth-76,gameHeight-124,74,34))
                    if activeButton1 == True:
                        if mouseWithin([(gameWidth-76,gameHeight-124),(gameWidth-2,gameHeight-90)]):
                            if displayColor == yellow or displayColor == white:
                                buyButton1 = cancelFont.render("Buy",1,black)
                            else:
                                buyButton1 = cancelFont.render("Buy",1,yellow)
                        else:
                            if displayColor == yellow or displayColor == white:
                                buyButton1 = cancelFont.render("Buy",1,medgray)
                            else:
                                buyButton1 = cancelFont.render("Buy",1,white)
                    else:
                        buyButton1= cancelFont.render("Buy",1,lightgray)
                    screen.blit(buyButton1,(gameWidth-55,gameHeight-118))
                    """ Displaying the upper button (key 2 when buying a railroad"""
                    if totalGraph.has_edge(citySelect1,citySelect2,key=2):
                        if totalGraph[citySelect1][citySelect2][2]['color'] == "Any":
                            activeButton = False
                            for a in range(0,len(colors)):
                                if hand[turnPlayer].count(colors[a])+hand[turnPlayer].count("Wild") >= totalGraph[citySelect1][citySelect2][1]['weight']:
                                    activeButton = True
                                    displayColor = medgray
                        else:
                            for a in range(0,len(colors)):
                                if totalGraph[citySelect1][citySelect2][2]['color'] == colors[a]:
                                    if hand[turnPlayer].count(colors[a])+hand[turnPlayer].count("Wild") >= totalGraph[citySelect1][citySelect2][2]['weight'] and totalGraph[citySelect1][citySelect2][2]['owned'] == -1 and numTrains[turnPlayer] >= totalGraph[citySelect1][citySelect2][2]['weight'] and totalGraph[citySelect1][citySelect2][1]['owned'] != turnPlayer:
                                        activeButton2 = True
                                        displayColor = colorPresets[a]
                                    else:
                                        activeButton2 = False
                                        displayColor = medgray
                        draw.rect(screen,displayColor,(gameWidth-76,gameHeight-160,74,34))
                        if activeButton2 == True:
                            if mouseWithin([(gameWidth-76,gameHeight-160),(gameWidth-2,gameHeight-126)]):
                                if displayColor == yellow or displayColor == white:
                                    buyButton2= cancelFont.render("Buy",1,black)
                                else:
                                    buyButton2 = cancelFont.render("Buy",1,yellow)
                            else:
                                if displayColor == yellow or displayColor == white:
                                    buyButton2 = cancelFont.render("Buy",1,medgray)
                                else:
                                    buyButton2 = cancelFont.render("Buy",1,white)
                        else:
                            buyButton2 = cancelFont.render("Buy",1,lightgray)
                        screen.blit(buyButton2,(gameWidth-55,gameHeight-154))
        
        if option == 4: #Exit
            draw.rect(screen,darkgray,(gameWidth/2-exitWindow[0]/2-optionBorder,gameHeight/2-exitWindow[1]/2-optionBorder,exitWindow[0]+optionBorder*2,exitWindow[1]+optionBorder*2))
            draw.rect(screen,tan,(gameWidth/2-exitWindow[0]/2,gameHeight/2-exitWindow[1]/2,exitWindow[0],exitWindow[1]))
            draw.rect(screen,darkgray,(gameWidth/2+4,gameHeight/2,84,34))
            draw.rect(screen,darkgray,(gameWidth/2-88,gameHeight/2,84,34))
            screen.blit(saveExit,(gameWidth/2-84,gameHeight/2-30))
            if mouseWithin([(gameWidth/2+4,gameHeight/2),(gameWidth/2+88,gameHeight/2+34)]):
                cancel = cancelFont.render("Cancel",1,yellow)
            else:
                cancel = cancelFont.render("Cancel",1,white)
            screen.blit(cancel,(gameWidth/2+14,gameHeight/2+6))
            if mouseWithin([(gameWidth/2-88,gameHeight/2),(gameWidth/2+-4,gameHeight/2+34)]):
                cancel = cancelFont.render("Exit",1,yellow)
            else:
                cancel = cancelFont.render("Exit",1,white)
            screen.blit(cancel,(gameWidth/2-64,gameHeight/2+6))
            
    if room == 2: #Post-game window
        if screenCheck2 == False:
            screenCheck2 = True
            gameWidth = 640
            gameHeight = 480
            screen = pygame.display.set_mode((gameWidth,gameHeight))
            if gameSave == 1:
                if os.path.isfile("save1.txt"):
                    os.remove("save1.txt")
            if gameSave == 2:
                if os.path.isfile("save2.txt"):
                    os.remove("save2.txt")
            if gameSave == 3:
                if os.path.isfile("save3.txt"):
                    os.remove("save3.txt")
            routesComplete = [0,0,0,0,0]
            routesIncomplete = [0,0,0,0,0]
            
            for x in range(0,numPlayers):
                for y in range(0,len(playerRoutes[x])):
                    if playerRoutes[x][y][3] == -1 or playerRoutes[x][y][3] == 0:
                        routesIncomplete[x] -= playerRoutes[x][y][2]
                    else:
                        routesComplete[x] += playerRoutes[x][y][2]
            totalScores = []
            for x in range(0,numPlayers):
                totalScores.append((x,points[x]+routesComplete[x]+routesIncomplete[x]))
            placeOrder = []
            for x in range(0,numPlayers):
                placeOrder.append(totalScores[x][1])
            placeOrder.sort()
            placeOrder.reverse()
            placeFinal = [5,5,5,5,5]
            for x in range(0,numPlayers):
                for y in range(0,numPlayers):
                    if placeOrder[y] == totalScores[x][1]:
                        placeFinal[x] = y+1
        screen.fill(tan)
        gameFinished = titleFont.render("Game complete!",1,darkgray)
        playerFinal = nameFont.render("Player",1,darkgray)
        pointsFinal = nameFont.render("Points",1,darkgray)
        compFinal = nameFont.render("Complete",1,darkgray)
        routesFinal = nameFont.render("Routes",1,darkgray)
        incompFinal = nameFont.render("Incomplete",1,darkgray)
        totalFinal = nameFont.render("Total Points",1,darkgray)
        place = nameFont.render("Place",1,darkgray)
        screen.blit(gameFinished,(190,20))
        screen.blit(pointsFinal,(40,150))
        screen.blit(compFinal,(25,200))
        screen.blit(routesFinal,(40,220))
        screen.blit(incompFinal,(15,270))
        screen.blit(routesFinal,(40,290))
        screen.blit(totalFinal,(10,340))
        screen.blit(place,(48,395))
        draw.line(screen,darkgray,(5,120),(635,120))
        draw.line(screen,darkgray,(145,5),(145,475))
        
        if numPlayers == 5:
            placements = [160,255,350,445,540]
        if numPlayers == 4:
            placements = [180,285,390,495]
        if numPlayers == 3:
            placements = [200,340,480]
        if numPlayers == 2:
            placements = [250,420]
        rowPlace = [150,210,280,340,395]
            
        p1 = cancelFont.render(name[0],1,darkgray)
        screen.blit(p1,(placements[0],100))
        p1points = cancelFont.render(str(points[0]),1,darkgray)
        screen.blit(p1points,(placements[0]+20,rowPlace[0]))
        p1comp = cancelFont.render(str(routesComplete[0]),1,darkgray)
        screen.blit(p1comp,(placements[0]+20,rowPlace[1]))
        p1incomp = cancelFont.render(str(routesIncomplete[0]),1,darkgray)
        screen.blit(p1incomp,(placements[0]+20,rowPlace[2]))
        p1total = cancelFont.render(str(totalScores[0][1]),1,darkgray)
        screen.blit(p1total,(placements[0]+20,rowPlace[3]))
        p1place = cancelFont.render(str(placeFinal[0]),1,darkgray)
        screen.blit(p1place,(placements[0]+20,rowPlace[4]))
        
        p2 = cancelFont.render(name[1],1,darkgray)
        screen.blit(p2,(placements[1],100))
        p2points = cancelFont.render(str(points[1]),1,darkgray)
        screen.blit(p2points,(placements[1]+20,rowPlace[0]))
        p2comp = cancelFont.render(str(routesComplete[1]),1,darkgray)
        screen.blit(p2comp,(placements[1]+20,rowPlace[1]))
        p2incomp = cancelFont.render(str(routesIncomplete[1]),1,darkgray)
        screen.blit(p2incomp,(placements[1]+20,rowPlace[2]))
        p2total = cancelFont.render(str(totalScores[1][1]),1,darkgray)
        screen.blit(p2total,(placements[1]+20,rowPlace[3]))
        p2place = cancelFont.render(str(placeFinal[1]),1,darkgray)
        screen.blit(p2place,(placements[1]+20,rowPlace[4]))
        if numPlayers > 2:
            p3 = cancelFont.render(name[2],1,darkgray)
            screen.blit(p3,(placements[2],100))
            p3points = cancelFont.render(str(points[2]),1,darkgray)
            screen.blit(p3points,(placements[2]+20,rowPlace[0]))
            p3comp = cancelFont.render(str(routesComplete[2]),1,darkgray)
            screen.blit(p3comp,(placements[2]+20,rowPlace[1]))
            p3incomp = cancelFont.render(str(routesIncomplete[2]),1,darkgray)
            screen.blit(p3incomp,(placements[2]+20,rowPlace[2]))
            p3total = cancelFont.render(str(totalScores[2][1]),1,darkgray)
            screen.blit(p3total,(placements[2]+20,rowPlace[3]))
            p3place = cancelFont.render(str(placeFinal[2]),1,darkgray)
            screen.blit(p3place,(placements[2]+20,rowPlace[4]))
        if numPlayers > 3:
            p4 = cancelFont.render(name[3],1,darkgray)
            screen.blit(p4,(placements[3],100))
            p4points = cancelFont.render(str(points[3]),1,darkgray)
            screen.blit(p4points,(placements[3]+20,rowPlace[0]))
            p4comp = cancelFont.render(str(routesComplete[3]),1,darkgray)
            screen.blit(p4comp,(placements[3]+20,rowPlace[1]))
            p4incomp = cancelFont.render(str(routesIncomplete[3]),1,darkgray)
            screen.blit(p4incomp,(placements[3]+20,rowPlace[2]))
            p4total = cancelFont.render(str(totalScores[3][1]),1,darkgray)
            screen.blit(p4total,(placements[3]+20,rowPlace[3]))
            p4place = cancelFont.render(str(placeFinal[3]),1,darkgray)
            screen.blit(p4place,(placements[3]+20,rowPlace[4]))
        if numPlayers > 4:
            p5 = cancelFont.render(name[4],1,darkgray)
            screen.blit(p5,(placements[4],100))
            p5points = cancelFont.render(str(points[4]),1,darkgray)
            screen.blit(p5points,(placements[4]+20,rowPlace[0]))
            p5comp = cancelFont.render(str(routesComplete[4]),1,darkgray)
            screen.blit(p5comp,(placements[4]+20,rowPlace[1]))
            p5incomp = cancelFont.render(str(routesIncomplete[4]),1,darkgray)
            screen.blit(p5incomp,(placements[4]+20,rowPlace[2]))
            p5total = cancelFont.render(str(totalScores[4][1]),1,darkgray)
            screen.blit(p5total,(placements[4]+20,rowPlace[3]))
            p5place = cancelFont.render(str(placeFinal[4]),1,darkgray)
            screen.blit(p5place,(placements[4]+20,rowPlace[4]))
        
        
        
        draw.rect(screen,darkgray,(350,446,80,30))
        if mouseWithin([(350,446),(430,476)]):
            exitFinal = cancelFont.render("Exit",1,yellow)
        else:
            exitFinal = cancelFont.render("Exit",1,white)
        screen.blit(exitFinal,(372,450))
        
        
        
        
            
            
        """END DISPLAY EVENTS HERE"""
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameEnd = True        
            
        """=============================BEGIN CLICKING EVENTS HERE================================"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            """Title Screen"""
            if room == 0: #draw.rect(screen,medgray,(420,380,70,30))
                if option != 0:
                    if mouseWithin([(420,380),(490,410)]) and ((option == 1 and save1 == True) or (option == 2 and save2 == True) or (option == 3 and save3 == True)):
                        #Continue/start game
                        room = 1
                        gameSave = option
                        saveSection = 1
                        if gameSave == 1:
                            if save1 == True:
                                openF = "save1.txt"
                        elif gameSave == 2:
                            if save2 == True:
                                openF = "save2.txt"
                        elif gameSave == 3:
                            if save3 == True:
                                openF = "save3.txt"
                        if (gameSave == 1 and save1 == True) or (gameSave == 2 and save2 == True) or (gameSave == 3 and save3 == True):
                            p = 0
                            playerRoutes = [[],[],[],[],[]]
                            routes = []
                            d = False
                            with open(openF) as f:
                                for line in f:
                                    inp = line.split()
                                    if inp[0] == "Final":
                                        finalTurn = int(inp[1])
                                    if inp[0] == "Map":
                                        openSaveFile = inp[1]
                                    if inp[0] == "Names":
                                        for x in range(0,numPlayers):
                                            removeUnderscore = list(inp[x+1])
                                            for y in range(0,len(removeUnderscore)):
                                                if removeUnderscore[y] == '_':
                                                    removeUnderscore[y] = ' '
                                            removeUnderscore = "".join(removeUnderscore)
                                            name[x] = removeUnderscore
                                    if inp[0] == "Railroads":
                                        scanSection = 2
                                        continue
                                    if inp[0] == "NumPlayers":
                                        numPlayers = int(inp[1])
                                    if inp[0] == "Turnplayer":
                                        turnPlayer = int(inp[1])
                                    if inp[0] == "Trains":
                                        for x in range(0,numPlayers):
                                            numTrains[x] = int(inp[x+1])
                                    if inp[0] == "Points":
                                        for x in range(0,numPlayers):
                                            points[x] = int(inp[x+1])
                                        continue
                                    if inp[0] == "Routes":
                                        scanSection = 7
                                        continue
                                    if inp[0] == "Hands":
                                        scanSection = 8
                                        p = 0
                                        continue
                                    if inp[0] == "Draw":
                                        deck = []
                                        for y in range(1,10):
                                            for x in range(0,int(inp[y])):
                                                deck.append(colors[y-1])
                                        random.shuffle(deck)
                                        scanSection = 0
                                    if inp[0] == "Discard":
                                        discard = []
                                        for y in range(1,10):
                                            for x in range(0,int(inp[y])):
                                                discard.append(colors[y-1])
                                    if inp[0] == "Display":
                                        for x in range(0,5):
                                            display[x] = inp[x+1]
                                        sortedDisplay = sortDisplay(display)
                                    if scanSection == 1:
                                        totalGraph.add_node(int(inp[0]),name=inp[1],x=int(inp[2]),y=int(inp[3]))
                                        numCities += 1
                                    if scanSection == 2:
                                        if inp[0] == "NumPlayers":
                                            scanSection = 0
                                            continue
                                        if int(inp[3]) != -1:
                                            totalGraph[int(inp[0])][int(inp[1])][int(inp[2])]['owned'] = int(inp[3])
                                            if int(inp[3]) == 0:
                                                p1Bought.add_edge(int(inp[0]),int(inp[1]))
                                            if int(inp[3]) == 1:
                                                p2Bought.add_edge(int(inp[0]),int(inp[1]))
                                            if int(inp[3]) == 2:
                                                p3Bought.add_edge(int(inp[0]),int(inp[1]))
                                            if int(inp[3]) == 3:
                                                p4Bought.add_edge(int(inp[0]),int(inp[1]))
                                            if int(inp[3]) == 4:
                                                p5Bought.add_edge(int(inp[0]),int(inp[1]))
                                    if scanSection == 7:
                                        if inp[0] == "Next":
                                            p += 1
                                            continue
                                        if inp[0] == "Deck":
                                            d = True
                                            continue
                                        if d == False:
                                            playerRoutes[p].append((int(inp[0]),int(inp[1]),int(inp[2]),int(inp[3])))
                                        else:
                                            routes.append((int(inp[0]),int(inp[1]),int(inp[2]),int(inp[3])))
                                    if scanSection == 8:
                                        hand[p] = []
                                        for y in range(0,9):
                                            for x in range(0,int(inp[y])):
                                                hand[p].append(colors[y])
                                        p += 1
                                        sortedHand = sortHands(hand)
                            f.close()
                    if mouseWithin([(494,380),(564,410)])  and ((option == 1 and save1 == True) or (option == 2 and save2 == True) or (option == 3 and save3 == True)):
                            """Loading files"""
                            if option == 1:
                                os.remove('save1.txt')
                            if option == 2:
                                os.remove('save2.txt')
                            if option == 3:
                                os.remove('save3.txt')
                            if os.path.isfile('save1.txt'):
                                save1 = True
                            else:
                                save1 = False
                            if os.path.isfile('save2.txt'):
                                save2 = True
                            else:
                                save2 = False
                            if os.path.isfile('save3.txt'):
                                save3 = True
                            else:
                                save3 = False
                    if ((option == 1 and save1 == False) or (option == 2 and save2 == False) or (option == 3 and save3 == False)):
                            if  mouseWithin([(455,380),(525,410)]):
                                room = 1
                                gameSave = option
                                numPlayers = newNumPlayers
                                if inputNames == True:
                                    name[0] = input("Enter the name for the first (red) player: ")
                                    name[1] = input("Enter the name for the second (blue) player: ")
                                    if numPlayers > 2:
                                        name[2] = input("Enter the name for the third (orange) player: ")
                                    if numPlayers > 3:
                                        name[3] = input("Enter the name for the fourth (green) player: ")
                                    if numPlayers > 4:
                                        name[4] = input("Enter the name for the fifth (pink) player: ")
                            if mouseWithin([(455,265),(477,291)]) and newNumPlayers > 2:
                                newNumPlayers -= 1
                            if mouseWithin([(509,265),(531,291)]) and newNumPlayers < 5:
                                newNumPlayers += 1
                            if mouseWithin([(441,338),(541,368)]):
                                if inputNames == True:
                                    inputNames = False
                                else:
                                    inputNames = True
                        
                        
                if mouseWithin([(105,235),(335,285)]):
                    option = 1
                if mouseWithin([(105,305),(335,355)]):
                    option = 2
                if mouseWithin([(105,375),(335,425)]):
                    option = 3
                
                        
            """Main Game Room"""
            if room == 1:
                if mouseY < 50:
                    nextPlayer()
                if option == 0:
                    if option == 0 and mouseWithin([(gameWidth/2-101,gameHeight-36),(gameWidth/2-69,gameHeight-4)]):
                        option = 1 #Drawing cards
                        cardsTaken = 0
                        sortDisplay(display)
                    if option == 0 and len(routes) > 0 and mouseWithin([(gameWidth/2-67,gameHeight-36),(gameWidth/2-33,gameHeight-4)]):
                        action = True
                        option = 2 #Swap routes
                    if option == 0 and mouseWithin([(gameWidth/2-33,gameHeight-36),(gameWidth/2-1,gameHeight-4)]):
                        leftClicked = True
                        anyCol = []
                        option = 3 #Buying railroads
                    if mouseWithin([(gameWidth/2+1,gameHeight-36),(gameWidth/2+34,gameHeight-4)]):
                        option = 4 #Exit/save
                    
                if option == 1:
                    if mouseWithin([(gameWidth/2-42,gameHeight/2+113),(gameWidth/2+42,gameHeight/2+147)]) and cardsTaken == 0:
                        option = 0 #Cancel drawing cards
                    if mouseWithin([(gameWidth/2-104,gameHeight/2-82),(gameWidth/2-36,gameHeight/2)]):
                        hand[turnPlayer].append(drawCard())
                        cardsTaken += 1
                        sortedHand = sortHands(hand)
                    if mouseWithin([(gameWidth/2-34,gameHeight/2-82),(gameWidth/2+30,gameHeight/2)]):
                        if sortedDisplay[0] != 8 or cardsTaken == 0:
                            hand[turnPlayer].append(colors[sortedDisplay[0]])
                            display[0] = drawCard()
                            if sortedDisplay[0] != 8:
                                cardsTaken += 1
                            else:
                                cardsTaken = 2
                            sortedHand = sortHands(hand)
                            sortedDisplay = sortDisplay(display)
                    if mouseWithin([(gameWidth/2+36,gameHeight/2-82),(gameWidth/2+104,gameHeight/2)]):
                        if sortedDisplay[1] != 8 or cardsTaken == 0:
                            hand[turnPlayer].append(colors[sortedDisplay[1]])
                            display[1] = drawCard()
                            if sortedDisplay[1] != 8:
                                cardsTaken += 1
                            else:
                                cardsTaken = 2
                            sortedHand = sortHands(hand)
                            sortedDisplay = sortDisplay(display)
                    if mouseWithin([(gameWidth/2-104,gameHeight/2+6),(gameWidth/2-36,gameHeight/2+88)]):
                       if sortedDisplay[2] != 8 or cardsTaken == 0:
                            hand[turnPlayer].append(colors[sortedDisplay[2]])
                            display[2] = drawCard()
                            if sortedDisplay[2] != 8:
                                cardsTaken += 1
                            else:
                                cardsTaken = 2
                            sortedHand = sortHands(hand)
                            sortedDisplay = sortDisplay(display)
                    if mouseWithin([(gameWidth/2-34,gameHeight/2+6),(gameWidth/2+30,gameHeight/2+88)]):
                        if sortedDisplay[3] != 8 or cardsTaken == 0:
                            hand[turnPlayer].append(colors[sortedDisplay[3]])
                            display[3] = drawCard()
                            if sortedDisplay[3] != 8:
                                cardsTaken += 1
                            else:
                                cardsTaken = 2
                            sortedHand = sortHands(hand)
                            sortedDisplay = sortDisplay(display)
                    if mouseWithin([(gameWidth/2+36,gameHeight/2+6),(gameWidth/2+104,gameHeight/2+88)]):
                        if sortedDisplay[4] != 8 or cardsTaken == 0:
                            hand[turnPlayer].append(colors[sortedDisplay[4]])
                            display[4] = drawCard()
                            if sortedDisplay[4] != 8:
                                cardsTaken += 1
                            else:
                                cardsTaken = 2
                            sortedHand = sortHands(hand)
                            sortedDisplay = sortDisplay(display)
                
                if mouseWithin([(gameWidth/2+42,gameHeight-34),(gameWidth/2+64,gameHeight-8)]) and (option == 0 or option == 3 or option == 5):
                    if routeScroller[turnPlayer] >= 2:
                        routeScroller[turnPlayer] -= 2
                if mouseWithin([(gameWidth/2+324,gameHeight-34),(gameWidth/2+346,gameHeight-8)]) and (option == 0 or option == 3 or option == 5):
                    if len(playerRoutes[turnPlayer]) - routeScroller[turnPlayer] > 2:
                        routeScroller[turnPlayer] += 2
                
                if option == 2 :
                    if mouseWithin([(gameWidth/2+4,gameHeight/2),(gameWidth/2+88,gameHeight/2+34)]):
                        option = 0 #Route cancel
                    if mouseWithin([(gameWidth/2-88,gameHeight/2),(gameWidth/2+-4,gameHeight/2+34)]):
                        option = 5
                        takeRoute1 = False
                        takeRoute2 = False
                        takeRoute3 = False
                if option == 5:
                    if mouseWithin([(gameWidth/2+132,gameHeight-96),(gameWidth/2+206,gameHeight-62)]) and (takeRoute1 == True or takeRoute2 == True or takeRoute3 == True):
                        if takeRoute1 == True:
                            playerRoutes[turnPlayer].append(routes[len(routes)-1])
                        if takeRoute2 == True:
                            playerRoutes[turnPlayer].append(routes[len(routes)-2])
                        if takeRoute3 == True:
                            playerRoutes[turnPlayer].append(routes[len(routes)-3])
                        newRoutes = []
                        for x in range(0,len(routes)):
                            if takeRoute1 == True and x == len(routes)-1:
                                continue
                            if takeRoute2 == True and x == len(routes)-2:
                                continue
                            if takeRoute3 == True and x == len(routes)-3:
                                continue
                            newRoutes.append(routes[x])
                        routes = newRoutes
                        nextPlayer()
                    if mouseWithin([(gameWidth/2-128,gameHeight-70),(gameWidth/2+128,gameHeight-54)]):
                        if takeRoute1 == True:
                            takeRoute1 = False
                        else:
                            takeRoute1 = True
                    if mouseWithin([(gameWidth/2-128,gameHeight-86),(gameWidth/2+128,gameHeight-70)]):
                        if takeRoute2 == True:
                            takeRoute2 = False
                        else:
                            takeRoute2 = True
                    if mouseWithin([(gameWidth/2-128,gameHeight-104),(gameWidth/2+128,gameHeight-88)]):
                        if takeRoute3 == True:
                            takeRoute3 = False
                        else:
                            takeRoute3 = True
                if option == 3:
                    if mouseWithin([(gameWidth-86,gameHeight-88),(gameWidth-2,gameHeight-54)]):
                        option = 0 #Buy cancel
                        citySelect1 = -1
                        citySelect2 = -1
                        citiesChosen = 0
                    if citiesChosen == 0 and citySelect1 != -1:
                        citiesChosen = 1
                    if citiesChosen == 1 and citySelect2 != -1:
                        citiesChosen = 2
                    #Buying on lower button
                    if citiesChosen == 2:
                        anyRemove = 0
                        removed = totalGraph[citySelect1][citySelect2][1]['weight']
                        arrayBackup = []
                        wildCount = 0
                        if totalGraph[citySelect1][citySelect2][1]['color'] == "Any":
                            if mouseWithin([(gameWidth-76,gameHeight-124),(gameWidth-2,gameHeight-90)]) and len(anyCol) > 0:
                                anyRemove = anyCol[0]
                            elif mouseWithin([(gameWidth-76,gameHeight-160),(gameWidth-2,gameHeight-126)]) and len(anyCol) > 1:
                                anyRemove = anyCol[1]
                            elif mouseWithin([(gameWidth-76,gameHeight-196),(gameWidth-2,gameHeight-162)]) and len(anyCol) > 2:
                                anyRemove = anyCol[2]
                            elif mouseWithin([(gameWidth-76,gameHeight-232),(gameWidth-2,gameHeight-198)]) and len(anyCol) > 3:
                                anyRemove = anyCol[3]    
                            elif mouseWithin([(gameWidth-76,gameHeight-268),(gameWidth-2,gameHeight-234)]) and len(anyCol) > 4:
                                anyRemove = anyCol[4]    
                            elif mouseWithin([(gameWidth-76,gameHeight-304),(gameWidth-2,gameHeight-270)]) and len(anyCol) > 5:
                                anyRemove = anyCol[5]    
                            elif mouseWithin([(gameWidth-76,gameHeight-340),(gameWidth-2,gameHeight-306)]) and len(anyCol) > 6:
                                anyRemove = anyCol[6]    
                            elif mouseWithin([(gameWidth-76,gameHeight-376),(gameWidth-2,gameHeight-342)]) and len(anyCol) > 7:
                                anyRemove = anyCol[7]
                            else:
                                anyRemove = -1
                            if anyRemove != 0 and anyRemove != -1:
                                if activeButton1 == True and mouseWithin([(gameWidth-76,gameHeight-124),(gameWidth-2,gameHeight-90)]):
                                    removed = totalGraph[citySelect1][citySelect2][1]['weight']
                                    arrayBackup = []
                                    wildCount = 0
                                #Remove cards from hand
                                for a in range(0,len(hand[turnPlayer])):
                                    if removed > 0 and hand[turnPlayer][a] == anyRemove[0]:
                                        removed -= 1
                                        continue
                                    if hand[turnPlayer][a] != "Wild":
                                        arrayBackup.append(hand[turnPlayer][a])
                                for a in range(0,len(hand[turnPlayer])):
                                    if removed > 0 and hand[turnPlayer][a] == "Wild" and hand[turnPlayer][a].count(anyRemove[0]) == 0:
                                        removed -= 1
                                        wildCount += 1
                                        continue
                                    if hand[turnPlayer][a] == "Wild":
                                        arrayBackup.append(hand[turnPlayer][a])
                                hand[turnPlayer] = arrayBackup
                                
                                #Add removed cards to discard
                                for a in range(0,wildCount):
                                    discard.append("Wild")
                                for a in range(0,totalGraph[citySelect1][citySelect2][1]['weight']-wildCount):
                                    discard.append(anyCol[0])
                                if totalGraph[citySelect1][citySelect2][1]['owned'] == -1:
                                    k = 1
                                else:
                                    k= 2
                                #Changing the graphs
                                if turnPlayer == 0:
                                    p1Bought.add_edge(citySelect1,citySelect2,key=k)
                                else:
                                    p1Graph.remove_edge(citySelect1,citySelect2,key=k)
                                if turnPlayer == 1:
                                    p2Bought.add_edge(citySelect1,citySelect2,key=k)
                                else:
                                    p2Graph.remove_edge(citySelect1,citySelect2,key=k)
                                if numPlayers > 2:
                                    if turnPlayer == 2:
                                        p3Bought.add_edge(citySelect1,citySelect2,key=k)
                                    else:
                                        p3Graph.remove_edge(citySelect1,citySelect2,key=k)
                                if numPlayers > 3:
                                    if turnPlayer == 3:
                                        p4Bought.add_edge(citySelect1,citySelect2,key=k)
                                    else:
                                        p4Graph.remove_edge(citySelect1,citySelect2,key=k)
                                if numPlayers == 5:
                                    if turnPlayer == 4:
                                        p5Bought.add_edge(citySelect1,citySelect2,key=k)
                                    else:
                                        p5Graph.remove_edge(citySelect1,citySelect2,key=k)
                                totalGraph[citySelect1][citySelect2][k]['owned'] = turnPlayer
                                points[turnPlayer] += pointRewards[totalGraph[citySelect1][citySelect2][k]['weight']-1]
                                numTrains[turnPlayer] -= totalGraph[citySelect1][citySelect2][k]['weight']
                                sortedHand = sortHands(hand)
                                citySelect1 = -1
                                citySelect2 = -1
                                citiesChosen = 0
                                nextPlayer()
                        elif activeButton1 == True and mouseWithin([(gameWidth-76,gameHeight-124),(gameWidth-2,gameHeight-90)]):
                            for a in range(0,len(hand[turnPlayer])):
                                if removed > 0 and hand[turnPlayer][a] == totalGraph[citySelect1][citySelect2][1]['color']:
                                    removed -= 1
                                    continue
                                if hand[turnPlayer][a] != "Wild":
                                    arrayBackup.append(hand[turnPlayer][a])
                            for a in range(0,len(hand[turnPlayer])):
                                if removed > 0 and hand[turnPlayer][a] == "Wild" and hand[turnPlayer][a].count(totalGraph[citySelect1][citySelect2][1]['color']) == 0:
                                    removed -= 1
                                    wildCount += 1
                                    continue
                                if hand[turnPlayer][a] == "Wild":
                                    arrayBackup.append(hand[turnPlayer][a])
                            hand[turnPlayer] = arrayBackup
                            
                            #Add removed cards to discard
                            for a in range(0,wildCount):
                                discard.append("Wild")
                                for a in range(0,totalGraph[citySelect1][citySelect2][1]['weight']-wildCount):
                                    discard.append(totalGraph[citySelect1][citySelect2][1]['color'])
                            #Changing the graphs
                            if turnPlayer == 0:
                                p1Bought.add_edge(citySelect1,citySelect2,key=1)
                            else:
                                p1Graph.remove_edge(citySelect1,citySelect2,key=1)
                            if turnPlayer == 1:
                                p2Bought.add_edge(citySelect1,citySelect2,key=1)
                            else:
                                p2Graph.remove_edge(citySelect1,citySelect2,key=1)
                            if numPlayers > 2:
                                if turnPlayer == 2:
                                    p3Bought.add_edge(citySelect1,citySelect2,key=1)
                                else:
                                    p3Graph.remove_edge(citySelect1,citySelect2,key=1)
                            if numPlayers > 3:
                                if turnPlayer == 3:
                                    p4Bought.add_edge(citySelect1,citySelect2,key=1)
                                else:
                                    p4Graph.remove_edge(citySelect1,citySelect2,key=1)
                            if numPlayers == 5:
                                if turnPlayer == 4:
                                    p5Bought.add_edge(citySelect1,citySelect2,key=1)
                                else:
                                    p5Graph.remove_edge(citySelect1,citySelect2,key=1)
                            totalGraph[citySelect1][citySelect2][1]['owned'] = turnPlayer
                            points[turnPlayer] += pointRewards[totalGraph[citySelect1][citySelect2][1]['weight']-1]
                            numTrains[turnPlayer] -= totalGraph[citySelect1][citySelect2][1]['weight']
                            sortedHand = sortHands(hand)
                            citySelect1 = -1
                            citySelect2 = -1
                            citiesChosen = 0
                            nextPlayer()
                    #Buying on top button
                    if citiesChosen == 2 and len(anyCol) == 0 and activeButton2 == True and mouseWithin([(gameWidth-76,gameHeight-160),(gameWidth-2,gameHeight-126)]):
                        removed = totalGraph[citySelect1][citySelect2][2]['weight']
                        arrayBackup = []
                        wildCount = 0
                        #Remove cards from hand
                        for a in range(0,len(hand[turnPlayer])):
                            if removed > 0 and hand[turnPlayer][a] == totalGraph[citySelect1][citySelect2][2]['color']:
                                removed -= 1
                                continue
                            if hand[turnPlayer][a] != "Wild":
                                arrayBackup.append(hand[turnPlayer][a])
                        for a in range(0,len(hand[turnPlayer])):
                            if removed > 0 and hand[turnPlayer][a] == "Wild" and hand[turnPlayer][a].count(totalGraph[citySelect1][citySelect2][2]['color']) == 0:
                                removed -= 1
                                wildCount += 1
                                continue
                            if hand[turnPlayer][a] == "Wild":
                                arrayBackup.append(hand[turnPlayer][a])
                        hand[turnPlayer] = arrayBackup
                        #Add removed cards to discard
                        for a in range(0,wildCount):
                            discard.append("Wild")
                        for a in range(0,totalGraph[citySelect1][citySelect2][2]['weight']-wildCount):
                            discard.append(totalGraph[citySelect1][citySelect2][2]['color'])
                        #Changing the graphs
                        if turnPlayer == 0:
                            p1Bought.add_edge(citySelect1,citySelect2,key=2)
                        else:
                            p1Graph.remove_edge(citySelect1,citySelect2,key=2)
                        if turnPlayer == 1:
                            p2Bought.add_edge(citySelect1,citySelect2,key=2)
                        else:
                            p2Graph.remove_edge(citySelect1,citySelect2,key=2)
                        if numPlayers > 2:
                            if turnPlayer == 2:
                                p3Bought.add_edge(citySelect1,citySelect2,key=2)
                            else:
                                p3Graph.remove_edge(citySelect1,citySelect2,key=2)
                        if numPlayers > 3:
                            if turnPlayer == 3:
                                p4Bought.add_edge(citySelect1,citySelect2,key=2)
                            else:
                                p4Graph.remove_edge(citySelect1,citySelect2,key=2)
                        if numPlayers > 4:
                            if turnPlayer == 4:
                                p5Bought.add_edge(citySelect1,citySelect2,key=2)
                            else:
                                p5Graph.remove_edge(citySelect1,citySelect2,key=2)
                        totalGraph[citySelect1][citySelect2][2]['owned'] = turnPlayer
                        points[turnPlayer] += pointRewards[totalGraph[citySelect1][citySelect2][1]['weight']-1]
                        numTrains[turnPlayer] -= totalGraph[citySelect1][citySelect2][1]['weight']
                        sortedHand = sortHands(hand)
                        citySelect1 = -1
                        citySelect2 = -1
                        citiesChosen = 0
                        nextPlayer()
                    for x in range(0,len(playerRoutes[turnPlayer])):
                        if turnPlayer == 0 and nx.has_path(p1Bought,playerRoutes[turnPlayer][x][0],playerRoutes[turnPlayer][x][1]):
                            playerRoutes[turnPlayer][x] = list(playerRoutes[turnPlayer][x])
                            playerRoutes[turnPlayer][x][3] = 1
                            playerRoutes[turnPlayer][x] = tuple(playerRoutes[turnPlayer][x])
                        if turnPlayer == 1 and nx.has_path(p2Bought,playerRoutes[turnPlayer][x][0],playerRoutes[turnPlayer][x][1]):
                            playerRoutes[turnPlayer][x] = list(playerRoutes[turnPlayer][x])
                            playerRoutes[turnPlayer][x][3] = 1
                            playerRoutes[turnPlayer][x] = tuple(playerRoutes[turnPlayer][x])
                        if turnPlayer == 2 and nx.has_path(p3Bought,playerRoutes[turnPlayer][x][0],playerRoutes[turnPlayer][x][1]):
                            playerRoutes[turnPlayer][x] = list(playerRoutes[turnPlayer][x])
                            playerRoutes[turnPlayer][x][3] = 1
                            playerRoutes[turnPlayer][x] = tuple(playerRoutes[turnPlayer][x])
                        if turnPlayer == 3 and nx.has_path(p4Bought,playerRoutes[turnPlayer][x][0],playerRoutes[turnPlayer][x][1]):
                            playerRoutes[turnPlayer][x] = list(playerRoutes[turnPlayer][x])
                            playerRoutes[turnPlayer][x][3] = 1
                            playerRoutes[turnPlayer][x] = tuple(playerRoutes[turnPlayer][x])
                        if turnPlayer == 4 and nx.has_path(p5Bought,playerRoutes[turnPlayer][x][0],playerRoutes[turnPlayer][x][1]):
                            playerRoutes[turnPlayer][x] = list(playerRoutes[turnPlayer][x])
                            playerRoutes[turnPlayer][x][3] = 1
                            playerRoutes[turnPlayer][x] = tuple(playerRoutes[turnPlayer][x])
                
                    
                if option == 4 :
                    if mouseWithin([(gameWidth/2+4,gameHeight/2),(gameWidth/2+88,gameHeight/2+34)]):
                        option = 0 #Exit cancel
                if option == 4 :
                    if mouseWithin([(gameWidth/2-88,gameHeight/2),(gameWidth/2+-4,gameHeight/2+34)]):
                        saveGame()
                        gameEnd = True
                    
            if room == 2:
                
                if mouseWithin([(350,446),(430,476)]):
                    gameEnd = True
                    
            
            
      
    pygame.display.update()    
    clock.tick(30)
    
    

if finalTurn != -1:
    print("Thanks for playing!")

pygame.quit()