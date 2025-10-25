# Executes one round of Gerard Blocks the Way, which is an MCR-themed version of the game Frogger
# Fonts and images must be in the same folder as this program in order for the program to run properly

import turtle
import time

# sets up initial game screen by assigning properties to turtles and sending stationary turtles to their positions
def setupScreen():
    # registers all images
    imageStrings = ["emo", "face", "electric", "keyboard", "mic", "drum", "guitar", "bus", "karate", "singing", "car", "boxer", "sophie_forwards", "sophie_backwards", "sophie_left", "sophie_right", "dead", "rectangle"]
    for i in imageStrings:
        win.register_shape("{}.gif".format(i))
    
    # sets up properties for instruments and gerard way
    for i in range(0, 10):
        for j in (instruments+gerards)[i]:
            j.shape("{}.gif".format(imageStrings[i+2])) # assigns appropriate shape to turtle
            j.penup() # prevents turtle from drawing while moving
            j.speed("fastest") # ensures fast setup and movement
            
    # sets up emo faces for each slot, hides it so it can be shown when needed
    for i in emo:
        i.shape("emo.gif")
        i.penup()
        i.speed("fastest")
        i.goto(-240+120*emo.index(i),315)
        i.hideturtle()
    
    # sets up three faces to represent the three lives
    for i in lives:
        i.shape("face.gif")
        i.penup()
        i.speed("fastest")
        i.goto(150+50*lives.index(i),-335)
    
    # sets up properties for player
    player.shape("sophie_forwards.gif")
    player.penup()
    player.hideturtle()
    
    # sets up properties for dying emoji
    dead.shape("dead.gif")
    dead.penup()
    dead.speed("fastest")
    dead.hideturtle()
    
    # sets up properties for rectangle, used for game ending message
    rectangle.shape("rectangle.gif")
    rectangle.penup()
    rectangle.hideturtle()
    rectangle.goto(0, 25)
    
    # sets up score turtle
    scoreText.penup()
    scoreText.goto(-210,-340) 
    scoreText.hideturtle()
    scoreText.color('yellow')
    
    # sets up turtle for game over message
    gameDone.color("medium purple")
    gameDone.penup()
    gameDone.hideturtle()

# sends instruments, gerards, and player to their starting positions on the screen, and returns their starting coordinates for reference later on
def resetScreen():
    # empty lists to be filled with x-coordinates only, because y-coordinates do not change
    instrumentCoordsX = [[],[],[],[],[]]
    gerardCoordsX = [[],[],[],[],[]]
    
    for i in range(0, 5):
        # instruments
        for j in instruments[i]:
            if i == 3: # the drums appear four times so its position is different
                instrumentCoordsX[i].append(-225+150*instruments[i].index(j)) # 150 pixels between every two
            else: # all other indexes appear two times
                instrumentCoordsX[i].append(-150+300*instruments[i].index(j)) # 300 pixels between every two
            j.goto(instrumentCoordsX[i][instruments[i].index(j)], 265-50*i) # columns determined by index of instrument
        
        # gerards
        for j in gerards[i]:
            if i in [0, 3]: # the bus and car appear two times so its positions are different
                gerardCoordsX[i].append(-150+300*gerards[i].index(j)) # 300 pixels between every two
            else: # all other indexes appear three times
                gerardCoordsX[i].append(-200+200*gerards[i].index(j)) # 200 pixels between every two
            j.goto(gerardCoordsX[i][gerards[i].index(j)], -35-50*i) # column determined by index of instrument
    
    # sends player back to the beginning without showing its movement while resetting
    playerX, playerY =  0, -285
    player.hideturtle()
    player.goto(playerX, playerY)
    player.showturtle()
            
    return playerX, playerY, instrumentCoordsX, gerardCoordsX

# determines if the current round is over based on if the player has died or entered a slot
def checkCurrentRound(playerX, playerY, instrumentCoordsX, gerardCoordsX, slotsEntered):
    # the current round is assumed to be continuing, and if not, these booleans change as needed
    keepGoing = True
    alive = True
    onInstrument = False
    
    if playerY == 315: # player is in the same row as the slots
        keepGoing = False # this round cannot keep going
        if playerX >= -270 and playerX <= -210: # player is in first slot
            if 1 in slotsEntered: # slot was already entered
                alive = False
            else:
                slotsEntered.append(1) # slot is newly entered
                emo[0].showturtle()
                alive = True
        elif playerX >= -150 and playerX <= -90: # player is in second slot
            if 2 in slotsEntered: # slot was already entered
                alive = False
            else: # slot was not previously entered
                slotsEntered.append(2) # slot is newly entered
                emo[1].showturtle()
                alive = True
        elif playerX >= -30 and playerX <= 30: # player is in third slot
            if 3 in slotsEntered: # slot was already entered
                alive = False
            else: # slot was not previously entered
                slotsEntered.append(3) # slot is newly entered
                emo[2].showturtle()
                alive = True
        elif playerX >= 90 and playerX <= 150: # player is in fourth slot
            if 4 in slotsEntered: # slot was already entered
                alive = False
            else: # slot was not previously entered
                slotsEntered.append(4) # slot is newly entered
                emo[3].showturtle()
                alive = True
        elif playerX >= 210 and playerX <= 270: # player is in fifth slot
            if 5 in slotsEntered: # slot was already entered
                alive = False
            else: # slot was not previously entered
                slotsEntered.append(5)
                emo[4].showturtle()
                alive = True
        else: # player collided with the grass on the top row
            alive = False
    
    elif playerY >= -235 and playerY <= -35: # player is on the road
        ranges = [60, 25, 20, 50, 30] # half of the width of each gerard way
        row = int((-playerY - 35)/50) # row of gerard ways, top to bottom from 0 to 4
        for i in gerardCoordsX[row]: # check all the gerards in that row
            if playerX >= i-ranges[row]-15 and playerX <= i+ranges[row]+15: # player collides within range of gerard
                alive = False
                keepGoing = False
    
    elif playerY >= 65 and playerY <= 265: # player is in the river
        ranges = [75, 60, 60, 25, 60] # half of the width of each instrument
        row = int((-playerY + 265)/50) # row of instruments, top to bottom from 0 to 4
        alive = False # automatically assumes they fell in the river, changes later if necessary
        keepGoing = False
        for i in instrumentCoordsX[row]:
            if playerX >= i-ranges[row]-10 and playerX <= i+ranges[row]+10: # player is safe if they are on an instrument
                alive = True
                keepGoing = True
                onInstrument = True
    
    return keepGoing, alive, slotsEntered, onInstrument

# changes the score that is displayed on the screen to the new score
def updateScore(score):
    font1 = ('Press Start 2P', 6)
    scoreText.clear() # remove previous score
    scoreText.write(score, font = font1) # write new score

# removes the life that was lost, after the player dies
def removeLife(livesLeft):
    lives[livesLeft].hideturtle() # hides the corresponding turtle

# determines if the game is done (if the player has won or lost) based on the lives they have left and the number of slots entered
def checkGameDone(livesLeft, slotsEntered):
    done = False # assumes the game is not done
    if livesLeft == 0 or len(slotsEntered) == 5: # game is done if player lost all their lives or entered all slots
        done = True
    return done

# moves the instruments and gerard way by their respective increments, and moves the player if it is on an instrument
def updateCharacterPositions(instrumentCoordsX, gerardCoordsX, onInstrument):
    global playerX, playerY
    
    # each character moves at a different speed, which is determined by the increments by which their coordinates change
    instrumentIncrements = [3,4,5,4,4]
    gerardIncrements = [6,3,3.75,5,3]

    for i in range(0,5,2): # rows 1, 3, and 5
        for j in range(len(instrumentCoordsX[i])): # electric guitar, mic, and acoustic guitar move to the right
            if instrumentCoordsX[i][j] >= 360: # instrument must loop around when it goes off the screen
                instrumentCoordsX[i][j] = -360
                instruments[i][j].hideturtle()
            else: # instrument must move to the right by its respective increment
                instrumentCoordsX[i][j] += instrumentIncrements[i]
        
        for j in range(len(gerardCoordsX[i])): # bus, singing, and boxer move to the left
            if gerardCoordsX[i][j] <= -360: # gerard must loop around when it goes off the screen
                gerardCoordsX[i][j] = 360
                gerards[i][j].hideturtle()
            else: # gerard must move to the left by its respective increment
                gerardCoordsX[i][j] -= gerardIncrements[i]

    for i in range(1,5,2): # rows 2 and 4
        for j in range(len(instrumentCoordsX[i])): # keyboard and drum move to the left
            if instrumentCoordsX[i][j] <= -360: # instrument must loop around when it goes off the screen
                instrumentCoordsX[i][j] = 360
                instruments[i][j].hideturtle()
            else: # instrument must move to the left by its respective increment
                instrumentCoordsX[i][j] -= instrumentIncrements[i]
        
        for j in range(len(gerardCoordsX[i])): # karate and car move to the right
            if gerardCoordsX[i][j] >= 360: # gerard must loop around when it goes off the screen
                gerardCoordsX[i][j] = -360
                gerards[i][j].hideturtle()
            else: # # gerard must move to the right by its respective increment
                gerardCoordsX[i][j] += gerardIncrements[i]
    
    for i in range(0, 5): # each iteration is one of the five rows for the river and the road
        for j in range(len(instruments[i])):
            instruments[i][j].goto(instrumentCoordsX[i][j], 265-50*i) # moves each instrument to its new position
            instruments[i][j].showturtle() # in case turtle was hidden when it loops around
        for j in range(len(gerards[i])):
            gerards[i][j].goto(gerardCoordsX[i][j], -35-50*i) # moves each gerard to its new position
            gerards[i][j].showturtle() # in case turtle was hidden when it loops around
    
    if onInstrument == True: # player must move along with the instrument it is on
        row = int((-playerY + 265)/50) # figures out the row of the river the player is on (0 to 4)
        if row != 5: # except case where player went from row 5 onto the grass, and onInstrument was not updated yet
            playerX = playerX + instrumentIncrements[row] * (-1) ** row
    return instrumentCoordsX, gerardCoordsX

# displays the message if the player has won/lost
def endGame(slotsEntered):
    if len(slotsEntered) == 5: # player won the game because they entered all five slots
        message = "Congratulations, you won!\n\nThank you for playing.\n\nFinal score: {}".format(score)
    else: # player lost the game because they did not enter all five slots
        message = "You lost!\n\nThank you for playing.\n\nFinal score: {}".format(score)
    
    # sets up the rectangle, which is the background of the game ending message
    rectangle.left(90)
    rectangle.forward(5)
    rectangle.stamp() # to make sure it shows on top of all other characters
    
    # displays the right message
    font2 = ('Press Start 2P', 9)
    gameDone.write(message, align = "center", font = font2)

# makes player's coordinates global variables so they can be accessed in functions
global playerX, playerY

# player moves forwards if they haven't reached the boundary, and has the forwards shape
def forwards():
    global playerY
    if playerY <= 265: # player cannot move past the top boundary
        playerY += 50
        player.shape("sophie_forwards.gif")

# player moves backwards if they haven't reached the boundary, and has the backwards shape
def backwards():
    global playerY
    if playerY >= -235: # player cannot move past the lower boundary
        playerY -= 50
        player.shape("sophie_backwards.gif")

# player moves left if they haven't reached the boundary, and has the left shape
def left():
    global playerX
    if playerX >= -220: # player cannot move past the left boundary
        playerX -= 30
        player.shape("sophie_left.gif")

# player moves right if they haven't reached the boundary, and has the right shape
def right():
    global playerX
    if playerX <= 220: # player cannot move past the right boundary
        playerX += 30
        player.shape("sophie_right.gif")

# sets up window size, title, and background
win = turtle.Screen()
win.setup(600,820, starty=5)
win.title("Gerard Blocks the Way")
win.bgpic("background.gif")

# creates turtles
emo = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]
lives = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]

electric = [turtle.Turtle(), turtle.Turtle()]
keyboard = [turtle.Turtle(), turtle.Turtle()]
mic = [turtle.Turtle(), turtle.Turtle()]
drum = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]
guitar = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]

bus = [turtle.Turtle(), turtle.Turtle()]
karate = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]
singing = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]
car = [turtle.Turtle(), turtle.Turtle()]
boxer = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]

instruments = [electric, keyboard, mic, drum, guitar]
gerards = [bus, karate, singing, car, boxer]

player = turtle.Turtle()
dead = turtle.Turtle()
rectangle = turtle.Turtle()

scoreText = turtle.Turtle()
gameDone = turtle.Turtle()

# initial values
livesLeft = 3
slotsEntered = []
score = 0
onInstrument = False

# function calls begin
setupScreen()
updateScore(score)

win.tracer(5) # to ensure smooth graphics throughout the entire game

# must call movement functions when player presses up, down, left, or right keys
turtle.listen()
turtle.onkey(forwards, "Up")
turtle.onkey(backwards, "Down")
turtle.onkey(left, "Left")
turtle.onkey(right, "Right")

done = False
while done == False: # runs repeatedly until game is over
    playerX, playerY, instrumentCoordsX, gerardCoordsX = resetScreen()
    keepGoing = True
    alive = True
    farthest = -285 # farthest row that the player has reached
    
    while keepGoing == True: # runs repeatedly until round is over
        player.goto(playerX, playerY) # update player's position
        
        instrumentCoordsX,gerardCoordsX = updateCharacterPositions(instrumentCoordsX, gerardCoordsX, onInstrument) # characters must keep moving
        keepGoing, alive, slotsEntered, onInstrument = checkCurrentRound(playerX, playerY, instrumentCoordsX, gerardCoordsX, slotsEntered) # check if current round should continue
        
        # updates score, increasing by 10 for every new row reached within the round
        if playerY > farthest:
            score += 10
            updateScore(score)
            farthest = playerY
        
        # player dies if they go off the screen on the left/right, which can happen if they are on an instrument
        if playerX <= -300 or playerX >= 300:
            alive = False
            keepGoing = False
            onInstrument = False
        
    player.goto(playerX, playerY) # in case a command is pressed and the previous loop ends before it gets a chance to update the player's position
    
    if alive == False: # previous loop ended because player died
        if playerX <= -300: # player died going off the screen, so dying emoji must appear on the screen
            dead.goto(-250, playerY)
        elif playerX >= 300: # player died going off the screen, so dying emoji must appear on the screen
            dead.goto(250, playerY)
        else: # player died somewhere on the screen
            dead.goto(playerX, playerY)
        
        # show dying emoji, let it stay there for 0.5 seconds
        dead.showturtle() # repeat multiple times to ensure the screen updates showing the emoji
        dead.showturtle()
        dead.showturtle()
        dead.showturtle()
        dead.showturtle()
        time.sleep(0.5)
        dead.hideturtle()
        
        # remove a life
        livesLeft -= 1
        removeLife(livesLeft)
    
    else: # previous loop ended because player entered a slot
        score += 50 # player's score increases by another 50 if they successfully enter a slot
        updateScore(score)
    done = checkGameDone(livesLeft, slotsEntered) # check if player has won/lost

if len(slotsEntered) == 5: # score increases by 1000 if player wins
    score += 1000
    updateScore(score)

endGame(slotsEntered) # must retrieve game ending message

win.exitonclick() # prevent window from automatically closing