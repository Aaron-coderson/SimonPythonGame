import pygame
import random
import sys
import time
from pygame.locals import *
#define global constant variables
FPS = 36 #frame per second
WIDTH = 640
HEIGHT = 480
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4

#define global color varaibles
#                 R    G    B 
WHITE =         (255, 255, 255)
BLACK =         (0,   0,   0)
BRIGHT_RED =    (255, 0,   0)
RED =           (155, 0,   0)
BRIGHT_GREEN =  (0,   255, 0)
GREEN =         (0,   155, 0)
BRIGHT_BLUE =   (0,   0, 255)
BLUE =          (0,   0, 155)
BRIGHT_YELLOW = (255, 255, 0)
YELLOW =        (155, 155, 0)
DARKGRAY =      (40,  40,  40)
BG_COLOR =      BLACK

XMARGIN = int((WIDTH - (2*BUTTONSIZE) - BUTTONGAPSIZE)/2) 
YMARGIN = int((HEIGHT - (2*BUTTONSIZE) - BUTTONGAPSIZE)/2)

#rect objects
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

WHITE = (255,255,255)

def main():
	""" control game condition, game display, and main while loop"""
	global WINDOW, FPSCLOCK, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('simon')

	BASICFONT = pygame.font.SysFont('comicsansms',10) #defines text
	info_window = BASICFONT.render('Repeat the flashing pattern using the Q, W, A, S and if you get the patern correct you get a point but if you get it wrong you loose',1,BLACK) # writes down text
	infoRect = info_window.get_rect()
	infoRect.topleft = (10, HEIGHT -25) # place text
	BEEP1 = pygame.mixer.Sound('beep1.ogg') # add sound
	BEEP2 = pygame.mixer.Sound('beep2.ogg') # add sound
	BEEP3 = pygame.mixer.Sound('beep3.ogg') # add sound
	BEEP4 = pygame.mixer.Sound('beep4.ogg') # add sound
	# Inialize some variablrs for a newgame
	pattern = [] # stores parttern of colors
	current_step = 0 # the color the player must click nextffffff
	last_click_time = 0 # timestap of the player's last button clicked
	score = 0 # set score
	waiting_for_input = False
	running = True
	while running:
		clicked_button = None
		WINDOW.fill(BG_COLOR)
		draw_button()
		score_win = BASICFONT.render('YOUR SCORE IS ' + str(score), 1, WHITE)
		score_rect = score_win.get_rect()
		score_rect.topleft = (WIDTH -100,10)
		WINDOW.blit(score_win, score_rect)
		WINDOW.blit(info_window, infoRect)
		check_for_quit()
		for event in pygame.event.get():
			if event.type ==MOUSEBUTTONUP:
				mousex, mousey = event.pos
				clicked_button = get_botton_clicked(mousex, mousey)
			elif event.type == KEYDOWN:
				if event.key == K_q:
					clicked_button =  YELLOW
				elif event.key == K_w:
					clicked_button = BLUE
				elif event.key == K_a:
					clicked_button = RED
				elif event.key == K_s:
					clicked_button = GREEN
		if not waiting_for_input:
			# play the paterns
			pygame.display.update()
			pygame.time.wait(1000)
			pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
			for button in pattern:
				flash_botton_animation(button)
				pygame.time.wait(FLASHDELAY)
				waiting_for_input = True
		elif waiting_for_input:
			if clicked_button != None and clicked_button == pattern[current_step]:
				flash_botton_animation(clicked_button)
				current_step += 1
				last_click_time = time.time()

				if current_step == len(pattern):
					change_backround_color()
					score += 1
					waiting_for_input = False
					current_step = 0
			elif (clicked_button and clicked_button != pattern[current_step]) or (current_step != 0 and time.time() - TIMEOUT > last_click_time):
				game_over_animation()
				pygame.time.wait(1000)
				go_surf = BASICFONT.render("Game Over", True, (0,0,0))
				go_rect = go_surf.get_rect()
				go_rect.topleft = (20,100)				

		draw_button()
def terminate():
	"""end the game"""
	pygame.quit()
	sys.exit()
def check_for_quit():
	"""see if  user quits"""
	# for event in pygame.event.get():
	# 	if event.type == pygame.QUIT:
	# 		terminate()
	# for event in pygame.event.get():
	# 	if event.type == K_ESCAPE:
	# 		terminate()
	for event in pygame.event.get(KEYUP):
		if event.key == K_ESCAPE:
			terminate()
		pygame.event.post(event)

def flash_botton_animation(color, animation_speed = 50):
	"""show user pattern"""
	if color == YELLOW:
		sound = BEEP1
		flashColor = BRIGHT_YELLOW
		rectangle = YELLOWRECT
		
	elif color == BLUE:
		sound = BEEP2
		flashColor = BRIGHT_BLUE
		rectangle = BLUERECT
	elif color == RED:
		sound = BEEP3
		flashColor = BRIGHT_RED
		rectangle = REDRECT
	elif color == GREEN:
		sound = BEEP4
		flashColor = BRIGHT_GREEN
		rectangle = GREENRECT

	oriwindow = WINDOW.copy()
	flashWINDOW = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
	flashWINDOW = flashWINDOW.convert_alpha()
	r, g, b = flashColor
	sound.play()
	for start, end, step in ((0,255,12),(255,0,-1)):
		for alpha in range(start, end, animation_speed * step):
			check_for_quit()
			WINDOW.blit(oriwindow,(0,0))
			flashWINDOW.fill((r, g, b, alpha))
			WINDOW.blit(flashWINDOW, rectangle.topleft)
			pygame.display.update()
			FPSCLOCK.tick(FPS)
		WINDOW.blit(oriwindow,(0,0))

def draw_button():
	"""make boxes"""
	pygame.draw.rect(WINDOW,YELLOW,YELLOWRECT)
	pygame.draw.rect(WINDOW,RED,REDRECT)
	pygame.draw.rect(WINDOW,BLUE,BLUERECT)
	pygame.draw.rect(WINDOW,GREEN,GREENRECT)
	pygame.display.update()

def change_backround_color(animationSpeed=24):
	"""change backround color"""
	global BG_COLOR
	new_bg_color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
	new_bg_surf = pygame.Surface((WIDTH, HEIGHT))
	new_bg_surf = new_bg_surf.convert_alpha()
	r, g, b = new_bg_color
	for alpha in range(0, 256, animationSpeed):
		check_for_quit()
		WINDOW.fill(BG_COLOR)
		new_bg_surf.fill((r, g, b, alpha))
		WINDOW.blit(new_bg_surf, (0, 0))
		draw_button()
		pygame.display.update()
		FPSCLOCK.tick(FPS)
	BG_COLOR = new_bg_color
def game_over_animation(color = WHITE, animation_speed = 48):
	"""show game over"""
	oriwindow = WINDOW.copy()
	flashwinndow= pygame.Surface(WINDOW.get_size())
	flashwinndow= flashwinndow.convert_alpha()
	BEEP1.play()
	BEEP2.play()
	BEEP3.play()	
	BEEP4.play()
	r,g,b = color
	for i in range(3):
		for start, end, step in ((0,255,1),(255,0,-1)):
			for alpha in range(start, end, animation_speed*step):
				check_for_quit()
				flashwinndow.fill((r, g, b, alpha))
				WINDOW.blit(oriwindow,(0,0))
				WINDOW.blit(flashwinndow,(0,0))
				draw_button()
				pygame.display.update()
				FPSCLOCK.tick(FPS)
def get_botton_clicked(x,y):
	"""sense if button pressed"""
	if YELLOWRECT.collidepoint(x,y):
		return YELLOW
	elif BLUERECT.collidepoint(x,y):
		return BLUE
	elif REDRECT.collidepoint(x,y):
		return RED
	elif GREENRECT.collidepoint(x,y):
		return GREEN
	else:
		return None

main()
	



