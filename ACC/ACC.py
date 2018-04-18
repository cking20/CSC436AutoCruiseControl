from gopigo import *
import time
import signal
import sys
import multiprocessing

#get encoder values
time.sleep(0.1)
left_enc_init = enc_read(0)
time.sleep(0.1)
right_enc_init = enc_read(1)
    
####Really really scary pin functions, don't touch
###PS TY chris wells
###honorable mention: gopigo and dexter industries
ADDRESS = 0x08
ENC_READ_CMD = [53]

import smbus
bus = smbus.SMBus(1)

def write_i2c_block(address, block):
    try:
        op = bus.write_i2c_block_data(address, 1, block)
        time.sleep(0.005)
        return op
    except IOError:
        return -1
    return 1

def enc_read(motor):
    write_i2c_block(ADDRESS, ENC_READ_CMD+[motor,0,0])
    #time.sleep(0.01)
    #time.sleep(0.08)
    try:
        b1 = bus.read_byte(ADDRESS)
        b2 = bus.read_byte(ADDRESS)
    except IOError:
        return -1
    if b1 != -1 and b2 != -1:
        v = b1 * 256 + b2
        return v
    else:
        return -1

US_CMD = [117]

def us_dist(pin):
    write_i2c_block(ADDRESS, US_CMD+[pin,0,0])
    time.sleep(0.01)
    #time.sleep(0.08)
    try:
        b1 = bus.read_byte(ADDRESS)
        b2 = bus.read_byte(ADDRESS)
    except IOError:
        return -1
    if b1 != -1 and b2 != -1:
        v = b1 * 256 + b2
        return v
    else:
        return -1

def check_encoders():
    #encl1 = enc_read(0)
    encr1 = enc_read(1)
    encl1 = enc_read(0)
    
    #encr2 = enc_read(1)
    #encl2 = enc_read(0)
    
    #encl3 = enc_read(0)
    #encr3 = enc_read(1)
    
    #print "left: ",encl1," ",encl2," ",encl3
    #print "right: ",encr1," ",encr2," ",encr3
   # if encl1 > encl2:
   #     encl1 = encl2
   # if encl1 > encl3:
   #     encl1 = encl3
   # if encr1 < encr2:
    #    encr1 = encr2
    #if encr1 < encr3:
     #   encr1 = encr3
    
    left_enc_diff = encl1 - left_enc_init
    right_enc_diff = encr1 - right_enc_init

    return (left_enc_diff, right_enc_diff)

def compensate(speed):
    if speed == 0:
        return 0
    else:
        if speed > 40:
            return int((9.0/(speed/100.0)) /1.5)
            #return int(speed/100) * 10
        else:        
            return int(speed/100) * 10

class ACC:
    def __init__(self):

        self.left_enc_diff = 0
        self.right_enc_diff = 0
        
        #set initial speed
        self.minimum_start = 40
        self.max_speed = 150
        self.accel = 20
        
        #set distances
        self.min_safe_dist = 15
        self.max_safe_dist = 50

    def main_loop(self,q):
        #initalize detected object to 
        detected_object = True
        should_move = False
        old_dist = 0
        speed = self.minimum_start
        set_speed(speed)
        comp = compensate(speed)
        command = ""
        queue = q
        run_acc = False
        try:
            while command != "exit":
                if not queue.empty():
                    command = queue.get_nowait()
                    #print command
                    if command == "go":
                        run_acc = True
                        set_right_speed(speed + compensate(speed))
                        set_left_speed(speed + compensate(speed))
                        #set_right_speed(speed + compensate(speed))
                        #set_left_speed(speed)
                        fwd()
                    elif command == "stop":
                        run_acc = False
                        stop()
                    elif command != "exit":
                        self.max_speed = command
                if run_acc:
                    balance = True
                    can_accel = True
                    distance = us_dist(15)
                    #print "dist: ",distance," cm"
                    if(distance > 0):
                        if distance < self.min_safe_dist:
                            stop()
                            self.speed = self.minimum_start
                            set_speed(speed)
                            should_move = False
                            #print "Hazard!  Emergency stop!"
                        elif distance >= self.min_safe_dist and distance <= self.max_safe_dist:
                            #print "Object ahead!"
                            can_accel = False
                            if old_dist > distance:
                                #print "Approching, decelerating."
                                speed = speed - (self.accel)
                                if speed < self.minimum_start:
                                    speed = self.minimum_start
                                #set_speed(speed)
                                set_left_speed(speed) #(comp - 25))
                                set_right_speed(speed + compensate(speed))  #(comp + 100))    
                                comp = compensate(speed)
                                balance = False
                        else:
                            fwd()
                            should_move = True
                        old_dist = distance
                    else:
                        time.sleep(.01)
                    if should_move:
                        #calculate the difference since last tick
                        left_enc_diff,right_enc_diff = check_encoders()
                        #print "left enc:", left_enc_diff
                        #print "right enc:", right_enc_diff
                        
                        #update the previous tick values
                        if balance:
                            #if the left wheel has moved farther than the right
                            if left_enc_diff > right_enc_diff:
                                print "left more"
                                #set_left_speed(speed - compensate(speed)) #(comp - 25))
                                set_right_speed(speed + compensate(speed))  #(comp + 100))
                                #print "left speed", speed - comp
                                #print "right speed",speed + comp
                            elif left_enc_diff < right_enc_diff:
                                print "right more"
                                set_left_speed(speed + compensate(speed))
                                #set_right_speed(speed - compensate(speed))
                                #print "left speed", speed + comp
                                #print "right speed",speed - comp
                            else:
                                print "Balanced"
                                #keep the speeds equal
                                set_left_speed(speed)
                                set_right_speed(speed)
                                #print "left speed", speed
                                #print "right speed",speed
                        else:
                            print "Balanced"
                            #keep the speeds equal
                            set_left_speed(speed)
                            set_right_speed(speed)
                            #print "left speed", speed
                            #print "right speed",speed
                    #print "speeds: " , read_motor_speed_cmd()
                    if can_accel:
                        if speed < self.max_speed:
                            speed = speed + self.accel
                        else:
                            speed = self.max_speed
                        comp = compensate(speed)
                        set_speed(speed)
                    time.sleep(.1)
                    #print "******************"
            #print "done"
        except KeyboardInterrupt:
                stop()
            

