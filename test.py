import praw
import re
from datetime import datetime, timedelta

reddit = praw.Reddit('bot1')


def tester():

    subreddit = reddit.subreddit("LivestreamFail")

    for comment in subreddit.stream.comments():
        now = datetime.now()
        t1 = datetime.fromtimestamp(comment.created_utc)
        age = now - t1
        t2 = timedelta(seconds=180)
        if age < t2:
            print(comment.body)
        else:
            pass


def test2():

    string = ["MF DOOM",
              "mf DOOM",
              "GHJ",
              "HUBIHE",
              "MF DOOM",
              "of MF DOOM",
              "remember ALL CAPS when you spell the mans name. MF DOOM",
              "hello there mf dOoM",
              "mf doom",
              "remember ALL CAPS when you spell the mans name. MF DOOM",
              "ALL CAPS when you spell the mans name. mf doom"]

    for comment in string:

        r = re.findall("(mf doom)", comment, re.IGNORECASE)
        if re.search("[mfdom]+", str(r)):
            print(comment)



test2()
