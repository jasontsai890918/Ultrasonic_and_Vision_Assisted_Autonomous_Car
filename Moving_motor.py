import RPi.GPIO as GPIO
import time

Motor_R1_Pin = 16
Motor_R2_Pin = 18
Motor_L1_Pin = 11
Motor_L2_Pin = 13
t = 0.01
dc = 100
miss = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor_R1_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_R2_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_L1_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_L2_Pin, GPIO.OUT, initial=GPIO.LOW)

pwm_r1=GPIO.PWM(Motor_R1_Pin, 100)
pwm_r2=GPIO.PWM(Motor_R2_Pin, 100)
pwm_l1=GPIO.PWM(Motor_L1_Pin, 100)
pwm_l2=GPIO.PWM(Motor_L2_Pin, 100)

pwm_r1.start(0)
pwm_r2.start(0)
pwm_l1.start(0)
pwm_l2.start(0)

def stop():
    pwm_r1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(0)

def forward():
    pwm_r1.ChangeDutyCycle(50)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(50)
    pwm_l2.ChangeDutyCycle(0)
    time.sleep(0.05)
    stop()

def backward():
    pwm_r1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(dc)
    pwm_l1.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(dc)
    time.sleep(t)
    stop()

def turnLeft():
    pwm_r1.ChangeDutyCycle(dc)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(0)
    time.sleep(0.1)
    forward()

def turnRight():
    pwm_r1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(dc)
    pwm_l2.ChangeDutyCycle(0)
    time.sleep(0.1)
    forward()

def onlyleft():
    pwm_r1.ChangeDutyCycle(dc)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(dc)
    time.sleep(0.15)
    stop()

def onlyright():
    pwm_r1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(dc)
    pwm_l1.ChangeDutyCycle(dc)
    pwm_l2.ChangeDutyCycle(0)
    time.sleep(0.25)
    stop()

def cleanup():
    stop()
    GPIO.cleanup()

