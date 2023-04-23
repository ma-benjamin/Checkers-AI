import numpy as np
import tensorflow as tf
import random
import os
from .constants import ROWS, COLS, RED, WHITE
from .game import Game
from .board import Board

class model:
  def __init__(self):
    # Define the neural network model
    self.actions = []
    self.model = tf.keras.Sequential([
                    tf.keras.layers.Dense(64, activation='relu', input_shape=(64,)),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(len(self.actions), activation=None)
                  ])
    self.optimizer = tf.keras.optimizers.Adam()
    self.memory = [] # stores the model's experience in the form of transitions
                     # stored as (state, action, reward, new_state, done)

  # implementation for the reward function for the model
  def get_reward(board: list, action) -> int:
    reward = 0
    new_state = board.map_action(action)
    reward += new_state.get_score()
    
    return reward
  
  def loss_function(target_Q, predicted_Q):
    return tf.reduce_mean(tf.square(target_Q - predicted_Q))
  
  def train(self, num):

    batch_size = 32
    epsilon = 1.0
    epsilon_decay = 0.99
    discount_factor = 1

    for i in range(num):
      board = initialize_board() # i think we need to have a list
      done = False
      while not done:
        action = self.choose_action(board, epsilon)
        reward = self.get_reward(board, action)
        new_board = self.update_board(board, action)
        done = board.check_game_over() # we have winner function
        self.memory.append((board, action, reward, new_board))
        batch = random.sample(self.replay_memory, min(len(self.memory), batch_size))
        target_Q = self.calculate_target_Q(self.model, batch, discount_factor)
        predicted_Q = self.model(batch[:, 0])
        with tf.GradientTape() as tape:
          loss = self.loss_function(target_Q, predicted_Q)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        board = new_board
      epsilon = self.update_epsilon(epsilon, i, epsilon_decay)

  def initialize_board():
    return
  
  def choose_action(board, epsilon):
    return
  
  def update_board(board, action):
    return
  
  def calculate_target_Q(model, batch, discount_factor):
    return
  
  def update_epsilon(epsilon, episode, epsilon_decay):
    return


       





# # Define a function to play a game
# def play_game(model):
#   # Initialize the board
#   game = Game()

#   # Initialize variables to keep track of the game
#   turn = 1
#   game_over = False

#   # Play the game
#   while not game_over:
#     # Get the valid moves
#     valid_moves = game.get_possible_moves()

#     if valid_moves:
#       if game.turn == RED:
#         # Player's turn
#         if turn == 1:
#           print("Initial board:")
#           print(game.board)

#         # Get the player's move
#         move = None
#         while move not in valid_moves:
#           print(f"Player {game.turn}'s turn.")
#           x1 = int(input("Enter the row number of the piece you want to move: "))
#           y1 = int(input("Enter the column number of the piece you want to move: "))
#           x2 = int(input("Enter the row number of the square you want to move to: "))
#           y2 = int(input("Enter the column number of the square you want to move to: "))
#           move = (x1, y1, x2, y2)

#         # Apply the player's move
#         game.select((x1, y1))
#         game.select((x2, y2))

#         if turn == 1:
#           print("Player's move:")
#           print(game.board)

#       else:
#         # AI's turn
#         # Convert the board to a tensor
#         board_tensor = tf.convert_to_tensor(game.board.board.reshape((1, ROWS, COLS, 1)), dtype=tf.float32)

#         # Get the AI's move
#         predicted_value = model(board_tensor).numpy()[0][0]
#         valid_move_scores = {}
#         for move in valid_moves:
#             x1, y1, x2, y2 = move
#             new_board = np.copy(game.get_board())
#             new_board[x2, y2] = new_board[x1, y1]
#             new_board[x1, y1] = 0
#             if abs(x1 - x2) == 2:
#               x3 = (x1 + x2) // 2
#               y3 = (y1 + y2) // 2
#               new_board[x3, y3] = 0
#             move_tensor = tf.convert_to_tensor(new_board.reshape((1, ROWS, COLS, 1)), dtype=tf.float32)
#             score = model(move_tensor).numpy()[0][0]
#             valid_move_scores[move] = score
#         best_move = max(valid_move_scores, key=valid_move_scores.get)

#         # Apply the AI's move
#         game.apply_move(best_move)

#         if turn == 1:
#           print("AI's move:")
#           print(game.board)

#     else:
#       # No valid moves, game over
#       game_over = True
#       print("No valid moves, game over.")
#       if np.count_nonzero(game.board == 1) > np.count_nonzero(game.board == -1):
#           print("Player 1 wins!")
#       else:
#           print("Player -1 wins!")

#       # Increment the turn counter
#       turn += 1
#   return game.board

# # Define a function train the model against itself
# def train_model(model):
    # Initialize the board
    game = Game()

    # Play the game
    while True:
        # Get the valid moves for the current player
        valid_moves = game.get_possible_moves()

        # If there are no valid moves, the game is over
        if len(valid_moves) == 0:
            return opponent

        # Get the model's predicted value for each move
        values = []
        for move in valid_moves:
            new_board = game.map_move(move)
            flattened_board = np.reshape(new_board, (1, ROWS, COLS, 1))
            value = model.predict(flattened_board)
            values.append(value)
        values = np.array(values).flatten()

        # Choose the move with the highest predicted value
        best_move_index = np.argmax(values)
        best_move = valid_moves[best_move_index]

        # Apply the chosen move to the board
        game.select(best_move[0])
        game.select(best_move[1])

        # Switch the players
        player, opponent = opponent, player

        # Check if the game is over
        if game.winner() == WHITE:
            return -1
        elif game.winner() == RED:
            return 1
        
