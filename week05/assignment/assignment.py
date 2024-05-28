"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: <Your name>

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier
- Do not use try...except statements
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50
NO_MORE_CARS = -1

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal

        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, quota:threading.Semaphore, lot:threading.Semaphore, q:Queue251, factory_stats:list, factory_finish:threading.Barrier):
        super().__init__()
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.quota = quota
        self.lot = lot
        self.q = q
        self.factory_stats = factory_stats
        self.factory_finish = factory_finish
        self.cars_produced = 0


    def run(self):
        # TODO produce the cars, the send them to the dealerships
        while self.cars_to_produce > 0:
            self.cars_to_produce -= 1
            self.quota.acquire() #acquire authorization to make a car
            self.q.put(Car())
            self.cars_produced += 1
            self.lot.release() #release car to the lot to be sold by a dealer
        # TODO wait until all of the factories are finished producing cars
        if self.factory_finish.n_waiting == self.factory_finish.parties - 1: #Then we know you're last.
            self.quota.acquire()
            self.q.put(NO_MORE_CARS)
            self.lot.release()
        self.factory_finish.wait()
        self.factory_stats.append(self.cars_produced)



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, q:Queue251, lot:threading.Semaphore, quota:threading.Semaphore, dealer_stats:list):
        super().__init__()
        self.q = q
        self.lot = lot
        self.quota = quota
        self.dealer_stats = dealer_stats
        self.cars_sold = 0

    def run(self):
        while True:
        # TODO handle a car
            self.lot.acquire() #request a car to sell
            car = self.q.get() #sell the car
            if car == NO_MORE_CARS:
                # Selling is over, all cars have been produced.
                self.q.put(NO_MORE_CARS)
                self.lot.release() #Allow all other dealers to receive the signal.
                self.dealer_stats.append(self.cars_sold)
                break
            self.cars_sold += 1
            self.quota.release() #authorize a new car to be produced
        # Sleep a little - don't change. This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))

class DebugThread(threading.Thread):
    def __init__(self, quota:threading.Semaphore, lot:threading.Semaphore):
        super().__init__()
        self.quota = quota
        self.lot = lot
        
    def run(self):
        while True:
            print("\n\n\n\n")
            print(f"Quota sem: {self.quota._value}")
            print(f"Lot sem: {self.lot._value}")
            time.sleep(0.25)
        

def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create semaphore(s) if needed
    quota = threading.Semaphore(MAX_QUEUE_SIZE) #Represents that number of cars which can be produced
    lot = threading.Semaphore(0) #Represents the number of cars in the lot.
    # TODO Create queue
    car_queue = Queue251()
    # TODO Create lock(s) if needed
    # TODO Create barrier
    factory_finish = threading.Barrier(factory_count)

    factory_stats = []
    
    # This is used to track the number of cars received by each dealer
    # dealer_stats = list([0] * dealer_count)
    dealer_stats = []

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = [Factory(quota, lot, car_queue, factory_stats, factory_finish) for _ in range(factory_count)]
    # TODO create your dealerships
    dealers = [Dealer(car_queue, lot, quota, dealer_stats) for _ in range(dealer_count)]

    log.start_timer()

    # Initialize and start debug thread
    # DebugThread(quota, lot).start()

    # TODO Start all dealerships
    for d in dealers: d.start()

    # TODO Start all factories
    for f in factories: f.start()

    # TODO Wait for factories and dealerships to complete
    for f in factories: f.join()
    for d in dealers: d.join()

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produced needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


