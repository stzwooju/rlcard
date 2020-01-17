from itertools import combinations

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.category = 0
        self.best = None
        self.best_index = None

        self.RANK_LOOKUP = "A23456789TJQK"
        self.RANK_TO_NUM = {'A': 12, '2': 11, '3': 10, '4': 9, '5': 8, '6': 7,
                            '7': 6, '8': 5, '9': 4, 'T': 3, 'J': 2, 'Q': 1, 'K': 0}

    def __str__(self):
        h = [card.get_index() for card in self.cards]
        b = [card.get_index() for card in self.best]
        return 'Cards : {}\nCategory: {}\nBest: {}\n'.format(', '.join(h), hex(self.category), ', '.join(b))

    def _sort_cards(self):
        self.cards = sorted(
            self.cards, key=lambda card: self.RANK_LOOKUP.index(card.rank))

    def evaluate_hand(self):
        card_cnt = len(self.cards)
        if card_cnt != 4:
            raise Exception(
                "There are not enough 4 cards in this hand, quit evaluation now ! ")

        self._sort_cards()

        for i in range(card_cnt):
            candidates = combinations(enumerate(self.cards), card_cnt - i)
            for candidate in candidates:
                candidate_cnt = len(candidate)
                valid = True

                for i in range(candidate_cnt):
                    if i == candidate_cnt - 1 or not valid:
                        break
                    for j in range(i + 1, candidate_cnt):
                        if candidate[i][1].suit == candidate[j][1].suit or candidate[i][1].rank == candidate[j][1].rank:
                            valid = False
                            break
                
                if valid:
                    self.best_index, self.best = zip(*candidate)
                    break
            if self.best is not None:
                break

        self.category = 0x10000 * len(self.best)

        base = 0x1000
        for b in reversed(self.best):
            self.category += base * self.RANK_TO_NUM[b.rank]
            base = int(base / 16)


def compare_hands(hands):
    hand_category = [] # such as high_card, straight_flush, etc
    all_players = [0] * len(hands) # all the players in this round, 0 for losing and 1 for winning or draw

    if None in hands:
        fold_players = [i for i, j in enumerate(hands) if j is None]
        if len(fold_players) == len(all_players) - 1:
            for _ in enumerate(hands):
                if _[0] in fold_players:
                    all_players[_[0]] = 0
                else:
                    all_players[_[0]] = 1
            return all_players
        else:
            for _ in enumerate(hands):
                if hands[_[0]] is not None:
                    hands[_[0]] = Hand(hands[_[0]])
                    hands[_[0]].evaluate_hand()
                    hand_category.append(hands[_[0]].category)
                elif hands[_[0]] is None:
                    hand_category.append(0)
    else:
        for i in enumerate(hands):
            hands[i[0]] = Hand(hands[i[0]])
            hands[i[0]].evaluate_hand()
            hand_category.append(hands[i[0]].category)

    winner_index = [i for i, j in enumerate(hand_category) if j == max(hand_category)]

    for i in winner_index:
        all_players[i] = 1

    return all_players


# Test
# if __name__ == '__main__':
#     from rlcard.utils.utils import init_standard_deck, get_random_cards

#     hands = []
#     for i in range(5):
#         deck = init_standard_deck()
#         cards, _ = get_random_cards(deck, 4)

#         hands.append(cards)

#     ret = compare_hands(hands)

#     print(ret)
