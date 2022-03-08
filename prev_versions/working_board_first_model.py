import pygame
import random
import numpy as np
import time

pygame.init()


def player(x,y,width,height,color):
	pygame.draw.rect(gameDisplay,color, [x,y,width,height])

def text_objects(text,font,color):
	textSurface = font.render(text,True,color)
	return textSurface, textSurface.get_rect()

def epsilon_greedy_action(state, q_table):
	max_score = np.max(q_table[state, :])

	actions_max_score = np.where(q_table[state, :] == max_score)[0]
	a = random.choice(actions_max_score)
    #a = np.argmax(q_table[state, :])
	if np.random.rand() < epsilon:
		a = np.random.randint(q_table.shape[1])
		print('Random')

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
		#reward = rewards[states_positions[new_state][0]][states_positions[new_state][1]]
		done = False

	elif box_type == 1:
		reward = -1
		#reward = rewards[states_positions[new_state][0]][states_positions[new_state][1]]
		done = True

	elif box_type == 2:
		reward = 1
		#reward = rewards[states_positions[new_state][0]][states_positions[new_state][1]]
		done = True

	#if new_state == state:
		#reward = 0

	return new_state,reward,done

def q_learning_update(q_table, state, action, reward, state_prime):
    best_next_action = np.argmax(q_table[state_prime])     
    td_target = reward + gamma * q_table[state_prime][best_next_action] 
    td_delta = td_target - q_table[state][action]
    return q_table[state][action] + alpha * td_delta 

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

disp_height = 900
disp_width = 900


gameDisplay = pygame.display.set_mode((disp_height,disp_width))

gameDisplay.fill(black)

board = [[0,0,1,1],
		 [1,0,0,0],
		 [1,0,1,0],
		 [1,1,1,2]]


board = [[0,0,1,1,1,1],
		 [1,0,1,0,0,0],
		 [1,0,0,0,1,0],
		 [1,1,1,0,1,0],
		 [0,0,0,0,1,0],
		 [1,1,1,1,1,2]]


board = [[0,1,1,1,1,0,1,0],
		 [0,0,0,1,0,0,0,0],
		 [0,1,0,0,1,0,1,0],
		 [0,1,1,0,0,0,1,0],
		 [0,1,0,1,1,1,1,0],
		 [0,1,0,0,1,0,0,0],
		 [0,1,1,0,1,0,1,1],
		 [0,0,0,0,1,0,0,2]]


rewards = [[-13,-12,5,5,5,5],
		 [20,-11,-50,-7,-50,-5],
		 [20,-10,-9,-8,-50,-4],
		 [20,-50,-50,-8,-50,-3],
		 [20,-5,-6,-7,-50,-2],
		 [20,20,20,20,20,1]]

knowledge = np.zeros((np.array(board).shape[0],np.array(board).shape[1]))

n_states = np.array(board).shape[0]*np.array(board).shape[1]

states_positions = {}

pos = 0
for row in range(np.array(board).shape[0]):
	for col in range(np.array(board).shape[1]):
		states_positions[pos]=(row,col)
		pos+=1

print(states_positions)



#print(positions_states)

n_actions = 4

q_table = np.zeros([n_states, n_actions])

alpha = 0.05
gamma = 0.99
epsilon = 1
epsilon_decay = 0.99
verbose = True

n_episodes = 1000
max_tries = 500

#print(q_table)


box_height = disp_height/len(board)

box_width = disp_height/len(board[0])

box_colors = {0:black,1:red,2:green}

box_x = 0

box_y = 0

player_x = 0
player_y = 0
x_change = 0
y_change = 0


player(player_x,player_y,box_width,box_height,white)

clock = pygame.time.Clock()

steps = 0

while True:

	for i_episode in range(n_episodes):

		player_x = 0
		player_y = 0

		state = 0

		action = epsilon_greedy_action(state, q_table)



		for i_step in range(max_tries):

			box_x = 0
			box_y = 0
			x_change = 0
			y_change = 0

			for line in board:
						#print(line)
				for column in line:
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
			text_x = 50

			largeText = pygame.font.Font('freesansbold.ttf',20)
			TextSurf, TextRect = text_objects('Episode:'+str(i_episode), largeText,blue)
			TextRect.center = ((text_x),(text_y))

			gameDisplay.blit(TextSurf, TextRect)

					

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			state_prime, reward, done = take_step(state,action)

			actions_list = ['LEFT', 'DOWN', 'RIGHT', 'UP']

			print('episode:',i_episode,'step:',i_step,'epsilon:',epsilon,'state:',state,'action:',actions_list[action],'state_prime:',state_prime, 'reward:',reward, 'done:',done,'x',player_x,'y',player_y)

			action_prime = epsilon_greedy_action(state_prime, q_table)

			if state_prime!= state:

				q_table[state, action] = q_learning_update(q_table, state, action, reward, state_prime)


				if action==0:
					x_change = -box_width
				elif action==2:
					x_change = box_width

				if action==1:
					y_change = box_height
				elif action==3:
					y_change = -box_height

			if player_x + x_change >= 0 and player_x+box_width + x_change <= disp_width:
				if player_y + y_change >= 0 and player_y+box_height + y_change <= disp_height:
					player_x += x_change
					player_y += y_change
					steps +=1
					player(player_x,player_y,box_width,box_height,white)

			else:
				player(player_x,player_y,box_width,box_height,white)

			state = state_prime
			action = action_prime

			if done:
				break
			pygame.display.update()
			#time.sleep(0.1)
			clock.tick(120)

			print()

		epsilon = epsilon * epsilon_decay
	
		print(q_table)
	break
	#pygame.display.update()

#pygame.quit()
#quit()