from includes import *
from algorithms import *
import utils
from copy import copy



def run_episode(env, gambler):
	gambler.reset(utils.draw(color='black'))     #At the start of the game both the player 
	dealer = Dealer(utils.draw(color='black'))   #and the dealer draw one black card (fully observed)
	
	episode_activity = []
	terminal = False
	state = (dealer, gambler, 0, False)
	action = None
	reward = 0
	
	while not terminal:
		if not action: #This will skip, if the action has been determined by `update` in the previous iteration
			action = gambler.choose_action(state)

		(dealer, gambler, reward, terminal) = state
		state_copy = (copy(dealer), copy(gambler), state[2], state[3]) #Otherwise, python passes object instances by reference
		state_prime = env.step(state_copy, action)

		(dealer_prime, gambler_prime, reward_prime, terminal_prime) = state_prime
		episode_activity.append(((dealer.first_card[1], gambler.sum, terminal, reward_prime), action)) #That's only used in MC
		
		(dealer, gambler, reward, terminal) = state_prime
		#action_bak = copy(action)
		action = gambler.update(state, action, state_prime, reward) # Used for Sarsa, does nothing for MC
		
		state = state_prime

	return (state, reward, episode_activity)
	
def simulation(episodes, alg):
	env = Environment()
	gambler = Gambler(algorithm=alg)

	for i in range(episodes):
		(_, reward, episode_activity) = run_episode(env, gambler)
		gambler.train(episode_activity, reward) #For MC, does nothing for Sarsa

	utils.plot_2d(gambler.get_P(), "Dealer showing", "Player sum", "Policy")
	utils.plot_3d(gambler.get_V(), "Dealer showing", "Player sum", "Value", "Value function")


alg = MonteCarlo(N_0=100) #Monte Carlo
#alg = SarsaL(N_0=100, gamma=1, lmbda = 0.5) #Sarsa
simulation(10000000, alg)


	

