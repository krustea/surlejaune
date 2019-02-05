import RPi.GPIO as GPIO
import time
class Led:
    def __init__(self, status):
        self.status = status
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)


    def led_status(self):
        if (self.status == 'on'):
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
        elif (self.status == 'off'):
            GPIO.output(24, GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
        else:
            return 'Erreur de manipulation'

    def blink(self):
        i=0
        while i < 5:
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(14, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
            time.sleep(1)
            i=i+1

ledtest=Led()
ledtest.blink()