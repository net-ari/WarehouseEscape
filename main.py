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

# PYGAME SETUP
pygame.init()
screen       = pygame.display.set_mode((1088,544),pygame.SCALED)
pygame.display.set_caption("Warehouse Escape")
clock        = pygame.time.Clock()
running      = True

# GAME CONSTANTS
IMGSCALE     = 32   # x y size of images used as tiles
PLAYERDELAY  = 0.00 # introduces a delay to the movement
                    # of the player to allow tile by tile
                    # movement. set to 0 for no delay
DROPPERDELAY = 0.05 # introduces a delay to the movement
                    # of the dropper to allow tile by tile
                    # movement. set to 0 for no delay.
GRAVDELAY    = 0.05 # the delay of gravity in the game
X            = screen.get_width()
Y            = screen.get_height()

# GAME VARIABLES
levelNumber  = 0
turnNumber   = 0

# LOAD IMAGES
try:
    background:pygame.Surface = pygame.image.load("assets/background.png")
    assert background.get_width() == IMGSCALE and background.get_height() == IMGSCALE
    background = background.convert()

    floor:pygame.Surface = pygame.image.load("assets/floor.png")
    assert floor.get_width() == IMGSCALE and floor.get_height() == IMGSCALE
    floor = floor.convert()

    wall:pygame.Surface = pygame.image.load("assets/wall.png")
    assert wall.get_width() == IMGSCALE and wall.get_height() == IMGSCALE
    wall = wall.convert()

    ceiling:pygame.Surface = pygame.image.load("assets/ceiling.png")
    assert ceiling.get_width() == IMGSCALE and ceiling.get_height() == IMGSCALE
    ceiling = ceiling.convert()

    box:pygame.Surface = pygame.image.load("assets/box.png")
    assert box.get_width() == IMGSCALE and box.get_height() == IMGSCALE
    box = box.convert()

    itembox:pygame.Surface = pygame.image.load("assets/itembox.png")
    assert itembox.get_width() == IMGSCALE and itembox.get_height() == IMGSCALE
    itembox = itembox.convert()

    door:pygame.Surface    = pygame.image.load("assets/door.png")
    assert door.get_width() == IMGSCALE and door.get_height() == IMGSCALE
    door = door.convert()

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

        x (int): The horizontal position of the player. Set to 1.

        y (int): The vertical position of the player. Set to one tile
        above the bottom of the window.

        playerImage (pygame.Surface): Stores the Surface with the player
        image loaded.
    """

    def __init__(self):
        """The constructor method for class Player."""

        self.cooldown     = 0.00
        self.gravCooldown = 0.00
        self.x            = 1
        self.y            = (Y-(2*IMGSCALE))//IMGSCALE
        self.playerImage  = p

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
            if (currentTiles[self.x-1][self.y] == background):
                self.setPosition(self.x-1,self.y)
                self.cooldown = PLAYERDELAY

            if (currentTiles[self.x-1][self.y] == box 
                    and currentTiles[self.x-1][self.y-1] == background):
                player.setPosition(self.x-1,self.y-1)
    
    # METHOD TO MOVE THE PLAYER RIGHT
    def moveRight(self) -> None:
        """
        A method to move the player right by one tile and
        move one tile up on to boxes.
        """

        if self.cooldown <= 0 and self.x < 34:
            if (currentTiles[self.x+1][self.y] == background 
                    or currentTiles[self.x+1][self.y] == door):
                self.setPosition(self.x+1,self.y)
                self.cooldown = PLAYERDELAY

            if (currentTiles[self.x+1][self.y] == box 
                    and currentTiles[self.x+1][self.y-1] == background):
                player.setPosition(self.x+1,self.y-1)

    def applyPlayerGravity(self) -> None:
        """
        A method used to add gravity to the player's
        movements.
        """
        
        if self.gravCooldown <= 0:
            if currentTiles[self.x][self.y+1] == background:
                self.setPosition(self.x,self.y+1)
                self.gravCooldown = PLAYERDELAY

    def breakBox(self) -> None:
        """
        A method that allows the player to break adjacent
        boxes, checking on the left first.
        """

        if currentTiles[self.x-1][self.y] == box:
            currentTiles[self.x-1][self.y] = background
        elif currentTiles[self.x+1][self.y] == box:
            currentTiles[self.x+1][self.y] = background

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
            if player.getX() < self.getX():
                self.x -= 1
            elif player.getX() > self.getX():
                self.x += 1

            self.cooldown = DROPPERDELAY

    def activateDropper(self) -> None:
        """
        A method that allows the dropper to
        drop boxes. These boxes spawn one tile
        below the dropper.
        """

        if self.cooldown <= 0:
            if self.x == player.getX():
                currentTiles[self.x][self.y+1] = box
    
    def applyBoxGravity(self) -> None:
        """
        A method that handles gravity for the boxes
        dropped by the dropper.
        If a box is found, it is moved down by one tile.
        """

        if self.gravCooldown <= 0:
            for x in range(0,X//IMGSCALE):
                for y in range(Y//IMGSCALE-1,0,-1):
                    if (currentTiles[x][y] == box 
                            and currentTiles[x][y+1] == background):
                        currentTiles[x][y] = background
                        currentTiles[x][y+1] = box

# HOLDS TILEMAP
currentTiles:list = [[None for _ in range(Y//IMGSCALE)] 
    for _ in range(X//IMGSCALE+1)]

# INSTANTIATE PLAYER AND DROPPER
player  = Player()
dropper = Dropper()

# GENERATE TILEMAP FOR LEVEL
for x in range(0,X//IMGSCALE):
    for y in range(0,Y//IMGSCALE):
        if x == 33 and y == 15:
            currentTiles[x][y] = door
        elif x == 0:
            currentTiles[x][y] = wall
        elif x == 33:
            currentTiles[x][y] = wall
        elif y == 0:
            currentTiles[x][y] = ceiling
        elif y == 16:
            currentTiles[x][y] = floor
        else:
            currentTiles[x][y] = background

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

            # HANDLE INPUT FOR KEY 'D'
            if event.key == pygame.K_d:
                player.moveRight()

            # HANDLE INPUT FOR KEY 'A'
            if event.key == pygame.K_a:
                player.moveLeft()

            # HANDLE INPUT FOR KEY 'Q' 
            if event.key == pygame.K_q:
                player.breakBox()

            # HANDLE GRAVITY FOR PLAYER AND BOXES
            player.applyPlayerGravity()
            dropper.applyBoxGravity()
            
            # DROPPER MOVES EVERY TWO TURNS
            if turnNumber % 2 == 0:
                dropper.moveDropper()

            # DROPPER ACTIVATES EVERY SEVEN TURNS
            if turnNumber % 3== 0:
                dropper.activateDropper()

    # DRAW LEVEL
    for x in range(0,X//IMGSCALE):
        for y in range(0,Y//IMGSCALE):
            if currentTiles[x][y] != None:
                screen.blit(currentTiles[x][y],
                            (x*IMGSCALE,
                             y*IMGSCALE))
    
    # CRUSH PLAYER IF BOX HITS THEM
    if currentTiles[player.getX()][player.getY()-1] == box:
        exit(0)
    
    # INCREASE LEVEL NUMBER WHEN PLAYER GETS TO NEXT LEVEL
    if currentTiles[player.getX()][player.getY()] == door:
        # INCREMENT LEVEL NUMBER BY 1
        levelNumber += 1
        
        # REPLACE OLD POSITION OF DOOR WITH WALL,
        # ADD DOOR AT NEW POSITION
        currentTiles[player.getX()][player.getY()] = wall
        currentTiles[player.getX()][player.getY()-1] = door

        player.setPosition(1,(Y - (2*IMGSCALE))//IMGSCALE)

    # CALCULATE DECREMENT FOR COOLDOWNS
    delta:float = clock.tick()/1000

    # DRAW PLAYER
    screen.blit(player.playerImage,
                (player.getX()*IMGSCALE,
                 player.getY()*IMGSCALE))

 
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
