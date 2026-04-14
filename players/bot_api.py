import sys, os
import _config
import _stats
import json


# log_file_path = os.path.join(os.path.dirname(__file__), 'latest.log')
# log_file = open(log_file_path, 'w')
def log(*msg):
    message = ' '.join(msg) + '\n'
    sys.stderr.write(message)
    sys.stderr.flush()
    # log_file.write(message)
    # log_file.flush()
log("Initialized log file.")

def run(player):
    turn = 0
    while True:
        # Read the game state sent by the manager
        line = sys.stdin.readline()
        
        # Exit if the manager closes the connection
        if not line:
            break
            
        game_state = line.strip()
        
        log(f"\nTURN {turn}")
        # Logic to determine the next move
        move = player.make_turn(game_state)
        
        # Write the move to stdout and flush to ensure the manager receives it
        sys.stdout.write(move.parse() + "\n")
        sys.stdout.flush()
        
        turn += 1

    # Errors will be captures by host
    # except Exception as e:
    #     log(f"Error in the RUN function (in bot_api): {e}")

def process_move(state):
    # Logic for the competition goes here
    return "MOVE_DATA"