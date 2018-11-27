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
import glob
from ConfigParser import SafeConfigParser
import motor


def get_motparam(motor):
	if motor == '1':
		name = 'Motor_1'
		file = '/home/mar345/log/motor1.cfg'
	elif motor == '2':
		name = 'Motor_2'
		file = '/home/mar345/log/motor2.cfg'
	elif motor == '3':
		name = 'Motor_3'
		file = '/home/mar345/log/motor3.cfg'
	elif motor == '4':
		name = 'Motor_4'
		file = '/home/mar345/log/motor4.cfg'
	elif motor == '5':
		name = 'Motor_5'
		file = '/home/mar345/log/motor5.cfg'
	elif motor == '6':
		name = 'Motor_6'
		file = '/home/mar345/log/motor6.cfg'
	elif motor == '7':
		name = 'Motor_7'
		file = '/home/mar345/log/motor7.cfg'
	else:
		print ":: ERROR"
		exit()
	return name, file

def get_param(motor,param):
	name,file = get_motparam(motor)

	parser = SafeConfigParser()
	parser.read(file)	
	return parser.get(name, param)

def save_param(motor,param,val):
	name,file = get_motparam(motor)

	parser = SafeConfigParser()
	parser.read(file)	
	parser.set(name, param, val)
	cfgfile = open(file,'w')
	parser.write(cfgfile)
	cfgfile.close()
	return 0



def set_position(mot, step):

	if float(step) > 0:
		directions = 1.0 
	else:
		directions = -1.0

	mot_unit    =        get_param(mot,"unit"    )
	mot_ratio   = float( get_param(mot,"ratio"   ))
	mot_old_pos = float( get_param(mot,"position"))
	mot_error   =   int( get_param(mot,"error"   ))
	mot_realpos = float( get_param(mot,"real_pos"))
	mot_new_pos = float( step )
        mot_posmin  = float( get_param(mot,"pos_min"))
        mot_posmax  = float( get_param(mot,"pos_max"))

	mot_todo       = mot_new_pos - mot_old_pos
	mot_todo_steps = int(mot_todo*mot_ratio )

        if ( (mot_realpos+mot_todo) >= mot_posmax ):
                print ":: ERROR Step is to big, reach MAX position"
                print ":: ERROR You can move only: ", str(mot_posmax-mot_realpos),mot_unit
                sys.exit()

        if ( (mot_realpos+mot_todo) <= mot_posmin ):
                print ":: ERROR Step is to big, reach MIN position"
                print ":: ERROR You can move only: ", str(mot_posmin-mot_realpos), mot_unit
                sys.exit()

	print "MOTOR: [",mot,"] OLD POSITION: ",mot_old_pos,"[",mot_unit,"] MOVE TO: ", mot_new_pos, "[",mot_unit,"] :: TO DO: ",mot_todo," :: ",mot_todo_steps

	done_errpl = motor.move_motor(mot,(   directions*mot_error*0.5) )
	done_steps = motor.move_motor(mot,int(mot_todo_steps)           )
	done_errmi = motor.move_motor(mot,(-1*directions*mot_error*0.5) )

	mot_new_done    = mot_old_pos + (float(done_steps)/mot_ratio)
	mot_new_realpos = mot_realpos + (float(done_steps)/mot_ratio)
	

	print "MOTOR: [",mot,"] NEW POSITION: ",mot_new_done,"[",mot_unit,"] DONE: ",done_steps/mot_ratio,"[",mot_unit,"] :: e: [should be 0]",(done_errmi+done_errpl)

	save_param(mot,"position",str(mot_new_done))
	save_param(mot,"real_pos",str(mot_new_realpos))

	return 0
	

#--------------------------------------------------#
#-------- Here the actual program starts ----------#
#--------------------------------------------------#




if len(sys.argv) != 3:
	print "::"
	print ":: ERROR "
	print ":: Please double check command "
	print ":: motor_mv [motor] [absolut position]"
	print "::"
	sys.exit()
else:
	st = sys.argv[2]
	mo  = sys.argv[1]

	set_position(mo,st)

	text_file = open("/home/mar345/log/silnik.log", "a")
	txt=time.strftime("%Y:%m:%d-%H:%M:%S")+" :: MOTOR: "+str(mo)+" :: STEPS: "+str(st)+'\r\n'
	text_file.write(txt)
	text_file.close()
	sys.exit()

#--------------------------------------------------#
