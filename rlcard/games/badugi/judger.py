from rlcard.games.badugi.utils import compare_hands

class BadugiJudger(object):
    ''' The Judger class for Badugi
    '''

    def __init__(self):
        ''' Initialize a judger class
        '''
        super().__init__()

    @staticmethod
    def judge_game(players, hands):
        ''' Judge the winner of the game.

        Args:
            players (list): The list of players who play the game
            hands (list): The list of hands that from the players

        Returns:
            (list): Each entry of the list corresponds to one entry of the
        '''
        winners = compare_hands(hands)
        print(winners)

        # Compute the total chips
        total = 0
        for p in players:
            total += p.in_chips

        print(total)

        each_win = float(total) / sum(winners)

        payoffs = []
        for i, _ in enumerate(players):
            if winners[i] == 1:
                payoffs.append(each_win - players[i].in_chips)
            else:
                payoffs.append(float(-players[i].in_chips))

        return payoffs
