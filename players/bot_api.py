import sys, os
import _stats
import json

# IMPORTANT: Always log into stderr, stdout is reserved for communication with the server 
def log(*msg):
    message = ' '.join(msg) + '\n'
    sys.stderr.write(message)
    try:
        sys.stderr.flush()
    except:
        pass
log("Initialized log function.")

def run(player):
    turn = 0
    while True:
        # Read the game state sent by the server
        line = sys.stdin.readline()
        
        # Exit if the server closes the connection
        if not line:
            break
            
        game_state = line.strip()
        
        # Purely for readibility of the log file
        log(f"\nTURN {turn}")

        # Logic to determine the next move
        move = player.make_turn(game_state)
        
        # Write the move to stdout and flush to ensure the server receives it
        sys.stdout.write(move.parse() + "\n")
        try:
            sys.stdout.flush()
        except:
            pass

        turn += 1

    # Errors will be captures by the server, no error handling needed
    # except Exception as e:
    #     log(f"Error in the RUN function (in bot_api): {e}")

