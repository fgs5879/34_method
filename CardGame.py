# CardGame.py
import random, copy
from collections import defaultdict
from Sandbag import Sandbag

class CardGame:

    def __init__(self, deck, MAX_ENERGY):
        self.original_deck = deck
        self.sandbag = Sandbag()
        self.MAX_ENERGY = MAX_ENERGY
        self.reset_game()

    def reset_game(self):
        self.deck = copy.deepcopy(self.original_deck)
        random.shuffle(self.deck)
        self.hand = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.energy = self.MAX_ENERGY
        self.total_damage = 0
        self.player_strength = 0
        self.card_usage_damage = defaultdict(int)
        self.turn_num = 1

    def start_turn(self):
        self.energy = self.MAX_ENERGY
        self.draw_card(5)

    def draw_card(self, draw_num = 1):
        #指定した枚数分ドローする(指定が無ければ1ドロー)
        for _ in range(draw_num):
            if not self.deck:
                # デッキが空なら捨て札からシャッフルしてリセット
                if self.discard_pile:
                    self.deck = random.sample(self.discard_pile, len(self.discard_pile))
                    self.discard_pile.clear()
                else:
                    return 0  # デッキも捨て札も空ならドローできない
            card = self.deck.pop()
            self.hand.append(card)

    def use_card(self, card):
        if card.usable == False:
            return  #このカードは使用不可

        if card.cost <= self.energy:
            self.energy -= card.cost

            # ダメージ計算
            damage = 0
            if card.card_type == 'attack':
                damage = self.sandbag.calculate_damage(card.damage + self.player_strength)  # 引数のsandbagで計算
                # vulnerableターン数がある場合、sandbagに適用
                if card.vulnerable_turns > 0:
                    self.sandbag.apply_vulnerable(card.vulnerable_turns)  # 引数のsandbagで適用
                # ダメージの加算
                self.total_damage += damage
                self.card_usage_damage[card.name] += damage

                # カードを手札から捨て札へ移動
                # カードの属性で同じものを削除
                for i, c in enumerate(self.hand):
                    if c.name == card.name and c.cost == card.cost and c.card_type == card.card_type:
                        del self.hand[i]
                        break
                self.discard_pile.append(card)
            elif card.card_type == 'skill':
                # カードを手札から捨て札へ移動
                # カードの属性で同じものを削除
                for i, c in enumerate(self.hand):
                    if c.name == card.name and c.cost == card.cost and c.card_type == card.card_type:
                        del self.hand[i]
                        break
                self.discard_pile.append(card)
            elif card.card_type == 'power':
                # Inflameカードを使ったときのstrength増加
                if card.name == "Inflame":
                    self.player_strength += 2  # strengthを2増加
                    # カードの属性で同じものを削除
                    for i, c in enumerate(self.hand):
                        if c.name == card.name and c.cost == card.cost and c.card_type == card.card_type:
                            del self.hand[i]
                            break
            #カードドロー
            if card.draw_num > 0:
                self.draw_card(card.draw_num)

    def end_turn(self):
        self.sandbag.end_turn()
        for card in self.hand[:]:
            if card.name == "Ascender's_Bane":
                self.hand.remove(card)
                self.exhaust_pile.append(card)  # exhaust_pileに移動
        self.discard_pile.extend(self.hand)
        self.hand.clear()
        self.turn_num += 1
