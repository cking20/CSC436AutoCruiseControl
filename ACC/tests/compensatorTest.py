from gopigo import *
import time
stop()
#enable_encoders()
#trim_write(0)
set_speed(50)
left_enc = enc_read(0)
right_enc = enc_read(1)
old_trim = trim_read()
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
    if right_dif - left_dif != 0:
        dif = (right_dif - left_dif)
        dif =int(dif)
        #trim_write((2 *(dif - old_trim)) - dif)
        if old_trim - dif > 80:
            trim_write(dif+60)
            print "if"
        else:
            trim_write(dif-60)
        time.sleep(.1)
        trim_write(dif)
        left_dif = left_enc - left_old
        print "left dif: ",left_dif
        right_dif = right_enc - right_old
        print "right dif: ",right_dif
        old_trim = dif
        print dif
    else:
        print "balanced"
    print "************"
    dist=us_dist(15)
    if dist < 10:
        stop()
    time.sleep(.1)
    

