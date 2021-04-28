import praw
import re
from multiprocessing import Process, Pool
import dataset
import sqlalchemy
import time
import requests
import random

# Initialise the reddit instance
reddit = praw.Reddit('bot1')
# Create/connect to the database
db = dataset.connect('sqlite:///doom_db.db')

# create a table for commments that have been replied to
db.create_table('replied_to')
rt = db['replied_to']

# create the column for storing ids
db['replied_to'].create_column('comment_id', sqlalchemy.String)

# Selection of MF DOOM Lyrics, more to be added later if necessary
DOOM_LYRICS = ["Catch a throatful from the fire vocal \n\n Ash and molten glass like Eyjafjallajökull",
               "One for the money, two for the better green \n\n 3-4-methylenedioxymethamphetamine \n\n Told the knock kneed ghetto queen get the head fiend \n Tell him it's for Medallin and use oxcyocetaline",
               "Only in America could you find a way to earn a healthy buck and still keep your attitude on self destruct",
               "Wrote this lyric in the bed with a chick \n\n She had the tightest grip around the head of my... \n\n ...Bic, now can I get my pen back? \n\n Get no enemy, got no friend, black",
               "Livin' off borrowed time, the clock ticks faster...",
               "Remember me God, clean timbs with emery board? \n\n He only came to save the game like a memory card",
               "DOOM nominated for the best rolled L's \n\n And they wondered how he dealt with stress so well",
               "Made his chrome dome glisten \n\n At first he couldn’t tell she had a chromosome missing \n\n He kept a spare somewhere, in his underwear he swear \n\n Then helped her get the gum out her hair",
               "What up? \n\n To all rappers: shut up with your shutting up \n\n And keep your shirt on, at least a button-up \n\n Yuck, is they rhymers or strippin' males? \n\n Out of work jerks since they shut down Chippendales"]


# Main function
def doom_bot():

    # Selection of subreddits to search
    subreddit = reddit.subreddit("90sHipHop+freshalbumart+hiphop+Hiphopcirclejerk+HipHopImages+hiphopvinyl+"
                                 "ifyoulikeblank+makinghiphop+MetalFingers+mfdoom+MFDOOMCIRCLEJERK+Music+rap+"
                                 "treemusic+Bossfight+hiphopheads")

    # Searching through each comment, checking if the ID is already in the database
    # If not check for appropriate pattern and capitalisation (or lack thereof), respond appropriately
    for comment in subreddit.stream.comments():
        if rt.find_one(comment_id=comment.id) is None:
            if re.search("mf doom", str(comment.body), re.IGNORECASE) and re.search("^(?=.*[a-z]+).", str(comment.body)):
                doom_bot_reply = "Just remember ALL CAPS when you spell the man name!"
                comment.reply(doom_bot_reply + "\n***\n" + "^^I ^^am ^^a ^^bot.")

                # Add ID to the database once done
                data = dict(comment_id=str(comment.id))
                rt.insert(data)
            elif re.search("MF DOOM", str(comment.body)):
                comment.reply(random.choice(DOOM_LYRICS) + "\n" + "***" + "\n" + "^^I ^^am ^^a ^^bot.")
                data = dict(comment_id=str(comment.id))
                rt.insert(data)

            else:
                pass
        else:
            pass


# Running the bot and raising exceptions
def main():

    while True:
        try:
            doom_bot()
            print('Sleeping...')
            time.sleep(150)
        except requests.exceptions.ConnectionError as e:
            print("ERROR: Reddit is down...")
            time.sleep(150)  # sleep because reddit is down
        except Exception as e:
            print("ERR: {}".format(e))
            exit(1)


if __name__ == '__main__':
    main()
