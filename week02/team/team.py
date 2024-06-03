"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self, URL:str):
        super().__init__()
        self.URL = URL.strip()
        self.result = None
        self.result_ready = threading.Lock()
        self.run()
    
    def run(self):
        self.result_ready.acquire()
        self.result = requests.get(self.URL)
        self.result_ready.release()
        
    def get_result(self):
        self.result_ready.acquire() #Block if the result isn't ready yet
        self.result_ready.release() #Release the lock
        return self.result.json()
        

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        print('Reshuffle Deck')
        # TODO - add call to reshuffle
        Request_thread(rf"https://deckofcardsapi.com/api/deck/{self.id}/shuffle/?deck_count=1").get_result()


    def draw_cards(self, count):
        # TODO add call to get a card
        # requests.get(rf'https://deckofcardsapi.com/api/deck/tocvr8nvaavj/draw/?count={count}')
        if self.remaining-count > 0:
            self.remaining -= count
            result = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count={count}').get_result()
            cards = result["cards"] #get the list of cards from the response
            return cards
        else:
            print("Not enough cards!")

    def cards_remaining(self):
        return self.remaining

    def draw_endless(self):
        if self.remaining == 0:
            self.reshuffle()
        card = self.draw_cards(1)[0]
        value = card["value"]
        suit = card["suit"]
        card_str = f"{value} of {suit}"
        return card_str


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'q1chjq477f4m'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

