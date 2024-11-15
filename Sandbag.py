# Sandbag.py
import math
class Sandbag:
    def __init__(self):
        self.vulnerable = 0  # vulnerableターン数を保持

    def apply_vulnerable(self, turns):
        """指定されたターン数だけvulnerable状態を追加"""
        self.vulnerable += turns

    def calculate_damage(self, damage):
        """vulnerable状態を考慮してダメージを計算"""
        if self.vulnerable > 0:
            return math.floor(damage * 1.5)
        return damage

    def end_turn(self):
        """ターン終了時にvulnerableの更新"""
        self.vulnerable = max(0, self.vulnerable - 1)
