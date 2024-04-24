from cse251 import *
import threading

print("Hello World!")

# Variables
# t1 = 1
# t2 = dict()
# t2["key"] = 1337
# print(t2)
# t3 = ["hello", "world"]
# print(t3)

# Functions
def do_something(param1=0, param2=0):
    print('before', param1, param2)
    time.sleep(2)
    print('after', param1, param2)

t4 = threading.Thread(target=do_something, args=(1,))
t5 = threading.Thread(target=do_something, args=(2,))
t4.start()
t5.start()
t4.join()
t5.join()
