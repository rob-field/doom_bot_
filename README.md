# MF DOOM Bot (aka doom_bot_)

<p align="center">
  <img src="https://github.com/rob-field/doom_bot_/blob/master/DOOM.jpeg" />
</p>
https://www.reddit.com/user/doom_bot_/  <br></br>
A reddit bot that searches for comments mentioning MF DOOM, and if the user has failed to capiltalise the name (i.e. mf doom, MF doom etc.), corrects them.
If the user has referenced the late rate correctly the bot will reply with a random choice of MF DOOM lyrics.  

The bot filters through the comment stream of certain music related subreddits and utilises REGEX to look for specific pattern matches, then responds appropriately. The comment ID is then added to an SQLite dataset to ensure that comments aren't replied to more than once.

Given that users are able to edit their comments within 3 minutes of posting without record, I was able to check the  age of the comments using a datetime delta and the unique comment unix timestamp, thus preventing the bot from replying to comments that are less than 3 minutes old. Furthermore I implemented a scheduler using the multiprocessing and time modules, to prevent overloading the bot with requests (although unlikely given the limited number of subreddits it is searching). The bot only runs for a set period of time (60 seconds), is then terminated and sleeps for another period of time (120 seconds) after which it is restarted. 
<br></br>

# Package Requirements
Python 3.8.5  
praw  
SQLAlchemy  
dataset  
datetime  
