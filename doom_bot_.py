import praw
from prawcore import Forbidden, ResponseException
import re
import time
import random
import multiprocessing
from datetime import datetime, timedelta
import os
import requests
from sqlalchemy import create_engine, String, Column, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Initialise the reddit instance
# Credentials are stored in a praw.ini file
# reddit = praw.Reddit('bot1')

# When deploying with Heroku use environmental variables
reddit = praw.Reddit(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    username=os.environ['USERNAME'],
    password=os.environ['PASSWORD'],
    user_agent="MF_DOOM"
)


# Selection of MF DOOM Lyrics
DOOM_LYRICS = ["Catch a throatful from the fire vocal \n\n Ash and molten glass like Eyjafjallajökull",
               "One for the money, two for the better green \n\n 3-4-methylenedioxymethamphetamine \n\n "
               "Told the knock kneed ghetto queen get the head fiend \n\n Tell him it's for Medallin and use "
               "oxcyocetaline",
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
               "Out of work jerks since they shut down Chippendales",
               "Spit so many verses sometimes my jaw twitches \n\n One thing this party could use is more... booze",
               "Couldn't find a pen, had to think of a new trick \n\n This one he wrote in cold blood with a toothpick",
               "There's four sides to every story \n\n If these walls could talk, they'd probably still ignore me",
               "You ain't know he sell hooks and choruses? \n\n They couldn't bang slang if they looked in thesauruses",
               "Hold the cold one \n\n Like he hold the old gun \n\n Like he hold the microphone \n\n "
               "And stole the show for fun",
               "Crime pays, no dental nor medical \n\n Unless you catch retirement \n\n County, state, or federal",
               "Make no mistake son, it's Jake One \n\n He makes beats well like I likes my steaks done",
               "Simply smashing in a fashion that's timely \n\n Mad Villain dashing in a beat rhyme crime spree",
               "Money comes and goes like that two bit hussy that night that tried to rush me \n\n "
               "Dwight pass the dutchie \n\n So I can calm down so they don't get it twisted \n\n "
               "Take it from the fire side it won't get blistered",
               "Told the streets, 'What you staring at?' \n\n The sewer cap opened up and said, 'Why you wearing that?'",
               "A shot of Jack got her back it's not an act stack \n\n "
               "Forgot about the cackalack, holla back, clack clack blocka \n\n "
               "Villainy, feel him in ya heart chakra, chart toppa \n\n Start shit stoppa be a smart shoppa"
               ]


uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


engine = create_engine(uri, convert_unicode=True, pool_pre_ping=True)  # Creating an engine object to connect to the database
# Creating a session object to provide access when querying the database
db_session = (sessionmaker(bind=engine))
db_session = db_session()

Base = declarative_base()  # A base class that can be used to declare class definitions which define the database tables


class MyTable(Base):
    __tablename__ = "replied_to"  # Name of the database table
    # __table_args__ = {'extend_existing': True}  # Specifies that a table with this name already exists in the database

    comment_id = Column(String, primary_key=True)  # Primary key acts as a unique identifier for each database entry

    def __init__(self, comment_id):  # Assigning the appropriate attribute names to each column header of the table
        self.comment_id = comment_id


Base.metadata.create_all(bind=engine, checkfirst=True)


# Main function
def doom_bot():

    # Selection of subreddits to search
    subreddit = reddit.subreddit("90sHipHop+freshalbumart+hiphop+Hiphopcirclejerk+HipHopImages+hiphopvinyl+"
                                 "ifyoulikeblank+MetalFingers+mfdoom+MFDOOMCIRCLEJERK+Music+rap+"
                                 "treemusic+Bossfight+ListenToThis+DubStep+AlbumArtPorn+Audiophile+"
                                 "OFWGKTA+chillmusic+Spotify+triphop+musicnews+Grime+altrap+backpacker+"
                                 "ukhiphopheads+hiphoptruth+asianrap+80sHipHop+backspin+hiphopheadsnorthwest+"
                                 "hiphop101+NYrap+raprock+rhymesandbeats+rapverses+undergroundchicago+LofiHipHop+"
                                 "doom_bot_")

    # Ban list - HipHopHeads, makinghiphop, LetsTalkMusic

    # Searching through each comment, checking if the ID is already in the database
    # If not check for appropriate pattern and capitalisation (or lack thereof), respond appropriately
    for comment in subreddit.stream.comments():
        # Check if the comment is older than 180 seconds
        now = datetime.now()
        t1 = datetime.fromtimestamp(comment.created_utc)
        age = now - t1
        t2 = timedelta(seconds=180)
        test = timedelta(seconds=5)

        if age > test:

            # if not comment.saved:

            query = db_session.query(MyTable).filter(MyTable.comment_id == comment.id).all()
            # query = db_session.query(MyTable).filter(MyTable.comment_id.contains(comment.id)).all()

            if query.count() == 0:

                r = re.findall("(mf doom)", comment.body, re.IGNORECASE)

                if re.search("[mfdo]+", str(r)):

                    doom_bot_reply = "Just remember ALL CAPS when you spell the man name!"
                    comment.reply(doom_bot_reply + "\n***\n" + "^^I ^^am ^^a ^^bot.")

                    comment.save()

                elif re.search("MF DOOM", str(comment.body)):
                    comment.reply(random.choice(DOOM_LYRICS) + "\n" + "***" + "\n" + "^^I ^^am ^^a ^^bot.")

                    comment.save()


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
        except ResponseException as e:
            print("ERR: {}".format(e))
            time.sleep(200)
        except Forbidden as e:
            print(print("ERR: {}".format(e)))
        except requests.exceptions.ConnectionError as e:
            print("ERROR: Reddit is down...")
            time.sleep(200)  # sleep because reddit is down
        except Exception as e:
            print("ERR: {}".format(e))
            exit(1)


if __name__ == '__main__':
    print("Off we go...")
    scheduler()
