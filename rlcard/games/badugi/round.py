
class BadugiRound(object):

    def __init__(self, allowed_raise_num, num_players, seed_money):
        ''' Initilize the round class

        Args:
            num_players (int): The number of players
        '''
        self.start_pointer = None
        self.game_pointer = None
        self.allowed_raise_num = allowed_raise_num
        self.num_players = num_players
        self.seed_money = seed_money

        # Count the number of raise
        self.have_raised = 0
        self.died = 0

        # Count the number without raise
        # If every player agree to not raise, the round is over
        self.not_raise_num = 0

        # Raised amount for each player
        self.raised = [0 for _ in range(self.num_players)]
        self.raise_cnt = [0 for _ in range(self.num_players)]
        self.previous_action = [None for _ in range(self.num_players)]

        self.is_bet_round = False
        self.is_first = True

    def start_new_round(self, game_pointer, allowed_raise_num, raised=None):
        ''' Start a new bidding round

        Args:
            raised (list): Initialize the chips for each player

        '''
        self.start_pointer = game_pointer
        self.game_pointer = game_pointer

        self.allowed_raise_num = allowed_raise_num
        self.previous_bet = 0
        self.have_raised = 0
        self.not_raise_num = 0

        if raised:
            self.raised = raised
        else:
            self.raised = [0 for _ in range(self.num_players)]
        
        self.raise_cnt = [0 for _ in range(self.num_players)]
        self.previous_action = [None for _ in range(self.num_players)]

        self.is_bet_round = not self.is_bet_round
        self.is_first = True

    def proceed_round(self, players, action):
        if action not in self.get_legal_actions():
            raise Exception('{} is not legal action. Legal actions: {}'.format(action, self.get_legal_actions()))
        
        if self.is_bet_round:
            bet = 0
            if action == 'die':
                players[self.game_pointer].status = 'died'
                self.died += 1
            elif action == 'call':
                bet = max(self.raised) - self.raised[self.game_pointer]
            elif action == 'bbing':
                bet = self.seed_money - self.raised[self.game_pointer]
            elif action == 'ddadang':
                bet = self.previous_bet * 2 - self.raised[self.game_pointer]
            elif action == 'quarter':
                diff = max(self.raised) - self.raised[self.game_pointer]
                bet = round((sum(self.raised) + diff) * 0.25) + diff
            elif action == 'half':
                diff = max(self.raised) - self.raised[self.game_pointer]
                bet = round((sum(self.raised) + diff) * 0.5) + diff
            
            self.previous_bet = bet + self.raised[self.game_pointer]
            self.raised[self.game_pointer] += bet
            players[self.game_pointer].in_chips += bet
            self.previous_action[self.game_pointer] = action

            if action in ['call', 'check']:
                self.not_raise_num += 1
            elif action in ['bbing', 'ddadang', 'quarter', 'half']:
                self.raise_cnt[self.game_pointer] += 1
                self.have_raised += 1
                self.not_raise_num = 1
            
            self.is_first = self.is_first and (action == 'die')
        else:
            players[self.game_pointer].change_cards(action)
            self.is_first = False

        self.game_pointer = (self.game_pointer + 1) % self.num_players

        # Skip the folded players
        while players[self.game_pointer].status == 'died':
            self.game_pointer = (self.game_pointer + 1) % self.num_players

        return self.game_pointer

    def get_legal_actions(self):
        ''' Obtain the legal actions for the curent player

        Returns:
           (list):  A list of legal actions
        '''
        if self.is_bet_round:
            return self.get_bet_actions()
        else:
            return self.get_change_actions()
    
    def get_bet_actions(self):
        if self.is_first:
            actions = ['die', 'check', 'bbing']
        elif self.previous_action[self.game_pointer] == 'call' or \
             self.raise_cnt[self.game_pointer] >= self.allowed_raise_num:
            actions = ['die', 'call']
        elif self.previous_bet == 0:
            actions = ['die', 'call', 'quarter', 'half']
        else:
            actions = ['die', 'call', 'ddadang', 'quarter', 'half']
        return actions
    
    @staticmethod
    def get_change_actions():
        return [None, '0', '1', '2', '3', '0,1', '0,2', '0,3', '1,2', '1,3', '2,3', '0,1,2', '0,1,3', '0,2,3', '1,2,3', '0,1,2,3']

    def is_over(self):
        ''' Check whether the round is over

        Returns:
            (boolean): True if the current round is over
        '''
        if self.is_bet_round:
            return self.not_raise_num + self.died >= self.num_players
        else:
            return not self.is_first and self.game_pointer == self.start_pointer


# if __name__ == '__main__':
#     import numpy as np
#     from rlcard.games.badugi.player import BadugiPlayer as Player
    
#     players = [Player(i) for i in range(5)]
#     game_pointer = 0
#     r = BadugiRound(2, 5, 100)
#     r.start_new_round(game_pointer=game_pointer)
    
#     while not r.is_over():
#         legal_actions = r.get_legal_actions()
#         action = np.random.choice(legal_actions)
#         print(game_pointer, action, legal_actions)
#         game_pointer = r.proceed_round(players, action)
#         print(r.raised, r.have_raised, r.not_raise_num)

#     r.start_new_round(game_pointer = game_pointer)

#     while not r.is_over():
#         legal_actions = r.get_legal_actions()
#         action = np.random.choice(legal_actions)
#         print(game_pointer, action, legal_actions)
#         game_pointer = r.proceed_round(players, action)
#         print(r.raised, r.have_raised, r.not_raise_num)