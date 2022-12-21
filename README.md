# MH Discord Bot

Discord bot that shows obtainable items from monsters
in Monster Hunter games.

Infos available for :
* MHF1
* MHFU
* MHP3
* MHXX

----
## Requirements :
- python3
- pip

Any system that can run both should be able to host and run the bot.

----
## Install required modules using pip :
```sh
pip install -r files/modules.list
```

----
## Configure the Bot :
Open `files/config.json` and set your own bot authentication token in it.
<br>
If `files/config_.json` is present, it will be used as config file instead of
`files/config.json`

----
## Run the bot :
```sh
python run.py
```

## Run the bot in background :
```sh
nohup python -u run.py > output.log &
```
and check the logs in realtime with :
```sh
tail -f output.log
```
----
## Contributions - Monsters Data :
* [HERE](https://github.com/lirkas/mh-discord-bot/blob/master/files/README.md)
