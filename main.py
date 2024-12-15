"""
Made by net-ari

A game named 'Warehouse Escape' where the
player must get to an exit door every level as it
rises.

Made using the pygame-ce game library
Site: https://pyga.me
"""

# IMPORTS 
import pygame
import random

# PYGAME SETUP
pygame.init()
screen       = pygame.display.set_mode((1088,544),pygame.SCALED)
pygame.display.set_caption("Warehouse Escape")
clock        = pygame.time.Clock()
running      = True

# GAME CONSTANTS
# XY SCALE
IMGSCALE    :int      = 32 
# DELAYS ON PLAYER, DROPPER MOVEMENT
# AND GRAVITY
PLAYERDELAY :float    = 0.00 
DROPPERDELAY:float    = 0.00 
GRAVDELAY   :float    = 0.00
# WIDTH AND LENGTH OF WINDOW
X           :int      = screen.get_width()
Y           :int      = screen.get_height()
# GAME VARIABLES
levelNumber:int  = 1 # INITIALISE LEVEL NUMBER
turnNumber :int  = 0 # INITIALISE TURN NUMBER

# LOAD IMAGES
# USED ASSERT STATEMENT TO PREVENT BAD IMAGE SIZES
# FROM BEING USED
try:
    background:pygame.Surface  = pygame.image.load("assets/background.png")
    assert background.get_width() == IMGSCALE and background.get_height() == IMGSCALE
    background = background.convert()

    floor:pygame.Surface       = pygame.image.load("assets/floor.png")
    assert floor.get_width() == IMGSCALE and floor.get_height() == IMGSCALE
    floor = floor.convert()

    wall:pygame.Surface        = pygame.image.load("assets/wall.png")
    assert wall.get_width() == IMGSCALE and wall.get_height() == IMGSCALE
    wall = wall.convert()

    ceiling:pygame.Surface     = pygame.image.load("assets/ceiling.png")
    assert ceiling.get_width() == IMGSCALE and ceiling.get_height() == IMGSCALE
    ceiling = ceiling.convert()

    box:pygame.Surface = pygame.image.load("assets/box.png")
    assert box.get_width() == IMGSCALE and box.get_height() == IMGSCALE
    box = box.convert()

    itembox:pygame.Surface     = pygame.image.load("assets/itembox.png")
    assert itembox.get_width() == IMGSCALE and itembox.get_height() == IMGSCALE
    itembox = itembox.convert()

    door:pygame.Surface        = pygame.image.load("assets/door.png")
    assert door.get_width() == IMGSCALE and door.get_height() == IMGSCALE
    door = door.convert()

    entryPortal:pygame.Surface = pygame.image.load("assets/entryPortal.png")
    assert entryPortal.get_width() == IMGSCALE and entryPortal.get_height() == IMGSCALE
    
    exitPortal:pygame.Surface  = pygame.image.load("assets/exitPortal.png")
    assert exitPortal.get_width() == IMGSCALE and exitPortal.get_height() == IMGSCALE

    item:pygame.Surface = pygame.image.load("assets/item.png")
    assert item.get_width() == IMGSCALE and item.get_height() == IMGSCALE

    p:pygame.Surface = pygame.image.load("assets/player.png")
    assert p.get_width() == IMGSCALE and p.get_height() == IMGSCALE

    d:pygame.Surface = pygame.image.load("assets/dropper.png")
    assert d.get_width() == IMGSCALE and d.get_height() == IMGSCALE

except AssertionError:
    print("Error loading images...quitting")
    exit(0)

# PLAYER
class Player:
    """
    Class to store data about the player as well as
    handle the movement of the player on the grid.

    Attributes:
        cooldown (float): Initialises the cooldown for player
        movement.

        gravCooldown (float): Initialises the cooldown for player
        gravity.
        
        points (int): The current amount of points 
        the player has collected.

        maxEnergy (int): The maximum energy the player can have.

        currentEnergy (int): The current energy of the player.

        entryPortalExists (bool): Whether or not the player has
        created an entry portal.

        exitPortalExists (bool): Whether or not the player has
        created an exit portal.

        x (int): The horizontal position of the player. Set to 1.

        y (int): The vertical position of the player. Set to one tile
        above the bottom of the window.

        playerImage (pygame.Surface): Stores the Surface with the player
        image loaded.
    """

    def __init__(self):
        """The constructor method for class Player."""

        self.cooldown          = 0.00
        self.gravCooldown      = 0.00
        self.points            = 0
        self.maxEnergy         = 100
        self.currentEnergy     = self.maxEnergy
        self.entryPortalExists = False
        self.exitPortalExists  = False
        self.x                 = 1
        self.y                 = (Y-(2*IMGSCALE))//IMGSCALE
        self.playerImage       = p

    def decCooldown(self,n:float) -> None:
        """
        A method that decrements cooldown by a
        float value 'n'.

        Parameters:
            n (float): A float value used to decrement
            gravCooldown.
        """

        self.cooldown -= n

    def decGravCooldown(self,n:float) -> None:
        """
        A method that decrements gravCooldown by a
        float value 'n'.

        Parameters:
            n (float): A float value used to decrement
            gravCooldown.
        """

        self.gravCooldown -= n

    def incPoints(self) -> None:
        """
        A method used to increment the number 
        of points the player has by one.
        """

        self.points += 1

    def resetPoints(self) -> None:
        """"A method used to reset points."""

        self.points = 0

    def getPoints(self) -> int:
        """
        A method used to retrieve the value
        of points.

        Returns:
            points (int): The number of points
            the player has.
        """

        return self.points

    def changeEnergy(self,n:int) -> None:
        """
        A method used to modify the currentEnergy
        of the player.

        Parameters:
            n (int): Integer value to modify the player's
            current energy by. Can be positive to increase 
            or negative to decrease.
        """
        if n <= self.maxEnergy and n >= 0:
            self.currentEnergy += n
        else:
            self.currentEnergy = 0

    def getEnergy(self) -> int:
        """
        A method used to retrieve the currentEnergy.

        Returns:
            currentEnergy (int): The current energy of the
            player.
        """

        return self.currentEnergy

    def getMaxEnergy(self) -> int:
        """
        A method used to retrieve the maxEnergy
        of the player.

        Returns:
            maxEnergy (int): The max energy the player
            can have.
        """

        return self.maxEnergy

    def drawEnergyBar(self) -> None:
        """
        A method used to draw a bar representing
        the current energy of the player.
        """

        remainingEnergy = self.currentEnergy/self.maxEnergy

        pygame.draw.rect(screen,"blue",(self.x*IMGSCALE,
                                        self.y*IMGSCALE+29,
                                        IMGSCALE,
                                        3))
        pygame.draw.rect(screen,"cyan",(self.x*IMGSCALE,
                                        self.y*IMGSCALE+29,
                                        IMGSCALE*remainingEnergy,
                                        3))

    def makePortal(self,whichDirection:bool) -> None:
        """
        A method that allows the player to make a pair
        of portals. An entry portal at the player's
        current position, and an exit portal 10 tiles
        away, in either direction. The direction is
        based off of the boolean parameter, True being
        right, False being left.

        Note that there is some strange behaviour regarding
        portals and platforms, namely that multiple exit
        portals will appear in the event multiple floor tiles
        are found in the vertical slice of the grid the 
        method iterates over. I left this in since it adds some
        interesting ways to play to the game.

        Parameters:
            whichDirection (bool): The direction the exit
            portal will appear in. True is right, False is left.
        """

        if not self.entryPortalExists:
            room[self.x][self.y] = entryPortal
            self.entryPortalExists = True

            if not self.exitPortalExists:
                if whichDirection and self.x+10 < 33: 
                    for y in range(Y//IMGSCALE-1,0,-1):
                        if room[self.x+10][y] == floor and room[self.x+10][y-1] == background:
                            room[self.x+10][y-1] = exitPortal

                elif not whichDirection and self.x-10 > 0:
                    for y in range(Y//IMGSCALE-1,0,-1):
                        if room[self.x-10][y] == floor and room[self.x-10][y-1] == background:
                            room[self.x-10][y-1] = exitPortal

                self.exitPortalExists = True

    def findPortal(self,whichPortal:bool):
        """
        A method used to find a corresponding portal.
        The boolean parameter is used to distinguish
        which portal is being searched for, and when
        a portal is found, the player's position is set
        to that portal.

        Parameters:
            whichPortal (bool): A boolean variable signifying
            whether the portal being searched for is an exitPortal
            (True), or an entryPortal (False).
        """

        if whichPortal:
            for x in range(0,X//IMGSCALE):
                for y in range(Y//IMGSCALE-1,0,-1):
                    if room[x][y] == exitPortal:
                        player.setPosition(x,y)
        else:
            for x in range(0,X//IMGSCALE):
                for y in range(Y//IMGSCALE-1,0,-1):
                    if room[x][y] == entryPortal:
                        player.setPosition(x,y)

    def clearPortals(self):
        """
        A method used to clear the portals currently
        on the screen. It scans the grid from the top
        down for instances of entryPortal or exitPortal
        and changes them to background tiles.
        """
        self.entryPortalExists = False
        self.exitPortalExists  = False

        for x in range(X//IMGSCALE):
            for y in range(Y//IMGSCALE):
                if (room[x][y] == entryPortal 
                        or room[x][y] == exitPortal):
                    room[x][y] = background

        

    def setPosition(self,x: int,y: int) -> None:
        """
        A method that sets the position of the
        player to the integer numbers passed.

        Parameters:
            x (int): Horizontal position of player.

            y (int): Vertical Position of player.

        """

        self.x = x
        self.y = y

    def getX(self) -> int:
        """
        A method used to retrieve the attribute x.

        Returns:
            x (int): The horizontal position of
            the player.
        """

        return self.x

    def getY(self) -> int:
        """
        A method used to retrieve the attribute y.

        Returns:
            y (int): The vertical position of
            the player.
        """
        return self.y
    
    
    def moveLeft(self) -> None:
        """
        A method used to move the player left by one tile and
        move one tile up on to boxes.
        """

        if self.cooldown <= 0:
            if (room[self.x-1][self.y] == background):
                self.setPosition(self.x-1,self.y)
                self.cooldown = PLAYERDELAY

            if (room[self.x-1][self.y] == entryPortal):
                self.findPortal(True)

            if (room[self.x-1][self.y] == exitPortal):
                self.findPortal(False)

            elif ((room[self.x-1][self.y] == box or room[self.x-1][self.y] == itembox) 
                    and room[self.x-1][self.y-1] == background):
                player.setPosition(self.x-1,self.y-1)

            elif (room[self.x-1][self.y] == item):
                self.incPoints()
                room[self.x-1][self.y] = background
                player.setPosition(self.x-1,self.y)

            elif (room[self.x-1][self.y-1] == item):
                self.incPoints()
                room[self.x-1][self.y-1] = background
                player.setPosition(self.x-1,self.y-1)

            elif (room[self.x-1][self.y-1] == entryPortal):
                self.findPortal(True)

            elif (room[self.x-1][self.y-1] == exitPortal):
                self.findPortal(False)

    
    # METHOD TO MOVE THE PLAYER RIGHT
    def moveRight(self) -> None:
        """
        A method to move the player right by one tile and
        move one tile up on to boxes.
        """

        if self.cooldown <= 0 and self.x < 34:
            if (room[self.x+1][self.y] == background 
                    or room[self.x+1][self.y] == door):
                self.setPosition(self.x+1,self.y)
                self.cooldown = PLAYERDELAY

            elif (room[self.x+1][self.y] == entryPortal):
                self.findPortal(True)

            elif (room[self.x+1][self.y] == exitPortal):
                self.findPortal(False)

            elif ((room[self.x+1][self.y] == box or room[self.x+1][self.y] == itembox) 
                  and room[self.x+1][self.y-1] == background):
                player.setPosition(self.x+1,self.y-1)

            elif (room[self.x+1][self.y] == item):
                self.incPoints()
                room[self.x+1][self.y] = background
                player.setPosition(self.x+1,self.y)

            elif (room[self.x+1][self.y-1] == entryPortal):
                self.findPortal(True)

            elif (room[self.x+1][self.y-1] == exitPortal):
                self.findPortal(False)


    def applyPlayerGravity(self) -> None:
        """
        A method used to add gravity to the player's
        movements.
        """
        
        if self.gravCooldown <= 0:
            if (room[self.x][self.y+1] == background 
                or room[self.x][self.y+1] == item):
                self.setPosition(self.x,self.y+1)
                self.gravCooldown = PLAYERDELAY

            elif (room[self.x][self.y+1] == entryPortal):
                self.findPortal(True)

            elif (room[self.x][self.y+1] == exitPortal):
                self.findPortal(False)

    def breakBox(self) -> None:
        """
        A method that allows the player to break adjacent
        boxes, checking on the left first.
        """
        if self.currentEnergy > 50:
            if room[self.x-1][self.y] == box:
                room[self.x-1][self.y] = background
            elif room[self.x-1][self.y] == itembox:
                room[self.x-1][self.y] = item

            if room[self.x+1][self.y] == box:
                room[self.x+1][self.y] = background
            elif room[self.x+1][self.y] == itembox:
                room[self.x+1][self.y] = item

# DROPPER
class Dropper:
    """
    A class used to store data about the dropper,
    as well as handle the movement of the dropper
    on the grid and its ability to drop boxes.

    Attributes:
        cooldown (float): Initialises the cooldown for
        the dropper's movement.
        
        gravCooldown (float): Initialises the cooldown for
        the gravity of boxes dropped by the dropper.

        x (int): The horizontal position of the dropper.

        y (int): The vertical position of the dropper.

        dropperImage (pygame.Surface): Stores the Surface
        with the dropper image loaded.
    """

    def __init__(self):
        """The constructor method for class Dropper."""

        self.cooldown     = 0.00
        self.gravCooldown = 0.00
        self.x            = 1
        self.y            = 1
        self.dropperImage = d
    
    def decCooldown(self,n:float) -> None:
        """
        A method that decrements cooldown by
        a float value 'n'.

        Parameters:
            n (float): A float value used to decrement cooldown.
        """

        self.cooldown -= n
    
    def decGravCooldown(self,n:float) -> None:
        """
        A method that decrements gravCooldown by
        a float value 'n'.

        Parameters:
            n (float): A float value used to decrement cooldown.
        """

        self.gravCooldown -= n

    def setPosition(self,x,y) -> None:
        """
        A method that sets the position of
        the dropper to the integer values passed.

        Parameters:
            x (int): Horizontal position of the dropper.

            y (int): Vertical position of the dropper.
        """

        self.x = x
        self.y = y
    
    def getX(self) -> int:
        """
        A method used to retrieve the attribute x.

        Returns:
            x (int): Horizontal position of the dropper.
        """

        return self.x

    def getY(self) -> int:
        """
        A method used to retrieve the attribute y.

        Returns:
            y (int): Vertical position of the dropper.
        """

        return self.y

    def moveDropper(self) -> None:
        """
        A method used to move the dropper.
        The dropper moves one tile towards the player.
        """

        if self.cooldown <= 0:
            if (player.getX() < self.getX() 
                    and room[self.x-1][self.y] == background):
                self.x -= 1
            elif (player.getX() > self.getX() 
                and room[self.x+1][self.y] == background):
                self.x += 1

            self.cooldown = DROPPERDELAY

    def activateDropper(self) -> None:
        """
        A method that allows the dropper to
        drop boxes. These boxes spawn one tile
        below the dropper.
        """

        if self.x == player.getX():
            room[self.x][self.y+1] = box
            
    
    def applyBoxGravity(self) -> None:
        """
        A method that handles gravity for the boxes
        dropped by the dropper.
        If a box is found, it is moved down by one tile.
        If the player is right below a box, they are crushed
        and the program exits.
        """

        if self.gravCooldown <= 0:
            for x in range(0,X//IMGSCALE):
                for y in range(Y//IMGSCALE-1,0,-1):
                    if ((room[x][y] == box or room[x][y] == itembox)
                            and (x == player.getX() and y == player.getY()-1)):
                        exit(0)
                    
                    # STOP BOXES FROM LANDING ON ITEMS TO PREVENT SOFTLOCK
                    elif (room[x][y] == box 
                          and (room[x][y+1] == item)):
                        room[x][y] = background
 
                    elif (room[x][y] == box 
                            and room[x][y+1] == background):
                        room[x][y] = background
                        room[x][y+1] = box

                    elif (room[x][y] == itembox 
                          and room[x][y+1] == background):
                        room[x][y] = background
                        room[x][y+1] = itembox

def generateRoom(room:list,levelNumber:int) -> list:
    """
    Function used to generate the level
    for the game.

    Parameters:
        room (list): A 2D list representing the level.

        levelNumber (int): An integer that represents the
        number level the player is on.

    Returns:
        room (list): The filled version of the 2D list
        representing the level.
    """

    for x in range(X//IMGSCALE):
        for y in range(0,Y//IMGSCALE):
            if x == 33 and y == 16-levelNumber:
                room[x][16-levelNumber] = door
            elif x == 0:
                room[x][y] = wall
            elif x == 33:
                room[x][y] = wall
            elif y == 0:
                room[x][y] = ceiling
            elif y == 16:
                room[x][y] = floor
            else:
                room[x][y] = background

    room[5][15] = itembox

    if levelNumber > 1:
        for i in range(0,levelNumber+1):
            random.seed(i)
            randX = random.randint(3,31)
            randY = random.randint(3,14)
            for j in range(1,4):
                if randX+j < 30 and room[randX][randY+1] == background:
                    room[randX+j][randY] = floor
            if room[randX+1][randY] == floor:
                room[randX+1][randY-1] = itembox
                
    return room

# HOLDS TILEMAP
room:list = [[None for _ in range(Y//IMGSCALE)] 
    for _ in range(X//IMGSCALE+1)]

# INSTANTIATE PLAYER AND DROPPER
player  = Player()
dropper = Dropper()

room = generateRoom(room,levelNumber)

while running:
    # POLL FOR EVENTS
    for event in pygame.event.get():
        # QUIT PROGRAM
        if event.type == pygame.QUIT:
            running   = False

        # CHECK FOR KEYS BEING PRESSED 
        if event.type == pygame.KEYDOWN:
            # INCREMENT TURN NUMBER
            turnNumber += 1
            if player.getEnergy() < player.getMaxEnergy():
                player.changeEnergy(10)

            # HANDLE INPUT FOR KEY 'D'
            if event.key == pygame.K_d:
                player.moveRight()

            # HANDLE INPUT FOR KEY 'A'
            elif event.key == pygame.K_a:
                player.moveLeft()

            # HANDLE INPUT FOR KEY 'Q' 
            elif event.key == pygame.K_q:
                player.breakBox()
                player.changeEnergy(-50)

            elif event.key == pygame.K_RIGHT:
                player.makePortal(True)

            elif event.key == pygame.K_LEFT:
                player.makePortal(False)

            elif event.key == pygame.K_r:
                player.clearPortals()

            # HANDLE GRAVITY FOR PLAYER AND BOXES
            player.applyPlayerGravity()
            dropper.applyBoxGravity()
            
            # DROPPER MOVES EVERY TWO TURNS
            if turnNumber % 2 == 0:
                dropper.moveDropper()

            # DROPPER ACTIVATES EVERY SEVEN TURNS
            if turnNumber % 7 == 0:
                dropper.activateDropper()

    # DRAW LEVEL
    for x in range(0,X//IMGSCALE):
        for y in range(0,Y//IMGSCALE):
            if room[x][y] != None:
                screen.blit(room[x][y],
                            (x*IMGSCALE,
                             y*IMGSCALE))
    
    # INCREASE LEVEL NUMBER WHEN PLAYER GETS TO NEXT LEVEL
    if (room[player.getX()][player.getY()] == door 
        and player.getPoints() >= levelNumber):
        # INCREMENT LEVEL NUMBER BY 1
        levelNumber += 1

        # RESET POINTS
        player.resetPoints()

        # GENERATE THE ROOM AGAIN
        generateRoom(room,levelNumber)
        
        # SET THE PLAYER TO THE START AGAIN
        player.setPosition(1,(Y - (2*IMGSCALE))//IMGSCALE)

    if levelNumber == 16:
        exit(0)

    # CALCULATE DECREMENT FOR COOLDOWNS
    delta:float = clock.tick()/1000

    # DRAW PLAYER
    screen.blit(player.playerImage,
                (player.getX()*IMGSCALE,
                 player.getY()*IMGSCALE))

    # DRAW PLAYER ENERGY BAR
    player.drawEnergyBar()
 
    # DRAW DROPPER
    screen.blit(dropper.dropperImage,
                (dropper.getX()*IMGSCALE,
                 dropper.getY()*IMGSCALE))

    # DECREASE MOVEMENT COOLDOWN
    player.decCooldown(delta)
    dropper.decCooldown(delta)

    # DECREASE GRAVITY COOLDOWN
    player.decGravCooldown(delta)
    dropper.decGravCooldown(delta)
    
    # UPDATES DISPLAY
    pygame.display.flip()
    
    # LIMITS FPS
    clock.tick(60)

pygame.quit()
