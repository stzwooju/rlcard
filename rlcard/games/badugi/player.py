import random

from rlcard.utils.utils import init_standard_deck

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

    def get_state(self, public_cards, all_chips, legal_actions):
        ''' Encode the state for the player

        Args:
            public_cards (list): A list of public cards that seen by all the players
            all_chips (int): The chips that all players have put in

        Returns:
            (dict): The state of the player
        '''
        state = {}
        # state['hand'] = [c.get_index() for c in self.hand]
        # state['public_cards'] = [c.get_index() for c in public_cards]
        # state['all_chips'] = all_chips
        # state['my_chips'] = self.in_chips
        # state['legal_actions'] = legal_actions
        return state

    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    def shuffle(self):
        ''' Shuffle the deck
        '''
        random.shuffle(self.deck)

    def get_cards(num):
        cards = []
        while num > 0:
            cards.append(self.deck.pop())
            num -= 1
        return cards
    
    def change_cards(idx):
        if idx is None:
            return self.hand

        idxs = idx.split(',')
        for i in idxs:
            del self.hand[i]
        self.hand += self.get_cards(len(idxs))

        return self.hand
