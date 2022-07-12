import praw
import random
import re

import config

import logging

handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
handler.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def main():
    r = praw.Reddit(**config.REDDIT_CONF)
    me = r.user.me()
    config.IGNORED_USERS.add(me.name)

    sub = r.subreddit('DeepRockGalactic')
    # sub = r.redditor('kaewye')
    logger.info("Looking at sub: {}".format(sub))

    for comment in sub.stream.comments(skip_existing=True):
    # for comment in sub.comments(limit=30):
        # title = s.title
        text = comment.body
        logger.info("Checking comment: {}".format(comment.permalink))
        if should_reply(comment):
            logger.info("replying to comment with id: {}, author: {}, link: {}".format(comment, comment.author, comment.permalink))
            comment.reply(body = random.choice(config.REPLIES))
            comment.save()

def should_reply(comment):
    trig_re = r'.*rock and stone.*'
    text = comment.body
    if (re.match(trig_re, text, re.IGNORECASE)
        and comment.author.name not in config.IGNORED_USERS
        and not comment.saved):
        return True
    return False

if __name__ == '__main__':
    main()



