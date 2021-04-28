# MF DOOM Bot (aka doom_bot_)

<p align="center">
  <img src="https://github.com/rob-field/doom_bot_/blob/master/DOOM.jpeg" />
</p>

A reddit bot that searches for comments mentioning MF DOOM, and if the user has failed to capiltalise the name (i.e. mf doom, MF doom etc.), corrects them.
If the user has referenced the late rate correctly the bot will reply with a random choice of MF DOOM lyrics.  

The bot filters through the comment stream of certain music related subreddits and utilises REGEX to look for specific pattern matches, then responds appropriately. The comment ID is then added to an SQLite dataset to ensure that comments aren't replied to more than once.

Given that users are able to edit their comments within 3 minutes of posting without record, I also implented a scheduler using the multiprocessing and time modules. The bot runs for a set period of time (60 seconds), is then terminated and sleeps for another period of time (300 seconds) after which it is restarted. This hopefully prevents the bot from replying to comments that are less than 3 minutes old. 



# Package Requirements
Python 3.8.5  
praw  
SQLAlchemy  
dataset  
