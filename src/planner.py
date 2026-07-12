
#if trash detected (add voice command later), call skills that is move to trash 
#once on trash run trash picking up policy 
#if pen detected (and palm out and voice command), call skill that moves to pen 
#run pen picking up policy
#always return a word not actually do the action 

def next_action(trash_exists, command, on_trash): 
    if (command == "trash"): 
        if (trash_exists): 
            if (on_trash): 
                return "trash policy" 
            else: 
                return "go to trash"
        else: 
            return "no move"
    if (command == "stop"): 
        return "stop"
    if (command == "reset"): 
        return "reset"
    # elif (command == "pen"): 
    else: 
        return "no move"
            