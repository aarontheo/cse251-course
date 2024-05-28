"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 3

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(q:mp.Queue):
    with open('data.txt') as file:
        for line in file:
            q.put(int(line.strip()))
    q.put(False)

# TODO create prime_process function
def prime_process(q:mp.Queue, primes:mp.Queue):
    while True:
        num = q.get()
        if num == False:
            q.put(False)
            break
        if is_prime(num): primes.put(num)

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    q = mp.Queue()
    prime_q = mp.Queue()

    # TODO create reading thread
    r_thread = threading.Thread(target=read_thread, args=(q,))
    
    # TODO create prime processes
    prime_procs = [mp.Process(target=prime_process, args=(q, prime_q)) for _ in range(PRIME_PROCESS_COUNT)]
    
    # TODO Start them all
    r_thread.start()
    for p in prime_procs: p.start()
    
    # TODO wait for them to complete
    r_thread.join()
    for p in prime_procs: p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')
    
    primes = []
    while not prime_q.empty(): primes.append(prime_q.get())

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

