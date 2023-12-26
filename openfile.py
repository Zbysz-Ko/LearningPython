#!/usr/bin/env python3

# Learning Python
# Collected methods for open and read a file.

import sys
import time

### First method

f = None

with open("openfile-data.txt", encoding="UTF-8") as f:
    for line in f:
        print(line, end='')
        print("Press ctrl+c now")
        # To make sure it runs for a while
        time.sleep(2)

f.close()


### Second method

f = None

try:
    f = open("openfile-data.txt", encoding="UTF-8")
    # Our usual file-reading idiom
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print(line, end='', flush=True)
        print("Press ctrl+c now")
        # To make sure it runs for a while
        time.sleep(2)
except IOError:
    print("Could not find file openfile-data.txt")
except KeyboardInterrupt:
    print("!! You cancelled the reading from the file.")
finally:
    if f:
        f.close()
    print("(Cleaning up: Closed the file)")
