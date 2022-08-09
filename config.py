import os

REDDIT_CONF = {
    "user_agent" : "Reply rock and stone bot test. (By u/KaeWye)",
    "client_id" : os.environ.get("REDDIT_CLIENT_ID","<your client id>"),
    "client_secret" : os.environ.get("REDDIT_CLIENT_SECRET","<your_client_secret>"),
    "username": os.environ.get("REDDIT_USERNAME","<your_username>"),
    "password": os.environ.get("REDDIT_PASSWORD","<your_password>")
}

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
        # '': {  # root logger
        #     'handlers': ['default'],
        #     'level': 'WARNING',
        #     'propagate': False
        # },

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
            'level': os.environ.get('LOG_MAIN_LOGGER_LEVEL', 'INFO'),
            'propagate': False
        },
    }
}
