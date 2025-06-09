import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"logs/log_{timestamp}.txt"

def log_game_round(round_number, eel_side, captured_count, got_reward, eel_config, swapped):
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{time_str}] Round {round_number} | Side: {eel_side} | "
                f"Captured: {captured_count} | Reward: {got_reward} | "
                f"SlowFactor: {eel_config['slow_factor']} | "
                f"Growth: {eel_config['reward_growth_factor']} | "
                f"MaxProb: {eel_config['max_reward_probability']} | "
                f"Swapped: {swapped}\n")
