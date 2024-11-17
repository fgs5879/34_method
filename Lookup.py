import CardGame
from utilies import get_playable_cards, duplicate_game
import concurrent.futures
def lookup(game:CardGame, use_card, lookahead_end_turns):
    """
    ゲームの状態と選択されたカードを受け取り、
    選択されたカードが使用された場合のゲームをlookup_turnだけ先読みし、先読みの中で与えたダメージを返す。
    used_cardには"end_turn"という文字列が入ることがあり、その場合は使用できるカードがあるがターンエンドする。
    再帰関数である。
    """
    #選択をこのlookup内で実行
    #end_turnが選ばれた場合ターン終了する。lookahead_turnsを超えた場合、この推測での合計ダメージを返す。
    # print(game.turn_num, lookahead_end_turns, game.END_TURN_NUM)
    if use_card.name == "end_turn":
        game.end_turn()
        #終了条件
        if game.turn_num > lookahead_end_turns or game.turn_num > game.END_TURN_NUM:
            # print("end")
            return (game.total_damage, use_card)
        game.start_turn()
    #そのカードを使用してみる
    else:
        game.use_card(use_card)

    #使用可能カードリストを得る
    playable_cards = get_playable_cards(game.hand, game.energy)

    #それぞれの選択ごとにゲームの先読みし、先読み先で与えたダメージをlistに格納。最も効果が高い選択を推測する
    #len(playable_cards) <= 1だと、playable_cards = ["end_turn"]であり、ターンエンドするしかない
    # lookuped_damage_list = []
    # for played_card in playable_cards:
    #     simulated_game = duplicate_game(game)
    #     lookuped_damage_list.append((lookup(simulated_game, played_card, lookahead_end_turns)))
    lookuped_damage_list = []
    for played_card in playable_cards:
        simulated_game = duplicate_game(game)
        lookuped_damage_list.append((lookup(simulated_game, played_card, lookahead_end_turns)))
    max_damage, best_choice = max(lookuped_damage_list, key=lambda x: x[0])
    return (lookup(game, best_choice, lookahead_end_turns)[0], use_card)
        

        
