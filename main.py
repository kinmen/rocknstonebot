import logging
import praw
import random
import re

import config

def setup_logging():
    handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    for logger_name in ("praw", "prawcore"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

logger = setup_logging()

def main():

    # Instantiate reddit client and add my username to ignore list just in case.
    r = praw.Reddit(**config.REDDIT_CONF)
    me = r.user.me()
    config.IGNORED_USERS.add(me.name)

    # sub = r.subreddit('DeepRockGalactic')
    sub = r.subreddit('all')
    logger.info("Looking at sub: {}".format(sub))

    for comment in sub.stream.comments(skip_existing=True):
    # for comment in sub.comments(limit=30):
        text = comment.body
        logger.info("Checking comment: {}".format(comment.permalink))
        if should_reply(comment):
            logger.info("replying to comment with id: {}, author: {}, link: {}".format(comment, comment.author, comment.permalink))
            comment.reply(body = random.choice(config.REPLIES))
            comment.save() # We use save to save state and mark that we've already replied to this comment

def should_reply(comment: str) -> bool:
    trig_re = r'.*rock and stone.*'
    text = comment.body

    # Check if matches rock and stone, not our comment (or from ignored user), and not one we've seen before
    if (re.match(trig_re, text, re.IGNORECASE)
        and comment.author.name not in config.IGNORED_USERS
        and not comment.saved):
        return True
    return False

if __name__ == '__main__':
    main()



