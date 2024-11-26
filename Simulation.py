# Simulation.py
import statistics,time,tqdm,matplotlib.pyplot as plt
from Lookup import lookup
from utilies import get_playable_cards, duplicate_game
from CardGame import *
from card_details import *
import concurrent.futures
def comparison(games:list[CardGame],trials:int,lookahead_turns:int):
    battle_logs = []
    each_trial_damage_lists = []
    for game in games:
        battle_log, each_trial_damage_list = concurrent_full_search(game,trials,lookahead_turns)
        battle_logs.append(battle_log)
        each_trial_damage_lists.append(each_trial_damage_list)
    return battle_logs, each_trial_damage_lists
def concurrent_full_search(game: CardGame, trials: int, lookahead_turns: int):
    """並列処理を行い、battle_logsとeach_trial_damage_listを返す"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(full_search_trial, game, trial, lookahead_turns)
            for trial in range(trials)
        ]
        
        battle_logs = []
        each_trial_damage_list = []
        
        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing trials"):
            result = future.result()
            battle_logs.append(result[0])  # 各試行のログ
            each_trial_damage_list.append(result[1])  # 各試行のターンごとのダメージリスト
    
    return battle_logs, each_trial_damage_list
         
def full_search_trial(game:CardGame, trial:int, lookahead_turns:int):
    random.shuffle(game.draw_pile)
    #統計用に各ターンごとに与えたダメージの合計を記録
    each_turn_damage_list = []
    #ログ記録用のリスト
    log_lines = []        
    log_lines.append(f"=== 1 ターン目開始===\n")
    
    start_turn(game)
    
    #指定ターン超過までwhileループし戦闘継続
    while game.turn_num <= game.END_TURN_NUM:
        #手札表示
        log_lines.append("\n手札: " + ", ".join([get_card_detail(card["name"],"display_name") for card in game.hand]))
        #使用可能カードのリスト取得(end_turnを含む)
        playable_cards = get_playable_cards(game.hand, game.energy)
        #それぞれの選択ごとにゲームの先読みし、先読み先で与えたダメージをlistに格納。最も効果が高い選択を推測する
        #len(playable_cards) <= 1だと、playable_cards = はエンドターンだけであり、ターンエンドするしかない
        lookuped_damage_list = []
        #それぞれの選択ごとにゲームの先読みをする。
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(lookup, duplicate_game(game), played_card, lookahead_turns+game.turn_num)
                for played_card in playable_cards
                ]
            lookuped_damage_list = [future.result() for future in futures]
        #lookuped_damageの出力
        # for l, j in lookuped_damage_list:
        #     if(j  == "end_turn"):
        #         log_lines.append(str(l)+":"+str(j))
        #     else:
        #         log_lines.append(str(l)+":"+str(j.display_name))
        # log_lines.append("\n")
        max_damage, best_choice = max(lookuped_damage_list, key=lambda x: x[0])
        # 'best_choice'を実行する
        if best_choice["name"] == "end_turn":
            each_turn_damage_list.append(game.total_damage)
            end_turn(game)
            if game.turn_num > game.END_TURN_NUM:
                log_lines.append(f"\n=== 試行 {trial+1} 回目終了===\n与えた合計ダメージ:{game.total_damage}\n--------------------------------------\n")
            else:
                log_lines.append(f"\n\n==={game.turn_num}ターン目開始===")  # ターン終了を記録
                start_turn(game)
                log_lines.append(f"\n=== これまでのダメージ:{game.total_damage}===")
                if(game.e_vulnerable>0):
                    log_lines.append(f"\n=== 弱体:{game.e_vulnerable}===")
                if(game.p_strength>0):
                    log_lines.append(f"\n=== 筋力:{game.p_strength}===")
                
        else:
            log_lines.append(f"\n使用: {get_card_detail(best_choice['name'], 'display_name')}")  # 使用したカードの名前を記録
            use_card(game,best_choice)
    return (log_lines, each_turn_damage_list)

