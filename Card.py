class Card:
    def __init__(self, name,card_type,cost=0, damage=0, vulnerable_turns=0, draw_num=0, display_name = "", usable=True):
        self.name = name
        #display_nameの指定が無い場合プログラムが使用するカード名を使う
        if display_name == "":
            self.display_name = name
        else:
            self.display_name = display_name
        self.cost = cost
        self.card_type = card_type  # attack, skill, power, curse
        self.damage = damage  # ダメージ（attackタイプのみ）
        self.vulnerable_turns = vulnerable_turns  # vulnerableターン数（攻撃時使用）
        self.draw_num = draw_num #ドロー数
        self.usable = usable #使用可能かどうか