# CardGame.py
import random, copy, math
from card_details import *
class CardGame:

    def __init__(self, deck, MAX_ENERGY, END_TURN_NUM, name=""):
        self.original_deck = deck
        self.MAX_ENERGY_ORIGINAL = MAX_ENERGY
        self.END_TURN_NUM = END_TURN_NUM
        self.name = name
        self.draw_pile = copy.deepcopy(self.original_deck)#山札
        self.MAX_ENERGY = self.MAX_ENERGY_ORIGINAL#最大エナジー
        random.shuffle(self.draw_pile)#山札をシャッフル
        self.hand = []#手札
        self.discard_pile = []#捨て札
        self.exhaust_pile = []#廃棄したカード
        self.energy = self.MAX_ENERGY#エナジー
        self.total_damage = 0#ダメージの合計
        self.p_block = 0#プレイヤーのブロック

        #バフデバフ(プレイヤー)
        self.p_strength = 0#プレイヤーの筋力
        self.double_tap = 0#ダブルタップ

        #バフデバフ(サンドバッグ)
        self.e_vulnerable = 0 
        self.turn_num = 1

def apply_vulnerable(game, turns):
    """指定されたターン数だけvulnerable状態を追加"""
    game.e_vulnerable += turns

def calculate_damage(game, damage):
    """vulnerable状態を考慮してダメージを計算"""
    if game.e_vulnerable > 0:
        return math.floor(damage * 1.5)
    return damage

def start_turn(game):
    game.energy = game.MAX_ENERGY
    draw_card(game, 5)

def draw_card(game, draw_num = 1):
    """指定した枚数分ドローする(指定が無ければ1ドロー)"""
    for _ in range(draw_num):
        #手札が10枚以上の場合何もしない
        if(len(game.hand) >= 10):
            return
        if not game.draw_pile:
            # 山札が空なら捨て札からシャッフルしてリセット
            if game.discard_pile:
                game.draw_pile = random.sample(game.discard_pile, len(game.discard_pile))
                game.discard_pile.clear()
            else:
                return 0  # デッキも捨て札も空ならドローできない
        card = game.draw_pile.pop()
        game.hand.append(card)

def add_card(game:CardGame, card, place:str):
    """指定したカードをplaceで指定した場所に追加する"""
    #手札
    if place == "hand":
        #手札が10枚以上なら捨て札に追加
        if(len(game.hand) >= 10):
            game.discard_pile.append(card)
        else:
            game.hand.append(card)
    #捨て札
    elif place == "discard_pile":
        game.discard_pile.append(card)
    #山札
    elif place == "draw_pile":
        game.draw_pile.insert(random.randint(0, len(game.draw_pile)), card)

def end_turn(game:CardGame):
    #敵に弱体があれば-1する
    if(game.e_vulnerable):
        game.e_vulnerable -=1
    #ダブルタップを0にする
    game.double_tap = 0
    #プレイヤーのブロックを0にする
    game.p_block = 0
    for card in game.hand[:]:
        if get_card_detail(card["name"], "Ethereal"):
            game.exhaust_pile.append(card)  # exhaust_pileに移動
    game.discard_pile.extend(game.hand)
    game.hand.clear()
    game.turn_num += 1

def use_card(game:CardGame, card:dict):
        if get_card_detail(card["name"],"usable") == False:
            return  #このカードは使用不可

        #エナジー確認   
        card_type = get_card_detail(card["name"], "card_type")
        card_name = card["name"]
        card_cost = card["cost"]
        if card_cost <= game.energy:
            game.energy -= card_cost

            # ダメージ計算
            damage = 0
            #カード情報取得
            
            #ダブルタップがあれば2回アタックを使用
            if card_type == 'attack':
                for _ in range(min(game.double_tap+1,2)):
                    #ボディスラム
                    if card_name in {"Body_Slam", "Body_Slam+"}:
                        card_damage = game.p_block
                    else:
                        card_damage = get_card_detail(card_name, "damage")
                    damage = calculate_damage(game,card_damage + game.p_strength)   
                    #焼身
                    if card_name in{"Immolate", "Immolate+"}:
                        add_card(game, {"name":"Burn", "cost":0}, place="discard_pile")
                    # カードにvulnerableターン数がある場合に適用
                    if get_card_detail(card_name, "vulnerable_turns") > 0:
                        apply_vulnerable(game,get_card_detail(card_name, "vulnerable_turns")) 
                    # ダメージの加算
                    game.total_damage += damage
                    #ブロック増加
                    game.p_block += get_card_detail(card_name, "block")
                    # カードを手札から捨て札へ移動
                    # カードの属性で同じものを削除
                    # ダブルタップで起動した2回目のカードにはこの効果を適用しない
                    if _ == 0:
                        for i, c in enumerate(game.hand):
                            if c["name"] == card_name and c["cost"] == card_cost:
                                del game.hand[i]
                                break
                        game.discard_pile.append(card)
                    else:
                        game.double_tap -=1
            elif card_type == 'skill':
                game.p_block += get_card_detail(card_name, "block")
                #やせ我慢の負傷2枚追加処理
                if card_name in {"Power_Through", "Power_Through+"}:
                    for _ in range(2):
                        add_card(game,{"name":"Wound","cost":0},place="hand")

                #ダブルタップ
                if card_name in {"Double_Tap", "Double_Tap+"}:
                    if card_name == "Double_Tap+":
                        game.double_tap += 1
                    game.double_tap += 1

                # カードを手札から捨て札へ移動
                # カードの属性で同じものを削除
                for i, c in enumerate(game.hand):
                    if c["name"] == card_name and c["cost"] == card_cost:
                        del game.hand[i]
                        break
                game.discard_pile.append(card)

            elif card_type == 'power':
                # Inflameカードを使ったときのstrength増加
                if card_name in {"Inflame","Inflame+"}:
                    if card_name =="Inflame+":
                        game.p_strength += 1
                    game.p_strength += 2  # strengthを2増加
                    # カードの属性で同じものを削除
                for i, c in enumerate(game.hand):
                    if c["name"] == card_name and c["cost"] == card_cost:
                        del game.hand[i]
                        break
            #カードドロー
            if get_card_detail(card_name, "draw_num"):
                draw_card(game,get_card_detail(card_name, "draw_num"))
