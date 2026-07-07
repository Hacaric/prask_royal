## TODO
### Game logic
- Game map initialization (`gamemap.py.Map.new`)
- Define entity&tower types - In JSON, because they will be shared with bot developers who may be using different programming language
- End game upon player death in 1v1 (`game.py.Game.removePlayer` and `game.py.Game.should_stop_game`) 
- Update parsing function to send all required data (`game.py.Game.parse`, `gamemap.py.Map.parsemap`)
- Update tick function to move entities, add elixir to players (`game.py.Game.tick`)
- Validation of bots' turns (`game.py.Game.executeTurn`) 
- Update player turn function to: (`game.py.Game.executeTurn`) 
    - Use elixir
    - Spawn extities (summon them immieadately to avoid collision between players)
    - Restock their cards

- Make it compatible with backend (https://github.com/trojsten/ksp-proboj-web)

### Security
- Perform a security search to find and fix exploits
- Maybe red-team attack trough the bots to see if it is possible to manipulate the game? :)