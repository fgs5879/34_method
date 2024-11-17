# カード情報を定義
DEFAULT_CARD_DETAILS = {
    "display_name": "Unknown",
    "card_type": "unknown",
    "damage": 0,
    "block": 0,
    "vulnerable_turns": 0,
    "cost": 0,
    "usable":True,
    "Ethereal":False,
    "draw_num":0
}
CARD_DETAILS = {
    # 既存のカード
    "Strike": {"display_name": "ストライク", "card_type": "attack", "damage": 6},
    "Defend": {"display_name": "防御", "card_type": "skill", "block": 5},
    "Bash": {"display_name": "強打", "card_type": "attack", "damage": 8, "vulnerable_turns": 2},
    
    # 新しいカード
    "Ascender's_Bane": {
        "display_name": "アセンダーの災厄", 
        "usable": False, 
        "card_type": "curse", 
        "Ethereal": True
    },
    
    "Power_Through": {
        "display_name": "やせ我慢", 
        "card_type": "skill", 
        "cost": 1, 
        "block": 15
    },
    
    "Hemokinesis": {
        "display_name": "ヘモキネシス", 
        "cost": 1, 
        "card_type": "attack", 
        "damage": 15
    },
    
    "Double_Tap+": {
        "display_name": "ダブルタップ+", 
        "card_type": "skill", 
        "cost": 1
    },
    
    "Iron_Wave": {
        "display_name": "アイアンウェーブ", 
        "cost": 1, 
        "card_type": "attack", 
        "damage": 5, 
        "block": 5
    },
    
    "Body_Slam+": {
        "display_name": "ボディスラム+", 
        "cost": 0, 
        "card_type": "attack"
    },
    
    "Carnage+": {
        "display_name": "大虐殺+", 
        "cost": 2, 
        "card_type": "attack", 
        "damage": 28, 
        "Ethereal": True
    },
    
    "Immolate+": {
        "display_name": "焼身+", 
        "cost": 2, 
        "card_type": "attack", 
        "damage": 28
    },
    
    "Pommel_Strike+": {
        "display_name": "ポンメルストライク+", 
        "cost": 1, 
        "card_type": "attack", 
        "damage": 10, 
        "draw_num": 2
    },
    
    "Inflame": {
        "display_name": "発火", 
        "cost": 1, 
        "card_type": "power"
    },
    
    "Inflame+": {
        "display_name": "発火+", 
        "cost": 1, 
        "card_type": "power"
    },
    
    "Wound":{
        "display_name":"負傷",
        "card_type":"status",
        "usable":False
    }
    ,
    "Burn":{
        "display_name":"火傷",
        "card_type":"status",
        "usable":False
    }
}


def get_card_detail(card_name, key):
    return CARD_DETAILS.get(card_name, {}).get(key, DEFAULT_CARD_DETAILS[key])