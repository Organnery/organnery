import pygame
from pygame.locals import *
from pygame.midi import *

#prepare GUI window
pygame.init()

#verify MIDI ports
pygame.midi.init()
port = pygame.midi.get_default_output_id()
print ("Using midi output :%s" % port)
midiout = pygame.midi.Output(port, 0)

#define GUI dimensions and positions
size = width, height = 500, 240
pos1 = 20, 20
pos2 = 250, 20

#open the pygame window
screen = pygame.display.set_mode(size)

#load and set background image
background = pygame.image.load("wood.jpg").convert()
backgroundrect = background.get_rect()
screen.blit(background, backgroundrect)

#load and set buttons images
but_on = pygame.image.load("on.png").convert_alpha()
but_off = pygame.image.load("off.png").convert_alpha()
button1state = 0
button2state = 0
screen.blit(but_off, pos1)
screen.blit(but_off, pos2)

#refresh screen
pygame.display.flip()

#program loop
running = 1
while running:

    #check for events in the window
    for event in pygame.event.get():

        #if window to be closed or key q is pressed
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q: 
            running = 0

        #if left click mouse button or tactile screen touched
        if event.type == MOUSEBUTTONDOWN and event.button == 1:

            #if it is button1
            if (event.pos[0] > pos1[0] and event.pos[0] < pos1[0] + 150) and \
               (event.pos[1] > pos1[1] and event.pos[1] < pos1[1] + 150):
                button1state = not button1state
                #envoyer le message midi

            #if it is button2
            if (event.pos[0] > pos2[0] and event.pos[0] < pos2[0] + 150) and \
               (event.pos[1] > pos2[1] and event.pos[1] < pos2[1] + 150):
                button2state = not button2state

    #refresh background image
    screen.blit(background, backgroundrect)

    #update buttons state
    if button1state == 0:
        midiout.note_off(64)
        screen.blit(but_off, pos1)
    if button1state == 1:
        midiout.note_on(64,100)
        screen.blit(but_on, pos1)
    if button2state == 0:
        midiout.note_off(72)
        screen.blit(but_off, pos2)
    if button2state == 1:
        midiout.note_on(72,100)
        screen.blit(but_on, pos2)
    
    #refresh screen
    pygame.display.flip()