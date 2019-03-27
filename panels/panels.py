import pygame
from pygame.locals import *
from pygame.midi import *

#--------HEADER-----------------

# defines
ACTIVE    = 1
INACTIVE  = 0
NOTE = 0
CC = 1
PC = 2

class button:
	def __init__(self,name="button",imgon="on.png",imgoff="off.png",posx=0,posy=0,mtype=NOTE,mnum=64,mon=100,moff=0,mchan=1):
		self.name = name # name of the button
		self.imgon = imgon # name of file to be used when ACTIVE position
		self.imgoff = imgoff # name of file to be used when INACTIVE position
		self.imgonbuf = pygame.image.load(self.imgon).convert_alpha()
		self.imgoffbuf = pygame.image.load(self.imgoff).convert_alpha()
		self.imgonsize = self.imgonbuf.get_size()
		self.imgoffsize = self.imgoffbuf.get_size()
		self.position = posx,posy # top left corner gui position, pixel for fixed, or grid positions, or numbering for responsive
		self.mtype = mtype  # note/cc/pc
		self.mnum = mnum # notenumber/ccnumber/pcnumber
		self.mon  = mon # notevelocity/ccvalue/xx for on status
		self.moff = moff # notevelocity/ccvalue/xx for off status
		self.mchan = mchan  # midi channel
		self.status = INACTIVE # ACTIVE or INACTIVE , 1/0
	def __str__(self):
		return "DUMP: name %s, position %s, status %i" % (self.name, self.position, self.status)
	def SetPosition(self,x=0,y=0):
		self.position = x,y
	def LoadImages(self):
		self.imgonbuf  = pygame.image.load(self.imgon).convert_alpha()
		self.imgoffbuf = pygame.image.load(self.imgoff).convert_alpha()
	def ShowOn(self):
		screen.blit(self.imgonbuf, self.position)
	def ShowOff(self):
		screen.blit(self.imgoffbuf, self.position)
	def Refresh(self):
		if self.IsActive():
			self.ShowOn()
		if not self.IsActive():
			self.ShowOff()
	def SetActive(self):
		self.status = ACTIVE
	def SetInactive(self):
		self.status = INACTIVE
	def IsActive(self):
		return self.status
	def SendMidiOnTouch(self,event):
		if (event.pos[0] > self.position[0] and event.pos[0] < self.position[0] + self.imgonsize[0]) and \
	               (event.pos[1] > self.position[1] and event.pos[1] < self.position[1] + self.imgonsize[1]):
			if self.IsActive(): 
				self.SendMidiOff()
				self.SetInactive()
			else:
				self.SendMidiOn()
				self.SetActive()
	def SetMidi(self,t=0,b1=64,b2=100,b3=0,c=1):
		self.mtype = t  # note/cc/pc
		self.mnum  = b1 # notenumber/ccnumber/pcnumber
		self.mon   = b2 # notevelocity/ccvalue/xx
		self.moff  = b3 # notevelocity/ccvalue/xx
		self.mchan = c  # midi channel
	def SendMidiOn(self):
		if self.mtype == NOTE:
			midiout.note_on(self.mnum,self.mon,self.mchan)
			#midiout.write_short(0x90,self.mnum,self.mon)
		elif self.mtype == CC:
			midiout.write_short(0xb0,self.mnum,self.mon)
		elif self.mtype == PC:
			midiout.write_short(0xc0,self.mnum)
	def SendMidiOff(self):
		if self.mtype == NOTE:
			midiout.note_off(self.mnum,self.moff,self.mchan)
			#midiout.write_short(0x90,self.mnum,self.moff)
		elif self.mtype == CC:
			midiout.write_short(0xb0,self.mnum,self.moff)
		elif self.mtype == PC:
			pass			
			#midiout.write_short(0xc0,self.mnum)

#-------------------------------

#prepare GUI window
pygame.init()

#verify MIDI ports
pygame.midi.init()
#count = pygame.midi.get_count()
#print("get_default_input_id:%d" % pygame.midi.get_default_input_id())
#print("get_default_output_id:%d" % pygame.midi.get_default_output_id())
#print("No:(interf, name, input, output, opened)")
#for i in range(count):
#    print("%d:%s" % (i, pygame.midi.get_device_info(i)))

#assign port
port = pygame.midi.get_default_output_id()
print ("Using midi output :%s" % port)
midiout = pygame.midi.Output(port, 0)

#define GUI dimensions
size = width, height = 1160, 772
#open the pygame window
screen = pygame.display.set_mode(size)

#load and set background image
background = pygame.image.load("darkwood.jpg").convert()
backgroundrect = background.get_rect()
screen.blit(background, backgroundrect)

#create buttons for ManIII
butM3 = button("MANIII","MANIII.png","MANIII.png",450,590,CC,100,100,100,10)
but1 = button("but1","III-principal8-on.png","III-principal8-off.png",10,10,CC,0,100,0,1)
but2 = button("but2","III-gemshorn8-on.png","III-gemshorn8-off.png",300,10,CC,1,100,0,1)
but3 = button("but3","III-quintadena8-on.png","III-quintadena8-off.png",590,10,CC,2,100,0,1)
but4 = button("but3","III-suabile8-on.png","III-suabile8-off.png",880,10,CC,3,100,0,1)
but5 = button("but3","III-rohrflote4-on.png","III-rohrflote4-off.png",10,300,CC,4,100,0,1)
but6 = button("but3","III-dulzflote4-on.png","III-dulzflote4-off.png",300,300,CC,5,100,0,1)
but7 = button("but3","III-quintflote223-on.png","III-quintflote223-off.png",590,300,CC,6,100,0,1)
but8 = button("but3","III-superoctave2-on.png","III-superoctave2-off.png",880,300,CC,7,100,0,1)
butM3.LoadImages()
but1.LoadImages()
but2.LoadImages()
but3.LoadImages()
but4.LoadImages()
but5.LoadImages()
but6.LoadImages()
but7.LoadImages()
but8.LoadImages()
butM3.ShowOff()
but1.ShowOff()
but2.ShowOff()
but3.ShowOff()
but4.ShowOff()
but5.ShowOff()
but6.ShowOff()
but7.ShowOff()
but8.ShowOff()

#refresh screen
pygame.display.flip()

#program loop
running = 1
while running:

	#check for events in the window
	for event in pygame.event.get():

		#if window to be closed or key q is pressed
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_q): 
			running = 0

		#if left click mouse button or tactile screen touched
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			#check button1
			but1.SendMidiOnTouch(event)
			#check button2
			but2.SendMidiOnTouch(event)
			#check button3
			but3.SendMidiOnTouch(event)
			#check button4
			but4.SendMidiOnTouch(event)
			#check button5
			but5.SendMidiOnTouch(event)
			#check button6
			but6.SendMidiOnTouch(event)
			#check button7
			but7.SendMidiOnTouch(event)
			#check button8
			but8.SendMidiOnTouch(event)

		#refresh background image
		screen.blit(background, backgroundrect)

		#update buttons status images
		butM3.Refresh()
		but1.Refresh()
		but2.Refresh()
		but3.Refresh()
		but4.Refresh()
		but5.Refresh()
		but6.Refresh()
		but7.Refresh()
		but8.Refresh()

		#refresh screen
		pygame.display.flip()

pygame.midi.quit()
pygame.display.quit()
