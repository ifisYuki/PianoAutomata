import RPi.GPIO as GPIO
from time import sleep as sleep
from time import time as time
from adafruit_servokit import ServoKit
import random

laser_pin = 24
SPEED_OF_LIGHT = 299792458

kit = ServoKit(channels=16)
# key set up
key_interval_1 = 0.5
key_interval_2 = 0.1
# rotate set up
initial_speed = 0.0
speed = -0.5
min_speed = -1.0
max_speed = 1.0
servo_360 = kit.continuous_servo[0]
servo_360.throttle = initial_speed

def servo_key(DisRangeIsTrue):
	while DisRangeIsTrue:
		servo_pin = random.randint(5,16)
		if servo_pin == 16:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 180
			break
		elif servo_pin == 15:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 150
			break
		elif servo_pin == 14:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 60
			break
		elif servo_pin == 13:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 50
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 120
			break
		elif servo_pin == 12:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 60
			break
		elif servo_pin == 11:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 120
			break
		elif servo_pin == 10:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 60
			break
		elif servo_pin == 9:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 120
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 160
			break
		elif servo_pin == 8:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 180
			break
		elif servo_pin == 7:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 110
			break
		elif servo_pin == 6:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 120
			break
		elif servo_pin == 5:
			sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 110
			break
 			
def rotate(DisRangeIsTrue):
	# switch_servo_360 = input("请输入指令（stop, speed）：")

	while (DisRangeIsTrue == False):
		servo_360.throttle = initial_speed  # 停止舵机转动
		break
	while(DisRangeIsTrue == True):
		#speed = float(input("请输入转速值（范围: -1.0 到 1.0）："))
		#speed = max(min(speed, max_speed), min_speed)  # 限制转速在范围内
		servo_360.throttle = speed  # 设置舵机转速
		break
		
def distance():
	# set up
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(laser_pin, GPIO.OUT)
	GPIO.output(laser_pin, GPIO.LOW)
	
	# send laser signal
	GPIO.output(laser_pin, GPIO.HIGH)
	sleep(0.00001)
	GPIO.output(laser_pin,GPIO.LOW)
	
	# receive laser signal
	GPIO.setup(laser_pin, GPIO.IN)
	start_time = time()
	end_time = time()
	
	# wait for signal
	while GPIO.input(laser_pin) == GPIO.LOW:
		start_time = time()
	while GPIO.input(laser_pin) == GPIO.HIGH:
		end_time = time()	
	
	# calculate dist
	time_interval = end_time - start_time
	distance = time_interval * SPEED_OF_LIGHT / 2
	
	GPIO.cleanup()
	
	return distance



def DisRange(distance):
	sleep(0.000001)
	if distance < 50:
		return True
	else:
		return False

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		while True:
			dis = distance()
			print(dis)
			DisRangeIsTrue = DisRange(dis)
			#DisRangeIsTrue = True
			rotate(DisRangeIsTrue)
			servo_key(DisRangeIsTrue)
			print(DisRangeIsTrue)
			sleep(0.1)
	except KeyboardInterrupt:
		rotate(False)
		destroy()
