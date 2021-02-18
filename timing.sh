#!/bin/bash
# Common path for all GPIO access
BASE_GPIO_PATH=/sys/class/gpio

# Assign names to GPIO pin numbers
EVENT_1=18
EVENT_2=27
EVENT_3=22

# Assign names to states
ON="1"
OFF="0"

# Utility function to export a pin if not already exported
exportPin()
{
	if [ ! -e $BASE_GPIO_PATH/gpio$1 ]; then
		echo "$1" > $BASE_GPIO_PATH/export
	fi
}

# Funtion to set a pin as an input
setInput()
{
	echo "in" > $BASE_GPIO_PATH/gpio$1/direction
}

# Utility to change state of Event
setEvent()
{
	echo $2 > $BASE_GPIO_PATH/gpio$1/value
}

# Utility to reset all conditions
allEventsOff()
{
	setEvent $EVENT_1 $OFF
	setEvent $EVENT_2 $OFF
	setEvent $EVENT_3 $OFF
}

# Ctrl-C handler for shutdown
shutdown()
{
	allEventsOff
	exit 0
}

trap shutdown SIGINT

# Export pins for use
exportPin $EVENT_1
exportPin $EVENT_2
exportPin $EVENT_3

# Set Pins as Inputs
setInput $EVENT_1
setInput $EVENT_2
setInput $EVENT_3

while true
{
	if EVENT_1 = [ 1 ]
	{
	# Arm extension 
	# Turn off USB port
	# Power on camera
	# Start Recording
	}

	if EVENT_2 = [ 1 ]
	{
	# Arm retraction
	# Turn on USB Port
	# Transfer footage
	}

	if EVENT_3 = [ 1 ]
	{
	# Turn off camera
	# Shut down system power
	}

}