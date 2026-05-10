"""
Problem: Design Twitter

Description:
Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed. Implement the Twitter class: postTweet, getNewsFeed, follow, unfollow.

Constraints:
1 <= userId, followerId, followeeId <= 500, 0 <= tweetId <= 10^4. At most 3 * 10^4 calls will be made.

Example:
Input: ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"] -> Output: [null, null, [5], null, null, [6, 5], null, [6]]
"""

class Twitter:
    def __init__(self):
        pass
    def postTweet(self, userId: int, tweetId: int) -> None:
        pass
    def getNewsFeed(self, userId: int) -> List[int]:
        pass
    def follow(self, followerId: int, followeeId: int) -> None:
        pass
    def unfollow(self, followerId: int, followeeId: int) -> None:
        pass
