#他の自作pyファイルからimportされる関数を記述する
def get_playable_cards(hand, energy):
        
        """
        与えられた手札とエナジーに基づいて、使用可能なカードのリストを返す関数。
        """
        playable_cards = ["end_turn"]
        strike_cards = [card for card in hand if card.name == "Strike"]
        non_strike_cards = [card for card in hand if card.name != "Strike"]
        # 手札を一枚ずつ確認して、コストがエナジー以下のカードをリストに追加
        #ストライク以外に使用可能なカードが無いか確認
        for card in non_strike_cards:
            if card.usable == True and card.cost <= energy and card.name != "Defend":
                playable_cards.append(card)
        #ストライクしか使用可能カードが無い場合
        if len(playable_cards) == 1 and len(strike_cards) > 0:
            for card in strike_cards:
                if card.usable == True and card.cost <= energy:
                    playable_cards.append(card)
        return playable_cards