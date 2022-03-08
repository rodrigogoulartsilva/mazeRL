import pygame
import random
import numpy as np
import time
import json
from datetime import datetime
import sys, os

folder_path = os.path.dirname(sys.argv[0]) + '/'

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
dark_red = (200,0,0)
dark_green = (0,200,0)

boards = {
          '4x4':[[0,0,1,1],
		         [1,0,0,0],
		         [1,0,1,0],
		         [1,1,1,2]],
		 '6x6':[[0,0,1,1,1,1],
		        [1,0,1,0,0,0],
		        [1,0,0,0,1,0],
		        [1,1,1,0,1,0],
		        [0,0,0,0,1,0],
		        [1,1,1,1,1,2]],
		 '8x8':[[0,1,1,1,1,0,1,0],
		        [0,0,0,1,0,0,0,0],
		        [0,1,0,0,1,0,1,0],
		        [0,1,1,0,0,0,1,0],
		        [0,1,0,1,1,1,1,0],
		        [0,1,0,0,1,0,0,0],
		        [0,1,1,0,1,0,1,1],
		        [0,0,0,0,1,0,0,2]]
		 }

board = boards['6x6']

n_states = np.array(board).shape[0]*np.array(board).shape[1]

states_positions = {}

pos = 0
for row in range(np.array(board).shape[0]):
	for col in range(np.array(board).shape[1]):
		states_positions[pos]=(row,col)
		pos+=1

n_actions = 4

disp_height = 900
disp_width = 900

box_height = disp_height/len(board)
box_width = disp_height/len(board[0])
box_colors = {0:black,1:red,2:green}

gameDisplay = pygame.display.set_mode((disp_height,disp_width))
gameDisplay.fill(black)



clock = pygame.time.Clock()

def player(x,y,width,height,color):
	mouse_Img = pygame.image.load('JerryMouse.png')
	mouse_Img = pygame.transform.scale(mouse_Img, (int(box_width), int(box_height)))
	gameDisplay.blit(mouse_Img,(x,y))
	#pygame.draw.rect(gameDisplay,color, [x,y,width,height])

def text_objects(text,font,color):
	textSurface = font.render(text,True,color)
	return textSurface, textSurface.get_rect()

def draw_board(q_table,i_episode,avg_won):

	gameDisplay.fill(black)

	cat_Img = pygame.image.load('TomCat.png')
	cat_Img = pygame.transform.scale(cat_Img, (int(box_width), int(box_height)))

	cheese_Img = pygame.image.load('cheese.png')
	cheese_Img = pygame.transform.scale(cheese_Img, (int(box_width), int(box_height)))

	box_x = 0
	box_y = 0
	for line in board:
		for column in line:
			if column == 1:
				pygame.draw.rect(gameDisplay,box_colors[column],(box_x,box_y,box_height,box_width))
				gameDisplay.blit(cat_Img,(box_x,box_y))
			elif column == 2:
				gameDisplay.blit(cheese_Img,(box_x,box_y))
			else:
				pygame.draw.rect(gameDisplay,box_colors[column],(box_x,box_y,box_height,box_width))
			box_x += box_width
		box_x = 0
		box_y += box_height

	importances = np.mean(np.array(q_table),axis=1).reshape((np.array(board).shape[0],np.array(board).shape[1]))
	
	text_y = box_height/2

	for line in importances:
		text_x = box_width/2
		for column in line:
			largeText = pygame.font.Font('freesansbold.ttf',20)
			TextSurf, TextRect = text_objects("{0:.2f}".format(column), largeText,white)
			TextRect.center = ((text_x),(text_y))

			gameDisplay.blit(TextSurf, TextRect)

			text_x += box_width

		text_y += box_height

	text_y = 10
	text_x = 150

	largeText = pygame.font.Font('freesansbold.ttf',20)
	TextSurf, TextRect = text_objects('Episode:'+str(i_episode)+' Win Rate:'+"{0:.2f}".format(avg_won*100), largeText,blue)
	TextRect.center = ((text_x),(text_y))

	gameDisplay.blit(TextSurf, TextRect)



def epsilon_greedy_action(state, q_table,epsilon):
	max_score = np.max(q_table[state, :])

	actions_max_score = np.where(q_table[state, :] == max_score)[0]
	a = random.choice(actions_max_score)
    #a = np.argmax(q_table[state, :])
	if np.random.rand() < epsilon:
		a = np.random.randint(q_table.shape[1])
		print('Random choice')

	return a

def take_step(state,action):
	positions_states = {states_positions[key]:key for key in states_positions.keys()}

	if action == 0:
		new_position = (states_positions[state][0],states_positions[state][1]-1)
	elif action == 1:
		new_position = (states_positions[state][0]+1,states_positions[state][1])
	elif action == 2:
		new_position = (states_positions[state][0],states_positions[state][1]+1)
	elif action == 3:
		new_position = (states_positions[state][0]-1,states_positions[state][1])

	if new_position in positions_states.keys():
		new_state = positions_states[new_position]
	else:
		new_state = state

	box_type = board[states_positions[new_state][0]][states_positions[new_state][1]]

	done = False

	if box_type == 0:
		reward = 0
		done = False

	elif box_type == 1:
		reward = -1
		done = True

	elif box_type == 2:
		reward = 1
		done = True

	return new_state,reward,done

def q_learning_update(q_table, state, action, reward, state_prime,gamma,alpha):
    best_next_action = np.argmax(q_table[state_prime])     
    td_target = reward + gamma * q_table[state_prime][best_next_action] 
    td_delta = td_target - q_table[state][action]
    return q_table[state][action] + alpha * td_delta 

def button(msg,x,y,width,height,act_color,inact_color,action=None):

	mouse = pygame.mouse.get_pos()

	click = pygame.mouse.get_pressed()

	if x+width > mouse[0] > x and y+height > mouse[1] > height:
		pygame.draw.rect(gameDisplay,act_color,(x,y,width,height))
		if click[0] == 1 and action != None:
			action()
			# if action == 'play':
			# 	game_loop()
			# elif action == 'quit':
			# 	pygame.quit()
			# 	quit()
	else:
		pygame.draw.rect(gameDisplay,inact_color,(x,y,width,height))

	largeText = pygame.font.Font('freesansbold.ttf',20)
	TextSurf, TextRect = text_objects(msg, largeText,black)
	TextRect.center = ((x+(width/2)),(y+(height/2)))
	gameDisplay.blit(TextSurf, TextRect)

def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(black)

		largeText = pygame.font.Font('freesansbold.ttf',60)
		TextSurf, TextRect = text_objects("RLabyrinth", largeText,white)
		TextRect.center = ((disp_width/2),(disp_height/2))
		gameDisplay.blit(TextSurf, TextRect)

		button("Start Training",150,550,150,50,green,dark_green,game_loop)

		button("Quit",550,550,150,50,red,dark_red,quit)

		pygame.display.update()
		clock.tick(15)



def game_loop():

	q_table = np.zeros([n_states, n_actions])

	episodes_data = {}

	alpha = 0.05
	gamma = 0.99
	epsilon = 0.9
	epsilon_decay = 0.99
	verbose = True
	n_episodes = 1000
	max_tries = 500
	batch_size = 50

	avg_won = 0


	while True:

		for i_episode in range(n_episodes):

			begin_time = datetime.now()

			player_x = 0
			player_y = 0

			state = 0
			action = epsilon_greedy_action(state, q_table,epsilon)

			for i_step in range(max_tries):

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						print('Saved to: training_'+str(datetime.now())+'.json')

						with open('./training_results/training_'+str(datetime.now()).replace(':','-')+'.json', 'w') as outfile:
							json.dump(episodes_data, outfile,sort_keys=True, indent=4)
						pygame.quit()
						quit()

				x_change = 0
				y_change = 0

				draw_board(q_table,i_episode,avg_won)

				state_prime, reward, done = take_step(state,action)

				action_prime = epsilon_greedy_action(state_prime, q_table,epsilon)

				if state_prime!= state:

					q_table[state, action] = q_learning_update(q_table, state, action, reward, state_prime,gamma,alpha)

					if action==0:
						x_change = -box_width
					elif action==2:
						x_change = box_width
					if action==1:
						y_change = box_height
					elif action==3:
						y_change = -box_height

				actions_list = ['LEFT', 'DOWN', 'RIGHT', 'UP']

				if verbose:
					print('episode:',i_episode,'step:',i_step,'epsilon:',epsilon,'state:',state,'action:',actions_list[action],'state_prime:',state_prime, 'reward:',reward, 'done:',done,'x',player_x,'y',player_y,'x_change',x_change,'y_change',y_change)
					print()

				if player_x + x_change >= 0 and player_x+box_width + x_change <= disp_width:
					if player_y + y_change >= 0 and player_y+box_height + y_change <= disp_height:
						player_x += x_change
						player_y += y_change
						player(player_x,player_y,box_width,box_height,white)
						
				else:
					player(player_x,player_y,box_width,box_height,white)

				state = state_prime
				action = action_prime

				pygame.display.update()

				clock.tick(120)

				if done:
					break


			end_time = datetime.now()

			episodes_data[i_episode] = {'board':np.array(board).shape,
			'num_of_steps':i_step,
			'won':1 if reward == 1 else 0,
			'time':(end_time-begin_time).total_seconds(),
			'epsilon':epsilon}

			all_results = np.array([episodes_data[key]['won'] for key in episodes_data])

			avg_won = np.mean(all_results[-100:])
			episodes_data[i_episode]['average_won'] = np.mean(all_results[-100:])

			epsilon = epsilon * epsilon_decay

		pygame.quit()
		quit()


game_intro()
#game_loop()
pygame.quit()
#quit()