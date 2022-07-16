# rocknstonebot
Simple reddit bot that replies "Rock and stone" quotes to other comments that rock and stone.

Right now deployed in Heroku, running as reddit user [u/WanderingDwarfMiner](https://new.reddit.com/user/WanderingDwarfMiner/)

## Setup
1. Install requirements:

    `pip install -r requirements.txt`

2. Edit `REDDIT_CONF` in config.py to add in your reddit creds, else grabs from env var REDDIT_... (for Heroku deployment with config vars for now)

3. Run:

    `python main.py`

Currently pulls from stream of new comments from r/all

## **ROCK AND STONE!**
