#!/usr/bin/python
# -*- coding: utf-8 -*-

#########################################
# program do obslugi silnika krokowego 
#
# 2016.01.11 v.1.2
# zajaczkowski@mpip-mainz.mpg.de
#
#########################################

import time
import serial
import getopt
import sys
import math

#some constans
delay=0.3
delta = 1.0 # provide a reasonable default value...


def init_controler():
  ser = serial.Serial(
	port='/dev/ttyUSB2',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.EIGHTBITS,
	timeout=10,
	xonxoff=0,
	rtscts=0)

#  ser.open() # we dont need this anymore in new version of python library 
  ser.isOpen()
  ser.flushOutput()
  ser.flushInput()
  return ser


def close_controler(ser):
	write_slowly(ser, "\x1B", delay=0.3)
	ser.close()

def write_slowly(ser, cmdstring, delay=0):
  for i in cmdstring:
	time.sleep(delay)
        ser.write(i)

def read_slowly(ser, delay=0):
	line = ''
	lines= ''
	ss = 0
	while line!="P1":
		for c in ser.read():
			if c == '\n':
				lines=line
				line = ''
				if lines != '\r':
					if lines[:1] != "?":
						ss += int(lines)
				break
			else:
				line += c
			break

	return(int(ss))


def move_motor_steps(ser,motor,steps):
	cmd="\x1B"+str(motor)+'X'+str(steps)+'\r\n'
	write_slowly(ser, cmd, delay=0.2)
	return  read_slowly(ser, 0.1)
	#return steps
	
def move_motor(motor, steps):
	ser=init_controler()
	done_steps=move_motor_steps(ser, motor, steps)
	close_controler(ser)
	save_log(motor,steps)
	return done_steps


def save_log(motor, stepss):
	text_file = open("/home/mar345/log/motor_move.log", "a")
	txt=time.strftime("%Y:%m:%d-%H:%M:%S")+" :: MOTOR: "+str(motor)+" :: STEPS: "+str(stepss)+'\r\n'
	text_file.write(txt)
	text_file.close()
	return 0

