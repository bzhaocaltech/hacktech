import serial 
import struct 
from Tkinter import *

import tkMessageBox
import tkSimpleDialog
import sys, glob

import _winreg as winreg
import itertools

Cmds = {'P': '128', 'S': '132', 'F': '132', 'C': '135',
        'D': '143', 'SPACE': '140 3 1 64 16 141 3', 'R': '7'
        }


connection = None

VELOCITYUNIT = 200 # How much faster robot moves with each up/down
ROTATIONUNIT = 300 # How much faster robot rotates with each left/right
MAXSPEED = 3 # Max number of VELOCITYUNITS and ROTATIONUNITS robot can go

upMotion = 0
leftMotion = 0

def sendCommandRaw(command):
    global connection

    try:
        if connection is not None:
            print type(connection)
            connection.write(command)
        else:
            print "Not Connnected!!"
    
    except serial.SerialException:
        print "Lost connection!"
        connection = None

    
    cmd = ' '.join([str(ord(c)) for c in command])
    if cmd[:3] == '145':
        print 'MOTION' + cmd[3:]
        text.insert(END, 'MOTION' + cmd[3:])
        text.insert(END, '\n')
        text.see(END)      

def sendCommandASCII(command):
    cmd = ""
    for v in command.split():
        sendCommandRaw(chr(int(v)))

def printToCMD(command):
    print command
    text.insert(END, command)
    text.insert(END, '\n')
    text.see(END)

def callbackKey(event):
    global upMotion, leftMotion, connection
    k = event.keysym.upper()
    motionChange = False

    if event.type == '2':
<<<<<<< HEAD
        if k == 'P': 
            sendCommandASCII(Cmds['P'])
            print 'PASSIVE MODE'
        elif k =='S':
            sendCommandASCII(Cmds['S'])
            print 'SAFE MODE'
        elif k == 'F':
            sendCommandASCII(Cmds['F'])
            print 'FULL MODE'
        elif k == 'C':
            sendCommandASCII(Cmds['C'])
            print 'CLEAN'
        elif k == 'D':
            sendCommandASCII(Cmds['D'])
            print 'DOCK'
        elif k == 'SPACE':
            sendCommandASCII(Cmds['SPACE'])
            print 'BEEEEEEP'
        elif k == 'R':
            sendCommandASCII(Cmds['R'])
            print 'RESET'
        elif k == 'UP':
            upMotion += 1
            motionChange = True
        elif k == 'LEFT':
            leftMotion += 1
            motionChange = True
        elif k == 'RIGHT':
            leftMotion -= 1
            motionChange = True
        elif k == 'DOWN':
            upMotion -= 1
            motionChange = True

        elif k == 'M': # Stop movement
            upMotion = 0
            leftMotion = 0
            motionChange = True
        
        elif k == 'Q': 
            sendCommandASCII('148 2 29 13')
            connection.read()


    if motionChange == True:
        velocity = upMotion * VELOCITYUNIT
        rotation = leftMotion * ROTATIONUNIT

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
