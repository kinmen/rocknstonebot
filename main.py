import logging
import logging.config
import praw
import prawcore
import random
import re
from typing import Generator, Optional

import config

# Configure logging
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Precompile regex pattern for efficiency
ROCK_AND_STONE_REGEX = re.compile(
    r'.*rock and stone.*',
    flags=re.IGNORECASE | re.DOTALL
)


class RockAndStoneBot:

    def __init__(self):
        self.reddit, self.subreddit = self.initialize_reddit_client()

    def main(self) -> None:
        """Main entry point for the Reddit bot."""
        self.process_comment_stream(self.subreddit)
        # for mention in praw.models.util.stream_generator(self.reddit.inbox.mentions, skip_existing=True):
        #     print(f"{mention.author}\\n{mention.body}\\n")
        #     count += 1

    def initialize_reddit_client(self) -> tuple[praw.Reddit, praw.models.Subreddit]:
        """Initialize and configure the Reddit client."""
        reddit = praw.Reddit(**config.REDDIT_CONF)
        me = reddit.user.me()
        config.IGNORED_USERS.add(me.name)  # Add bot to ignored users
        return reddit, reddit.subreddit(config.SUBREDDIT)

    def process_comment_stream(self, subreddit: praw.models.Subreddit) -> None:
        """Process comments from the subreddit stream."""
        logger.info(
            f"Monitoring comment stream in subreddit: {subreddit.display_name}")
        for comment in subreddit.stream.comments(skip_existing=True):
            self.handle_comment(comment)

    def handle_comment(self, comment: praw.models.Comment) -> None:
        """Process and potentially reply to a comment."""
        logger.debug(f"Checking comment: {comment.permalink}")

        if not self.should_reply(comment):
            return

        logger.info(
            f"Replying to comment ID: {comment.id}, Author: {comment.author}")
        try:
            reply_body = self.generate_reply()
            comment.reply(body=reply_body)
            comment.save()  # Mark as replied
        except praw.exceptions.RedditAPIException as e:
            handle_reddit_api_error(e, comment)
        except prawcore.exceptions.Forbidden as e:
            handle_forbidden_error(e, comment)

    def should_reply(self, comment: praw.models.Comment) -> bool:
        """Determine if we should reply to the comment."""
        return all([
            self.is_rock_and_stone_comment(comment),
            not self.is_ignored_user(comment),
            not self.already_replied(comment)
        ])

    def is_rock_and_stone_comment(self, comment: praw.models.Comment) -> bool:
        """Check if comment contains the target phrase."""
        return bool(ROCK_AND_STONE_REGEX.match(comment.body))

    def is_ignored_user(self, comment: praw.models.Comment) -> bool:
        """Check if comment author is in the ignored list."""
        return comment.author.name in config.IGNORED_USERS if comment.author else True

    def already_replied(self, comment: praw.models.Comment) -> bool:
        """Check if we've already replied to this comment or its ancestors."""
        return comment.saved or self.any_ancestor_replied(comment)

    def any_ancestor_replied(self, comment: praw.models.Comment) -> bool:
        """Check if any parent comment in the chain has been replied to."""
        for ancestor in self.iterate_comment_ancestors(comment):
            if ancestor.saved:
                logger.debug(f"Found replied ancestor: {ancestor.id}")
                return True
        return False

    def iterate_comment_ancestors(self, comment: praw.models.Comment) -> Generator[praw.models.Comment, None, None]:
        """Generator yielding all ancestors of a comment with periodic refreshes."""
        ancestor = comment
        refresh_counter = 0

        while not ancestor.is_root:
            ancestor = ancestor.parent()

            # Refresh every 9 ancestors to prevent stale data
            if refresh_counter % 9 == 0:
                ancestor.refresh()

            refresh_counter += 1
            yield ancestor

    def generate_reply(self) -> str:
        """Generate a random reply from configured options."""
        return random.choice(config.REPLIES)


def handle_reddit_api_error(exception: praw.exceptions.RedditAPIException, comment: praw.models.Comment) -> None:
    """Handle Reddit API exceptions."""
    for sub_exception in exception.items:
        if sub_exception.error_message == config.REDDIT_EXCEPTIONS['BLOCKED_PARENT_USER']:
            logger.warning(
                f"Blocked from replying to comment {comment.permalink} by user restriction"
            )
            return
    logger.exception(f"Reddit API error responding to {comment.permalink}")


def handle_forbidden_error(exception: prawcore.exceptions.Forbidden, comment: praw.models.Comment) -> None:
    """Handle forbidden exceptions (typically subreddit bans)."""
    logger.warning(
        f"Forbidden from replying in {comment.subreddit.display_name} "
        f"(comment {comment.id})"
    )


if __name__ == '__main__':
    rnsbot = RockAndStoneBot()
    rnsbot.main()
