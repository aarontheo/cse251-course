# Copyright (c) 2024, Aaron Theobald
# All rights reserved.

# This file is part of [project]
# and is released under the [license] License.
# Please see the [license] file for more information.

# File: split.py
# Description: A module for splitting numbers and intervals evenly.

# splits a number (n) into a list of c parts,
# with all parts adding to n and the size of each part being similar.
# Think, dividing n cookies evenly amongst c toddlers without splitting cookies.
def split_num(n, c) -> list:
    parts = [0] * c # How many 'cookies' each 'child' gets
    # If the amount divides evenly
    if n % c == 0:
        size = n // c
        for i in range(c):
            parts[i] += size
        return parts
    # If the amount doesn't divide evenly:
    while n > 0: # while there are still cookies to go around
        # give the largest possible chunk to each toddler, 
        # subtracting cookies from the pile (n) as we do so.
        size = n // c #size of the chunks we're distributing
        while size == 0: 
            #if the number of cookies doesn't distribute evenly, 
            #get rid of children until it does
            c -= 1 
            size = n // c
        for i in range(c): # for each toddler
            n -= size # take from pile
            parts[i] += size # give to toddler
    return parts

# Splits an interval, (start, end) into c intervals, each as even as possible.
# Start is inclusive, end is exclusive.
# Each interval in the output is a 2-tuple (start, end).
def split_interval(start, end, c):
    intervals = []
    sizes = split_num(end-start, c)
    for size in sizes:
        intervals.append((start, start+size))
        start += size
    return intervals

def split_test(n, c):
    print(f"Splitting {n} cookies among {c} children:")
    print(split_num(n, c))