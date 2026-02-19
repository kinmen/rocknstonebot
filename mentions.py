
import praw
import praw.models.util
from praw.models.reddit.subreddit import Subreddit

from main import RockAndStoneBot


class RockAndStoneBotMentionBot(RockAndStoneBot):

    def process_comment_stream(self, subreddit: Subreddit) -> None:
        for mention in praw.models.util.stream_generator(self.reddit.inbox.mentions, skip_existing=True):
            comment = self.reddit.comment(mention.id)
            self.handle_comment(comment)

    def should_reply(self, comment: praw.models.Comment) -> bool:
        """Determine if we should reply to the comment."""
        return all([
            not self.is_ignored_user(comment),
            not self.already_replied(comment)
        ])


rnsbot = RockAndStoneBotMentionBot()
rnsbot.main()
