from gopigo import *
import time

#enable_encoders()
#trim_write(0)
set_speed(150)
left_enc = enc_read(0)
right_enc = enc_read(1)
print "left enc: ",left_enc
print "right enc",right_enc
print "press ENTER to begin"
raw_input()
fwd()

while True:
    print "left enc: ",left_enc
    print "right enc",right_enc
    left_old = left_enc
    left_enc = enc_read(0)
    right_old = right_enc
    right_enc = enc_read(1)

    left_dif = left_enc - left_old
    print "left dif: ",left_dif
    right_dif = right_enc - right_old
    print "right dif: ",right_dif
    if left_dif != 0 and right_dif - left_dif != 0:
        dif = (right_dif - left_dif)#/left_dif
        #trim_write((1+dif)*100)
        dif =int(dif)
        trim_write(dif)
        print dif
    else:
        print "balanced"
    print "************"
    time.sleep(.1)
