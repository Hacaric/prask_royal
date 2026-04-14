from _config import Settings
from _stats import Stats
import json
import subprocess
import os
from gamemap import *

class Game:
    def __init__(self, map_:Map):
        self.map = map_
    def executeTurns(self, turns):
        for playerID, turn in enumerate(turns):
            if self.validateTurn(playerID, turn):
                self.executeTurn(playerID, turn)
            else:
                print(f"Invalid turn from player: {playerID}")
    def parse(self):
        return self.map.parse()

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

gamedir, logdir = setupGameDir(CONFIG_JSON, GAMES_JSON)

player_programs = [(key, value['path'], value['command']) for key, value in CONFIG_JSON.items()]

player_subprocesses = {
    # subprocess.Popen(['python3', 'bot.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True),
    # subprocess.Popen(['python3', 'bot.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
}

for id, path, command in player_programs:
    with open(os.path.join(logdir, str(id) + '.log'), 'w') as stderr_output:
        player_subprocesses[id] = subprocess.Popen([command, path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr_output, text=True)

def handle_timeout_or_error(p):
    print(f"Timeout: {p}")

m = Map()
m.new()
g = Game(m)
game_active = True
turn = 0
while game_active:
    state = g.parse()
    moves = []
    for player_id in player_subprocesses:
        player = player_subprocesses[player_id]
        # Send data
        player.stdin.write(state + "\n")
        player.stdin.flush()
        # Get response with timeout logic
        try:
            move = player.stdout.readline().strip()
            moves.append((move, player))
        except Exception as e:
            print(f"Error {e} occured while playing turn of player {player}")
            handle_timeout_or_error(player)
        print(f'Heppy turns! {moves}')
    turn += 1
    if turn > 20:
        print("\n\nFOR TESTING PURPOSES TURNS WERE CAPPED TO 20\nEnding game...\n\n")
        break
for player_subprocess in player_subprocesses.values():
    player_subprocess.terminate()