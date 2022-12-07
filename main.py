import logging
import logging.config
import praw
import prawcore
import random
import re

import config

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

print("kyang test uptop")
def main():
    print("starting in main")

    # Instantiate reddit client and add my username to ignore list just in case.
    r = praw.Reddit(**config.REDDIT_CONF)
    me = r.user.me()
    config.IGNORED_USERS.add(me.name)

    # sub = r.subreddit('DeepRockGalactic')
    sub = r.subreddit('all')
    logger.info("Looking at sub: {}".format(sub))

    for comment in sub.stream.comments():
    # for comment in sub.comments(limit=30):
    # if True:
    #     comment = r.comment('ilprh2g')
        text = comment.body
        logger.debug("Checking comment: {}".format(comment.permalink))
        if should_reply(comment):
            logger.info("replying to comment with id: {}, author: {}, link: {}".format(comment, comment.author, comment.permalink))
            try:
                comment.reply(body = random.choice(config.REPLIES))
                comment.save() # We use save to save state and mark that we've already replied to this comment
            except praw.exceptions.RedditAPIException as e:
                for subexception in e.items:
                    # If a user blocked me in the comment chain, it raises a generic 'something is broken' error
                    if subexception.error_message == config.REDDIT_EXCEPTIONS['BLOCKED_PARENT_USER']:
                        logger.warning("Couldn't reply to comment, most likely due to user block in thread. id: {}, author: {}, link: {}".format(
                            comment, comment.author, comment.permalink))
                logger.exception("Failed to reply to comment/save for id: {}, author: {}, link: {}. Error: {}".format(
                            comment, comment.author, comment.permalink, e), exc_info = e)
            except prawcore.exceptions.Forbidden as e:
                logger.warning("Couldn't reply to comment because forbidden, most likely due to banned from sub. id: {}, author: {}, link: {}".format(
                            comment, comment.author, comment.permalink))

def should_reply(comment) -> bool:
    trig_re = r'.*rock and stone.*'
    text = comment.body

    # Check if matches rock and stone, not our comment (or from ignored user), and not one we've seen before
    if (re.match(trig_re, text, re.IGNORECASE | re.DOTALL)
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
    print("name main gonna run")
    main()



