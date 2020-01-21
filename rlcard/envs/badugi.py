import json
import os
import numpy as np

import rlcard
from rlcard.envs.env import Env
from rlcard.games.badugi.game import BadugiGame as Game
from rlcard.utils.utils import print_card

class BadugiEnv(Env):
    ''' Badugi Environment
    '''

    def __init__(self, allow_step_back=False):
        ''' Initialize the Badugi environment
        '''
        super().__init__(Game(allow_step_back), allow_step_back)

        self.actions = [
            'die', 'check', 'bbing', 'call', 'ddadang', 'quarter', 'half',
            None, '0', '1', '2', '3', '0,1', '0,2', '0,3', '1,2', '1,3', '2,3', '0,1,2', '0,1,3', '0,2,3', '1,2,3', '0,1,2,3'
        ]
        self.state_shape=[63]

        with open(os.path.join(rlcard.__path__[0], 'games/badugi/card2index.json'), 'r') as file:
            self.card2index = json.load(file)

    def get_legal_actions(self):
        ''' Get all leagal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        '''
        return self.game.get_legal_actions()

    def extract_state(self, state):
        ''' Extract the state representation from state dictionary for agent

        Note: Currently use the hand cards. TODO: encode the states

        Args:
            state (dict): Original state from the game

        Returns:
            observation (list): player's score
        '''
        processed_state = {}

        legal_actions = [self.actions.index(a) for a in state['legal_actions']]
        processed_state['legal_actions'] = legal_actions
        processed_state['hand_best_index'] = state['hand_best_index']
        processed_state['hand_category'] = hex(state['hand_category'])

        cards = state['hand']
        raise_nums = state['raise_nums']
        idx = [self.card2index[card] for card in cards]
        obs = np.zeros(63)
        obs[idx] = 1

        for i in state['hand_best_index']:
            obs[52 + i] = 1
        for i, num in enumerate(raise_nums):
            obs[56 + i] = num
        processed_state['obs'] = obs

        return processed_state

    def get_payoffs(self):
        ''' Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        '''
        return self.game.get_payoffs()

    def decode_action(self, action_id):
        ''' Decode the action for applying to the game

        Args:
            action id (int): action id

        Returns:
            action (str): action for the game
        '''
        legal_actions = self.game.get_legal_actions()
        if self.actions[action_id] not in legal_actions:
            if 'check' in legal_actions:
                return 'check'
            elif 'die' in legal_actions:
                return 'die'
            else:
                return None
        return self.actions[action_id]
