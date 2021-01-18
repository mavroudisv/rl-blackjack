import utils
	

class Gambler:
	def __init__(self, algorithm=None):
		self.algorithm = algorithm
		self.sum = 0

	def reset(self, first_card = None):
		self.sum = 0
		if first_card:
			self.add(first_card)
		self.algorithm.reset()
			
	def add(self, card):
		(color, num) = card
		if color == 'black':
			self.sum += num
		else:
			self.sum -= num

	def choose_action(self, state):
		return self.algorithm.choose_action(state)

	def update(self, state, action, state_prime, reward):
		return self.algorithm.update(state, action, state_prime, reward)
		
	def train(self, episode_activity, reward):
		self.algorithm.train(episode_activity, reward)

	def get_V(self):
		self.algorithm.derive_V()
		return self.algorithm.V
		
	def get_P(self):
		self.algorithm.derive_P()
		return self.algorithm.P


class Dealer:
	def __init__(self, first_card=None):
		self.first_card = first_card
		self.sum = 0
		if first_card:
			self.add(first_card)

	def add(self, card):
		(color, num) = card
		if color == 'black':
			self.sum += num
		else:
			self.sum -= num

	def choose_action(self):
		if self.sum < 17:
			return 'hit'
		else:
			return 'stick'


class Environment:
	def __init__(self):
		pass
	
	def step(self, state, action_g):
		(dealer, gambler, _, _) = state
		
		if action_g == 'hit':
			terminal = False
			new_card = utils.draw()
			gambler.add(new_card)		
			reward = 0
		elif action_g == 'stick':
			terminal = True
			action_d = dealer.choose_action()
			while action_d == 'hit':				
				dealer.add(utils.draw())
				if utils.is_bust(dealer.sum):
					break
				action_d = dealer.choose_action()

			if utils.is_bust(dealer.sum):
				reward = +1
			elif gambler.sum > dealer.sum:
				reward = 1
			elif gambler.sum < dealer.sum:
				reward = -1
			elif gambler.sum == dealer.sum:
				reward = 0

		if utils.is_bust(gambler.sum):
			reward = -1
			terminal = True
		
				
		return(dealer, gambler, reward, terminal)
		
	

				
			
			
			
			
			
