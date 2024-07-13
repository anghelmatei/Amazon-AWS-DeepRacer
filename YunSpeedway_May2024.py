def reward_function(params):
    # Read input variables
    progress = params['progress']
    speed = params['speed']
    is_offtrack = params['is_offtrack']
    steps = params['steps']

    # Constants
    SPEED_THRESHOLD = 1.0
    MAX_SPEED_DIFF = 0.02
    TOTAL_NUM_STEPS = 300 
    
    # Initialize rewards
    on_track_reward = 0.0
    speed_reward = 0.0
    steps_reward = 0.0
    
    # Reward for progress and steps
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
        steps_reward = 1.0  # Normalized reward

    # Reward for keeping all wheels on track and speed
    if is_offtrack:
        on_track_reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        on_track_reward = 1e-3
    else:
        on_track_reward = 1.0

    # Speed reward
    speed_diff = abs(1.0 - speed)
    if speed_diff < MAX_SPEED_DIFF:
        speed_reward = 1 - (speed_diff / MAX_SPEED_DIFF) ** 2
    else:
        speed_reward = 1e-3
    
    # Combine rewards
    final_reward = on_track_reward + (speed_reward*25) + steps_reward

    return float(final_reward)