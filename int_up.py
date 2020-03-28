from __future__ import print_function

import socket
import sys
import threading
import Queue
from Queue import *
import time
import select
from decimal import Decimal
import copy
import inspect
import base64
import random

import platform

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    Default = '\033[99m'

# python asciiVID.py laddjones 4000 128.61.18.196 3000
# ------ ----------   name    yr port    f_ip   f_port

# Luke was here

# lukes 199.111.213.244
print ("")
# globals
# listening at port - client_port
this_addr = socket.gethostname()
client_port = 0
f_port = 0
user_id = "anonymous"

print_flag = 0
print_message = 1
f_addr = []

pingFlag = 0

nodes_alive = []

attack_spam = False
diamond_attach = False

try: 
  user_id = str(sys.argv[1])
  client_port = int(sys.argv[2])
except:
  print ("entered stuff in wrong")
i = 3
while i < 100:
  try:
    f_addr.append((str(socket.gethostname()), int(sys.argv[i])))
  except:
    print("here are your friends locations")
    i = 100
  i = i + 1
print(f_addr)

listen_at = (this_addr, client_port)


def randomColor():
  num = random.randint(1, 8)
  if num == 1:
    return bcolors.Red
  if num == 2:
    return bcolors.Green
  if num == 3:
    return bcolors.Blue
  if num == 4:
    return bcolors.Cyan
  if num == 5:
    return bcolors.Yellow
  if num == 6:
    return bcolors.Magenta
  if num == 7:
    return bcolors.White
  if num == 8:
    return bcolors.Grey

def command_list():
  global attack_spam
  global diamond_attach

  while True:
    if (attack_spam == True):
      spamTime = time.time()
      while time.time() - spamTime < 1:
        print(str(randomColor()) + "***HACKED***" + str(bcolors.ENDC), end='')
      attack_spam = False
    if (diamond_attach == True):
      spamTime = time.time()
      while time.time() - spamTime < 1:
        print(str(randomColor()) + " $ " + str(bcolors.ENDC), end='')
      diamond_attach = False



def print_command(pass_id, pass_mess):
  global print_flag
  global print_message

  if print_flag == 1:
    rainbow = "1"
    orange = "2"
    magenta = "3"
    if rainbow in pass_id:
      for i in pass_id:
        print(str(randomColor()) + i + str(bcolors.ENDC), end='')
    elif orange in pass_id:
      print(bcolors.WARNING + pass_id + bcolors.ENDC, end='')
    elif magenta in pass_id:
      print(bcolors.Magenta + pass_id + bcolors.ENDC, end='')
    else:
      print (bcolors.White + pass_id + bcolors.ENDC, end='')
    print (bcolors.Cyan + ": " + pass_mess + bcolors.ENDC)
  print_flag = 0

def network_listner():
  global f_addr
  global pingFlag
  global nodes_alive
  
  nodes_alive_hold = []

  udpNetMonSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  while True:
    for i in f_addr:
      pingFlag = 0
      timer = time.time()
      while pingFlag == 0 and time.time() - timer < 1:
        try:
          uInput = "*networkTest"
          packet = user_id + "|" + str(client_port) + "|" + uInput
          sent = udpNetMonSocket.sendto(packet.encode(), i)
          waitTime = time.time()
          while time.time() - waitTime < .4:
            wait = True
        except:
          print ("the connection got fucked")
      if time.time() - timer < 1:
        nodes_alive_hold.append(i)
      else:
        skip = True
    
    if nodes_alive != nodes_alive_hold:
      nodes_alive = nodes_alive_hold
      print("Updated nodes alive: ")
      for i in nodes_alive:
        print("--port--" + str(i[1]))
      if nodes_alive == []:
        print("--no nodes online--")

    nodes_alive_hold = []

def server():
  global client_port
  global f_port
  global listen_at
  global user_id
  global print_flag
  global f_addr
  global pingFlag
  global attack_spam
  global diamond_attach

  udpSocketListen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udpSocketListen.bind(listen_at)

  while True:
    data, address = udpSocketListen.recvfrom(65535)
    data = data.decode()
    i = 0
    sender_id = ""
    sender_port = ""
    while data[i] != "|":
      sender_id = sender_id + str(data[i])
      i = i + 1
    i = i + 1
    while data[i] != "|":
      sender_port = sender_port + str(data[i])
      i = i + 1
    txt_mess = data[i+1:]
    
    if txt_mess == "*status":
      packet = user_id + "|" + str(client_port) + "|" + "**status"
      sent = udpSocketListen.sendto(packet.encode(), (socket.gethostname(), int(sender_port)))
    elif txt_mess == "**status":
      print(sender_id + " @port: " + sender_port)

    elif txt_mess == "*networkTest":
      packet = user_id + "|" + str(client_port) + "|" + "**networkTest"
      sent = udpSocketListen.sendto(packet.encode(), (socket.gethostname(), int(sender_port))) 
    elif txt_mess == "**networkTest":
      pingFlag = 1
    elif txt_mess == "*hack":
      attack_spam = True
    elif txt_mess == "diamond":
      diamond_attach = True
    else:
      print_flag = 1
      print_command(sender_id, txt_mess)

    

def client():
  global clinet_name
  global client_port
  global f_port
  global f_loc
  global listen_at
  global user_id
  global f_addr

  udpSocketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  print ("________________CHAT__________________")
  
  while True:
    try:
      uInput = raw_input('')
    except:
      print ("ok what>.....")

    if uInput == "*status":
      for i in f_addr:
        try:
          packet = user_id + "|" + str(client_port) + "|" + uInput
          sent = udpSocketClient.sendto(packet.encode(), i)
        except:
          print ("the connection got fucked")

    else:
      for i in f_addr:
        try:
          packet = user_id + "|" + str(client_port) + "|" + uInput
          sent = udpSocketClient.sendto(packet.encode(), i)
        except:
          print ("the connection got fucked")



def intel_method(value):
  if value == 1:
    server()
  if value == 2:
    client()
  if value == 3:
    print_command("", "")
  if value == 4:
    network_listner()
  if value == 5:
    command_list()

def process_threads():
  while True:
    intel_method(threads_queue.get())
    threads_queue.task_done()


threads_queue = Queue()

threads_queue.put(1)
threads_queue.put(2)
threads_queue.put(3)
threads_queue.put(4)
threads_queue.put(5)



for i in range(5):
  t = threading.Thread(target=process_threads)
  t.daemon = True
  t.start()


while True == True:
  wait = True
