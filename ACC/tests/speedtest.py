from gopigo import *
import time
speed = 0
accel = 30

print "Press ENTER to start"
raw_input()
set_speed(speed)
fwd()
while True:
    speed = speed + accel
    set_speed(speed)
    time.sleep(.1)
    
