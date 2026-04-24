# from game._config import Settings
from game._stats import Stats
import json
import subprocess
import os
from datetime import datetime # why is there datetime inside datetime??
from game.gamemap import *
from game.game import Game
from observer_logger import Observer

# Open configuration files
with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as f:
    CONFIG_JSON = json.load(f)
with open(os.path.join(os.path.dirname(__file__), '..', 'games.json')) as f:
    GAMES_JSON = json.load(f)

def setupGameDir(CONFIG_JSON:dict, GAMES_JSON:dict):
    """
        Creates game output directory if doesn't exist
        Creates game/log directoruy if doesn't exists 
        Deletes old *.log files from game/log if GAMES_JSON.keep_logs_from_unused_bots is False
        Returns game direcory path and log directory path which are defined as:
            gamedir = {GAMES_JSON.gamefolder}
            logdir = {gamedir}/log
        
        Return: gamedir:str, logdir:str
    """
    gamedir = os.path.join(os.path.dirname(__file__), '..', GAMES_JSON['gamefolder'])
    os.makedirs(gamedir, exist_ok=True)
    logdir = os.path.join(gamedir, 'log')
    os.makedirs(logdir, exist_ok=True)
    if not GAMES_JSON.get('keep_logs_from_unused_bots', True):
        for file in os.listdir(logdir):
            if file[:-len('.log')] == '.log':
                os.remove(os.path.join(logdir, file))
    return gamedir, logdir

# LOG_FILE is global
LOG_FILE = None
def setupLogger(logdir):
    """
        Param: logdir - location of log file

        Creates log file and returns function to log into that file.
        Log file is located in {logdir}/__server__.log

        Return: log:function - usage: log(*msg:tuple[any])
    """
    global LOG_FILE
    LOG_FILE = open(os.path.join(logdir, '__server__.log'), 'w')
    def log(*msg):
        """Log into server log file"""
        message = f"[{datetime.now().strftime('%d.%m.%Y-%H:%M:%S')}] {' '.join([str(i) for i in msg])}\n"
        LOG_FILE.write(message)
        print(message, end='')
    return log

gamedir, logdir = setupGameDir(CONFIG_JSON, GAMES_JSON)
log = setupLogger(logdir)
log(f'Start of log file')


# Run players' programs
#
# Loaded from CONFIG_JSON
# Piping strout and stdin, communication canals
# Stderr is directed into log file

# MAKE SURE ALL PLAYER IDs ARE STRINGS!
player_program_files = [(str(key), value['path'], value['command']) for key, value in CONFIG_JSON.items()]
player_subprocesses = {}
for id, path, command in player_program_files:
    with open(os.path.join(logdir, str(id) + '.log'), 'w') as stderr_output:
        player_subprocesses[id] = subprocess.Popen([command, path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr_output, text=True)


def handle_timeout_or_error(p):
    log(f"Timeout or error: {p}")

observer = Observer(os.path.join(gamedir, 'observer.gz'))
# gamemap = Map()
# gamemap.new()
game_map_type = None
with open(os.path.join(os.path.dirname(__file__), '..', GAMES_JSON['map_path'])) as f:
    game_map_type = json.load(f)
game = Game(log, list(player_subprocesses.keys()), game_map_type)
# game.logToObserver(observer)
observer.write(game.parse(None))
game_active = True
round = 0
players_errored_out:dict[int, Exception] = {}
while game_active:
    
    for player_id in player_subprocesses:
        if player_id in players_errored_out:
            continue
        player = player_subprocesses[player_id]
        try:
            # Send data
            player.stdin.write(game.parse(player_id) + "\n")
            player.stdin.flush()
        except BrokenPipeError:
            log(f"Error getting response from player {player_id}: Broken pipe")
            log(f"Removing player from game...")
            game.removePlayer(player_id)
            player_subprocesses[player_id].terminate()
            players_errored_out[player_id] = BrokenPipeError
        # Get response with timeout logic
        try:
            move = player.stdout.readline().strip()
            game.executeTurn(move, player)
        except Exception as e:
            log(f"Error \"{e}\" occured while playing turn of player {player}")
            handle_timeout_or_error(player)
        observer.write(game.parse())
    round += 1
    if game.should_stop_game(round):
        break #TODO

observer.write(game.parse())
observer.close() # DONT FORGET TO CLOSE THE FILE!!!
for key, player_subprocess in player_subprocesses.items():
    if not key in players_errored_out:
        player_subprocess.terminate()

with open(os.path.join(gamedir, "score.json"), "w") as f:
    json.dump(game.getScore(), f)