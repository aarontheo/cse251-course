"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = "http://127.0.0.1:8790"

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class RequestThread(threading.Thread):
    def __init__(self, URL):
        super().__init__()
        self.URL = URL
        self.lock = threading.Lock()
        self._result = None
        self.start()
    
    def run(self):
        self.lock.acquire()
        self._result = requests.get(self.URL)
        self.lock.release()
        global call_count 
        call_count += 1
        
    def result(self):
        self.lock.acquire()
        self.lock.release()
        return self._result
        


# TODO Add any functions you need here


def main():
    log = Log(show_terminal=True)
    log.start_timer("Starting to retrieve data from the server")

    # TODO Retrieve Top API urls
    url_dict = RequestThread(TOP_API_URL).result().json()
    # print(url_dict)
    # print(requests.get(url_dict))

    # TODO Retrieve Details on film 6
    film_dict = RequestThread(url_dict['films']+"6").result().json()
    
    # TODO Display results
    for key in film_dict:
        value = film_dict[key]
        if isinstance(value, list):
            log.write(f"{key}: {len(value)}")
            items = []
            for URL in value:
                items.append(RequestThread(URL).result().json()["name"])
            log.write(', '.join(items))
        else:
            log.write(f"{key}: {value}")
    log.stop_timer("Total Time To complete")
    log.write(f"There were {call_count} calls to the server")


if __name__ == "__main__":
    main()
