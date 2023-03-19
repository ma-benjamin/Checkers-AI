from game import Game
import random

LEARNING_RATE = 0.5
DISCOUNT_RATE = 0.9

  
def reward(game):
  q1 = game.get_score()
  game.change_turn()
  q2 = game.get_score()
  game.change_turn()
  return q1 - q2

class AI: 
  def __init__(self, learning_rate, discount_rate, random_move=0, game=None):
    self.lr = learning_rate
    self.dr = discount_rate
    self.rm = random_move
    self.game = game
    self.transitions = {}

    self.premove_state = None
    self.postmove_state = None

  def set_rmp(self, prob):
    self.rmp = prob

  def set_lr(self, lr):
    self.lr = lr

  def get_state(self, game):
    return game.get_state()

  def get_states(self, games):
    game_states = []
    for k in range(len(games)):
      game_states[k] = games[k].get_state()
    return game_states


  def get_transitions(self):
    start_of_transitions = {}
    max_value = float("-inf")
    min_value = float("inf")
    total_value = 0
    for k,v in self.transitions.items():
        if start_of_transitions.get(k[0]) is None:
            start_of_transitions.update({k[0]:0})
        if v > max_value:
            max_value = v
        if v < min_value:
            min_value = v
        total_value = total_value + v
    return [len(self.transitions), len(start_of_transitions), float(total_value/len(self.transitions)), max_value, min_value]
  
  def get_desired_transition(self, possible_states, initial_value = 10):
    current_state = tuple(self.get_states(self.game)[0])
    done_transitions = {}
    for state in possible_states:
      if done_transitions.get((current_state, tuple(state))) is None:
        if self.transitions((current_state, tuple(state))) is None:
          self.transitions.update({(current_state, tuple(state)):initial_value})
        done_transitions.update({(current_state, tuple(state)):self.transitions.get((current_state, tuple(state)))})
    
    if random != 0 and random.random() < self.rm:
      try:
        return list(done_transitions.keys())[random.randint(0, len(done_transitions)-1)]
      except:
        return []
      
    try:
      reverse_dict = {j:i for i,j in done_transitions.items()}
      return reverse_dict.get(max(reverse_dict))
    except:
      return []

  def get_optimal_potential(self):
    answer = float("-inf")
    current_state = tuple(self.get_states(self.game)[0])
    for k,v in self.transitions.items():
      if v > answer and k[0] == current_state:
        answer = v
    
    if answer == float("-inf"):
      return None
    return answer
  
  def get_potential_positions(possible_next_moves):
    potential_positions = []
    for move in possible_next_moves:
      game = Game()
      game.board.move(move)
      potential_positions.append(game)
    return potential_positions

  def get_next_move(self):
    if self.premove_state is not None:
      current_state = tuple(self.get_states(self.game)[0])
      transition = (self.premove_state, self.postmove_state)
      try:
        max_future_state = self.get_optimal_potential()
        self.transitions[transition] = self.transitions[transition] + self.lr * (reward(transition[0], current_state) + self.dr * max_future_state - self.transitions[transition])
      except:
        self.transitions[transition] = self.transitions[transition] + self.lr * (reward(transition[0], current_state))

    self.premove_state = self.get_states()

    possible_next_moves = self.game.get_possible_moves()
    possible_next_states = self.get_states(self.get_potential_positions(possible_next_moves))

    self.postmove_state = self.get_desired_transition(possible_next_states)[1]

    considered_moves = []
    for j in range(len(possible_next_states)):
      if tuple(possible_next_states[j]) == self.postmove_state:
        considered_moves.append(possible_next_moves[j])

    return considered_moves[random.randint(0, len(considered_moves)-1)]

    
