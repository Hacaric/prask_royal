from _config import Settings
from _stats import Stats
import json
import subprocess
import os
from datetime import datetime # why is there datetime inside datetime??
from gamemap import *

# This developer is stupid ;)


class Game:
    def __init__(self, map_:Map, log):
        self.map = map_
        self.log = log
    def executeTurns(self, turns):
        for playerID, turn in enumerate(turns):
            if self.validateTurn(playerID, turn):
                self.executeTurn(playerID, turn)
            else:
                self.log(f"Invalid turn from player: {playerID}")
    def parse(self):
        return self.map.parse()
    def removePlayer(self, playerID):
        pass #TODO

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as f:
    CONFIG_JSON = json.load(f)
with open(os.path.join(os.path.dirname(__file__), '..', 'games.json')) as f:
    GAMES_JSON = json.load(f)

print(GAMES_JSON)
print(type(GAMES_JSON))
print(GAMES_JSON['gamefolder'])

def setupGameDir(CONFIG_JSON:dict, GAMES_JSON:dict):
    gamedir = os.path.join(os.path.dirname(__file__), '..', GAMES_JSON['gamefolder'])
    os.makedirs(gamedir, exist_ok=True)
    logdir = os.path.join(gamedir, 'log')
    os.makedirs(logdir, exist_ok=True)
    if not GAMES_JSON.get('keep_logs_from_unused_bots', True):
        for file in os.listdir(logdir):
            if file[:-len('.log')] == '.log':
                os.remove(os.path.join(logdir, file))
    return gamedir, logdir
LOG_FILE = None
def setupLogger(logdir):
    global LOG_FILE
    LOG_FILE = open(os.path.join(logdir, '__server__.log'), 'w')
    def log(*msg):
        message = ' '.join([str(i) for i in msg]) + '\n'
        LOG_FILE.write(message)
        print(message, end='')
    return log

gamedir, logdir = setupGameDir(CONFIG_JSON, GAMES_JSON)

log = setupLogger(logdir)
log(f'[{datetime.now().strftime('%d.%B.%Y-%H:%M:%S')}] Start of log file')

player_program_files = [(key, value['path'], value['command']) for key, value in CONFIG_JSON.items()]

player_subprocesses = {
    # subprocess.Popen(['python3', 'bot.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True),
    # subprocess.Popen(['python3', 'bot.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
}

for id, path, command in player_program_files:
    with open(os.path.join(logdir, str(id) + '.log'), 'w') as stderr_output:
        player_subprocesses[id] = subprocess.Popen([command, path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr_output, text=True)

def handle_timeout_or_error(p):
    log(f"Timeout: {p}")

m = Map()
m.new()
g = Game(m, log)
game_active = True
turn = 0
players_errored_out:dict[int, Exception] = {}
while game_active:
    state = g.parse()
    moves = []
    for player_id in player_subprocesses:
        if player_id in players_errored_out:
            continue
        player = player_subprocesses[player_id]
        # Send data
        try:
            player.stdin.write(state + "\n")
            player.stdin.flush()
        except BrokenPipeError:
            log(f"Error getting response from player {player_id}: Broken pipe")
            log(f"Removing player from game...")
            g.removePlayer(player_id)
            player_subprocesses[player_id].terminate()
            players_errored_out[player_id] = BrokenPipeError
        # Get response with timeout logic
        try:
            move = player.stdout.readline().strip()
            moves.append((move, player))
        except Exception as e:
            log(f"Error {e} occured while playing turn of player {player}")
            handle_timeout_or_error(player)
        log(f'Heppy turns! {moves}')
    turn += 1
    if turn > 20:
        log("\n\nFOR TESTING PURPOSES TURNS WERE CAPPED TO 20\nEnding game...\n\n")
        break
for key, player_subprocess in player_subprocesses.items():
    if not key in players_errored_out:
        player_subprocess.terminate()