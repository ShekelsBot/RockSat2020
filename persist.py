#!/usr/bin/python
"""
    persist - This module saves a variable to a 'state' file to be read in the
              event of a power interruption during flight.

    Contributors:
        Konstantin Zaremski
    
    05.11.2021
"""

# Import dependencies
import os

# Save a variable as the first line of the state file
async def set(value):
    try:
        statefile = open("state", "w")
        statefile.write(str(value))
        statefile.close()
        return True
    except: return False

# Read the state file and return the first line with no newline charecters
async def read():
    try:
        statefile = open("state", "r")
        value = statefile.readline().replace("\n", "")
        statefile.close()
        return value
    except: return None

# Delete the state file so that None is returned when read
async def clear():
    try:
        os.remove("state")
        return True
    except: return False