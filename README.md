# DISCLAIMER: This project is mostly finalized but at any time Tinder can change one little thing on their backend API and it can break the whole bot. This currently posted version of the bot is not perfect either; the bot as of now is SEMI-AUTONOMOUS and swipes based upon a randomness factor. I do not have a work around for updating the the auth key automatically, however I am currently implementing a machine learning algorithm in order to swipe based on a 'prettiness score.' I have included a documentation pdf which will provide some insight on how to obtain your X-AUTH-KEY in order to setup the bot. 

# Description: 
My initial inspiration for this project was because I wanted to get the results (matches) from Tinder without swiping in the pure toxcicity of the app. I noticed that I was putting more time and primaryly more effort into it than I would care to admit and getting nothing from it. So with this approach I can use it from time to time when I am uniquely bord but I have no sweat off my back because I am able to match passively. This bot does not amplify the quality or quantity of your matches beyond what it was to begin with, it just swipes for you. So whatever kind of matches you were initially getting, you will continue to get...just without any effort :) 
    

## Last successful test: 06/12/2021
    Distro Debian GNU/Linux 9
    Selenium 4.0.0.a1
    Python 3.8.6
    Chromium 83.0.4103.116
    Chromedriver 83.0.4103.14

# General information: 

    * Before running this program, you want to make sure you update your X-AUTH-TOKEN as shown in the documentation. 
    * To my knowledge a unique key is generated after a period of 7 days from issue time. This means the longest period of time that the bot will run on its own for is 7 days after which Tinder will revoke the token and issue a new one. 
    * The X-AUTH-TOKEN is nothing more than a key witch authenticates requests made to the Tinder API. 
    * If the urls for the API endpoints happen to change at any point at time, you attempt to update them yourself by using either Postman or with Chrome dev tools. Chrome dev tools helps to clue you into what urls are needed for get/post requests and what parameters need to be sent. 
    * If ever an error/exception is encountered, it will print a vague error statement to console and it will also notate it in the log file. 
    * As I mention in the disclaimer...the user is still required to: (a) hold a conversation upon a successful match (b) manually update stale api keys at least once a week
    * As with any regular Tinder account, it work best with Tinder+ because you get to change your location and you get unlimited likes. 
    
    *AVOIDING BANS/SHADOWN BANS* 
     
    
## TO DO: 
    1. Create a method for updating X-AUTH-TOKEN automatically 
    2. Implement an AI chat bot with a web hook for messaging matches  
    3.   
    
## DEPENDENCIES: 
    PYPI Modules                [Arrow, Selenium, Time, Psutil, Datetime, etc...]
    Chrome webdriver            [That corresponds to your version of installed Chrome]
    Python 3+                   [This script is written in Python 3]
    Linux flavor of choice      [This can also be used on Windows but the included files are for Linux] 

_Credit: https://github.com/fbessez/Tinder_
