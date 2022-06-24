# DISCLAIMER: This project is no longer maintained. I strongly encourage you to take what I have written and improve upon it. Tinder can and most certainly will change the backend API endpoints at some point so know that they will need to be altered. You will also need to obtain your API key using Chrome Dev Tools. This bot, in its current state, is finalized but not perfect. The To-Do section notes the improvements I would like to have implemented.

# Description: 
My initial inspiration for this project was because I wanted to get the results from Tinder without swiping in the toxic piss-pit of an app. I noticed that I was putting more time and primarily more effort into it without getting anything in return from it. So with this approach I can use it from time to time when I am uniquely bored but and it will passively run when I don't care to use it. This bot does not amplify the quality or quantity of your matches beyond what it is to begin with, it just swipes for you. So whatever kind of matches you were initially getting, you will continue to get...just without any effort :) 
    

## Last successful test: 06/12/2021
    Distro Debian GNU/Linux 9
    Python 3.8.6

# General information: 
    
        NOTES
    
     * API keys (X-AUTH-TOKENS) change after a 1 week period - add yours into the source code before running
     * Use Postman and Chrome Dev Tools to update broken API endpoints 
     * Semi-Autonomous: (a) hold a conversation after a successful match (b) manually update stale api keys at least once a week
     * Tinder+ works best because the bot doesn't have to pause
     * Only corny liners are supported as messaging from the bot
    
        AVOIDING BANS/SHADOWN BANS
     
     1. Create an operate a new account from a spoofed IP 
     2. Use a brand new email, some fake email generators may work
     3. TextVerified.com (although cheaply paid) is an execellent service for SMS verification 
     4. Do not ever make your account exactly the same  
     5. Never use the same photos. Tinder actively collects and retains photos along with their meta data. Go through any photos and wipe all meta data
     6. If you buy Tinder+ ... always use different payment details. Use online virtual credit card if you need to.
    
     
    
## TO DO: 
    1. Create a method for updating X-AUTH-TOKEN automatically 
    2. Implement an AI chat bot with a web hook for messaging matches  
    3. Setup a UI to use to display an interface similar to that of Tinder 
    4. Implement a system for analysing profile pictures and assigning an 'attractiveness score' with ML 
    
## DEPENDENCIES: 
    Python3 Libraries           [Colorama, shapely, pyproj, requests]


_Credit for api endpoints: https://github.com/fbessez/Tinder_
