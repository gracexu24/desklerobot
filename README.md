# desklerobot

# project 


notes: 
- all code written by hand to learn and practice unless marked by a coment 

# data 

# need this 
brew install portaudio 

# parts 

# AI usage

- used cursor to assist with errors and debugging

# Records

7/9: 
- tested camera detection, running policy with python, and moving the robot joints
- issues: trained policy struggled to run (had to download locally), robot motor broke, camera is unable to detect trash on table or aruco tags, certain join positions stopped by lerobot for safety
- test fixes: increase camera resolution, lower confidence threshhold, use different yolo model, maybe try just white color? 

Put the fugging face policy locally 

Write design decisions 

Write how I built this 

7/15: 
- python -m pip install "mediapipe==0.10.21" "numpy==1.26.4" \
  "opencv-python==4.11.0.86" \
  "opencv-contrib-python==4.11.0.86" \
  "opencv-python-headless==4.11.0.86"

Main robot config lacks relative motion limits, loop-rate control, and robust emergency/fault handling.

I tested just white bc yolo cant detect properlly 
Things i need to test: 
-camera - detection
-movement
- boice 

-calibrated resting position
- additional testing code 

- i like the additional controls 

-     'wrist_roll': {   'original goal_pos': 89.53075408935547,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 8.996175765991211,
                         'safe goal_pos': 14.372160264353582},
    'wrist_flex': {   'original goal_pos': 64.99324035644531,
                      'safe goal_pos': 68.61111111111111},
    'wrist_roll': {   'original goal_pos': 90.61540985107422,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 11.18256950378418,
                         'safe goal_pos': 14.372160264353582},
    'wrist_flex': {   'original goal_pos': 63.313873291015625,
                      'safe goal_pos': 68.39743589743591},
    'wrist_roll': {   'original goal_pos': 90.70844268798828,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 10.234132766723633,
                         'safe goal_pos': 14.04171829822387},
    'shoulder_pan': {   'original goal_pos': 80.2197265625,
                        'safe goal_pos': 80.01312335958005},
    'wrist_flex': {   'original goal_pos': 56.59815979003906,
                      'safe goal_pos': 67.43589743589746},
    'wrist_roll': {   'original goal_pos': 91.71285247802734,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 10.598836898803711,
                         'safe goal_pos': 13.628665840561752},
    'wrist_flex': {   'original goal_pos': 57.67157745361328,
                      'safe goal_pos': 65.94017094017093},
    'wrist_roll': {   'original goal_pos': 91.4839859008789,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 10.323358535766602,
                         'safe goal_pos': 13.298223874432054},
    'wrist_flex': {   'original goal_pos': 57.50341796875,
                      'safe goal_pos': 64.87179487179486},
    'wrist_roll': {   'original goal_pos': 91.52841186523438,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 9.93229866027832,
                         'safe goal_pos': 13.050392399834763},
    'wrist_flex': {   'original goal_pos': 49.49394226074219,
                      'safe goal_pos': 63.69658119658121},
    'wrist_roll': {   'original goal_pos': 92.40849304199219,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 11.336202621459961,
                         'safe goal_pos': 12.719950433705094},
    'wrist_flex': {   'original goal_pos': 53.62873077392578,
                      'safe goal_pos': 62.52136752136752},
    'wrist_roll': {   'original goal_pos': 91.84809875488281,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 10.310869216918945,
                         'safe goal_pos': 12.224287484510526},
    'wrist_flex': {   'original goal_pos': 51.41883087158203,
                      'safe goal_pos': 61.23931623931625},
    'wrist_roll': {   'original goal_pos': 92.07704162597656,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 10.713125228881836,
                         'safe goal_pos': 11.893845518380829},
    'wrist_flex': {   'original goal_pos': 51.76342010498047,
                      'safe goal_pos': 59.74358974358972},
    'wrist_roll': {   'original goal_pos': 92.17715454101562,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 16.37349510192871,
                   'safe goal_pos': 13.919270833333332},
    'shoulder_lift': {   'original goal_pos': 10.842660903930664,
                         'safe goal_pos': 11.728624535315987},
    'wrist_flex': {   'original goal_pos': 45.142059326171875,
                      'safe goal_pos': 58.78205128205127},
    'wrist_roll': {   'original goal_pos': 93.06803131103516,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 18.100914001464844,
                   'safe goal_pos': 14.440104166666668},
    'shoulder_lift': {   'original goal_pos': 10.447649002075195,
                         'safe goal_pos': 11.315572077653854},
    'wrist_flex': {   'original goal_pos': 43.44613265991211,
                      'safe goal_pos': 57.606837606837615},
    'wrist_roll': {   'original goal_pos': 93.30036926269531,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 10.092935562133789,
                         'safe goal_pos': 11.067740603056578},
    'wrist_flex': {   'original goal_pos': 46.419921875,
                      'safe goal_pos': 56.43162393162393},
    'wrist_roll': {   'original goal_pos': 92.99958801269531,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 16.545984268188477,
                   'safe goal_pos': 16.263020833333332},
    'shoulder_lift': {   'original goal_pos': 10.265069961547852,
                         'safe goal_pos': 10.572077653862038},
    'wrist_flex': {   'original goal_pos': 41.688232421875,
                      'safe goal_pos': 55.25641025641028},
    'wrist_roll': {   'original goal_pos': 93.57160186767578,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 17.86248207092285,
                   'safe goal_pos': 17.6953125},
    'shoulder_lift': {   'original goal_pos': 9.755910873413086,
                         'safe goal_pos': 10.324246179264776},
    'wrist_flex': {   'original goal_pos': 40.114078521728516,
                      'safe goal_pos': 53.97435897435898},
    'wrist_roll': {   'original goal_pos': 93.97964477539062,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'wrist_flex': {   'original goal_pos': 39.69120788574219,
                      'safe goal_pos': 52.799145299145295},
    'wrist_roll': {   'original goal_pos': 93.98021697998047,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 10.26531982421875,
                   'safe goal_pos': 10.364583333333334},
    'wrist_flex': {   'original goal_pos': 39.46022033691406,
                      'safe goal_pos': 51.730769230769226},
    'wrist_roll': {   'original goal_pos': 94.21958923339844,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 10.458697319030762,
                   'safe goal_pos': 10.8203125},
    'wrist_flex': {   'original goal_pos': 39.335479736328125,
                      'safe goal_pos': 50.448717948717956},
    'wrist_roll': {   'original goal_pos': 94.3526840209961,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'gripper': {   'original goal_pos': 9.045065879821777,
                   'safe goal_pos': 10.104166666666666},
    'shoulder_lift': {   'original goal_pos': 9.082735061645508,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 38.103355407714844,
                      'safe goal_pos': 49.27350427350427},
    'wrist_roll': {   'original goal_pos': 94.71263885498047,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'wrist_flex': {   'original goal_pos': 37.11335754394531,
                      'safe goal_pos': 48.205128205128204},
    'wrist_roll': {   'original goal_pos': 94.87263488769531,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 8.465875625610352,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 38.33153533935547,
                      'safe goal_pos': 46.923076923076906},
    'wrist_roll': {   'original goal_pos': 94.97956848144531,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 9.124181747436523,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 37.958984375,
                      'safe goal_pos': 45.854700854700866},
    'wrist_roll': {   'original goal_pos': 95.06884765625,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 8.48957633972168,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 38.421424865722656,
                      'safe goal_pos': 44.57264957264957},
    'wrist_roll': {   'original goal_pos': 95.07386779785156,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 8.254781723022461,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 38.36753463745117,
                      'safe goal_pos': 43.5042735042735},
    'wrist_roll': {   'original goal_pos': 95.12470245361328,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 8.266374588012695,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 39.20914077758789,
                      'safe goal_pos': 42.22222222222223},
    'wrist_roll': {   'original goal_pos': 95.08867645263672,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 7.83656120300293,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 39.78113555908203,
                      'safe goal_pos': 41.15384615384613},
    'wrist_roll': {   'original goal_pos': 95.14086151123047,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 6.705617904663086,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.1172103881836,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 6.816766738891602,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.17393493652344,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 6.605104446411133,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.20489501953125,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 5.68548583984375,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.19428253173828,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 4.744462966918945,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.22392272949219,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 4.9538726806640625,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.23698425292969,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': 3.3982677459716797,
                         'safe goal_pos': 9.58075175547296},
    'wrist_roll': {   'original goal_pos': 95.27424621582031,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': -0.14896392822265625,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 51.2756233215332,
                      'safe goal_pos': 49.017094017094024},
    'wrist_roll': {   'original goal_pos': 95.3512954711914,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': -2.8061676025390625,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 54.38594055175781,
                      'safe goal_pos': 49.97863247863248},
    'wrist_roll': {   'original goal_pos': 95.36974334716797,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'shoulder_lift': {   'original goal_pos': -6.61060905456543,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 56.765777587890625,
                      'safe goal_pos': 51.581196581196565},
    'wrist_roll': {   'original goal_pos': 95.40814971923828,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 13.438253402709961,
                      'safe goal_pos': 8.700401248328134},
    'shoulder_lift': {   'original goal_pos': -15.219216346740723,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 62.50354766845703,
                      'safe goal_pos': 52.97008547008548},
    'wrist_roll': {   'original goal_pos': 95.41293334960938,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 13.135515213012695,
                      'safe goal_pos': 10.394560855996431},
    'shoulder_lift': {   'original goal_pos': -16.076496124267578,
                         'safe goal_pos': 9.58075175547296},
    'wrist_flex': {   'original goal_pos': 64.96456909179688,
                      'safe goal_pos': 54.25213675213675},
    'wrist_roll': {   'original goal_pos': 95.4204330444336,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 26.29233169555664,
                      'safe goal_pos': 12.267053053945617},
    'shoulder_lift': {   'original goal_pos': -32.11817932128906,
                         'safe goal_pos': 9.58075175547296},
    'shoulder_pan': {   'original goal_pos': 75.91307830810547,
                        'safe goal_pos': 80.3018372703412},
    'wrist_flex': {   'original goal_pos': 71.26392364501953,
                      'safe goal_pos': 55.854700854700866},
    'wrist_roll': {   'original goal_pos': 95.4028091430664,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 28.17537498474121,
                      'safe goal_pos': 13.87204636647347},
    'shoulder_lift': {   'original goal_pos': -34.64687728881836,
                         'safe goal_pos': 9.58075175547296},
    'shoulder_pan': {   'original goal_pos': 75.90049743652344,
                        'safe goal_pos': 79.7769028871391},
    'wrist_flex': {   'original goal_pos': 72.48419952392578,
                      'safe goal_pos': 57.02991452991452},
    'wrist_roll': {   'original goal_pos': 95.39177703857422,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 33.045345306396484,
                      'safe goal_pos': 15.744538564422655},
    'shoulder_lift': {   'original goal_pos': -40.85784149169922,
                         'safe goal_pos': 9.58075175547296},
    'shoulder_pan': {   'original goal_pos': 71.33645629882812,
                        'safe goal_pos': 78.72703412073491},
    'wrist_flex': {   'original goal_pos': 74.80240631103516,
                      'safe goal_pos': 58.52564102564102},
    'wrist_roll': {   'original goal_pos': 95.39290618896484,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 33.08409881591797,
                      'safe goal_pos': 17.43869817209095},
    'shoulder_lift': {   'original goal_pos': -40.137603759765625,
                         'safe goal_pos': 9.58075175547296},
    'shoulder_pan': {   'original goal_pos': 73.7928237915039,
                        'safe goal_pos': 77.25721784776903},
    'wrist_flex': {   'original goal_pos': 73.94757080078125,
                      'safe goal_pos': 59.91452991452991},
    'wrist_roll': {   'original goal_pos': 95.4192123413086,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 36.061546325683594,
                      'safe goal_pos': 19.222024074899693},
    'shoulder_lift': {   'original goal_pos': -44.060768127441406,
                         'safe goal_pos': 9.58075175547296},
    'shoulder_pan': {   'original goal_pos': 73.1952133178711,
                        'safe goal_pos': 75.68241469816272},
    'wrist_flex': {   'original goal_pos': 74.75547790527344,
                      'safe goal_pos': 61.30341880341879},
    'wrist_roll': {   'original goal_pos': 95.39778900146484,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 37.17449188232422,
                      'safe goal_pos': 20.82701738742756},
    'shoulder_lift': {   'original goal_pos': -47.28807067871094,
                         'safe goal_pos': 9.58075175547296},
    'shoulder_pan': {   'original goal_pos': 72.17256927490234,
                        'safe goal_pos': 74.31758530183728},
    'wrist_flex': {   'original goal_pos': 76.88870239257812,
                      'safe goal_pos': 62.37179487179486},
    'wrist_roll': {   'original goal_pos': 95.40377807617188,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 44.4074821472168,
                      'safe goal_pos': 22.34284440481497},
    'shoulder_lift': {   'original goal_pos': -53.38063049316406,
                         'safe goal_pos': 9.49814126394051},
    'shoulder_pan': {   'original goal_pos': 67.82850646972656,
                        'safe goal_pos': 72.9527559055118},
    'wrist_flex': {   'original goal_pos': 74.0610122680664,
                      'safe goal_pos': 63.547008547008545},
    'wrist_roll': {   'original goal_pos': 95.36844635009766,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 47.405128479003906,
                      'safe goal_pos': 23.769505127061976},
    'shoulder_lift': {   'original goal_pos': -56.52239990234375,
                         'safe goal_pos': 9.41553077240809},
    'shoulder_pan': {   'original goal_pos': 66.98037719726562,
                        'safe goal_pos': 71.69291338582678},
    'wrist_flex': {   'original goal_pos': 72.71581268310547,
                      'safe goal_pos': 64.72222222222223},
    'wrist_roll': {   'original goal_pos': 95.33641815185547,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 52.34416961669922,
                      'safe goal_pos': 25.01783325902808},
    'shoulder_lift': {   'original goal_pos': -60.22423553466797,
                         'safe goal_pos': 9.085088806278392},
    'shoulder_pan': {   'original goal_pos': 66.31499481201172,
                        'safe goal_pos': 70.53805774278214},
    'wrist_flex': {   'original goal_pos': 69.95789337158203,
                      'safe goal_pos': 65.7905982905983},
    'wrist_roll': {   'original goal_pos': 95.34515380859375,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 53.313446044921875,
                      'safe goal_pos': 26.80115916183682},
    'shoulder_lift': {   'original goal_pos': -62.085731506347656,
                         'safe goal_pos': 8.258983890954141},
    'shoulder_pan': {   'original goal_pos': 65.4887924194336,
                        'safe goal_pos': 69.38320209973753},
    'wrist_flex': {   'original goal_pos': 70.28264617919922,
                      'safe goal_pos': 66.96581196581198},
    'wrist_roll': {   'original goal_pos': 95.32390594482422,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 58.75116729736328,
                      'safe goal_pos': 28.31698617922426},
    'shoulder_lift': {   'original goal_pos': -67.3663101196289,
                         'safe goal_pos': 7.4328789756299045},
    'shoulder_pan': {   'original goal_pos': 63.66267395019531,
                        'safe goal_pos': 68.01837270341207},
    'wrist_roll': {   'original goal_pos': 95.31339263916016,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 62.99344253540039,
                      'safe goal_pos': 31.437806509139534},
    'shoulder_lift': {   'original goal_pos': -70.1881332397461,
                         'safe goal_pos': 6.276332094175956},
    'shoulder_pan': {   'original goal_pos': 63.16216278076172,
                        'safe goal_pos': 65.60367454068242},
    'wrist_roll': {   'original goal_pos': 95.31808471679688,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 67.68870544433594,
                      'safe goal_pos': 32.329469460543905},
    'shoulder_lift': {   'original goal_pos': -73.55530548095703,
                         'safe goal_pos': 5.8632796365138375},
    'shoulder_pan': {   'original goal_pos': 61.58884048461914,
                        'safe goal_pos': 64.65879265091863},
    'wrist_roll': {   'original goal_pos': 95.30204772949219,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 77.48922729492188,
                      'safe goal_pos': 35.45028979045921},
    'shoulder_lift': {   'original goal_pos': -78.70558166503906,
                         'safe goal_pos': 4.624122263527468},
    'shoulder_pan': {   'original goal_pos': 59.34547805786133,
                        'safe goal_pos': 62.24409448818898},
    'wrist_flex': {   'original goal_pos': 52.90929412841797,
                      'safe goal_pos': 59.31623931623932},
    'wrist_roll': {   'original goal_pos': 95.29084777832031,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 78.79983520507812,
                      'safe goal_pos': 36.163620151582705},
    'shoulder_lift': {   'original goal_pos': -79.36309051513672,
                         'safe goal_pos': 4.706732755059889},
    'shoulder_pan': {   'original goal_pos': 59.58119583129883,
                        'safe goal_pos': 61.929133858267704},
    'wrist_flex': {   'original goal_pos': 52.66583251953125,
                      'safe goal_pos': 57.92735042735043},
    'wrist_roll': {   'original goal_pos': 95.28936767578125,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 86.36868286132812,
                      'safe goal_pos': 39.19527418635755},
    'shoulder_lift': {   'original goal_pos': -82.43041229248047,
                         'safe goal_pos': 3.880627839735638},
    'shoulder_pan': {   'original goal_pos': 58.61821365356445,
                        'safe goal_pos': 61.08923884514434},
    'wrist_flex': {   'original goal_pos': 46.86699676513672,
                      'safe goal_pos': 55.25641025641028},
    'wrist_roll': {   'original goal_pos': 95.26780700683594,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 88.9713134765625,
                      'safe goal_pos': 39.90860454748105},
    'shoulder_lift': {   'original goal_pos': -83.69480895996094,
                         'safe goal_pos': 3.137133415943822},
    'shoulder_pan': {   'original goal_pos': 58.28266525268555,
                        'safe goal_pos': 59.514435695538054},
    'wrist_flex': {   'original goal_pos': 44.26947784423828,
                      'safe goal_pos': 55.25641025641028},
    'wrist_roll': {   'original goal_pos': 95.26024627685547,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 94.62847900390625,
                      'safe goal_pos': 40.35443602318324},
    'shoulder_lift': {   'original goal_pos': -85.47001647949219,
                         'safe goal_pos': 2.476249483684441},
    'shoulder_pan': {   'original goal_pos': 58.20349884033203,
                        'safe goal_pos': 58.35958005249344},
    'wrist_flex': {   'original goal_pos': 41.17392349243164,
                      'safe goal_pos': 55.68376068376068},
    'wrist_roll': {   'original goal_pos': 95.22959899902344,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 98.16185760498047,
                      'safe goal_pos': 43.386090057958086},
    'shoulder_lift': {   'original goal_pos': -86.09235382080078,
                         'safe goal_pos': 0.6588186699710832},
    'wrist_flex': {   'original goal_pos': 39.727760314941406,
                      'safe goal_pos': 53.22649572649573},
    'wrist_roll': {   'original goal_pos': 95.19613647460938,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 99.91619873046875,
                      'safe goal_pos': 43.47525635309853},
    'shoulder_lift': {   'original goal_pos': -86.4354019165039,
                         'safe goal_pos': 0.6588186699710832},
    'wrist_flex': {   'original goal_pos': 42.09837341308594,
                      'safe goal_pos': 52.58547008547009},
    'wrist_roll': {   'original goal_pos': 95.1726303100586,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.05317687988281,
                      'safe goal_pos': 43.386090057958086},
    'shoulder_lift': {   'original goal_pos': -86.42633056640625,
                         'safe goal_pos': 0.9066501445683741},
    'wrist_flex': {   'original goal_pos': 43.95563507080078,
                      'safe goal_pos': 52.264957264957275},
    'wrist_roll': {   'original goal_pos': 95.17756652832031,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 99.98829650878906,
                      'safe goal_pos': 45.169415960766855},
    'shoulder_lift': {   'original goal_pos': -86.30760955810547,
                         'safe goal_pos': -0.08467575382073278},
    'wrist_flex': {   'original goal_pos': 45.140174865722656,
                      'safe goal_pos': 49.80769230769232},
    'wrist_roll': {   'original goal_pos': 95.1817626953125,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.29238891601562,
                      'safe goal_pos': 47.487739634418176},
    'shoulder_lift': {   'original goal_pos': -85.9552001953125,
                         'safe goal_pos': -1.571664601404379},
    'wrist_flex': {   'original goal_pos': 45.118263244628906,
                      'safe goal_pos': 48.52564102564102},
    'wrist_roll': {   'original goal_pos': 95.17591857910156,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.71426391601562,
                      'safe goal_pos': 48.646901471243865},
    'shoulder_lift': {   'original goal_pos': -85.98065948486328,
                         'safe goal_pos': -2.23254853366376},
    'wrist_roll': {   'original goal_pos': 95.13465118408203,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.55887603759766,
                      'safe goal_pos': 51.05439144003566},
    'shoulder_lift': {   'original goal_pos': -85.62459564208984,
                         'safe goal_pos': -3.5543163981825785},
    'wrist_roll': {   'original goal_pos': 95.14605712890625,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.78561401367188,
                      'safe goal_pos': 52.570218457423096},
    'shoulder_lift': {   'original goal_pos': -85.64219665527344,
                         'safe goal_pos': -4.380421313506815},
    'wrist_roll': {   'original goal_pos': 95.11540985107422,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.47798919677734,
                      'safe goal_pos': 54.35354436023184},
    'shoulder_lift': {   'original goal_pos': -85.39898681640625,
                         'safe goal_pos': -5.536968194960764},
    'wrist_roll': {   'original goal_pos': 95.12767028808594,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.54398345947266,
                      'safe goal_pos': 56.13687026304058},
    'shoulder_lift': {   'original goal_pos': -85.14398193359375,
                         'safe goal_pos': -6.610904584882277},
    'wrist_roll': {   'original goal_pos': 95.10867309570312,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.13398742675781,
                      'safe goal_pos': 57.47436469014713},
    'shoulder_lift': {   'original goal_pos': -84.62982177734375,
                         'safe goal_pos': -7.354399008674108},
    'wrist_roll': {   'original goal_pos': 95.11601257324219,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.39682006835938,
                      'safe goal_pos': 59.614355773517616},
    'shoulder_lift': {   'original goal_pos': -84.62150573730469,
                         'safe goal_pos': -8.593556381660463},
    'wrist_roll': {   'original goal_pos': 95.09298706054688,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.2383041381836,
                      'safe goal_pos': 60.86268390548372},
    'shoulder_lift': {   'original goal_pos': -84.02210998535156,
                         'safe goal_pos': -9.419661296984714},
    'wrist_roll': {   'original goal_pos': 95.09365844726562,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.36565399169922,
                      'safe goal_pos': 62.02184574230941},
    'shoulder_lift': {   'original goal_pos': -83.83649444580078,
                         'safe goal_pos': -10.328376703841386},
    'wrist_roll': {   'original goal_pos': 95.06375122070312,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 100.38072204589844,
                      'safe goal_pos': 63.80517164511815},
    'shoulder_lift': {   'original goal_pos': -83.27014923095703,
                         'safe goal_pos': -11.402313093762913},
    'wrist_roll': {   'original goal_pos': 95.0587387084961,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 23.766773223876953,
                      'safe goal_pos': 57.46098974587605},
    'shoulder_lift': {   'original goal_pos': 0.4147911071777344,
                         'safe goal_pos': -3.963238331268073},
    'shoulder_pan': {   'original goal_pos': 45.35078048706055,
                        'safe goal_pos': 57.41469816272968},
    'wrist_flex': {   'original goal_pos': 88.73295593261719,
                      'safe goal_pos': 60.235042735042725},
    'wrist_roll': {   'original goal_pos': 78.9557113647461,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 25.7296199798584,
                      'safe goal_pos': 57.90682122157824},
    'shoulder_lift': {   'original goal_pos': -2.947795867919922,
                         'safe goal_pos': -4.21106980586535},
    'shoulder_pan': {   'original goal_pos': 46.804161071777344,
                        'safe goal_pos': 57.41469816272968},
    'wrist_flex': {   'original goal_pos': 88.1671371459961,
                      'safe goal_pos': 60.769230769230774},
    'wrist_roll': {   'original goal_pos': 79.72869873046875,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 28.797325134277344,
                      'safe goal_pos': 57.28265715559519},
    'shoulder_pan': {   'original goal_pos': 48.24118423461914,
                        'safe goal_pos': 56.15485564304461},
    'wrist_flex': {   'original goal_pos': 87.1474609375,
                      'safe goal_pos': 62.69230769230768},
    'wrist_roll': {   'original goal_pos': 80.5094223022461,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 28.471994400024414,
                      'safe goal_pos': 55.855996433348196},
    'shoulder_pan': {   'original goal_pos': 48.72591018676758,
                        'safe goal_pos': 54.79002624671915},
    'wrist_flex': {   'original goal_pos': 86.4940414428711,
                      'safe goal_pos': 63.76068376068375},
    'wrist_roll': {   'original goal_pos': 81.05157470703125,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 29.29202651977539,
                      'safe goal_pos': 54.69683459652251},
    'shoulder_pan': {   'original goal_pos': 50.43161392211914,
                        'safe goal_pos': 53.42519685039369},
    'wrist_flex': {   'original goal_pos': 84.79805755615234,
                      'safe goal_pos': 64.61538461538461},
    'wrist_roll': {   'original goal_pos': 82.04627990722656,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 29.12066078186035,
                      'safe goal_pos': 53.53767275969685},
    'wrist_flex': {   'original goal_pos': 84.1509780883789,
                      'safe goal_pos': 66.0042735042735},
    'wrist_roll': {   'original goal_pos': 83.28412628173828,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 26.186038970947266,
                      'safe goal_pos': 52.46767721801157},
    'wrist_flex': {   'original goal_pos': 84.61399841308594,
                      'safe goal_pos': 67.39316239316238},
    'wrist_roll': {   'original goal_pos': 83.74149322509766,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 24.800567626953125,
                      'safe goal_pos': 51.4868479714668},
    'wrist_flex': {   'original goal_pos': 82.07609558105469,
                      'safe goal_pos': 68.56837606837607},
    'wrist_roll': {   'original goal_pos': 85.2282485961914,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 17.623411178588867,
                      'safe goal_pos': 50.06018724921978},
    'shoulder_lift': {   'original goal_pos': 3.2424373626708984,
                         'safe goal_pos': -0.3283767038413856},
    'wrist_flex': {   'original goal_pos': 84.04255676269531,
                      'safe goal_pos': 70.38461538461539},
    'wrist_roll': {   'original goal_pos': 85.67539978027344,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 22.443359375,
                      'safe goal_pos': 48.811859117253675},
    'wrist_flex': {   'original goal_pos': 80.93706512451172,
                      'safe goal_pos': 71.45299145299145},
    'wrist_roll': {   'original goal_pos': 86.07467651367188,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 18.25039291381836,
                      'safe goal_pos': 47.74186357556843},
    'shoulder_lift': {   'original goal_pos': 2.19561767578125,
                         'safe goal_pos': 1.9847170590665115},
    'shoulder_pan': {   'original goal_pos': 61.925010681152344,
                        'safe goal_pos': 61.535433070866134},
    'wrist_flex': {   'original goal_pos': 78.75495147705078,
                      'safe goal_pos': 72.62820512820514},
    'wrist_roll': {   'original goal_pos': 87.23323059082031,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 18.710880279541016,
                      'safe goal_pos': 45.869371377619274},
    'shoulder_pan': {   'original goal_pos': 62.01232147216797,
                        'safe goal_pos': 61.9553805774278},
    'wrist_flex': {   'original goal_pos': 76.98896026611328,
                      'safe goal_pos': 74.33760683760684},
    'wrist_roll': {   'original goal_pos': 87.2817153930664,
                      'safe goal_pos': 64.56043956043956}}
safety=normal, speed=1.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 16.135704040527344,
                      'safe goal_pos': 44.62104324565314},
    'shoulder_lift': {   'original goal_pos': 4.880731582641602,
                         'safe goal_pos': 4.215200330441959},
    'shoulder_pan': {   'original goal_pos': 64.91407775878906,
                        'safe goal_pos': 63.530183727034114},
    'wrist_flex': {   'original goal_pos': 76.02758026123047,
                      'safe goal_pos': 75.5128205128205},
    'wrist_roll': {   'original goal_pos': 87.98833465576172,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 14.455387115478516,
                      'safe goal_pos': 42.65938475256354},
    'shoulder_pan': {   'original goal_pos': 66.5575942993164,
                        'safe goal_pos': 64.89501312335958},
    'wrist_roll': {   'original goal_pos': 88.27760314941406,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 11.280908584594727,
                      'safe goal_pos': 39.71689701292911},
    'shoulder_pan': {   'original goal_pos': 68.10737609863281,
                        'safe goal_pos': 67.83464566929132},
    'wrist_roll': {   'original goal_pos': 88.50341033935547,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 11.636768341064453,
                      'safe goal_pos': 39.27106553722692},
    'shoulder_pan': {   'original goal_pos': 68.79814147949219,
                        'safe goal_pos': 67.20472440944883},
    'wrist_roll': {   'original goal_pos': 88.4576187133789,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 6.64771842956543,
                      'safe goal_pos': 36.95274186357557},
    'shoulder_pan': {   'original goal_pos': 72.76850891113281,
                        'safe goal_pos': 68.14960629921259},
    'wrist_roll': {   'original goal_pos': 88.95098114013672,
                      'safe goal_pos': 64.56043956043956}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 6.019077301025391,
                      'safe goal_pos': 37.57690592955862},
    'shoulder_pan': {   'original goal_pos': 71.94490051269531,
                        'safe goal_pos': 67.83464566929132},
    'wrist_roll': {   'original goal_pos': 88.62156677246094,
                      'safe goal_pos': 64.41391941391942}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 4.671430587768555,
                      'safe goal_pos': 35.97191261703077},
    'shoulder_pan': {   'original goal_pos': 75.16512298583984,
                        'safe goal_pos': 69.51443569553805},
    'wrist_roll': {   'original goal_pos': 89.38536834716797,
                      'safe goal_pos': 64.07203907203908}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 6.283761978149414,
                      'safe goal_pos': 34.90191707534552},
    'shoulder_pan': {   'original goal_pos': 76.02909851074219,
                        'safe goal_pos': 70.66929133858267},
    'wrist_flex': {   'original goal_pos': 68.98126220703125,
                      'safe goal_pos': 70.10683760683762},
    'wrist_roll': {   'original goal_pos': 89.61917114257812,
                      'safe goal_pos': 64.07203907203908}}
safety=stop, speed=0.0x, hand_distance=n/a
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 7.586139678955078,
                      'safe goal_pos': 33.386090057958086},
    'shoulder_lift': {   'original goal_pos': -1.0816268920898438,
                         'safe goal_pos': -0.9933911606774046},
    'shoulder_pan': {   'original goal_pos': 76.45174407958984,
                        'safe goal_pos': 73.18897637795277},
    'wrist_flex': {   'original goal_pos': 65.66996002197266,
                      'safe goal_pos': 68.82478632478632},
    'wrist_roll': {   'original goal_pos': 89.57841491699219,
                      'safe goal_pos': 64.26739926739927}}
WARNING:root:Relative goal position magnitude had to be clamped to be safe.
{   'elbow_flex': {   'original goal_pos': 8.496816635131836,
                      'safe goal_pos': 33.29692376281767},
    'shoulder_pan': {   'original goal_pos': 77.1084976196289,
                        'safe goal_pos': 73.50393700787401},
    'wrist_flex': {   'original goal_pos': 61.031761169433594,
                      'safe goal_pos': 67.22222222222223},
    'wrist_roll': {   'original goal_pos': 89.81971740722656,
                      'safe goal_pos': 64.41391941391942}}
Policy paused.

error im getting 