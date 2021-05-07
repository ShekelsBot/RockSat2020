#!/usr/bin/python
"""
    log - self module logs a line of text to the console and a file.
          The log file gets a timestamp and is stored in the logs folder.

    Contributors:
        Konstantin Zaremski
        Andrew Bruckbauer
"""

# Import dependencies
import configparser
import os
import datetime

class Logger:
    def __init__(self):
        self.logfile = open("./logs/vrse-" + str(datetime.datetime.now().strftime("%Y%m%d-T%H%M%S")) + ".txt", "w")
        self.timestarted = datetime.datetime.timestamp(datetime.datetime.now())

    # Logging function (to the console & the log file)
    def out(self, message):
        # Make sure nothing breaks
        try:
            if self.logfile == None or self.timestarted == None:
                return print("Logging Error: Please call log.start() before sending any messages.")
        except:
            return print("Logging Error: Please call log.start() before sending any messages.")
        # Calculate elapsed time
        present = datetime.datetime.timestamp(datetime.datetime.now())
        elapsed = present - self.timestarted
        # Predefining log output so that the time remains constant on both the console output and file output
        logOutput = "[" + str(datetime.datetime.fromtimestamp(elapsed).strftime("T+%M:%S")) + "] " + message + "\n"
        # Output to the console
        print(logOutput, end='')
        # Output to the log file
        self.logfile.write(logOutput)

    def close(self):
        self.logfile.close()
        self.timestarted = None;
        self.logfile = None;