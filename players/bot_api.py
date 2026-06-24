import sys, os
import _stats
import json
from turn_type import Turn

"""
This file is ment to be executed by server.py on a separate thread and servers for the bot as interface to interact with the server
Communication with server happens trough stdout/stdin
All logs and errors of the bots are sent to stderr and should be forwarded to a log file
"""

# IMPORTANT: Always log into stderr, stdout is reserved for communication with the server 
def log(*msg):
    """
    Log messages to stderr and flush
    Server will forward it into a log file `game/log/{bot_name}.log`
    """
    message = ' '.join(msg) + '\n'
    sys.stderr.write(message)
    try:
        sys.stderr.flush()
    except:
        pass
log("Initialized log function.")

def run(player):
    """
    Args: player, type: has function player.make_turn(server_data:str)
    Creates while-true cycle that waits for input from stdin, forwards it to player.make_turn() and output of the function is written into stdout
    player.make_turn() shall return an instacne of child class of Turn, eg. instance of EmptyTurn or of PlaceTurn
    """
    turn_i = 0
    while True:
        # Read the game state sent by the server
        line = sys.stdin.readline()
        
        # Exit if the server closes the connection
        if not line:
            break
            
        game_state = line.strip()
        
        # Purely for readibility of the log file
        log(f"\nTURN {turn_i}")

        # Logic to determine the next move
        player_turn = player.make_turn(game_state)

        if not isinstance(player_turn, Turn):
            log(f"\n\nWARNING: player.make_turn() returned object of type {type(player_turn)}. Expected child class of Turn. If this type doesn't support .parse() function it'll likely fail.\n")
        
        # Write the move to stdout and flush to ensure the server receives it
        sys.stdout.write(player_turn.parse() + "\n")
        try:
            sys.stdout.flush()
        except:
            pass

        turn_i += 1

    # Errors will be captures by the server, no error handling needed
    # When you handle errors, you make it harder to debug, because all logs to  already being directed trough stderr and showing the full trace is more useful than some other message
    # except Exception as e:
    #     log(f"Error in the RUN function (in bot_api): {e}")

