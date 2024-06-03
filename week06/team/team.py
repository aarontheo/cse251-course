"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

- After you can copy a text file word by word exactly,
  Change the program (any way you want) to be faster 
  (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing.connection import Connection as Conn
from multiprocessing import Value, Process
import filecmp

# Include cse 251 common Python files
from cse251 import *

EOF = False

def sender(path:str, pipe:Conn):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(path, 'r') as file:
        for line in file:
            for word in line.replace(' ', '&space ').split('&space'):
                pipe.send(word)
    pipe.send(EOF)
        


def receiver(path:str, pipe:Conn, item_ct:mp.Value):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(path, 'w') as file: file.truncate(0) #get rid of the previous copy
    with open(path, 'a') as file:
        while True:
            next_word = pipe.recv()
            item_ct.value += 1
            if next_word == EOF:
                break
            file.write(next_word)


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    (pipe_in, pipe_out) = mp.Pipe()
    # TODO create variable to count items sent over the pipe
    item_ct = Value("i", 0)
    # TODO create processes 
    read_p = Process(target=sender, args=(filename1, pipe_in))
    write_p = Process(target=receiver, args=(filename2, pipe_out, item_ct))
    
    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    read_p.start()
    write_p.start()
    
    # TODO wait for processes to finish
    read_p.join()
    write_p.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {item_ct.value}: ')
    log.write(f'items / second = {item_ct.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')
