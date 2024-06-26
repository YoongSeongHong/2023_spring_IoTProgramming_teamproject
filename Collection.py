import time
import cv2
import RPi.GPIO as GPIO


class SPEED:
    LOW = 0.3
    MIDDLE = 0.5
    HIGH = 0.65


PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24


def motor_go(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1


def motor_back(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def motor_stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def motor_right(speed):
    L_Motor.ChangeDutyCycle(speed*SPEED.HIGH)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1


def motor_left(speed):
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(speed*SPEED.HIGH)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2,GPIO.OUT)
GPIO.setup(AIN1,GPIO.OUT)
GPIO.setup(PWMA,GPIO.OUT)

GPIO.setup(BIN1,GPIO.OUT)
GPIO.setup(BIN2,GPIO.OUT)
GPIO.setup(PWMB,GPIO.OUT)

L_Motor= GPIO.PWM(PWMA,100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB,100)
R_Motor.start(0)

speedSet = 50

camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)
        
def main():
    filepath = "/home/threeZo/AI_CAR/video/train"
    i = 0
    carState = "stop"
    try:
        while True:
            
            keyValue = cv2.waitKey(1)
        
            if keyValue == ord('q'):
                break
            elif keyValue == 82:
                print("go")
                carState = "go"
                motor_back(speedSet)
            elif keyValue == 84:
                print("stop")
                carState = "stop"
                motor_stop()
            elif keyValue == 81:
                print("left")
                carState = "left"
                motor_left(speedSet)
            elif keyValue == 83:
                print("right")
                carState = "right"
                motor_right(speedSet)

            _, image = camera.read()
            image = cv2.flip(image,-1)
            height, _, _ = image.shape
            image = image[int(height/2):,:,:]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            image = cv2.resize(image, (200,66))
            h,w = image.shape[:2]
            image = image[:,int(w*0.1):] #Crop the image again to check lane only
            image = cv2.GaussianBlur(image,(5,5),0)
            _,image = cv2.threshold(image,160,255,cv2.THRESH_BINARY_INV) #Apply the binary threshold to check lane well
            
            if carState == "right":
                cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 45), image)
                i += 1
            elif carState == "left":
                cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 135), image)
                i += 1
            elif carState == "go":
                cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 90), image)
                i += 1
            
            cv2.imshow('Original', image)
            
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
    GPIO.cleanup()
