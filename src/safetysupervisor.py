#used chat to help with slowing and stopping funcitons 
#future improvement: handle chunks not single actions 

def decide_mode(hand_distance, hand_detected, distance_threshold): 
    if hand_detected and hand_distance is not None: 
        #figure out this number 
        if hand_distance < distance_threshold: 
            return "stop"
        else: 
            return "slow"
    else: 
        return "normal"

def filter_action(action, observation, mode, slow_factor, previous_action=None): 
    """Filter a LeRobot joint-position action dictionary. - chat generated"""
    if mode == "stop": 
        return {
            joint: float(observation[joint])
            for joint in action
        }
    elif mode == "slow": 
        safe_action = {}
        for joint, target in action.items():
            if previous_action is not None and joint in previous_action:
                current = previous_action[joint]
            else:
                current = observation[joint]
            safe_action[joint] = float(current + slow_factor * (target - current))
        return safe_action
    else: 
        return action 
