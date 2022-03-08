import pygame
import random
import numpy as np

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

disp_height = 900
disp_width = 900


gameDisplay = pygame.display.set_mode((disp_height,disp_width))

gameDisplay.fill(black)


board = [[0,0,1,1,1,1],
		 [1,0,1,0,0,0],
		 [1,0,0,0,1,0],
		 [1,1,1,0,1,0],
		 [0,0,0,0,1,0],
		 [1,1,1,1,1,2]]

knowledge = np.zeros((np.array(board).shape[0],np.array(board).shape[1]))

box_height = disp_height/len(board)

box_width = disp_height/len(board[0])

box_colors = {0:black,1:red,2:green}

box_x = 0

box_y = 0

def player(x,y,width,height,color):
	pygame.draw.rect(gameDisplay,color, [x,y,width,height])

def text_objects(text,font):
	textSurface = font.render(text,True,white)
	return textSurface, textSurface.get_rect()

player_x = 0
player_y = 0

x_change = 0

y_change = 0


player(player_x,player_y,box_width,box_height,white)

clock = pygame.time.Clock()

steps = 0

while True:

	box_x = 0
	box_y = 0

	for line in board:
				#print(line)
		for column in line:
			pygame.draw.rect(gameDisplay,box_colors[column],(box_x,box_y,box_height,box_width))
			box_x += box_width
		box_x = 0
		box_y += box_height

	
	text_y = box_height/2

	for line in knowledge:
		text_x = box_width/2
		for column in line:
			largeText = pygame.font.Font('freesansbold.ttf',20)
			TextSurf, TextRect = text_objects(str(column), largeText)
			TextRect.center = ((text_x),(text_y))

			gameDisplay.blit(TextSurf, TextRect)

			text_x += box_width

		text_y += box_height



	#if steps == 0:


	#else:



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x_change = -box_width

			elif event.key == pygame.K_RIGHT:
				x_change = box_width

			if event.key == pygame.K_UP:
				y_change = -box_height

			elif event.key == pygame.K_DOWN:
				y_change = box_height

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				x_change = 0
				y_change = 0

		#print(player_x,x_change)

	keys_pressed = pygame.key.get_pressed()

	if keys_pressed[pygame.K_LEFT]:
		x_change = -box_width
	elif keys_pressed[pygame.K_RIGHT]:
		x_change = box_width

	if keys_pressed[pygame.K_UP]:
		y_change = -box_height
	elif keys_pressed[pygame.K_DOWN]:
		y_change = box_height

	if player_x + x_change >= 0 and player_x+box_width + x_change <= disp_width:
		if player_y + y_change >= 0 and player_y+box_height + y_change <= disp_height:
			player_x += x_change
			player_y += y_change
			steps +=1
			player(player_x,player_y,box_width,box_height,white)

			pygame.display.update()



	#parameters enable game item update
	
	#number of frames/second
	clock.tick(10)	

	#pygame.display.update()

pygame.quit()
quit()