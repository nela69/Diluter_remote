import RPi.GPIO as GPIO
from time import sleep

class Actuator:
    def __init__(self, GPIO_IN1, GPIO_IN2 = 0, GPIO_pwm = 0, freq = 0, init_pwm = 100):
        global GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.GPIO_IN1 = GPIO_IN1
        GPIO.setup(GPIO_IN1, GPIO.OUT)     
        self.GPIO_pwm = GPIO_pwm                            
        self.GPIO_IN2 = GPIO_IN2
        
        if GPIO_IN2 > 0:
            GPIO.setup(GPIO_IN2, GPIO.OUT)
        else:
            self.GPIO_CONTROL = GPIO_IN1
        
        if self.GPIO_pwm > 0:
            GPIO.setup(self.GPIO_pwm, GPIO.OUT)
            if freq > 0:
                self.pwm = GPIO.PWM(self.GPIO_pwm, freq)
                self.pwm.start(init_pwm)
            else:
                GPIO.output(self.GPIO_pwm, GPIO.HIGH)

    def setSpeed(self,PWM):
        if self.GPIO_pwm > 0:
#            GPIO.output(self.GPIO_control, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(PWM)
            
    def On(self, direction = 1, run_time = 0):
        if self.GPIO_IN2 > 0 and direction == 1:
            GPIO.output(self.GPIO_IN1, GPIO.HIGH)
            GPIO.output(self.GPIO_IN2, GPIO.LOW)
        elif self.GPIO_IN2 > 0 and direction == -1:
            GPIO.output(self.GPIO_IN1, GPIO.LOW)
            GPIO.output(self.GPIO_IN2, GPIO.HIGH)
        else:
            GPIO.output(self.GPIO_IN1, GPIO.HIGH)
            
        if run_time > 0:
            sleep(run_time)
            GPIO.output(self.GPIO_IN1, GPIO.LOW)
        
    def Off(self):
        GPIO.output(self.GPIO_IN1, GPIO.LOW)
        if self.GPIO_IN2 > 0:
            GPIO.output(self.GPIO_IN2, GPIO.LOW)
        
    def Toggle(self):
        if GPIO.input(self.GPIO_IN1):
            GPIO.output(self.GPIO_IN1, GPIO.LOW)
        else:
            GPIO.output(self.GPIO_IN1, GPIO.HIGH)
            
    def stopPWM(self):
        self.pwm.stop()

class Heater:
    def __init__(self, GPIO_control, GPIO_temp_input):
        self.self.GPIO_control = self.GPIO_control
        GPIO.setup(GPIO_control, GPIO.OUT)
        GPIO.setup(GPIO_temp_input, GPIO.IN)

    def On(self):
        GPIO.output(self.GPIO_control, GPIO.HIGH)
        
    def Off(self):
        GPIO.output(self.GPIO_control, GPIO.LOW)
        
class UniStepper:
# 28BYJ-48 5V Stepper Motor (unipolar) driver
# PWMA, PWMB, STBY must be set to HIGH on TB6612!!!  
    def __init__(self, AIN1, AIN2, BIN1, BIN2):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.AIN1 = AIN1
        self.AIN2 = AIN2
        self.BIN1 = BIN1
        self.BIN2 = BIN2

        GPIO.setup(AIN2, GPIO.OUT)
        GPIO.setup(AIN1, GPIO.OUT)
        GPIO.setup(BIN1, GPIO.OUT)
        GPIO.setup(BIN2, GPIO.OUT)

        GPIO.output(AIN1,GPIO.LOW)
        GPIO.output(AIN2,GPIO.LOW)
        GPIO.output(BIN1,GPIO.LOW)
        GPIO.output(BIN2,GPIO.LOW)

    def runStepper(self, spd, angle):
        
        O = self.AIN1
        P = self.AIN2
        B = self.BIN1
        Y = self.BIN2
        
        hc = (1/spd)/2

        steps = int(abs(angle)/(360/128))
        
        if angle < 0:
            B = self.AIN1
            Y = self.AIN2
            O = self.BIN1
            P = self.BIN2
            
        GPIO.output(O,1)
        sleep(hc)

        for i in range(steps):
            GPIO.output(Y,1)
            sleep(hc)
            GPIO.output(O,0)
            sleep(hc)  
            GPIO.output(P,1)
            sleep(hc)
            GPIO.output(Y,0)
            sleep(hc)
            GPIO.output(B,1)
            sleep(hc)
            GPIO.output(P,0)
            sleep(hc)
            GPIO.output(O,1)
            sleep(hc)
            GPIO.output(B,0)
            sleep(hc)