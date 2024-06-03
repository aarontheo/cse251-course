"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Aaron Theobald
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
from multiprocessing.connection import Connection as Conn
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = "settings.txt"
BOXES_FILENAME = "boxes.txt"

# Settings consts
MARBLE_COUNT = "marble-count"
CREATOR_DELAY = "creator-delay"
NUMBER_OF_MARBLES_IN_A_BAG = "bag-count"
BAGGER_DELAY = "bagger-delay"
ASSEMBLER_DELAY = "assembler-delay"
WRAPPER_DELAY = "wrapper-delay"

NO_MORE_ITEMS = False

# No Global variables


class Bag:
    """bag of marbles - Don't change"""

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift:
    """Gift of a large marble and a bag of marbles - Don't change"""

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f"Large marble: {self.large_marble}, marbles: {marbles[1:-1]}"


class Marble_Creator(mp.Process):
    """This class "creates" marbles and sends them to the bagger"""

    colors = (
        "Gold",
        "Orange Peel",
        "Purple Plum",
        "Blue",
        "Neon Silver",
        "Tuscan Brown",
        "La Salle Green",
        "Spanish Orange",
        "Pale Goldenrod",
        "Orange Soda",
        "Maximum Purple",
        "Neon Pink",
        "Light Orchid",
        "Russian Violet",
        "Sheen Green",
        "Isabelline",
        "Ruby",
        "Emerald",
        "Middle Red Purple",
        "Royal Orange",
        "Big Dip O’ruby",
        "Dark Fuchsia",
        "Slate Blue",
        "Neon Dark Green",
        "Sage",
        "Pale Taupe",
        "Silver Pink",
        "Stop Red",
        "Eerie Black",
        "Indigo",
        "Ivory",
        "Granny Smith Apple",
        "Maximum Blue",
        "Pale Cerulean",
        "Vegas Gold",
        "Mulberry",
        "Mango Tango",
        "Fiery Rose",
        "Mode Beige",
        "Platinum",
        "Lilac Luster",
        "Duke Blue",
        "Candy Pink",
        "Maximum Violet",
        "Spanish Carmine",
        "Antique Brass",
        "Pale Plum",
        "Dark Moss Green",
        "Mint Cream",
        "Shandy",
        "Cotton Candy",
        "Beaver",
        "Rose Quartz",
        "Purple",
        "Almond",
        "Zomp",
        "Middle Green Yellow",
        "Auburn",
        "Chinese Red",
        "Cobalt Blue",
        "Lumber",
        "Honeydew",
        "Icterine",
        "Golden Yellow",
        "Silver Chalice",
        "Lavender Blue",
        "Outrageous Orange",
        "Spanish Pink",
        "Liver Chestnut",
        "Mimi Pink",
        "Royal Red",
        "Arylide Yellow",
        "Rose Dust",
        "Terra Cotta",
        "Lemon Lime",
        "Bistre Brown",
        "Venetian Red",
        "Brink Pink",
        "Russian Green",
        "Blue Bell",
        "Green",
        "Black Coral",
        "Thulian Pink",
        "Safety Yellow",
        "White Smoke",
        "Pastel Gray",
        "Orange Soda",
        "Lavender Purple",
        "Brown",
        "Gold",
        "Blue-Green",
        "Antique Bronze",
        "Mint Green",
        "Royal Blue",
        "Light Orange",
        "Pastel Blue",
        "Middle Green",
    )

    def __init__(self, out_p: Conn, marble_count: int, delay: float):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.out_pipe = out_p
        self.marble_count = marble_count
        self.delay = delay

    def run(self):
        """
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        """
        while self.marble_count > 0:
            self.out_pipe.send(random.choice(self.colors))
            self.marble_count -= 1
            time.sleep(self.delay)
        self.out_pipe.send(NO_MORE_ITEMS)


class Bagger(mp.Process):
    """Receives marbles from the marble creator, when there are enough
    marbles, the bag of marbles are sent to the assembler"""

    def __init__(self, in_p: Conn, out_p: Conn, marbles_per_bag: int, delay: float):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.in_p = in_p
        self.out_p = out_p
        self.marbles_per_bag = marbles_per_bag
        self.delay = delay

    def run(self):
        """
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        """
        exit = False
        while True:
            new_bag = Bag()
            for _ in range(self.marbles_per_bag):
                next_marble = self.in_p.recv()
                if next_marble == NO_MORE_ITEMS:
                    # finish this bag if it has marbles, I guess
                    if new_bag.get_size() > 0:
                        self.out_p.send(new_bag)
                    exit = True
                    break
                new_bag.add(next_marble)
            if exit: break
            self.out_p.send(new_bag)
            # print("Sending Bag!")
            time.sleep(self.delay)
        self.out_p.send(NO_MORE_ITEMS)


class Assembler(mp.Process):
    """Take the set of marbles and create a gift from them.
    Sends the completed gift to the wrapper"""

    marble_names = (
        "Lucky",
        "Spinner",
        "Sure Shot",
        "Big Joe",
        "Winner",
        "5-Star",
        "Hercules",
        "Apollo",
        "Zeus",
    )

    def __init__(self, in_p: Conn, out_p: Conn, delay: float, gift_count: mp.Value):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.in_p = in_p
        self.out_p = out_p
        self.delay = delay
        self.gift_count = gift_count

    def run(self):
        """
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        """
        while True:
            next_bag = self.in_p.recv()
            if next_bag == NO_MORE_ITEMS:
                break
            self.out_p.send(Gift(random.choice(self.marble_names), next_bag))
            # print("Gift sent!")
            self.gift_count.value += 1
            time.sleep(self.delay)
        self.out_p.send(NO_MORE_ITEMS)


class Wrapper(mp.Process):a
    """Takes created gifts and wraps them by placing them in the boxes file"""

    def __init__(self, in_p: Conn, delay: float):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.in_p = in_p
        self.delay = delay

    def run(self):
        """
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        """
        with open(BOXES_FILENAME, "a") as boxes:
            while True:
                next_gift = self.in_p.recv()
                if next_gift == NO_MORE_ITEMS:
                    break
                boxes.write(f"{next_gift}: {datetime.now()}\n")
                # print("Writing box")
                time.sleep(self.delay)


def display_final_boxes(filename, log):
    """Display the final boxes file to the log file -  Don't change"""
    if os.path.exists(filename):
        log.write(f"Contents of {filename}")
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f"The file {filename} doesn't exist.  No boxes were created.")


def main():
    """Main function"""

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f"Problem reading in settings file: {CONTROL_FILENAME}")
        return

    log.write(f"Marble count     = {settings[MARBLE_COUNT]}")
    log.write(f"Marble delay     = {settings[CREATOR_DELAY]}")
    log.write(f"Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}")
    log.write(f"Bagger delay     = {settings[BAGGER_DELAY]}")
    log.write(f"Assembler delay  = {settings[ASSEMBLER_DELAY]}")
    log.write(f"Wrapper delay    = {settings[WRAPPER_DELAY]}")

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    pipes = [
        mp.Pipe(),
        mp.Pipe(),
        mp.Pipe(),
    ]

    # TODO create variable to be used to count the number of gifts
    gift_count = mp.Value("i")

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write("Create the processes")

    # TODO Create the processes (ie., classes above)
    procs = [
        Marble_Creator(pipes[0][0], settings[MARBLE_COUNT], settings[CREATOR_DELAY]),
        Bagger(
            pipes[0][1],
            pipes[1][0],
            settings[NUMBER_OF_MARBLES_IN_A_BAG],
            settings[BAGGER_DELAY],
        ),
        Assembler(pipes[1][1], pipes[2][0], settings[ASSEMBLER_DELAY], gift_count),
        Wrapper(pipes[2][1], settings[WRAPPER_DELAY]),
    ]

    log.write("Starting the processes")
    for p in procs:
        p.start()

    log.write("Waiting for processes to finish")
    # TODO add code here
    for p in procs:
        p.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f"Total number of gifts: {gift_count.value}")


if __name__ == "__main__":
    main()
