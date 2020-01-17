from copy import deepcopy, copy
from random import randrange
import numpy as np

from rlcard.games.badugi.player import BadugiPlayer as Player
from rlcard.games.badugi.judger import BadugiJudger as Judger
from rlcard.games.badugi.round import BadugiRound as Round

class BadugiGame(object):

    def __init__(self, allow_step_back=False):
        ''' Initialize the class limitholdem Game
        '''
        self.seed_money = 100
        self.allow_step_back = allow_step_back
        self.allowed_raise_num = 1
        self.num_players = 5
        self.round_num = 7
        self.history_raise_nums = [0 for _ in range(self.round_num)]

    def init_game(self):
        ''' Initialilze the game of Badugi

        Returns:
            (tuple): Tuple containing:

                (dict): The first state of the game
                (int): Current player's id
        '''

        # Initilize two players to play the game
        self.players = [Player(i) for i in range(self.num_players)]
        for i in range(self.num_players):
            self.players[i].in_chips += self.seed_money

        # Initialize a judger class which will decide who wins in the end
        self.judger = Judger()

        # Random player plays the first
        self.start_pointer = self.game_pointer = randrange(self.num_players)

        # Initilize a bidding round, in the first round, the big blind and the small blind needs to
        # be passed to the round for processing.
        self.round = Round(allowed_raise_num=self.allowed_raise_num,
                           num_players=self.num_players,
                           seed_money=self.seed_money)

        self.round.start_new_round(game_pointer=self.game_pointer,
                                   allowed_raise_num=self.allowed_raise_num,
                                   raised=[p.in_chips for p in self.players])

        # Count the round. There are 7 rounds in each game.
        self.round_counter = 0

        # Save the hisory for stepping back to the last state.
        self.history = []

        state = self.get_state(self.game_pointer)

        # Save betting history
        self.history_raise_nums = [0 for _ in range(self.round_num)]

        return state, self.game_pointer

    def step(self, action):
        ''' Get the next state

        Args:
            action (str): a specific action. (call, raise, fold, or check)

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''
        if self.allow_step_back:
            # First snapshot the current state
            r = deepcopy(self.round)
            b = self.game_pointer
            r_c = self.round_counter
            ps = deepcopy(self.players)
            rn = copy(self.history_raise_nums)
            self.history.append((r, b, r_c, ps, rn))

        # Then we proceed to the next round
        self.game_pointer = self.round.proceed_round(self.players, action)

        # Save the current raise num to history
        self.history_raise_nums[self.round_counter] = self.round.have_raised

        # If a round is over, we deal more public cards
        if self.round.is_over():
            self.round_counter += 1
            if self.round_counter >= 4:
                self.allowed_raise_num = 2
            self.round.start_new_round(game_pointer=self.game_pointer,
                                       allowed_raise_num=self.allowed_raise_num,
                                       raised=[p.in_chips for p in self.players])

        state = self.get_state(self.game_pointer)

        return state, self.game_pointer

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if len(self.history) > 0:
            self.round, self.game_pointer, self.round_counter, self.players, self.history_raises_nums = self.history.pop()
            return True
        return False

    def get_player_num(self):
        ''' Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    def get_action_num():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 4 actions (call, raise, check and fold)
        '''
        return len(self.get_legal_actions())

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.game_pointer

    def get_state(self, player):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        chips = [self.players[i].in_chips for i in range(self.num_players)]
        legal_actions = self.get_legal_actions()
        state = self.players[player].get_state(chips, legal_actions)
        state['raise_nums'] = self.history_raise_nums

        return state

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        alive_players = [1 if p.status=='alive' else 0 for p in self.players]
        # If only one player is alive, the game is over.
        if sum(alive_players) == 1:
            return True

        # If all rounds are finshed
        if self.round_counter >= self.round_num:
            return True
        return False

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        hands = [p.hand if p.status=='alive' else None for p in self.players]
        chips_payoffs = self.judger.judge_game(self.players, hands)
        payoffs = np.array(chips_payoffs)
        return payoffs

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''
        return self.round.get_legal_actions()

# Test the game

# if __name__ == "__main__":
#     game = BadugiGame()
#     print('New Game')
#     state, game_pointer = game.init_game()
#     print(game_pointer, state)
        
#     while not game.is_over():
#         legal_actions = game.get_legal_actions()
#         action = np.random.choice(legal_actions)
#         print(game_pointer, action, legal_actions)
#         state, game_pointer = game.step(action)
#         print(game_pointer, state)
    
#     print(game.get_payoffs())
