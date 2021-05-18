#!/usr/bin/python
"""
    manualcamctl - This script manually controls the camera and is meant to 
                   be run as a standalone program.
"""

# Import dependencies
import usbcamctl
import sys
import asyncio

# Main
async def main(arguments):
    if "poweron" in arguments: usbcamctl.power(True)
    if "poweroff" in arguments: usbcamctl.power(False)
    if "record" in arguments: usbcamctl.toggleRecord()
    if "mode" in arguments: usbcamctl.toggleMode()
    if "usbon" in arguments: usbcamctl.usb(True)
    if "usboff" in arguments: usbcamctl.usb(False)

# Entry point
if __name__ == "__main__":
    arguments = sys.argv
    arguments.pop(0)
    main(arguments)
