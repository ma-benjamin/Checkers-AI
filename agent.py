import torch
import random
import numpy as np
from collections import deque
from learning_bot import CheckersGameAI
from constants import RED, WHITE
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.09 # discount rate, must be < 1
        self.memory = deque(maxlen=MAX_MEMORY) #popleft()
        self.model = Linear_QNet() # TODO: input_size=32, hidden_size, output_size=32
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma) # TODO
        # TODO: model, trainer


    def get_state(self, game):
        state = [
            # number of pieces
            # number of opponent pieces
            # single jumps
            # double jumps
            # triple jumps
            # pieces on enemy side
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = None
        if random.randint(0, 200) < self.epsilon:
            final_move = None # random move assignment
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) # will execute forward function in model
            final_move = torch.argmax(prediction).item()

        return final_move
            
            

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = CheckersGameAI()
    while True:
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.select_square(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            #TODO: plot
            

if __name__ == '__main__':
    train()