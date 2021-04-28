# MF DOOM Bot (aka doom_bot_)

![alt text](https://github.com/rob-field/doom_bot_/blob/master/DOOM.jpeg)

A reddit bot that searches for comments mentioning MF DOOM, and if the user has failed to capiltalise the name (i.e. mf doom, MF doom etc.), corrects them.
If the user has referenced the late rate correctly the bot will reply with a random choice of MF DOOM lyrics.  

The bot filters through the comment stream of certain music related subreddits and utilises REGEX to look for specific pattern matches, then responds appropriately. The comment ID is then added to an SQLite dataset to ensure that comments aren't replied to more than once.



# Package Requirements
Python 3.8.5  
praw  
SQLAlchemy  
dataset  
