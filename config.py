import logging
import os

REDDIT_CONF = {
    "user_agent" : "Reply rock and stone bot test. (By u/KaeWye)",
    "client_id" : os.environ.get("REDDIT_CLIENT_ID","<your client id>"),
    "client_secret" : os.environ.get("REDDIT_CLIENT_SECRET","<your_client_secret>"),
    "username": os.environ.get("REDDIT_USERNAME","<your_username>"),
    "password": os.environ.get("REDDIT_PASSWORD","<your_password>")
}

SUBREDDIT = 'DeepRockGalactic'

IGNORED_USERS = {"WanderingDwarfMiner"}
REPLIES = [
    "Rock and Stone!",
    "Rock and Stone, Brother!",
    "Rock and Stone everyone!",
    "Rock and Stone forever!",
    "Rock and roll and stone!",
    "Rock and Stone to the Bone!",
    "Rock and Stone in the Heart!",
    "Rockity Rock and Stone!",
    "Can I get a Rock and Stone?",
    "Did I hear a Rock and Stone?",
    "For Karl!",
    "For Rock and Stone!",
    "If you don't Rock and Stone, you ain't comin' home!",
    "That's it lads! Rock and Stone!",
    "To Rock and Stone!",
    "We fight for Rock and Stone!"
]

GIMLI_QUOTES = [
    "And my Axe!",
    "Nobody tosses a dwarf!",
    "Not the beard!",
    "I have the eyes of a hawk and the ears of a fox!",
    "I’ll have no pointy-ear outscoring me!",
    "It’s the Dwarves that go swimming with little, hairy women!",
    "Well, this is a thing unheard of! An Elf would go underground, where a Dwarf dare not? Oh, I’d never hear the end of it!",
    "Certainty of death? Small chance of success? What are we waiting for?",
    "Let them come! There is one Dwarf yet in Moria who still draws breath!",
    "Bring your pretty face to my axe.",
    "Aye. I could do that.",
    "Roaring Fires, Malt Beer, Ripe Meat Off The Bone!",
    "Give me your name, Horse Master, and I shall give you mine!",
    "Toss me! I cannot jump the distance, you'll have to toss me!",
    "Don't tell the elf!",
    "That still only counts as one!",
    "I will be dead before I see the Ring in the hands of an Elf! Never trust an Elf!",
    "I’m wasted on cross-country! We Dwarves are natural sprinters, very dangerous over short distances!",
    "There’s plenty for the both of us, may the best Dwarf win!"
]

LOGGING_CONFIG = {
    'version': 1,
    # 'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': os.environ.get('LOG_STREAMHANDLER_LEVEL', 'INFO'),
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },

        'praw': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },

        'prawcore': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },

        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': os.environ.get('LOG_MAIN_LOGGER_LEVEL', 'DEBUG'),
            'propagate': False
        },
        'main': {
            'handlers': ['default'],
            'level': os.environ.get('LOG_MAIN_LOGGER_LEVEL', 'DEBUG'),
            'propagate': False
        }
    }
}

REDDIT_EXCEPTIONS = {
    'BLOCKED_PARENT_USER': "SOMETHING_IS_BROKEN: 'Something is broken, please try again later.' on field 'parent'"
}
