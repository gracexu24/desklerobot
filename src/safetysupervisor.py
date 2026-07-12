#take in action and distance/presence of a human
#modify action if needed 
# return the modified action 

#used chat to help with slowing and stopping funcitons 

#handle chunks or single actions? 

def decide_mode(hand_distance, hand_detected): 
    if hand_detected and hand_distance is not None: 
        #figure out this number 
        if hand_distance < 20: 
            return "stop"
        else: 
            return "slow"
    else: 
        return "normal"

def filter_action(action, observation, mode, previous_action=None): 
    """Filter a LeRobot joint-position action dictionary. - chat generated"""
    if mode == "stop": 
        return {
            joint: float(observation[joint])
            for joint in action
        }

    if mode == "slow": 
        safe_action = {}
        for joint, target in action.items():
            if previous_action is not None and joint in previous_action:
                current = previous_action[joint]
            else:
                current = observation[joint]

            safe_action[joint] = float(current + 0.5 * (target - current))

        return safe_action

    return action 
