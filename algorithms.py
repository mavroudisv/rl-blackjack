import numpy as np
from random import randrange, uniform

class MonteCarlo:
	def __init__(self, N_0):
		self.N_0 = N_0
		
		# Number of visits on State: Dealer's first card (10 options), gambler's sum (21 options)
		self.NS = np.zeros([10, 21])

		# Number of visits on State-Action: Dealer's first card (10 options), gambler's sum (21 options), actions (2 options, 0:hit, 1:stick)
		self.NSA = np.zeros([10, 21, 2])

		# State-Action Reward: Dealer's first card (10 options), gambler's sum (21 options), actions (2 options)
		self.Q = np.zeros([10, 21, 2])
		
		# Value function: Dealer's first card (10 options), gambler's sum (21 options)
		self.V = np.zeros([10, 21])
		
		self.P = np.zeros([10, 21])
		
	def choose_action(self, state):
		(dealer, gambler, _, _) = state
		#dealer_showing_idx = (dealer.first_card[1] if dealer.first_card[0]=='black' else dealer.first_card[1]+10)-1
		dealer_showing_idx = dealer.first_card[1]-1
		gambler_idx = gambler.sum-1		
		
		epsilon = self.N_0/(self.N_0 + self.NS[dealer_showing_idx, gambler_idx])
		die = uniform(0, 1)
		
		if die <= epsilon: #Explore
			if randrange(2)== 0:
				action = 'hit'
			else:
				action = 'stick'		
		else: #Exploit
			if self.Q[dealer_showing_idx,gambler_idx,0] > self.Q[dealer_showing_idx,gambler_idx,1]: # 0:hit, 1:stick
				action = 'hit'
			else:
				action = 'stick'

		#Update counts
		self.NS[dealer_showing_idx, gambler_idx] += 1
		if action == 'hit':
			self.NSA[dealer_showing_idx, gambler_idx, 0] += 1
			#print("Updated", dealer_showing_idx, gambler_idx, 0, action)
		else:
			self.NSA[dealer_showing_idx, gambler_idx, 1] += 1
			#print("Updated", dealer_showing_idx, gambler_idx, 1, action)
				
		return action
	
	def update(self, state, action, state_prime, reward):
		return None
	
	def train(self, episode_activity, reward):

		G = sum([ea[0][3] for ea in episode_activity])

		for snapshot, action in episode_activity:
			(dealer_showing, gambler_sum, _, _) = snapshot
			dealer_showing_idx = dealer_showing-1
			gambler_idx = gambler_sum-1
			action_idx = 0 if action == 'hit' else 1

			alpha = 1.0 / self.NSA[dealer_showing_idx, gambler_idx, action_idx]
			self.Q[dealer_showing_idx, gambler_idx, action_idx] += alpha * (G - self.Q[dealer_showing_idx, gambler_idx, action_idx])
	
	def reset(self):
		pass
		
	def derive_V(self):
		for dealer_showing_idx in range(10):
			for gambler_idx in range(21):
				self.V[dealer_showing_idx, gambler_idx] = max(self.Q[dealer_showing_idx, gambler_idx, :])
	
	def derive_P(self):
		for dealer_showing_idx in range(10):
			for gambler_idx in range(21):
				if self.Q[dealer_showing_idx, gambler_idx, 0] > self.Q[dealer_showing_idx, gambler_idx, 1]:
					self.P[dealer_showing_idx, gambler_idx] = 0
				else:
					self.P[dealer_showing_idx, gambler_idx] = 1
	
class SarsaL:
	def __init__(self, N_0, gamma, lmbda):
		self.gamma = gamma
		self.lmbda = lmbda
		
		self.N_0 = N_0
		
		# Number of visits on State: Dealer's first card (10 options), gambler's sum (21 options)
		self.NS = np.zeros([10, 21])

		# Number of visits on State-Action: Dealer's first card (10 options), gambler's sum (21 options), actions (2 options, 0:hit, 1:stick)
		self.E = np.zeros([10, 21, 2])
		self.NSA = np.zeros([10, 21, 2])

		# State-Action Reward: Dealer's first card (10 options), gambler's sum (21 options), actions (2 options)
		self.Q = np.zeros([10, 21, 2])
		
		# Value function: Dealer's first card (10 options), gambler's sum (21 options)
		self.V = np.zeros([10, 21])
		self.P = np.zeros([10, 21])

	
	def choose_action(self, state):
		(dealer, gambler, _, _) = state
		dealer_showing_idx = dealer.first_card[1]-1
		gambler_idx = gambler.sum-1		
		
		epsilon = self.N_0/(self.N_0 + self.NS[dealer_showing_idx, gambler_idx])
		die = uniform(0, 1)
		
		if die <= epsilon: #Explore
			if randrange(2)== 0:
				action = 'hit'
			else:
				action = 'stick'		
		else: #Exploit
			if self.Q[dealer_showing_idx,gambler_idx,0] > self.Q[dealer_showing_idx,gambler_idx,1]: # 0:hit, 1:stick
				action = 'hit'
			else:
				action = 'stick'
	
		return action
	
	def update(self, state, action, state_prime, reward):
		#wow, that's a lot to unpack
		(dealer, gambler, reward, terminal) = state
		(dealer_prime, gambler_prime, reward_prime, terminal_prime) = state_prime
				
	
		#Bookkeeping for S
		dealer_showing = dealer.first_card[1]
		dealer_showing_idx = dealer_showing-1
		gambler_idx = gambler.sum-1
		action_idx = 0 if action == 'hit' else 1
		self.NS[dealer_showing_idx, gambler_idx] += 1
		self.E[dealer_showing_idx, gambler_idx, action_idx] += 1
		self.NSA[dealer_showing_idx, gambler_idx, action_idx] += 1
		Q = self.Q[dealer_showing_idx, gambler_idx, action_idx]	
		
		if terminal_prime:
			delta = reward_prime - Q
			action_prime = None
		else:
			action_prime = self.choose_action(state_prime) # Choose action A' to be taken from S'
	
			#Variables for S
			self.NS[dealer_showing_idx, gambler_idx] += 1
			self.E[dealer_showing_idx, gambler_idx, action_idx] += 1
			self.NSA[dealer_showing_idx, gambler_idx, action_idx] += 1
	
			#Variables for S'
			dealer_showing_idx_prime = dealer_prime.first_card[1] - 1
			gambler_idx_prime = gambler_prime.sum - 1
			action_idx_prime = 0 if action_prime == 'hit' else 1
			Q_prime = self.Q[dealer_showing_idx_prime, gambler_idx_prime, action_idx_prime]
			delta = reward_prime + self.gamma * Q_prime - Q
		
		alpha = 1.0 / self.NSA[dealer_showing_idx, gambler_idx, action_idx]
		self.Q += (alpha * delta * self.E)
		self.E *= (self.gamma * self.lmbda)
		#print(self.E[dealer_showing_idx, gambler_idx, action_idx], self.E[dealer_showing_idx_prime, gambler_idx_prime, action_idx_prime])

		return action_prime
		
	def train(self, episode_activity, reward):
		pass
	
	def reset(self):
		self.E = np.zeros([10, 21, 2])
	
	def derive_V(self):
		for dealer_showing_idx in range(10):
			for gambler_idx in range(21):
				self.V[dealer_showing_idx, gambler_idx] = max(self.Q[dealer_showing_idx, gambler_idx, :])
	
	def derive_P(self):
		for dealer_showing_idx in range(10):
			for gambler_idx in range(21):
				if self.Q[dealer_showing_idx, gambler_idx, 0] > self.Q[dealer_showing_idx, gambler_idx, 1]:
					self.P[dealer_showing_idx, gambler_idx] = 0
				else:
					self.P[dealer_showing_idx, gambler_idx] = 1