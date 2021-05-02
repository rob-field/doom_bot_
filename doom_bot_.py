import praw
import re
import time
import random
import multiprocessing
from datetime import datetime, timedelta
import os
from SQLA_init import init_db, db_session
from models import MyTable


# Initialise the reddit instance
# Credentials are stored in a praw.ini file
# reddit = praw.Reddit('bot1')
reddit = praw.Reddit(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    username=os.environ['USERNAME'],
    password=os.environ['PASSWORD'],
    user_agent="MF_DOOM"
)


# Initialise database
init_db()


# Selection of MF DOOM Lyrics, more to be added later if necessary
DOOM_LYRICS = ["Catch a throatful from the fire vocal \n\n Ash and molten glass like Eyjafjallajökull",
               "One for the money, two for the better green \n\n 3-4-methylenedioxymethamphetamine \n\n "
               "Told the knock kneed ghetto queen get the head fiend \n\n Tell him it's for Medallin and use"
               " oxcyocetaline",
               "Only in America could you find a way to earn a healthy buck and still keep your attitude on self "
               "destruct",
               "Wrote this lyric in the bed with a chick \n\n She had the tightest grip around the head of my... \n\n "
               "...Bic, now can I get my pen back? \n\n Get no enemy, got no friend, black",
               "Livin' off borrowed time, the clock ticks faster...",
               "Remember me God, clean timbs with emery board? \n\n He only came to save the game like a memory card",
               "DOOM nominated for the best rolled L's \n\n And they wondered how he dealt with stress so well",
               "Made his chrome dome glisten \n\n At first he couldn’t tell she had a chromosome missing \n\n "
               "He kept a spare somewhere, in his underwear he swear \n\n Then helped her get the gum out her hair",
               "What up? \n\n To all rappers: shut up with your shutting up \n\n "
               "And keep your shirt on, at least a button-up \n\n Yuck, is they rhymers or strippin' males? \n\n "
               "Out of work jerks since they shut down Chippendales"]


# Main function
def doom_bot():

    # Read
    replied_to = db_session.query(MyTable)

    # Selection of subreddits to search
    subreddit = reddit.subreddit("90sHipHop+freshalbumart+hiphop+Hiphopcirclejerk+HipHopImages+hiphopvinyl+"
                                 "ifyoulikeblank+MetalFingers+mfdoom+MFDOOMCIRCLEJERK+Music+rap+"
                                 "treemusic+Bossfight+ListenToThis+DubStep+AlbumArtPorn+Audiophile+"
                                 "OFWGKTA+LetsTalkMusic+chillmusic+Spotify+triphop+musicnews+Grime+altrap+backpacker+"
                                 "ukhiphopheads+hiphoptruth+asianrap+80sHipHop+backspin+hiphopheadsnorthwest+"
                                 "hiphop101+NYrap+raprock+rhymesandbeats+rapverses+undergroundchicago+LofiHipHop+"
                                 "doom_bot_")

    # Ban list - HipHopHeads, makinghiphop

    # Searching through each comment, checking if the ID is already in the database
    # If not check for appropriate pattern and capitalisation (or lack thereof), respond appropriately

    for comment in subreddit.stream.comments():
        # Check if the comment is older than 180 seconds
        now = datetime.now()
        t1 = datetime.fromtimestamp(comment.created_utc)
        age = now - t1
        t2 = timedelta(seconds=180)
        test = timedelta(seconds=10)

        if age > test:

            for reply in replied_to:
                if reply.comment_id is None:

                    r = re.findall("(mf doom)", comment.body, re.IGNORECASE)

                    if re.search("[mfdo]+", str(r)):

                        doom_bot_reply = "Just remember ALL CAPS when you spell the man name!"
                        comment.reply(doom_bot_reply + "\n***\n" + "^^I ^^am ^^a ^^bot.")

                        # Add ID to the database once done
                        add_reply = MyTable(comment_id=comment.id)
                        db_session.add(add_reply)
                        db_session.commit()

                        # data = dict(comment_id=str(comment.id))
                        # rt.insert(data)

                    elif re.search("MF DOOM", str(comment.body)):
                        comment.reply(random.choice(DOOM_LYRICS) + "\n" + "***" + "\n" + "^^I ^^am ^^a ^^bot.")

                        add_reply = MyTable(comment_id=comment.id)
                        db_session.add(add_reply)
                        db_session.commit()

                        # data = dict(comment_id=str(comment.id))
                        # rt.insert(data)

                    else:
                        pass
            else:
                pass
        else:
            pass


def scheduler():
    while True:
        try:
            # Run doom bot for 60 seconds
            # print("Doom bot running...")
            p = multiprocessing.Process(target=doom_bot,  name="doom_bot")
            p.start()
            time.sleep(60)

            # Terminate function
            p.terminate()

            # Sleep the bot for 120 seconds
            # print("Doom bot sleeping...")
            time.sleep(60)

            # Cleanup and rerun
            p.join()
        except Exception as e:
            print("ERR: {}".format(e))
            exit(1)

# if re.search("mf doom", str(comment.body)) and re.search("^(?=.*[a-z]+).",  str(comment.body)):


if __name__ == '__main__':
    print("Off we go...")
    scheduler()
