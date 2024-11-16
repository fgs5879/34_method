# CardGame.py
import random, copy, math
from Card import Card

class CardGame:

    def __init__(self, deck, MAX_ENERGY, END_TURN_NUM):
        self.original_deck = deck
        self.MAX_ENERGY_ORIGINAL = MAX_ENERGY
        self.END_TURN_NUM = END_TURN_NUM
        self.reset_game()

    def reset_game(self):
        """戦闘開始前の状態を作る"""
        self.deck = copy.deepcopy(self.original_deck)#山札
        self.MAX_ENERGY = self.MAX_ENERGY_ORIGINAL#最大エナジー
        random.shuffle(self.deck)#山札をシャッフル
        self.hand = []#手札
        self.discard_pile = []#捨て札
        self.exhaust_pile = []#廃棄したカード
        self.energy = self.MAX_ENERGY#エナジー
        self.total_damage = 0#ダメージの合計

        #バフデバフ(プレイヤー)
        self.player_strength = 0#プレイヤーの筋力
        self.double_tap = 0#ダブルタップ

        #バフデバフ(サンドバッグ)
        self.e_vulnerable = 0 
        self.turn_num = 1

    def apply_vulnerable(self, turns):
        """指定されたターン数だけvulnerable状態を追加"""
        self.e_vulnerable += turns

    def calculate_damage(self, damage):
        """vulnerable状態を考慮してダメージを計算"""
        if self.e_vulnerable > 0:
            return math.floor(damage * 1.5)
        return damage
    def start_turn(self):
        self.energy = self.MAX_ENERGY
        self.draw_card(5)

    def draw_card(self, draw_num = 1):
        """指定した枚数分ドローする(指定が無ければ1ドロー)"""
        for _ in range(draw_num):
            #手札が10枚以上の場合何もしない
            if(len(self.hand) >= 10):
                return
            if not self.deck:
                # デッキが空なら捨て札からシャッフルしてリセット
                if self.discard_pile:
                    self.deck = random.sample(self.discard_pile, len(self.discard_pile))
                    self.discard_pile.clear()
                else:
                    return 0  # デッキも捨て札も空ならドローできない
            card = self.deck.pop()
            self.hand.append(card)
    def add_card(self, card):
        """指定したカードを手札に追加する(ドローではない)"""
        #手札が10枚以上なら捨て札に追加
        if(len(self.hand) >= 10):
            self.discard_pile.append(card)
        else:
            self.hand.append(card)
    def use_card(self, card):
        if card.usable == False:
            return  #このカードは使用不可

        #エナジー確認    
        if card.cost <= self.energy:
            self.energy -= card.cost

            # ダメージ計算
            damage = 0
            #ダブルタップがあれば2回アタックを使用
            
            if card.card_type == 'attack':
                for _ in range(min(self.double_tap+1,2)):
                    damage = self.calculate_damage(card.damage + self.player_strength) 
                    # カードにvulnerableターン数がある場合に適用
                    if card.vulnerable_turns > 0:
                        self.apply_vulnerable(card.vulnerable_turns) 
                    # ダメージの加算
                    self.total_damage += damage

                    # カードを手札から捨て札へ移動
                    # カードの属性で同じものを削除
                    # ダブルタップで起動した2回目のカードにはこの効果を適用しない
                    if _ == 0:
                        for i, c in enumerate(self.hand):
                            if c.name == card.name and c.cost == card.cost and c.card_type == card.card_type:
                                del self.hand[i]
                                break
                        self.discard_pile.append(card)
                    else:
                        self.double_tap -=1
            elif card.card_type == 'skill':
                #やせ我慢の負傷2枚追加処理
                if card.name == "Power_Through" or card.name == "Power_Through+":
                    wound = Card("Wound",display_name="負傷",card_type="status",usable=False)
                    for _ in range(2):
                        self.add_card(wound)

                #ダブルタップ
                if card.name == "Double_Tap" or card.name == "Double_Tap+":
                    if card.name == "Double_Tap":
                        self.double_tap += 1
                    else:
                        self.double_tap += 2

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
        #敵に弱体があれば-1する
        if(self.e_vulnerable):
            self.e_vulnerable -=1
        #ダブルタップを0にする
        self.double_tap = 0
        for card in self.hand[:]:
            if card.ethereal:
                self.exhaust_pile.append(card)  # exhaust_pileに移動
        self.discard_pile.extend(self.hand)
        self.hand.clear()
        self.turn_num += 1
