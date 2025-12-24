from cmath import pi
from pickle import TRUE
from re import L
from unicodedata import name
import RPi.GPIO as GPIO
import threading
import Moving_motor as motor
import time
import smbus
import audio as aud
import detect_red as cap

GPIO.setmode(GPIO.BOARD)
bus = smbus.SMBus(1)        
control_ahead=False
def setup(Addr):
    global address
    address = Addr

def read(chn): 
    bus.read_byte(address)
    if chn == 0:
        bus.write_byte(address,0x40)   
    if chn == 1:
        bus.write_byte(address,0x41)
    if chn == 2:
        bus.write_byte(address,0x42)
    if chn == 3:
        bus.write_byte(address,0x43)
    return bus.read_byte(address)  
#白色數值比較大
def light_turn():
    global control_ahead
    L_monitor = 33
    R_monitor = 43
    Left = read(1)
    print("************************************")
    print ('光敏电阻 AIN0(左) = ', Left)
    Right = read(0)
    print ('光敏电阻 AIN1(右) = ', Right)
    if(Left > L_monitor and Right > R_monitor):  #L R 都碰到先轉左邊再轉右邊
        control_ahead=False
        print("--------------big turn--------------")
        motor.stop()
        for i in range(5):
            motor.onlyleft()
            Left = read(1)
            Right = read(0)
            if(Left < L_monitor or Right < R_monitor):
                break
        while (Left > L_monitor and Right > R_monitor):
            motor.onlyright()
            Left = read(1)
            Right = read(0)
            time.sleep(0.05)
    elif (Left < L_monitor and Right < R_monitor): #直走
        control_ahead=True
        print("--------------go ahead--------------")
        motor.forward()
    else:
        if(Left > L_monitor): #右轉
            control_ahead=False
            print("--------------turn right--------------")
            motor.turnRight()
            time.sleep(0.01)
        elif(Right > R_monitor): #左轉
            control_ahead=False
            print("--------------turn left--------------")
            motor.turnLeft()
            time.sleep(0.05)
        
    
if __name__ == "__main__":
    print("Press ctrl+c to quit...")
    setup(0x48)
    aud.set()
    try:
        while True:
            if(control_ahead): 
                if(aud.get_distance() > 15):
                    aud.set()
                    light_turn()            
                else:
                    aud.play(523)
                while(cap.get_red()==255):
                    print("交通安全")
            else:
                aud.set()
                light_turn()
    except KeyboardInterrupt:
        print("\nQuit")
        aud.stop()
        cap.finish()
        motor.cleanup()
        quit()
            
        