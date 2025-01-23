# 树莓派端DEMO
# 
import argparse
import math
import json
import datetime
import time
import hashlib

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

serverid = "pi" #树莓派端服务的自定义名
token = ""  #用于保存识别当前连上来的界面端

run_command1 = False
stop_command1 = False
run_command2 = False
stop_command2 = False
run_command3 = False
stop_command3 = False

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

def command1(ipaddr, jsonObj):
  global run_command1, stop_command1, client, token
  responseMesage(ipaddr, jsonObj, 0, u"模式1启动") #根据执行情况，返回成功或失败, 及具体信息
  while not stop_command1:#如果没有停止命令，就一直循环，如果不需要循环，这一句就不需要了
    #执行命令1 代替pass
    pass
  run_command1 = False #这里表示已执行完毕

def stopcommand1(ipaddr, jsonObj):
  global run_command1, stop_command1, client, token
  #执行停止命令
  while run_command1:
    time.sleep(100)
  responseMesage(ipaddr, jsonObj, 0, u"模式1已停止") #根据执行情况，返回成功或失败, 及具体信息


def command2(ipaddr, jsonObj):
  global run_command2, stop_command2, client, token
  responseMesage(ipaddr, jsonObj, 0, u"模式2启动") #根据执行情况，返回成功或失败, 及具体信息
  while not stop_command2:#如果没有停止命令，就一直循环，如果不需要循环，这一句就不需要了
    #执行命令1 代替pass
    pass
  run_command2 = False #这里表示已执行完毕

def stopcommand2(ipaddr, jsonObj):
  global run_command2, stop_command2, client, token
  #执行停止命令
  while run_command2:
    time.sleep(100)
  responseMesage(ipaddr, jsonObj, 0, u"模式2已停止") #根据执行情况，返回成功或失败, 及具体信息

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
  global run_command1, stop_command1, run_command2, stop_command2, run_command3, stop_command3, client, token
  try:
    jsonstring = args
    jsonObj = json.loads(jsonstring)
    print(ipaddr[0])
    print(jsonstring)
    if jsonObj["command"] == "conn" :
        handIn(ipaddr[0], jsonObj)  #ipaddr[0] 是连上来的客户端IP
    else:
        print(token)
        if jsonObj["token"] != token:
          responseMesage(ipaddr[0], jsonObj, 200, u"身份识别错误") #根据执行情况，返回成功或失败, 及具体信息
          return
        if jsonObj["command"] == "quit" :
          client = None
          token = None
          responseMesage(ipaddr[0], jsonObj, 0, u"连接关闭") #根据执行情况，返回成功或失败, 及具体信息
        elif jsonObj["command"] == "run" : 
          if run_command1 or run_command2 or run_command3: #如果某个模式正在运行，就不执行
            responseMesage(ipaddr[0], jsonObj, 201, u"运行中") #根据执行情况，返回成功或失败, 及具体信息
          elif jsonObj["mode"] == "1":
            stop_command1 = False
            run_command1 = True
            command1(ipaddr[0], jsonObj)
          elif jsonObj["mode"] == "2":
            stop_command1 = False
            run_command1 = True
            command2(ipaddr[0], jsonObj)
        elif jsonObj["command"] == "stop" :
          if jsonObj["mode"] == "1":
            if stop_command1 == True:
              if run_command1:
                responseMesage(ipaddr[0], jsonObj, 202, u"模式正在停止中") #根据执行情况，返回成功或失败, 及具体信息
              else:
                responseMesage(ipaddr[0], jsonObj, 0, u"模式已停止") #根据执行情况，返回成功或失败, 及具体信息
            elif not run_command1:
              responseMesage(ipaddr[0], jsonObj, 203, u"模式未运行") #根据执行情况，返回成功或失败, 及具体信息
            else:
              stop_command1 = True
              stopcommand1(ipaddr[0], jsonObj)
          elif jsonObj["mode"] == "2":
            if stop_command2 == True:
              if run_command2:
                responseMesage(ipaddr[0], jsonObj, 202, u"模式正在停止中") #根据执行情况，返回成功或失败, 及具体信息
              else:
                responseMesage(ipaddr[0], jsonObj, 0, u"模式已停止") #根据执行情况，返回成功或失败, 及具体信息
            elif not run_command2:
              responseMesage(ipaddr[0], jsonObj, 203, u"模式未运行") #根据执行情况，返回成功或失败, 及具体信息
            else:
              stop_command2 = True
              stopcommand2(ipaddr[0], jsonObj)
        elif jsonObj["sensor"] :
          sensor(ipaddr[0], jsonObj)

  except Exception as err: 
      print(err)

if __name__ == "__main__":
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/jsonmsg", dealjson, needs_reply_address = True)
  server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 9090), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
  #while (True):
  #  idle()
