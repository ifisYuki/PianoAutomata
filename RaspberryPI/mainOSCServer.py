# 树莓派端
# 
import argparse
import math
import json
import datetime
import time
import hashlib
import random
import RPi.GPIO as GPIO
import sys

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from adafruit_servokit import ServoKit

serverid = "pi" #树莓派端服务的自定义名
token = ""  #用于保存识别当前连上来的界面端

run_command1 = False
stop_command1 = False
run_command2 = False
stop_command2 = False
run_command3 = False
stop_command3 = False
default_start = False
default_stop = False

laser_pin = 24
SPEED_OF_LIGHT = 299792458

kit = ServoKit(channels=16)

# 初始化GPIO
GPIO.setmode(GPIO.BCM)
# key set up
key_interval_1 = 0.5
key_interval_2 = 0.1
key_num = 1
# rotate set up
initial_speed = 0.0
speed = -0.5
min_speed = -1.0
max_speed = 1.0
servo_360 = kit.continuous_servo[1]
servo_360.throttle = initial_speed
# sensor set up
DisRangeIsTrue = True
# other switch set up
RotateIsTrue = True
KeyIsTrue = True
 
def handIn(ipaddr, jsonObj):
  global client, token, serverid
  clientid = jsonObj["id"]
  client = udp_client.SimpleUDPClient(ipaddr, 9091) #界面端的IP和端口
  respObj = {}
  if serverid != jsonObj["server"] :
    #连接失败，名称错误
    respObj["error"] = 100
    respObj["message"] = u"服务器名错误"
  else :
    #连接成功
    respObj["error"] = 0
    respObj["message"] = u"连接成功"
    token = hashlib.md5((ipaddr + str(datetime.datetime.now)).encode(encoding='UTF-8')).hexdigest() #建立一个具有唯一性的token
    respObj["clientid"] = clientid
    respObj["timestamp"] = jsonObj["timestamp"]
    respObj["token"] = token
  client.send_message("/jsonmsg", json.dumps(respObj)) #向界面端发送返回消息

def rotate(RotateIsTrue, speed):
    if RotateIsTrue:
      speed = max(min(speed, max_speed), min_speed)  # 限制转速在范围内
      servo_360.throttle = speed  # 设置舵机转速
    else:
      servo_360.throttle = 0.0  # 停止舵机转动

def choose_which_key(key_num):
    global KeyIsTrue, RotateIsTrue
    KeyIsTrue = True
    RotateIsTrue = False
    servo_pin = 17 - key_num
    key_interval_1 = 1.0
    key_interval_2 = 0.2
    print("key number is", key_num)
    rotate(RotateIsTrue, 0.0)
    servo_key(KeyIsTrue, key_interval_1, key_interval_2,servo_pin)
    time.sleep(10000000)
    #while not RotateIsTrue:
    #    rotate(RotateIsTrue, speed)

def servo_key(KeyIsTrue, key_interval_1, key_interval_2,servo_pin = 1):
	while KeyIsTrue:
		if servo_pin == 16:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 180
			break
		elif servo_pin == 15:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 150
			break
		elif servo_pin == 14:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 60
			break
		elif servo_pin == 13:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 50
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 120
			break
		elif servo_pin == 12:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 60
			break
		elif servo_pin == 11:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 120
			break
		elif servo_pin == 10:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 60
			break
		elif servo_pin == 9:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 120
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 160
			break
		elif servo_pin == 8:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 180
			break
		elif servo_pin == 7:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 110
			break
		elif servo_pin == 6:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 60
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 120
			break
		elif servo_pin == 5:
			time.sleep(key_interval_1)
			kit.servo[servo_pin-1].angle = 180
			time.sleep(key_interval_2)
			kit.servo[servo_pin-1].angle = 110
			break
  #time.sleep(100)

def defaultStart(ipaddr, jsonObj):
  global default_start, default_stop, client, token, RotateIsTrue, KeyIsTrue
  responseMesage(ipaddr, jsonObj, 0, u"默认模式启动")
  while not default_stop:
    key_interval_1 = 1.0
    key_interval_2 = 0.2
    servo_pin = random.randint(5,16)
    RotateIsTrue = True
    KeyIsTrue = True
    rotate(RotateIsTrue, speed)
    servo_key(KeyIsTrue, key_interval_1, key_interval_2, servo_pin)

  default_start = False   
    
def defaultStop(ipaddr, jsonObj):
  global default_start, default_stop, client, token, RotateIsTrue, KeyIsTrue
  responseMesage(ipaddr, jsonObj, 0, u"默认模式关闭")
  while not default_start:
    RotateIsTrue = False
    KeyIsTrue = False
    rotate(RotateIsTrue, speed)
    servo_key(KeyIsTrue, key_interval_1, key_interval_2)
    time.sleep(10000000)
def command1(ipaddr, jsonObj):
  global RotateIsTrue, run_command1, stop_command1, client, token
  responseMesage(ipaddr, jsonObj, 0, u"模式1启动") #根据执行情况，返回成功或失败, 及具体信息
  while not stop_command1:#如果没有停止命令，就一直循环，如果不需要循环，这一句就不需要了
    #执行命令1 代替pass
    key_interval_1 = 0.8
    key_interval_2 = 0.2
    servo_pin = random.randint(5,16)
    RotateIsTrue = True
    KeyIsTrue = True
    rotate(RotateIsTrue, speed)
    servo_key(KeyIsTrue, key_interval_1, key_interval_2)
    
  run_command1 = False #这里表示已执行完毕

def stopcommand1(ipaddr, jsonObj):
  global KeyIsTrue, RotateIsTrue, run_command1, stop_command1, client, token
  #执行停止命令
  while run_command1:
    RotateIsTrue = False
    KeyIsTrue = False
    rotate(RotateIsTrue, speed)
    servo_key(DisRangeIsTrue, key_interval_1, key_interval_2)
    time.sleep(100)
  responseMesage(ipaddr, jsonObj, 0, u"模式1已停止") #根据执行情况，返回成功或失败, 及具体信息


def command2(ipaddr, jsonObj):
  global servo_pin,KeyIsTrue, RotateIsTrue, run_command2, stop_command2, client, token
  responseMesage(ipaddr, jsonObj, 0, u"模式2启动") #根据执行情况，返回成功或失败, 及具体信息
  while not stop_command2:#如果没有停止命令，就一直循环，如果不需要循环，这一句就不需要了
    #执行命令1 代替pass
    key_interval_1 = 0.5
    key_interval_2 = 0.1
    servo_pin = random.randint(5,16)
    RotateIsTrue = True
    KeyIsTrue = True
    rotate(RotateIsTrue, speed)
    servo_key(DisRangeIsTrue, key_interval_1, key_interval_2)
  run_command2 = False #这里表示已执行完毕
  time.sleep(100)

def stopcommand2(ipaddr, jsonObj):
  global KeyIsTrue, RotateIsTrue, run_command2, stop_command2, client, token
  #执行停止命令
  while run_command2:
    RotateIsTrue = False
    KeyIsTrue = False
    rotate(RotateIsTrue, speed)
    servo_key(DisRangeIsTrue, key_interval_1, key_interval_2)
    time.sleep(100)
  responseMesage(ipaddr, jsonObj, 0, u"模式3已停止") #根据执行情况，返回成功或失败, 及具体信息

def command3(ipaddr, jsonObj):
  global servo_pin,KeyIsTrue,RotateIsTrue, run_command3, stop_command3, client, token
  responseMesage(ipaddr, jsonObj, 0, u"模式3启动") #根据执行情况，返回成功或失败, 及具体信息
  while not stop_command3:#如果没有停止命令，就一直循环，如果不需要循环，这一句就不需要了
    #执行命令1 代替pass
    key_interval_1 = 0.2
    key_interval_2 = 0.08
    servo_pin = random.randint(5,16)
    RotateIsTrue = True
    KeyIsTrue = True
    rotate(RotateIsTrue, speed)
    servo_key(DisRangeIsTrue, key_interval_1, key_interval_2)
  run_command3 = False #这里表示已执行完毕
  

def stopcommand3(ipaddr, jsonObj):
  global KeyIsTrue, RotateIsTrue, run_command3, stop_command3, client, token
  #执行停止命令
  while run_command3:
    RotateIsTrue = False
    KeyIsTrue = False
    rotate(RotateIsTrue, speed)
    servo_key(DisRangeIsTrue, key_interval_1, key_interval_2)
    time.sleep(100)
  responseMesage(ipaddr, jsonObj, 0, u"模式3已停止") #根据执行情况，返回成功或失败, 及具体信息

def sensor(ipaddr, jsonObj):
  global client
  #执行enable或diable传感器的命令
  responseMesage(ipaddr, jsonObj, 0, u"") #根据执行情况，返回成功或失败, 及具体信息

def responseMesage(ipaddr, jsonObj, error, message) :
  global client
  respObj = {}
  respObj["error"] = error
  respObj["message"] = message
  respObj["timestamp"] = jsonObj["timestamp"]
  client.send_message("/jsonmsg", json.dumps(respObj)) #向界面端发送返回消息

def idle():#闲时操作
  time.sleep(100)

def dealjson(ipaddr, clientaddr, args):
    global RotateIsTrue, KeyIsTrue, default_start, default_stop, run_command1, stop_command1, run_command2, stop_command2, run_command3, stop_command3, client, token

    try:
        jsonstring = args
        jsonObj = json.loads(jsonstring)
        print(ipaddr[0])
        print(jsonstring)

        if jsonObj["command"] == "conn":
            handIn(ipaddr[0], jsonObj)  # ipaddr[0] 是连上来的客户端IP
        else:
            print(token)
            if jsonObj["token"] != token:
                responseMesage(ipaddr[0], jsonObj, 200, u"身份识别错误")  # 根据执行情况，返回成功或失败, 及具体信息
                return

            if jsonObj["command"] == "quit":
                client = None
                token = None
                responseMesage(ipaddr[0], jsonObj, 0, u"连接关闭")  # 根据执行情况，返回成功或失败, 及具体信息
            elif jsonObj["command"] == "default":
                if jsonObj["mode"] == "default_start":
                    if not default_start:
                        default_start = True
                        default_stop = False
                        defaultStart(ipaddr[0], jsonObj)
                    else:
                        responseMesage(ipaddr[0], jsonObj, 201, u"运行中")
                elif jsonObj["mode"] == "default_stop":
                    if  not default_stop:
                        default_stop = True
                        default_start = False
                        defaultStop(ipaddr[0], jsonObj)
                    else:
                        responseMesage(ipaddr[0], jsonObj, 203, u"模式未运行")
            elif jsonObj["command"] == "run":
                if jsonObj["mode"] == "1":
                    stop_command2 = True  # 停止模式2
                    stop_command3 = True  # 停止模式3

                    if not run_command1:
                        stop_command1 = False
                        run_command1 = True
                        command1(ipaddr[0], jsonObj)
                    else:
                        responseMesage(ipaddr[0], jsonObj, 201, u"运行中")  # 根据执行情况，返回成功或失败, 及具体信息
                elif jsonObj["mode"] == "2":
                    stop_command1 = True  # 停止模式1
                    stop_command3 = True  # 停止模式3

                    if not run_command2:
                        stop_command2 = False
                        run_command2 = True
                        command2(ipaddr[0], jsonObj)
                    else:
                        responseMesage(ipaddr[0], jsonObj, 201, u"运行中")  # 根据执行情况，返回成功或失败, 及具体信息
                elif jsonObj["mode"] == "3":
                        stop_command1 = True  # 停止模式1
                        stop_command2 = True  # 停止模式3

                        if not run_command3:
                            stop_command3 = False
                            run_command3 = True
                            command3(ipaddr[0], jsonObj)
                        else:
                            responseMesage(ipaddr[0], jsonObj, 201, u"运行中")  # 根据执行情况，返回成功或失败, 及具体信息
            elif jsonObj["command"] == "custom":
                KeyIsTrue = True
                RotateIsTrue = False
                
                key_num = int(jsonObj["key_num"])
                print("key number received ", key_num)
                choose_which_key(key_num)
                KeyIsTrue = False
                rotate(RotateIsTrue, speed)
                servo_key(KeyIsTrue, key_interval_1, key_interval_2)
                print("single key run")


            elif jsonObj["command"] == "stop":
                if jsonObj["mode"] == "1":
                    if run_command1 and not stop_command1:
                        stop_command1 = True
                        stopcommand1(ipaddr[0], jsonObj)
                    else:
                        responseMesage(ipaddr[0], jsonObj, 203, u"模式未运行")  # 根据执行情况，返回成功或失败, 及具体信息
                elif jsonObj["mode"] == "2":
                    if run_command2 and not stop_command2:
                        stop_command2 = True
                        stopcommand2(ipaddr[0], jsonObj)
                    else:
                        responseMesage(ipaddr[0], jsonObj, 203, u"模式未运行")  # 根据执行情况，返回成功或失败, 及具体信息
            elif jsonObj["sensor"]:
                sensor(ipaddr[0], jsonObj)
    except Exception as err: 
          print(err)

if __name__ == "__main__":
    try:
        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/jsonmsg", dealjson, needs_reply_address=True)
        server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 9090), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()
    except KeyboardInterrupt:
        RotateIsTrue = False
        speed = 0.0
        rotate(RotateIsTrue, speed)
        print("Program interrupted by keyboard")
        sys.exit()
 

