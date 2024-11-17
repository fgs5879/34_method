from card_details import CARD_DETAILS
class Card:
    def __init__(self, name,card_type,cost=0, damage=0, block = 0,vulnerable_turns=0, draw_num=0, display_name = "", usable=True, ethereal=False):
        self.name = name
        #display_nameの指定が無い場合プログラムが使用するカード名を使う
        if display_name == "":
            self.display_name = name
        else:
            self.display_name = display_name
        self.cost = cost
        self.card_type = card_type  # attack, skill, power, curse, status
        self.damage = damage  # ダメージ（attackタイプのみ）
        self.block = block #ブロック
        self.vulnerable_turns = vulnerable_turns  # vulnerableターン数（攻撃時使用）
        self.draw_num = draw_num #ドロー数
        self.usable = usable #使用可能かどうか
        self.ethereal = ethereal #エセリアル

def return_card(name, cost):
    details = CARD_DETAILS[name]
    return Card(name=name, cost=cost, **details)