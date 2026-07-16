# Reordered to make priority clear, stop should come first 
def next_action(trash_exists, command, on_trash, safety_mode): 
    if (command == "stop" or safety_mode == "stop"): 
        return "stop"
    if (command == "trash"): 
        if (trash_exists): 
            if (on_trash): 
                return "trash policy" 
            else: 
                return "go to trash"
        else: 
            return "no move"
    if (command == "reset"): 
        return "reset"
    # elif (command == "pen"): 
    else: 
        return "no move"
            