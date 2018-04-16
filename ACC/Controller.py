from gopigo import *
import time

def commandList():
    print "*****************************************************"
    print "*  Commands:                                        *"
    print "*  go                                               *"
    print "*  stop                                             *"
    print "*  speed                                            *"
    print "*  exit                                             *"
    print "*****************************************************"

command = ""
speed = 100

while command != "exit":
    commandList()
    command = raw_input()
    if "go" == command:
        fwd()
    elif "stop" == command:
        stop()
    elif "speed" == command:
        print "Enter speed (20-255): "
        speed = int(raw_input())
        if(speed < 20 or speed > 255):
            print "invalid speed, you suck!"
        else:
            set_speed(speed)

print "Goodbye!"
