import copy
from numpy import np
#take in action and distance/presence of a human
#modify action if needed 
# return the modified action 

#used chat to help with slowing and stopping funcitons 

#handle chunks or single actions? 

def decide_mode(hand_distance, hand_detected): 
    if (hand_detected): 
        #figure out this number 
        if (hand_distance < 20): 
            return "stop"
        else: 
            return "slow"
    else: 
        return "normal"

def filter_action(action, observation, mode, previous_action=None): 
    if (mode == "stop"): 
        return {
            "action": copy.deepcopy(observation["observation.state"])
        }
    elif (mode == "slow"): 
        #code provided by chat 
        if previous_action is None:
            previous_action = { "action": copy.deepcopy(observation["observation.state"])}
        current = np.array(previous_action["action"], dtype=float)
        target = np.array(action["action"], dtype=float)
        #0.5 slow scale 
        slowed = current + 0.5 * (target - current)
        safe_action = {
            "action": slowed
        }
        return safe_action
    else: 
        return action 
