# Proboj-like game created by Prask participants
**Inspirated by board game version clash royal played on Prask camp**

## Roles
- Head of game logic and runner: [@KaktusTim](https://github.com/KaktusTim)
- Head of observer: [@Slime636626](https://github.com/Slime636626)

**In development, not all fetures are functional yet**

## Features: 
- Supports multiple python bots, but integration of other languages should be easy
- Log game states to file (observer.gz), than replay trough website observer.html
- Log from bot to file
- Configure using json files

## Usage
To run a game, run `server/server.py`
The game will import and use bots from `games.json` (bots are defined in `config.json`)

Output logs will appear in `game/log/` (logs are named after bot names used in `games.json`, the server log is names `__server__.log`)
Replay file of the game is `game/observer.gz` and can be viewed in `observer/observer.html` (INDEV)
Game results are stored in `game/score.json`

## TODO:
- Cleanup _config.py, _stats.py and unite game settings
- Create the game
- Create Observer
