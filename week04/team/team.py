"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(log:Log, q:queue.Queue):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        if not q.empty():
            # TODO process the value retrieved from the queue
            next_value = q.get()
            if next_value == NO_MORE_VALUES: 
                q.put(NO_MORE_VALUES)
                break
            # TODO make Internet call to get characters name and log it
            response = requests.get(next_value)
            if response.status_code == 200:
                log.write(response.json()['name'])
            


def file_reader(log:Log, q:queue.Queue): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open('urls.txt') as file:
        for line in file:
            q.put(line.strip())
    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS): q.put(NO_MORE_VALUES)
    



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    # TODO create semaphore (if needed)
    q = queue.Queue()

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    reader_thread = threading.Thread(target=file_reader, args=(log, q))
    ret_threads = []
    for i in range(RETRIEVE_THREADS):
        new_thread = threading.Thread(target=retrieve_thread, args=(log, q))
        ret_threads.append(new_thread)

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for t in ret_threads: t.start()
    reader_thread.start()
    # TODO Wait for them to finish - The order doesn't matter
    for t in ret_threads: t.join()
    reader_thread.join()
    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




