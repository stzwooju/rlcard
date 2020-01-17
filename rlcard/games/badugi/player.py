import random

from rlcard.utils.utils import init_standard_deck
from rlcard.games.badugi.utils import Hand

class BadugiPlayer(object):

    def __init__(self, player_id):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.player_id = player_id
        self.status = 'alive'

        self.deck = init_standard_deck()
        self.shuffle()

        self.hand = self.get_cards(4)

        # The chips that this player has put in until now
        self.in_chips = 0

    def get_state(self, all_chips, legal_actions):
        ''' Encode the state for the player

        Args:
            public_cards (list): A list of public cards that seen by all the players
            all_chips (int): The chips that all players have put in

        Returns:
            (dict): The state of the player
        '''
        state = {}
        state['hand'] = [c.get_index() for c in self.hand]
        state['all_chips'] = all_chips
        state['my_chips'] = self.in_chips
        state['legal_actions'] = legal_actions

        hand = Hand(self.hand)
        hand.evaluate_hand()

        state['hand_best_index'] = hand.best_index
        state['hand_category'] = hand.category

        return state

    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    def shuffle(self):
        ''' Shuffle the deck
        '''
        random.shuffle(self.deck)

    def get_cards(self, num):
        cards = []
        while num > 0:
            cards.append(self.deck.pop())
            num -= 1
        return cards
    
    def change_cards(self, idx):
        if idx is None:
            return self.hand

        idxs = idx.split(',')
        hand = self.hand.copy()
        for i in idxs:
            hand.remove(self.hand[int(i)])

        self.hand = hand + self.get_cards(len(idxs))

        return self.hand
