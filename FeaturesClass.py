#Credit for the API methods goes to https://github.com/fbessez/Tinder
#This class holds all the actual implementation and functionality of API calls for the bot 

#I implemented checkResponse() and updateAuthKey() in this file to stream line updating the x-auth token and also formatted it into a class structure along with combined all the functions previously laid out in the linked github into a singular source file 


#This class manages all API calls 
from datetime import date, datetime
from random import random
from time import sleep
import json 
import requests 


get_headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
    "Accept": "application/json",
    "X-Auth-Token": 'KEYYYYYYYYYYYYYYYYYY'     #<--------------------- ENTER YOUR API KEY HERE 
}
headers = get_headers.copy()
#headers['content-type'] = "application/json"


class FeaturesClass: 

    def get_match_info(self):
        
        matches = self.get_updates()['matches']

        now = datetime.utcnow()
        match_info = {}
        for match in matches[:len(matches)]:
            try:
                person = match['person']
                person_id = person['_id']  
               
                match_info[person_id] = {
                    "name": person['name'],
                    "match_id": match['id'],  
                    "message_count": match['message_count'],
                    "photos": self.get_photos(person),
                    #"bio": person['bio'],
                    "gender": person['gender'],
                    #"avg_successRate": get_avg_successRate(person),
                    "messages": match['messages'],
                    "age": self.calculate_age(match['person']['birth_date']),
                    "distance": self.get_person(person_id)['results']['distance_mi'],
                    "last_activity_date": match['last_activity_date'],
                    }

            except Exception as ex:
                print(ex)
                #template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                #message = template.format(type(ex).__name__, ex.args)
                #print(message)
        return match_info

    def get_updates(self, last_activity_date=""):
        try:
            url = "https://api.gotinder.com" + '/updates'
            r = requests.post(url,
            headers=headers,
            data=json.dumps({"last_activity_date": last_activity_date}))

            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()

        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting updates:", e)


    #Returns a list of ids that have the same name as your input 
    def get_match_id_by_name(self, name, match_info):

        list_of_ids = []

        for match in match_info:

            if match_info[match]['name'] == name:
                list_of_ids.append(match_info[match]['match_id'])

        if len(list_of_ids) > 0:
            return list_of_ids
        
        return {"error": "No matches by name of %s" % name}

    #Returns a list of photo urls 
    def get_photos(self, person):

        photos = person['photos']
        photo_urls = []
        
        for photo in photos:
            
            photo_urls.append(photo['url'])
            
        return photo_urls

    #Converts from '1997-03-25T22:49:41.151Z' to an integer (age)
    def calculate_age(self, birthday_string):
        
        birthyear = int(birthday_string[:4])
        birthmonth = int(birthday_string[5:7])
        birthday = int(birthday_string[8:10])
        today = date.today()
        
        return today.year - birthyear - ((today.month, today.day) < (birthmonth, birthday))
    
    #Finds the last activity date 
    def get_last_activity_date(self, now, ping_time):
        
        ping_time = ping_time[:len(ping_time) - 5]
        datetime_ping = datetime.strptime(ping_time, '%Y-%m-%dT%H:%M:%S')
        difference = now - datetime_ping
        since = convert_from_datetime(difference)
        return since
    
    #Find how long it has been 
    def how_long_has_it_been(self, match_info):
        now = datetime.utcnow()
        times = {}
        for person in match_info:
            name = match_info[person]['name']
            ping_time = match_info[person]['last_activity_date']
            since = get_last_activity_date(now, ping_time)
            times[name] = since
            print(name, "----->", since)
        return times

    #Returns a list of users that you can swipe on
    def get_recommendations(self):
        
        try:
            r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting recomendations:", e)


    #Returns information on your own profile 
    def get_self(self):
        
        try:
            url = "https://api.gotinder.com" + '/profile'
            r = requests.get(url, headers=headers)
            
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
            
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your data:", e)
    
    #Returns all updates since the given activity date. The last activity date is defaulted at the beginning of time.
    def get_updates(self, last_activity_date=""):
    
        try:
            url = "https://api.gotinder.com" + '/updates'
            r = requests.post(url,
                              headers=headers,
                              data=json.dumps({"last_activity_date": last_activity_date}))
            
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
            
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting updates:", e)

    #Change profiles preferences 
    def change_preferences(self, **kwargs):
        '''
        ex: change_preferences(age_filter_min=30, gender=0)
        kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
        age_filter_min: 18..46
        age_filter_max: 22..55
        age_filter_min <= age_filter_max - 4
        gender: 0 == seeking males, 1 == seeking females
        distance_filter: 1..100
        discoverable: true | false
        {"photo_optimizer_enabled":false}
        '''
        try:
            url = 'https://api.gotinder.com' + '/profile'
            r = requests.post(url, headers=headers, data=json.dumps(kwargs))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not change your preferences:", e)
    
    #Returns all data on yourself and account 
    def get_meta(self):
        try:
            url = 'https://api.gotinder.com' + '/meta'
            r = requests.get(url, headers=headers)
            
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
            
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your metadata:", e)
    
    # A more detailed data excerpt from your profile and account 
    def get_meta_v2(self):
        try:
            url = 'https://api.gotinder.com' + '/v2/meta'
            r = requests.get(url, headers=headers)
            
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your metadata:", e)


    #Updates locations takes float coordinates 
    def update_location(self, lat, lon):
        try:
            url = 'https://api.gotinder.com' + '/passport/user/travel?locale=en'
            r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
            
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your location:", e)

    #Resets your profiles initial location 
    def reset_real_location(self):
        try:
            url = 'https://api.gotinder.com' + '/passport/user/reset?locale=en'
            r = requests.post(url, headers=headers)
            
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your location:", e)

    #Works more consistently because it seems to check location 
    def get_recs_v2(self):
        try:
            url = 'https://api.gotinder.com' + '/v2/recs/core?locale=en-US'
            r = requests.get(url, headers=headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except Exception as e:
            print('excepted')
            
    #Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
    def set_webprofileusername(self):
        try:
            url = 'https://api.gotinder.com' + '/profile/username'
            r = requests.put(url, headers=headers,
                             data=json.dumps({"username": username}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not set webprofile username:", e)
    #Resets the username for the webprofile
    def reset_webprofileusername(self, username):
    
        try:
            url = config.host + '/profile/username'
            r = requests.delete(url, headers=headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not delete webprofile username:", e)

    #Gets a user's profile via their id
    def get_person(self, id):
        try:
            url = 'https://api.gotinder.com' + '/user/%s' % id
            r = requests.get(url, headers=headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get that person:", e)
    
    #Send a message 
    def send_msg(self, match_id, msg):
        try:
            url = 'https://api.gotinder.com' + '/user/matches/%s' % match_id
            r = requests.post(url, headers=headers,
                              data=json.dumps({"message": msg}))
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not send your message:", e)
    
    #Unmatch with someone 
    def unmatch(self, match_id):
        try:
            url = 'https://api.gotinder.com' + '/user/matches/%s' % match_id
            r = requests.delete(url, headers=headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not unmatch person:", e)
    
    #Super like person 
    def superlike(self, person_id):
        try:
            url = 'https://api.gotinder.com' + '/like/%s/super' % person_id
            r = requests.post(url, headers=headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not superlike:", e)
    
    #Like person 
    def like(self, person_id):
        try:
            url = 'https://api.gotinder.com' + '/like/%s' % person_id
            r = requests.get(url, headers=get_headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not like:", e)
    
    #Dislike person 
    def dislike(self, person_id):
        try:
            url = 'https://api.gotinder.com' + '/pass/%s' % person_id
            r = requests.get(url, headers=get_headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not dislike:", e)
    
    #Report person 
    def report(self, person_id, cause, explanation=''):
        '''
        There are three options for cause:
            0 : Other and requires an explanation
            1 : Feels like spam and no explanation
            4 : Inappropriate Photos and no explanation
        '''
        try:
            url = 'https://api.gotinder.com' + '/report/%s' % person_id
            r = requests.post(url, headers=headers, data={
                              "cause": cause, "text": explanation})
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
            
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not report:", e)
    
    #Get info on match 
    def match_info(self, match_id):
        try:
            url = 'https://api.gotinder.com' + '/matches/%s' % match_id
            r = requests.get(url, headers=headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)
    
    #Get matches 
    def all_matches(self):
        try:
            url = 'https://api.gotinder.com' + '/v2/matches'
            r = requests.get(url, headers=headers)
            #Check the response before returning result 
            if (self.checkResponse(r.status_code) == True):
                return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)
    
    #Not sure 
    def fast_match_info(self):
      try:
          url = 'https://api.gotinder.com' + '/v2/fast-match/preview'
          r = requests.get(url, headers=headers)
          count = r.headers['fast-match-count']
          # image is in the response but its in hex..
          return count
      except requests.exceptions.RequestException as e:
          print("Something went wrong. Could not get your fast-match count:", e)
    
    #Lists trending gifs? 
    def trending_gifs(self, limit=3):
      try:
          url = 'https://api.gotinder.com' + '/giphy/trending?limit=%s' % limit
          r = requests.get(url, headers=headers)
          return r.json()
      except requests.exceptions.RequestException as e:
          print("Something went wrong. Could not get the trending gifs:", e)
    
    #Looks for gifs? 
    def gif_query(self, query, limit=3):
      try:
          url = 'https://api.gotinder.com' + '/giphy/search?limit=%s&query=%s' % (limit, query)
          r = requests.get(url, headers=headers)
          return r.json()
      except requests.exceptions.RequestException as e:
          print("Something went wrong. Could not get your gifs:", e)
    
    
    # def see_friends():
    #     try:
    #         url = config.host + '/group/friends'
    #         r = requests.get(url, headers=headers)
    #         return r.json()['results']
    #     except requests.exceptions.RequestException as e:
    #         print("Something went wrong. Could not get your Facebook friends:", e)
    
    
    
    
    
    
    
    #This function will check for known error codes in reponse 
    def checkResponse(self, code):

        if (code == 200):
            return True
        elif (code == 301):
            print(code)
            print("\n")
            print("The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint's name has changed.\n")
            exit(1) 
        elif(code == 400):
            print(code)
            print("\n")
            print("The server thinks you made a bad request. This can happen when you don't send the information the API requires to process your request, among other things.\n")
            exit(1)
        
        #IF WE HIT THIS WE MAY NEED TO UPDATE OUR KEY
        elif(code == 401):
            print(code)
            print("\n")
            print("The server thinks you're not authenticated. This happens when you don't send the right credentials to access an API\n")
            reponsenum = self.updateAuthKey()
            self.checkResponse(reponsenum)
            
        elif(code == 404):
            print(code)
            print("\n")
            print("The server didn't find the resource you tried to access.\n")
            exit(1)
        elif(code == 503):
            print(code)
            print("\n")
            print("Back-end server is at capacity.\n")
            exit(1)
        print("Auth key seems to be valid. Nice job.\n")
        return True 
        
    #This function should try to alter the value of headers xauth param
    def updateAuthKey(self, last_activity_date = ""):
        
        print("This x-auth-token may be stale...please enter a new one\n")
        
        #Add checks for this key 
        key = str(input("Enter auth token: "))
        
        #If they dont enter a key, exit 
        if (len(key) == 0):
            print("Key empty")
            print("Bye")
            exit(1)

        try:
            #Change the value currently held 
            token = str(headers['X-Auth-Token']) 
            
            #Open source file in read mode
            ffile = open("FeaturesClass.py", "rt")
            
            lines = ffile.read() 

            #Look for instances of old key 
            if token in lines: 
                #Copy all data and replace instance 
                flag = True 
                lines = lines.replace(token, key)
                print("Found old token in source code!\n")
            ffile.close() 
                
            #If the key was found 
            if flag is True: 
                
                #Open the same file in write mode and write to it 
                ffile = open("FeaturesClass.py", "wt")
                ffile.write(lines)
                ffile.close() 
                print(f"Changed x-auth-token from-> {headers['X-Auth-Token']} to {key} in current program and source code!\n")

            #Change the value currently held in memory 
            headers['X-Auth-Token'] = key
            
            flag = False
           
        except Exception as ex: 
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            print(traceback.format_exc())
            
        #Make a call to retrieve the updated status code 
        try: 
            r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
        except Exception as ex: 
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            print(traceback.format_exc())
        
        return r.status_code








































































