# deskbot
I built an so101 leader and follower arm to do simple pick and place tasks. I wanted to expand the project into something more usable and interesting. I'm curious about human robot interaction and building robots that work with humans, so I decided to build this desk bot to work on my desk with me and do tasks such as cleaning it up. 

# Project Set Up 
- so101 arm attatched to table 
- top camera input  
- lerobot library 
- paper towel "trash"  
- bowl for "trashcan" 
- voice commands: "pick up trash", "stop", "reset" 

# Install 
brew install portaudio 
pip install -r requirements.txt

# Note on AI usage
- I used cursor to assist with implementation recommendations, errors, and debugging
- all code written by hand to learn and practice unless marked by a comment  

# Notable Features
Main control loop: voice → planner → PID align -> ACT pick-place → safety filter → send action 
- Voice controlled 
- Slows when human is present and stops if a person's hands are too close 
- Can handle multiple pieces of trash 

# File Structure 
- scripts 
    - testing bash scripts 
- src 
    - detection 
        - objdetect.py 
    - voice 
        - command.py 
    - main.py 
    - safetysupervisor.py 
    - skills.py
    - runpolicy.py (AI generated) - runs trained policy 
    - planner.py 
- tests (AI asistanced in creating these scripts)
    - movementtest.py - test joint control, controlled safe movment, and find optimal resting position 
    - testrunpolicy.py - tests running trained ACT policy with python code 
    - policysafetytest.py - used to test values between hand and robot head and then can also start policy, test the slowed down policy, uses the safteysupervisor  
    - voiceinputtest.py - tests commands using speech_recognition, tests queue, test microphone and also parse strings to validate
    - detectiontest.py - used to try different ways to detect objects, markers, camera input - tested yolo, aruco, color detection, pixel distance 
    - skillspidtest.py - pid movement test 
- armconfig
- configs 
- datasets
- models 
- notebooks 
    - google collab notebook
- requirements.txt 

# Dataset 
https://huggingface.co/datasets/Gracexu28/so101_desk_trash_merged 
- 60 episodes 

# Trained Model 
https://huggingface.co/Gracexu28/act_desk_trash
- ACT policy 
- 70% sucess rate 
- put in project locally to run it 

# Design Choices 
- Harness built to decide robot state and move robot to correct position, closest piece of trash, before running the ACT policy 
- Listening thread with command queue to be constantly listening for voice commands while not interrupting policies, camera detection, or main logic 
- Reset position allowed for robot to move towards trash just by rotating one motor which made motion control simpler and allowed for distance measurments using just the one top camera 
- All robot observation calls and actions sent to robot in main, other files help with logic, detection, action selection, but the action is always run through the safetysupervisor and sent to the robot in main
- Safety supervisor filters actions before being sent to the robot 

# Resource Links 
- so101 arm documentation: https://wiki.seeedstudio.com/lerobot_so100m/ 
- https://github.com/huggingface/lerobot 
- visualize dataset: https://huggingface.co/spaces/lerobot/visualize_dataset?path=%2FGracexu28%2Fso101_desk_trash_merged%2Fepisode_0
- so101 servo kit: https://www.amazon.com/dp/B0FH8CPXP7?lv=shuf&channelId=500&plpRedirect=mhFallback&th=1 


# Future Improvements 
- A way to verify a sucessful completed task to cleanly stop policy instead of using a set amount of time  
- Explicit state machine to make planner and main loop logic more clear 
- Improved, clean and consistent, data collection for improved policy preformance 
- Finetune custom YOLO classifier to handle more trash types 
- Instead of just stopping, move around the human if it is in the way 
- More precise motion planning using methods such as inverse kinematics 
- Do more tasks such as picking up objects and handing them to the person 

# Things I Tried (and why it failed)
- YOLO for trash detection: pretrained models don't have a useful "trash" / "paper towel" class, so detections were unreliable on the desk. Switched to white color + size filtering for paper towel trash.
- ArUco markers on the robot head: markers were too small in the top-down camera view and often failed to detect. Switched to a red marker + color detection for the robot head.
- Raising camera resolution / lowering YOLO confidence: helped a bit, but still not stable enough for the control loop, so color detection stayed.
- PID on horizontal pixel error (left/right in the image): the arm pans around the shoulder axis, so horizontal error didn't map cleanly to motor commands and the head often overshot or turned the wrong way. Switched to angular error around a calibrated shoulder pivot in the image.
- Running the ACT policy straight from Hugging Face: downloads / path / version mismatches made inference flaky. Kept a local copy under `models/act_desk_trash`.
- Aggressive joint targets from the policy or reset moves: LeRobot clamps relative motion (`max_relative_target`) and joint ranges, which looked like the robot "refusing" to move. Had to tune step size / relative limits instead of fighting the clamp.
- Relying only on the ACT policy to find trash: from arbitrary start poses it was inconsistent. Added the PID "go to trash" harness so the policy starts closer to a known approach.
