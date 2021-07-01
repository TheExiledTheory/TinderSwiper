#My Tinder bot to alleviate my mental anguish ... or increase it. The base bot swipes based upon a 60% randomness factor 
#Written by Mark Cuccarese + last edited 6.11.21

''' imports '''
import Openers                         #<- Dictionary used for opening messages
from FeaturesClass import *            #<- Wrapper class dependancy
import time
import pprint
import random
import math
from datetime import datetime
import traceback
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
import logging
import colorama
from logging.config import fileConfig

#Not sure??? -> used in coordinate_generation() 
proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

#Setup the structure of logger object
logging.basicConfig(level = logging.WARNING, filename = 'log.txt', format = '%(asctime)s %(levelname)-12s: %(message)s')

class TindClass:
    ''' Prinary class that handles key app functionality '''

    #Class variables
    encounters_count = 0                            #Tracks total number of profiles encountered [SINCE RUN]
    encounters_count_current_cycle = 0 		        #Tracks total number of profiles encountered [BETWEEN HIBERNATIONS]
    likes = 0                                       #Track of the total number of likes through the session
    dislikes = 0                                     #Track of the total number of dis-likes through the session
    current_matches = 0                             #Traks the number of matches at the current moment of running the bot
    new_matches = 0                                 #Tracks the number of new matches since start of bot
    dict_match_info = {}                            #Dictionary to hold match info
    dict_self_info = {} 			                #Dictionary to hold general profile info
    dict_meta_info = {} 				            #Dictionary to hold meta profile on the account
    recommendation_list_length = 0                  #Gets length of the recommendation list
    current_lat = 0                                 #Base coord of users current 
    current_lon = 0                                 #Base coord of users current location
    range_list = []						            #Holds the coordinates for outter circle around current_lat and current_lon
    subscription = ["plus", "gold", "platinum"]     #Holds the type of subscription if any
    premium_flag = False                            #Tracks the users membership type
    purchase = None

    def __init__(self):
        '''Initialize all our starting data with time limited API calls'''

        print("Setting up initial bot with API calls ...\n")

        try: #Retrieve all the initial values for user

            self.dict_meta_info = FeaturesClass().get_meta()
            time.sleep(6)
            print("\tDone getting your profile's meta data ...\n")

            self.dict_match_info = FeaturesClass().get_match_info()
            time.sleep(6)
            print("\tDone getting your current match information ...\n")

            self.dict_self_info = FeaturesClass().get_self()
            time.sleep(6)
            print("\tDone getting your profiles data ...\n")

            #self.coordinate_generation()
            #time.sleep(6)
            #print("\tDone getting your current coordinates ...\n")

        except Exception as ex:
            print(ex)
            logging.warning(ex, exc_info = True)

        print("Done setting up initial values for you ...\n")
    #endd __init__

    def execute(self):
        '''Controller function for main loop '''
        '''Preform initial checks and begins indefinite swiping loop '''

        try: #Determine if has paid membership
            self.purchase = self.dict_meta_info['purchases'][0]['product_type']

        except: #Failed to get membership type - default none
            self.purchase = None

        #Set flag type
        if (self.purchase in self.subscription):
            print(f"Your account has a subscription of type -> {self.purchase}\n")
            self.premium_flag = True

        else:
            print("Your account has no paid subscription\n")

        #Check premium flag
        if (self.premium_flag):

            #Get users current location
            self.coordinate_generation()

        #self.dict_match_info

        #Generate info on current matches
        self.current_matches = len(self.dict_match_info)

        #Track profiles between hibernation cycles
        self.encounters_count_current_cycle = 0

        #Go through a random number of profiles
        if (self.premium_flag == True):
            rand = random.randint(250, 500)
        if (self.premium_flag == False):
            rand = random.randint(80, 100)

        print("Random profile goal chosen -> " + str(rand) + " total swipes\n")

        #Infinite loop
        while True:

            try:
                print(f"Total profiles swiped since bot start -> {self.encounters_count}\n")

                #Call to swipe loop
                self.main()

                #SHOULD IMPLEMENT A CHECK FOR PREMIUM HERE -> IN THE EVENT THAT A USERS PREMIUM HAS EXPIRED WHILE RUNNING BOT!!!!!

                if (self.premium_flag):
                    print(f"Now checking if swipes [{self.encounters_count_current_cycle}] > goal [{rand}] ... \n")
                else:
                    print(f"Now checking if likes [{self.likes}] > goal [{rand}] ... \n")

                #Check to see that we hit our swipe goal and user has unlimited swipes
                if (self.encounters_count_current_cycle > rand and self.premium_flag == True):

                    #Handle messaging of new matches
                    self.matchMessenger()

                    #Hibernate bot
                    self.hibernationClock()

                    #Reset counter
                    self.encounters_count_current_cycle = 0

                    print(f"Resuming from hibernation stats: likes: {self.likes} dislikes: {self.dislikes} total profiles: {self.encounters_count}\n")
                    rand = random.randint(250, 500)
                    print("New random goal chosen: " + str(rand) + "\n")

                #Check to see if we hit our like goal and user is not premium
                if (self.likes > rand and self.premium_flag == False):

                    #Handle messaging of new matches
                    self.matchMessenger()

                    #Hibernate bot
                    self.hibernationClock()

                    print(f"Resuming from hibernation stats: likes: {self.likes} dislikes: {self.dislikes} total profiles: {self.encounters_count}\n")

                    #Reset counters
                    self.likes = 0
                    self.dislikes = 0
                    self.encounters_count_current_cycle = 0

                    rand = random.randint(80, 100)
                    print("New random goal chosen: " + str(rand) + "\n")


            except Exception as ex:
                print(ex)
                print("Exception saved to log file!\n")
                logging.warning(ex, exc_info = True)
                exit()
    #end execute


    def main(self):
        '''Function to preform actual swiping'''
        try: #Attempt to get recommendation list
            recommendations = FeaturesClass().get_recommendations()
            try:  #Check for an expired key
                if ('error' in recommendations):

                    print("Possible 401 reponse error - may be the auth token...\n")

                    #Check the response from function
                    if (FeaturesClass().checkResponse(401) == True):

                        #Update data sets
                        sleep(4)
                        recommendations = FeaturesClass().get_recommendations()
                        recs = recommendations['results']
                        local_count = 1
                        self.recommendation_list_length = len(recs)

                #This is the case where no recommendations are left
                if('recs timeout' in recommendations):
                    #location_changer()
                    self.recommendations_list_length = 0

                #Get the actual people from list
                if ('results' in recommendations) :
                    recs = recommendations['results']
                    local_count = 1
                    self.recommendation_list_length = len(recs)

            except Exception as ex:
                print(ex)
                print("Exception saved to log file!\n")
                logging.warning(ex, exc_info = True)

        except Exception as ex:
            print(ex)
            print("Exception saved to log file!\n")
            logging.warning(ex, exc_info = True)

        #Check for case of no more recommendations
        if (self.recommendation_list_length == 0):

            #Possible infinite loop :)
            while (self.recommendation_list_length == 0):

                try:  #Check if the user can change location using API
                    if (self.premium_flag):
                        print(f"Your account has a paid subscription of type-> {self.purchase}\n")
                        self.location_changer()
                    else:
                        print("No recommendations and cannot change location. Exiting.\n")
                        exit()

                except Exception as ex:
                    print(ex)
                    print("Exception saved to log file!\n")
                    logging.warning(ex, exc_info = True)


                try:  #Attempt to break out of loop
                    sleep(20)
                    recs = get_recommendations()["results"]
                    local_count = 1
                    self.recommendation_list_length = len(recs)

                except Exception as ex:
                    print(ex)
                    print("Exception saved to log file!\n")
                    logging.warning(ex, exc_info = True)

        print("Total recomamnedations this iteration: " + str(self.recommendation_list_length))
        print("\n\t--------------------------------\n")

        #Loop through each person in the recommendations set
        for person in recs:


            #self.instance = Tensor(person)
            #self.instance = Tensor(person)
            #CALL THE ACTUAL ALGORITHM ONCE TRAINED TO GET A SCORE FOR THE PERSON
            #Make sure to notate in source that the person needs alot of space because it downloads a ton of images and they need to manually select who they like and dislike -> this part of bot is manual.
            #May need to catch keyboard interrupt in main and call a static function/destructor to close text file


            self.encounters_count += 1

            print(f"\tTotal profiles swiped: {self.encounters_count}")
            print("\tCurrent profile number: " + str(local_count) + "/" + str(self.recommendation_list_length) + "\n")

            try: #Get the details about recommendation
                person_id = person["_id"]
                person_bio = person["bio"]
                person_name = person["name"]
                person_distance = person["distance_mi"]
                person_match = person['group_matched']
                person_age = FeaturesClass().calculate_age(person['birth_date'])

            except Exception as ex:
                print(ex)
                print("Exception saved to log file!\n")
                logging.warning(ex, exc_info = True)

            #Generate a random like percentage
            rand = random.randint(0,100)

            #Like chane 60% of time
            if rand > 40:

                try:    #Attempt to like the person
                    FeaturesClass().like(person_id)

                    print(f"\tName: {person_name.upper()}")
                    print(f"\tDistance: {person_distance}")
                    print(f"\tAge: {person_age}")
                    print(f"\tThey liked us: {person_match}")
                    print(f"\tBio: {person_bio}")
                    #print(f"\t{Fore.BLUE}Liked with randomness chance of: {rand}%{Style.RESET_ALL}\n")
                    print(f"\tLiked with randomness chance of: {rand}%\n")
                    
                    self.likes += 1

                except Exception as ex:

                    print(ex)
                    print("Exception saved to log file!\n")
                    logging.warning(ex, exc_info = True)
            else:

                try: #Attempt to dislike person
                    FeaturesClass().dislike(person_id)

                    print(f"\tName: {person_name.upper()}")
                    print(f"\tDistance: {person_distance}")
                    print(f"\tAge: {person_age}")
                    print(f"\tThey liked us: {person_match}")
                    print(f"\tBio: {person_bio}")
                    print(f"\tDisliked with randomness chance of: {rand}%\n")
                    #print(f"\t{Fore.RED}Disiked with randomness chance of: {rand}%{Style.RESET_ALL}\n")


                    self.dislikes += 1

                except Exception as ex:

                    print(ex)
                    print("Exception saved to log file!\n")
                    logging.warning(ex, exc_info = True)

            local_count += 1

            print(f"\tTotal encounters: {self.encounters_count}")
            print(f"\tTotal likes: {self.likes}")
            print(f"\tTotal dislikes: {self.dislikes}")

            #Sleep function for swipes
            nap_length = random.random() * random.randint(5,40)

            print(f"\tSleepy time-> {round(nap_length, 2)} seconds.\n")
            print("\t--------------------------------\n")
            sleep(nap_length)


        #Keep tracking the total number of encounters during this session - to know when to hibernate
        self.encounters_count_current_cycle  += local_count
    #end main

    #This is a debugger function to break down nested dictionaries from json responses
    def nested_dictionary(self):

        #For ever key value pair in the dic
        for i, value in d.items():

            #Check if the value is a dictionary
            if (isinstance(value, dict)):

                #If it is print the key and go recursive
                print(f"    KEY:  {i}")
                self.nested_dictionary(value)

                #Once we hit a single key value pair - print
            else:
                print("{} : {}".format(i, value))
    #end nested_dictionary


    def matchMessenger(self):
        '''This function checks for new messages and sends a random opener '''

        #Update match and self info
        self.dict_match_info = FeaturesClass().get_match_info()
        sleep(4)
        self.dict_self_info = FeaturesClass().get_self()

        try: #Calculate new matches since start of program
            if (len(self.dict_match_info) > self.current_matches):
                self.new_matches = len(self.dict_match_info) - self.current_matches

        except Exception as ex:
            print(ex)
            print("Exception saved to log file!\n")
            logging.warning(ex, exc_info = True)

        print(f"New matches since start of program: {self.new_matches}")
        print(f"Total matches waiting to f*ck ;) {self.current_matches}")

        try:
            #Get each match into a list
            match_id_list = list(self.dict_match_info.keys())

            #Loop through each match
            for match in match_id_list:

                #Setup the values for the current match
                match_name = self.dict_match_info[match]['name']
                match_messages = list(self.dict_match_info[match]['messages'])
                match_message_count = len(match_messages)

                print("-------------------------------")
                print(f"\tMatch name: {match_name}")
                print(f"\tMatch message count: {match_message_count}\n")
                #print(f"\tMatch messages: {match_messages}")

                #Print the message history they sent to me
                #print(list(filter(lambda to: to['to'] == self_dict['_id'], match_messages)))

                #Determine if we have any message history with them
                if (match_message_count > 0):

                    print("\t----Message history----\n")
                    for index, value in enumerate(match_messages):

                        their_messages = []
                        my_messages = []

                        #Get all their messages
                        if (value['from'] == match):
                            print(match_name + ": " + str(value['message'] + "\n"))

                        #Get all my messages
                        if(value['to'] == match):
                            print("Me: " + str(value['message'] + "\n"))

                    print("\t----End Message history----\n")

                    #Check to see if they sent the last message
                    if (match_messages[match_message_count - 1]['from'] == match):

                        #Check to see if the last message was a gif
                        if ('gif' in match_messages[match_message_count - 1]['message']):
                            None
                            #send_msg(match, "lol")

                        #Respond with a generated message
                        print("They sent the last message ... should respond.")
                        #send_msg(match, "message")

                    else:
                        print(f"{match_name} has not responded we since last message was sent.")

                #Send them a random intro message
                else:
                    print("No previous message history...we should send a message.")
                    #send_msg(match, "message")

                #Add additional checks
                #->  harvest images to determine if unmatch
                #->  harvest distance to determine if unmatch
            print("-------------------------------\n")

        except Exception as ex:
            print(ex)
            print("Exception saved to log file!\n")
            logging.warning(ex, exc_info = True)


        #Factor in the new matches to our data set
        self.current_matches += self.new_matches
        self.new_matches = 0
        print(f"Total current matches: {self.current_matches}")
    #end matchMessenger


    def hibernationClock(self):
        '''This function handles hibernation of bot '''

        #Setup parameters
        now = datetime.now()
        starttime = now.replace(hour = 6, minute = 0, second = 0, microsecond = 0)
        endtime = now.replace(hour = 22, minute = 0, second = 0, microsecond = 0)

        #Check if it is 6am - 10pm
        if (now > starttime and now < endtime):
            #Sleep for 3-6
            print("Day time detected!")
            rand = 1.02352362345234 * random.randint(1,8)
            print("Random hour amount chosen: " + str(rand))
            print(f"Hibernating for {rand * 3600} seconds ... be back shortly :)")
            sleep(rand * 3600)
        else:
            #Sleep for 10-14 hours
            print("Night time detected!")
            rand = 1.08932288821456 * random.randint(8,14)
            print("Random hour amount chosen: " + str(rand))
            print(f"Hibernating for {rand * 3600} seconds ... be back shortly :)")
            sleep(rand * 3600)
        #end hibernationClock


    '''
    -> This function will attempt to change your location if you do not get recommendations
    -> This function is also contigent on the fact that you have tinder +
    -> This function is problematic - imagine your hometown is Miami and the algoirthm selects a random coord that in the Atlantic and it does that over and over -> I tried to fix this problem by only allowing coords within range of values but it goes off of the current coords listed on profile, this could be an issue if your profile is set to a passport location at the time of running the program
    '''
    @classmethod
    def location_Changer(self):
        lat_range = []      #Holds the range of latitude from current_lat to max range
        lon_range = []      #Holds the range of longitude from current_lon to max range
        true_range = []     #Holds the RANDOMLY CHOSEN max range coordinates of lat and lon

        try: #Get the data on profile
            self.dict_meta_info = FeaturesClass().get_meta()

            #Get current location of profile
            try:
                #The dictionary will contain 'admin_level' if within the states
                if ('administrative_area_level_1' in self.dict_meta_info['travel']['travel_location_info'][0]):
                    location = self.dict_meta_info['travel']['travel_location_info'][0]['administrative_area_level_1']['long_name']
                #Outside the states?
                else:
                    location = self.dict_meta_info['travel']['travel_location_info'][0]['country']['long_name']

            except Exception as ex:
                print(ex)
                print("Exception saved to log file!\n")
                logging.warning(ex, exc_info = True)


            print(f"Present location -> State: {location}\n")
            print(f"Present coordinates-> Lat:{self.current_lat} Lon:{self.current_lon}\n")
            print("Attempting to update coordinates to refresh swiping options...\n")

            #Select a random index from the list
            selected_index = random.randrange(len(self.range_list))

            #Select the target MAX range
            true_range = list(self.range_list[selected_index])

            #Swap around the values to the correct format
            temp1 = true_range[0]
            temp2 = true_range[1]
            true_range[0] = temp2
            true_range[1] = temp1

            #Set starting and ending range for random location
            lat_range.append(self.current_lat)
            lat_range.append(true_range[0])
            lon_range.append(self.current_lon)
            lon_range.append(true_range[1])


            #Generate a random coord within range
            latty = random.uniform(lat_range[0], lat_range[1])
            lonny = random.uniform(lon_range[0], lon_range[1])

            print(f"Randomly chosen coordinates to switch to-> {latty} {lonny}")

            #Saving current coordinates to check for success 
            previous_lat = self.current_lat
            previous_long = self.current_lon 


            try:  #Attempt to change user location
                FeaturesClass().update_location(latty, lonny)
                
                #If successfully, update will be reflected 
                self.current_lat = latty
                self.current_lon = lonny 
                
            except Exception as ex:
                print(ex)
                print("Exception saved to log file!\n")
                logging.warning(ex, exc_info = True)

            #Check for success
            if (previous_lat != self.current_lat and previous_long != self.current_lon):
                print("Successfully switched location\n")
            else: 
                print("Location switching may have failed\n")

        except Exception as ex:
            print(ex)
            print("Exception saved to log file!\n")
            logging.warning(ex, exc_info = True)

    #end location_changer
    
    @classmethod
    def geodesic_point_buffer(self, lat, lon, km):
        '''Function sourced from https://gis.stackexchange.com/questions/289044/creating-buffer-circle-x-kilometers-from-point-using-python '''
        # Azimuthal equidistant projection
        aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'

        project = partial(
            pyproj.transform,
            pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
            proj_wgs84)

        buf = Point(0, 0).buffer(km * 1000)  # distance in meters

        return transform(project, buf).exterior.coords[:]
    #end geodesic_point_buffer

    @classmethod
    def coordinate_generation(self):
        '''Generates base coordinates at start of bot '''

        self.dict_meta_info = FeaturesClass().get_meta()
        sleep(6)
        self.dict_self_info = FeaturesClass().get_self()

        try:
            if (self.dict_meta_info['travel']['is_traveling'] == True):

                #Get base coords at start of bot
                self.current_lat = self.dict_meta_info['travel']['travel_location_info'][0]['lat']
                self.current_lon = self.dict_meta_info['travel']['travel_location_info'][0]['lon']
            else:

                self.current_lat = self.dict_self_info['pos']['lat']
                self.current_lon = self.dict_self_info['pos']['lon']

        except Exception as ex:
            print(ex)
            print("Exception saved to log file!\n")
            logging.warning(ex, exc_info = True)
            return

        print(f"\tPresent coordinates[START OF SCRIPT]-> Lat:{self.current_lat} Lon:{self.current_lon}")

        #Generate a circular range of maximum cordinates (passes 50miles in km)
        self.range_list = self.geodesic_point_buffer(self.current_lat, self.current_lon, 80.4672)

        print("\tGeneration of coordinate range completed.\n")
    #end coordinateGeneration


if __name__ == "__main__":

    #Create a class instance and call main loop
    classInstance = TindClass()
    classInstance.execute()
