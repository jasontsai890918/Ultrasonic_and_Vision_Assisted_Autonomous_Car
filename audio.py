import RPi.GPIO as GPIO
import time
trigger_pin = 12
echo_pin = 15
buzz_pin = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(buzz_pin, GPIO.OUT, initial=GPIO.LOW)

pwm = GPIO.PWM(buzz_pin, 523)

def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count = count - 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 5000)
    start = time.time()
    wait_for_echo(False, 5000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 *100 /2
    distance_in = distance_cm / 2.5
    return (int(distance_cm))

def play(pitch):
    pwm.ChangeFrequency(pitch)
    pwm.ChangeDutyCycle(30)

def set():
    pwm.start(0)

def stop():
    pwm.stop()
