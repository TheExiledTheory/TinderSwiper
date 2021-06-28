# DISCLAIMER: This project is mostly finalized. Nevertheless, at any point in time, Tinder can change one little thing on the backend of their API and it can break the bot. This currently posted version of the bot is not perfect either; the bot as of now is SEMI-AUTONOMOUS and swipes based upon a randomness factor. I do not have a work around for updating the the auth key automatically. I amslowly working implementing a machine learning algorithm in order to swipe based on an ai determined score. I have included a documentation pdf which will provide some insight on how to obtain your X-AUTH-KEY and run the bot. 

# Description: 
My initial inspiration for this project was because I wanted to get the results from Tinder without swiping in the toxic piss-pit of an app. I noticed that I was putting more time and primarily more effort into it without getting anything in return from it. So with this approach I can use it from time to time when I am uniquely bored but and it will passively run when I don't care to use it. This bot does not amplify the quality or quantity of your matches beyond what it is to begin with, it just swipes for you. So whatever kind of matches you were initially getting, you will continue to get...just without any effort :) 
    

## Last successful test: 06/12/2021
    Distro Debian GNU/Linux 9
    Python 3.8.6

# General information: 

    * Before running this program, you want to make sure you update your X-AUTH-TOKEN as shown in the documentation. 
    * The X-AUTH-TOKEN is nothing more than a key witch authenticates requests made to the Tinder API. 
    * To my knowledge a unique key is generated after a period of 7 days from issue time. This means the longest period of time that the bot will run on its own for is 7 days after which Tinder will revoke the token and issue a new one. 
    * If the urls for the API endpoints happen to change at any point at time, you cant attempt to update them yourself by using either Postman or Chrome dev tools. These tools will help clue you into what url's are needed for get/post requests and what parameters need to be sent with them. 
    * If ever an error/exception is encountered, it will print a vague error statement to console and it will also notate it in the log file and continue running. 
    * As I mention in the disclaimer...the user is still required to: (a) hold a conversation after a successful match (b) manually update stale api keys at least once a week
    * This works best with Tinder+ because you get to change your location and you get unlimited likes. 
    * The bot does support messaging, however it is only limited to a simple corny openers 
    
    *AVOIDING BANS/SHADOWN BANS* 
    
    * To avoid getting banned or shadow banned (shown to fewer people) you can take a few or all of the following steps 
    * 1. Use a spoofed IP that you haven't used before 
    * 2. Use a never used before Google/Facebook/Phone# ... Google voice is great for the phone number 
    * 3. Use different profile details - name / location / school / bio 
    * 4. Use brand new photos. Tinder collects and retains your photos and meta data from those photos. You can import your photos into Window and go to properties to remove meta data. For linux you can use [sudo mogrify -strip ./*jpeg] 
    * 5. Use a new or portable browser before making a new account and while using in order to clear cookies and browser fingerprint 
    
     
    
## TO DO: 
    1. Create a method for updating X-AUTH-TOKEN automatically 
    2. Implement an AI chat bot with a web hook for messaging matches  
    3. Setup a UI to use to display an interface similar to that of Tinder 
    
## DEPENDENCIES: 
    Python3 Libraries           [Colorama, shapely, pyproj, requests]


_Credit for api endpoints: https://github.com/fbessez/Tinder_
