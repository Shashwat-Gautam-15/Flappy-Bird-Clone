import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 500
SCREENHEIGHT = 800
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Flappy/Iron1.png'
BACKGROUND = 'Flappy/space.png'
PIPE = 'Flappy/pipe111.png'

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5) #error and trial
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) # to get the stuff at centre
    #messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)# to to get the task doen at the centre
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                #SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY # acc and vel different sign therefore retardation

        if playerFlapped:
            playerFlapped = False       # This is beacause we wnat mutiple keydown up or space bar if not false it will keep moving up until it collide with just one key down     
        playerHeight = GAME_SPRITES['player'].get_height()
        # see here the other term after playerVelY is basially 0 but why written in this manner ?
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        # see we started with 2 pipes namely NewPipe1 and NewPipe2 and when NewPipe1 is about to end the screen we generate a new pipe
        #and place it there
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        # The upperpipe is a list two dictionary as elements each conatining a pipe
        # so should it not be uppPipe[0]['x'] ? cleared answer in pad notes
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        """
        score let say 123 so str(score) = '1' ,'2','3'
        then list(str(score)) = ['1','2','3']
        then int x for x in === [1,2,3]
        Width will be sum of all the digits size so dynamic
        """
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# def isCollide(playerx, playery, upperPipes, lowerPipes):
#     if playery> GROUNDY - 25  or playery<0:
#         #GAME_SOUNDS['hit'].play()
#         return True
    
#     for pipe in upperPipes:
#         pipeHeight = GAME_SPRITES['pipe'][0].get_height()
#         if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
#             #GAME_SOUNDS['hit'].play()
#             return True

#     for pipe in lowerPipes:
#         if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
#             #GAME_SOUNDS['hit'].play()
#             return True

#     return False


# THIS IS PIXEL PERFECT COLLISON EARLIER WE WERE CHECKING MANUALLY
def isCollide(playerx, playery, upperPipes, lowerPipes):
    playerRect = pygame.Rect(playerx, playery, GAME_SPRITES['player'].get_width(), GAME_SPRITES['player'].get_height())

    # Check collision with ground or ceiling
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    # Check collision with pipes
    #here pipe is the first element of list Upppipes which is dictionary with 2 keys X and Y
    for pipe in upperPipes:
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], GAME_SPRITES['pipe'][0].get_width(), GAME_SPRITES['pipe'][0].get_height())
        if playerRect.colliderect(pipeRect):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], GAME_SPRITES['pipe'][1].get_width(), GAME_SPRITES['pipe'][1].get_height())
        if playerRect.colliderect(pipeRect):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    This function returns a list which have 1 Upper and 1 Lowe pipe
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by CodeWithHarry')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('Flappy/0.png').convert_alpha(),
        pygame.image.load('Flappy/1.png').convert_alpha(),
        pygame.image.load('Flappy/2.png').convert_alpha(),
        pygame.image.load('Flappy/3.png').convert_alpha(),
        pygame.image.load('Flappy/4.png').convert_alpha(),
        pygame.image.load('Flappy/5.png').convert_alpha(),
        pygame.image.load('Flappy/6.png').convert_alpha(),
        pygame.image.load('Flappy/7.png').convert_alpha(),
        pygame.image.load('Flappy/8.png').convert_alpha(),
        pygame.image.load('Flappy/9.png').convert_alpha(),
    )

    #GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('Flappy/base1.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
