import math

def reward_function(params):
    # Read input parameters
    is_offtrack = params['is_offtrack']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering_angle = params['steering_angle']

    # Constants
    SPEED_THRESHOLD = 1.0  
    TOTAL_NUM_STEPS = 650
    MAX_REWARD = 1e3
    MIN_REWARD = 1e-3
    ABS_STEERING_THRESHOLD = 15

    # Reward for staying on the track
    if is_offtrack:
        return MIN_REWARD

    # Calculate the optimal racing line reward
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)
    direction_diff = min(direction_diff, 360 - direction_diff)
    racing_line_reward = max(0.0, 1.0 - (direction_diff / 45.0))

    # Continuous speed reward
    speed_reward = max(MIN_REWARD, min(1.0, speed / SPEED_THRESHOLD))

    # Penalize excessive steering to encourage smooth driving
    abs_steering = abs(steering_angle)
    if abs_steering > ABS_STEERING_THRESHOLD:
        steering_penalty = 0.8
    else:
        steering_penalty = 1.0

    # Reward for progress and steps
    step_reward = 1.0
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
        step_reward += 10.0

    # Combine rewards
    final_reward = 10 * racing_line_reward + 20 * speed_reward * steering_penalty + step_reward

    # Ensure the reward is within the bounds
    final_reward = min(MAX_REWARD, max(MIN_REWARD, final_reward))

    return float(final_reward)
