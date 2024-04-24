"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team activity details in I-Learn

"""

from datetime import datetime, timedelta
import threading

# Include cse 251 common Python files
from cse251 import *
from split import split_num

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

def is_prime(n):
    global numbers_processed
    numbers_processed += 1

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

def find_primes(start, range_count):
    global prime_count, numbers_processed
    for i in range(start, start + range_count):
        if is_prime(i):
            prime_count += 1
            print(i, end=', ', flush=True)
    print(flush=True)

def find_primes_threaded(num_threads:int, start:int, range_count:int):
    threads = []
    sizes = split_num(range_count, num_threads) # figure out how much work each thread needs to do
    for size in sizes:
        new_thread = threading.Thread(target=find_primes, args=(start, size))
        start += size
        threads.append(new_thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
        

if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    # TODO 3) change the program to divide the for loop into 10 threads

    start = 10000000000
    range_count = 100000
    find_primes_threaded(3, start, range_count)
    # size = range_count//2
    # t1 = threading.Thread(target=find_primes, args=(start,size))
    # t2 = threading.Thread(target=find_primes, args=(start+size, size))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    
    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')


