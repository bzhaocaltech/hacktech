import serial 
import struct 
from Tkinter import *

import tkMessageBox
import tkSimpleDialog
import sys, glob

import _winreg as winreg
import itertools

'''Cmds = {'128': 'PASSIVE MODE', '131': 'SAFE MODE', 
        '132': 'FULL MODE', '135': 'CLEAN', 
        '143': 'DOCK', 'SPACE': 'BEEP'
        '7': 'RESET'}
'''

connection = None

VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

def sendCommandRaw(command):
    global connection

    try:
        if connection is not None:
            connection.write(command)
        else:
            print "Not Connnected!!"
    
    except serial.SerialException:
        print "Lost connection!"
        connection = None
    print ' '.join([str(ord(c)) for c in command])
    text.insert(END, ' '.join([str(ord(c)) for c in command]))
    text.insert(END, '\n')
    text.see(END)

def sendCommandASCII(command):
    cmd = ""
    for v in command.split():
        sendCommandRaw(chr(int(v)))

def callbackKey(event):
    k = event.keysym.upper()
    motionChange = False

    if event.type == '2':
        callbackKey.up = False
        callbackKey.down = False
        callbackKey.left = False
        callbackKey.right = False
        if k == 'P': 
            sendCommandASCII('128')
        elif k =='S':
            sendCommandASCII('131')
        elif k == 'F':
            sendCommandASCII('132')
        elif k == 'C':
            sendCommandASCII('135')
        elif k == 'D':
            sendCommandASCII('143')
        elif k == 'SPACE':
            sendCommandASCII('140 3 1 64 16 141 3')
        elif k == 'R':
            sendCommandASCII('7')
        elif k == 'UP':
            callbackKey.up = True
            motionChange = True
        elif k == 'LEFT':
            callbackKey.left = True
            motionChange = True
        elif k == 'RIGHT':
            callbackKey.right = True
            motionChange = True
        elif k == 'DOWN':
            callbackKey.down = False
            motionChange = False

    if motionChange == True:
        velocity = 0
        velocity += VELOCITYCHANGE if callbackKey.up is True else 0 
        velocity -= VELOCITYCHANGE if callbackKey.down is True else 0 
        rotation = 0
        rotation += ROTATIONCHANGE if callbackKey.left is True else 0
        rotation += ROTATIONCHANGE if callbackKey.right is True else 0

        vr = velocity + (rotation / 2)
        vl = velocity - (rotation / 2)

        cmd = struct.pack(">Bhh", 145, vr, vl)
        if cmd != callbackKey.lastDriveCommand:
            sendCommandRaw(cmd)
            callbackKey.lastDriveCommand = cmd
        
def onConnect():
    global connection 

    ports = "COM3"

    if ports is not None:
        print 'Connecting to ' + str(ports) + '...'
        try:
            connection = serial.Serial(ports, baudrate=115200, timeout=1)
            print "Connected!"
        except:
            print "Failed."

def onQuit():
    root.destroy()

callbackKey.up = False
callbackKey.down = False
callbackKey.left = False
callbackKey.right = False
callbackKey.lastDriveCommand = ''

root = Tk()

menu = Menu(root)
menu.add_command(label="Connect", command=onConnect)
menu.add_command(label="Quit", command=onQuit)
root.config(menu=menu)

text = Text(root, height=16, width=40, wrap=WORD)
scroll = Scrollbar(root, command=text.yview)
text.configure(yscrollcommand=scroll.set)
text.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)

root.bind("<Key>", callbackKey)
root.bind("<KeyRelease>", callbackKey)

root.mainloop()
