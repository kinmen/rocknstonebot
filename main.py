import logging
import logging.config
import praw
import random
import re

import config

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main():

    # Instantiate reddit client and add my username to ignore list just in case.
    r = praw.Reddit(**config.REDDIT_CONF)
    me = r.user.me()
    config.IGNORED_USERS.add(me.name)

    # sub = r.subreddit('DeepRockGalactic')
    sub = r.subreddit('all')
    logger.info("Looking at sub: {}".format(sub))

    for comment in sub.stream.comments():
    # for comment in sub.comments(limit=30):
        text = comment.body
        logger.debug("Checking comment: {}".format(comment.permalink))
        if should_reply(comment):
            logger.info("replying to comment with id: {}, author: {}, link: {}".format(comment, comment.author, comment.permalink))
            comment.reply(body = random.choice(config.REPLIES))
            comment.save() # We use save to save state and mark that we've already replied to this comment

def should_reply(comment) -> bool:
    trig_re = r'.*rock and stone.*'
    text = comment.body

    # Check if matches rock and stone, not our comment (or from ignored user), and not one we've seen before
    if (re.match(trig_re, text, re.IGNORECASE)
        and comment.author.name not in config.IGNORED_USERS
        and not already_replied_comment(comment)
        and not already_replied_thread(comment)):
        return True
    return False

def already_replied_comment(comment):
    return comment.saved

def already_replied_thread(comment):
    if comment.saved:
        return True

    # Efficient way of discovering top level comment per:
    # https://praw.readthedocs.io/en/stable/code_overview/models/comment.html#praw.models.Comment.parent
    refresh_counter = 0
    ancestor = comment
    while not ancestor.is_root:
        ancestor = ancestor.parent()

        if refresh_counter % 9 == 0:
            ancestor.refresh()
        refresh_counter += 1

        if already_replied_comment(ancestor):
            logger.info("Already replied to comment: {}. Replied comment ancestor: {}".format(comment.id, ancestor.id))
            return True

    return False

if __name__ == '__main__':
    main()



