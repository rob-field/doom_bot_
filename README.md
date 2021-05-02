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


# Changelog
- 3.0.0 
  - Changed doom_bot_ to allow deployment from Heroku
- 2.0.0
  - Added bot scheduler and multiprocessing to prevent overloading with requests
- 1.2.0 
  - doom_bot_ now checks the age of each comment before replying, utilising datetime and timedeltas
  - If comments aren't older than 3 minutes, the bot won't reply
- 1.1.2
  - Fixed REGEX issue
- 1.1.1
  - Fixed issue where bot would reply to comments with the inappropriate response
- 1.1.0
  - doom_bot_ now replies to comments containing "MF DOOM" (no lowercase letters) with a random choice from a selection of MF DOOM lyrics
- 1.0.0 
  - doom_bot_ replies to comments where "MF DOOM" contains at least one lowercase letter with the reply: "Just remember ALL CAPS when you spell the man name!"
