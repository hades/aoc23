import collections

from .solver import Solver

_FIVE_OF_A_KIND  = 0x100000
_FOUR_OF_A_KIND  = 0x010000
_FULL_HOUSE      = 0x001000
_THREE_OF_A_KIND = 0x000100
_TWO_PAIR        = 0x000010
_ONE_PAIR        = 0x000001

_CARD_ORDER            = '23456789TJQKA'
_CARD_ORDER_WITH_JOKER = 'J23456789TQKA'

def evaluate_hand(hand: str, joker: bool = False) -> int:
  card_counts = collections.defaultdict(int)
  score = 0
  for card in hand:
    card_counts[card] += 1
  joker_count = 0
  if joker:
    joker_count = card_counts['J']
    del card_counts['J']
  counts = sorted(card_counts.values(), reverse=True)
  top_non_joker_count = counts[0] if counts else 0
  if top_non_joker_count + joker_count == 5:
    score |= _FIVE_OF_A_KIND
  elif top_non_joker_count + joker_count == 4:
    score |= _FOUR_OF_A_KIND
  elif top_non_joker_count + joker_count == 3:
    match counts, joker_count:
      case [3, 2], 0:
        score |= _FULL_HOUSE
      case [3, 1, 1], 0:
        score |= _THREE_OF_A_KIND
      case [2, 2], 1:
        score |= _FULL_HOUSE
      case [2, 1, 1], 1:
        score |= _THREE_OF_A_KIND
      case [1, 1, 1], 2:
        score |= _THREE_OF_A_KIND
      case _:
        raise RuntimeError(f'Unexpected card counts: {counts} with {joker_count} jokers')
  elif top_non_joker_count + joker_count == 2:
    match counts, joker_count:
      case [2, 2, 1], 0:
        score |= _TWO_PAIR
      case [2, 1, 1, 1], 0:
        score |= _ONE_PAIR
      case [1, 1, 1, 1], 1:
        score |= _ONE_PAIR
      case _:
        raise RuntimeError(f'Unexpected card counts: {counts} with {joker_count} jokers')
  card_order = _CARD_ORDER_WITH_JOKER if joker else _CARD_ORDER
  for card in hand:
    card_value = card_order.index(card)
    score <<= 4
    score |= card_value
  return score

class Day07(Solver):

  def __init__(self):
    super().__init__(7)
    self.hands: list[tuple[str, str]] = []

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    self.hands = [tuple(line.split(' ')) for line in lines]

  def solve_first_star(self):
    hands = self.hands[:]
    hands.sort(key=lambda hand: evaluate_hand(hand[0]))
    total_score = 0
    for rank, [_, bid] in enumerate(hands):
      total_score += (rank + 1) * int(bid)
    return total_score

  def solve_second_star(self):
    hands = self.hands[:]
    hands.sort(key=lambda hand: evaluate_hand(hand[0], True))
    total_score = 0
    for rank, [_, bid] in enumerate(hands):
      total_score += (rank + 1) * int(bid)
    return total_score

# vim: ts=2:sw=2:et
