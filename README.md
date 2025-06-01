# MH Discord Bot

Discord bot that shows obtainable items and hitzone data from monsters
in Monster Hunter games.

Data included:
```Rust
- MHF1  [Carves + Part Breaks]
- MHFU  [Carves + Part Breaks] [Hitzone Data]
- MHP3  [Carves + Part Breaks]
- MHXX  [Carves + Part Breaks]
```

The list of discord commands can be found [here](/docs/COMMANDS.md) or directly from discord with `$help` (when the bot is running).<br>
Does **not** support Discord *Slash Commands* feature.

## Requirements

### Main Requirements
- python >= 3.9
    - pip (installed as a python module)
- Bash >= 5.0 (if bash scripts are used)

Linux OS is preferred for bash scripts, but these scripts are not required to run the bot.

## Installing the required modules
```sh
python -m pip install -r files/modules.list
```
This command should also be run when module requirements change.


## Configuring the Bot
The recommended way is to copy/rename `files/config.json` to  `files/config_.json` and put the bot token and any other required infos mentionned below in it. <br>
`files/config_.json` is excluded from commits in `.gitignore`, and will therefore be completely ignored by git.

What goes in the config file:
- Bot authentication token, required for the bot to log into discord
- (Optional) Command prefix, used for discord commands, can be changed to avoid conficts
- (Optional) A discord User ID, to access to certain commands


## Running the Bot
```sh
python run.py
```
This starts the bot application and keep it running for as long as the terminal instance is kept open. <br>
`Ctrl + C` terminates the application and disconnects the Bot from Discord.

## Keeping it running in background (Linux)

On a Bash shell it is possible to keep it running in the background and manage the instance as explained below.

### Using bot.sh script
Utility bash script (`scripts/bot.sh`) compiling a variety of commands to ease up the bot application handling.<br>
A list of the most useful commands. They must be run directly from this project's root directory.

```yaml
bot start   # Runs a new the instance of the bot in the background
bot check   # Checks if a bot instance is currently running
bot stop    # Stops all bot running instances
bot help    # Display available commands and details
```
All `bot` script commands and more details can be found [here](/docs/scripts/COMMANDS.md).

### Using Bash commands
```sh
nohup python -u run.py > out.log &   # Runs the bot in the background
tail -f out.log                      # check the bot output in realtime
pkill py-mhbot-7940                  # Stops all bot running instances
```

## Contributions - Monsters Data
* [Contributors and sources](https://github.com/lirkas/mh-discord-bot/blob/master/files/README.md)

## License
This project is under the [MIT License](/LICENSE).