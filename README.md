# MH Discord Bot

Discord bot that shows obtainable items from monsters
in Monster Hunter games.

Has data for :
> MHF1<br>
> MHFU<br>
> MHP3<br>
> MHXX<br>


## Requirements
- python 3.9

The version is important. It may not run with lower versions.


## Install the  required modules
```sh
python -m pip install -r files/modules.list
```
This command should also be run when module requirements change.


## Configure the Bot
- Open `files/config.json`
- Set your bot authentication token in it
- Set your own discord user id in it (optional)

If `files/config_.json` is present, it will be used as config file instead.


## Run the bot
```sh
python run.py
```


## Run the bot in background
```sh
nohup python -u run.py > output.log &
```
and check the logs in realtime with
```sh
tail -f output.log
```
<br>


## Contributions - Monsters Data
* [Contributors and sources](https://github.com/lirkas/mh-discord-bot/blob/master/files/README.md)

## License
This project is under the [MIT License](/LICENSE).