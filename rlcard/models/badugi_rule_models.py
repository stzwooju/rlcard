''' Badugi rule models
'''

import numpy as np

import rlcard
from rlcard.models.model import Model

class BadugiRuleAgentV1(object):
    ''' Badugi Rule agent version 1
    '''

    def __init__(self):
        self.actions = [
            'die', 'check', 'bbing', 'call', 'ddadang', 'quarter', 'half',
            None, '0', '1', '2', '3', '0,1', '0,2', '0,3', '1,2', '1,3', '2,3', '0,1,2', '0,1,3', '0,2,3', '1,2,3', '0,1,2,3'
        ]

    def step(self, state):
        ''' Predict the action given raw state.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''

        hand_best_index = state['hand_best_index']
        hand_category = state['hand_category']
        round_counter = state['round_counter']

        if state['is_bet']:
            legal_actions = state['legal_actions']
            if hand_category >= 0x66000: # 메이드 7 이상
                order = ['half', 'quarter', 'ddadang', 'bbing', 'check', 'call', 'die']
            elif hand_category >= 0x63000: # 메이드 10 이상
                order = ['quarter', 'ddadang', 'bbing', 'check', 'call', 'die']
            elif hand_category >= 0x60000: # 메이드
                order = ['bbing', 'check', 'call', 'die']
            elif hand_category >= 0x48000 or round_counter < 4: # 베이스 5 이상이거나 점심 지나기 전까지는 기본 베팅만 하면서 손패 바꾸기
                order = ['check', 'call', 'die']
            else: # 베이스 5 미만 또는 투베이스 이하의 경우에는 다이
                order = ['die']
            
            for o in order:
                idx = self.actions.index(o)
                if idx in legal_actions:
                    return idx
        else:
            action = []
            for i in range(4):
                if i not in hand_best_index:
                    action.append(i)
            a = ','.join(map(str, action)) if action else None
            return self.actions.index(a)

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state)


class BadugiRuleModelV1(Model):
    ''' Badugi Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('badugi')

        rule_agent = BadugiRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True



