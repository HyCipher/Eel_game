# utils/logger.py
import os
from datetime import datetime

LOG_FILE = "game_log.txt"

def log_game_round(round_number, eel_side, captured_count, got_reward, eel_config):
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{time_str}] Round {round_number} | Side: {eel_side} | "
                f"Captured: {captured_count} | Reward: {got_reward} | "
                f"SlowFactor: {eel_config['slow_factor']} | "
                f"Growth: {eel_config['reward_growth_factor']} | "
                f"MaxProb: {eel_config['max_reward_probability']}\n")
