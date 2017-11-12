from __future__ import division

import RPi.GPIO as gpio
import Tkinter as tk
import time
import sys
import picamera
import time
import Adafruit_PCA9685
import curses
#import logging
#logging.basicConfig(level=logging.DEBUG)

pwm = Adafruit_PCA9685.PCA9685()
camera = picamera.PiCamera()
 
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm.set_pwm_freq(60)
old_position = 360
starting_laser = False

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    pulse_length //= 4096     # 12 bits of resolution
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.

def servo_left(sp, tf):
    servo_position = min(580,sp+20)
#print("__ "+str(servo_position))
    pwm.set_pwm(0,0, servo_position)
    time.sleep(tf)
    #gpio.cleanup()
    return servo_position

def servo_right(sp,tf):
    servo_position = max(160, sp-20)
 #   print("__ "+str(servo_position))
    pwm.set_pwm(0,0,servo_position)
    time.sleep(tf)
    #gpio.cleanup()
    return servo_position

def laser_toggle(lstatus):
    if lstatus == True:
        gpio.output(17, False)
        return False
    else:
        gpio.output(17, True)
        return True

def init():
     gpio.setmode(gpio.BCM)
     gpio.setup(20, gpio.OUT)
     gpio.setup(21, gpio.OUT)
     gpio.setup(5, gpio.OUT)
     gpio.setup(6, gpio.OUT)
#     gpio.setup(17,gpio.OUT)	
     gpio.output(20, False)
     gpio.output(21, False)
     gpio.output(5, False)
     gpio.output(6, False)
 #    print ("1")
     
def forward(tf):
     gpio.output(20, True)
     gpio.output(21, False)
     gpio.output(5, True) 
     gpio.output(6, False)
     time.sleep(tf)
     gpio.output(20, False) 
     gpio.output(5, False)
	#gpio.cleanup()
 
def reverse(tf):
     gpio.output(20, False)
     gpio.output(21, True)
     gpio.output(5, False) 
     gpio.output(6, True)
     time.sleep(tf)
#     gpio.cleanup()
     gpio.output(21, False)
     gpio.output(6, False)

def turn_right(tf):
     gpio.output(20, True)
     gpio.output(21, False)
     gpio.output(5, False) 
     gpio.output(6, True)
     time.sleep(tf)
#     gpio.cleanup()
     gpio.output(20, False)
     gpio.output(6, False)

def turn_left(tf):
     gpio.output(20, False)
     gpio.output(21, True)
     gpio.output(5, True) 
     gpio.output(6, False)
     time.sleep(tf)
     gpio.output(21, False)
     gpio.output(5, False)
    # gpio.cleanup()

def stop(tf):
     gpio.output(20, False)
     gpio.output(21, False)
     gpio.output(5, False) 
     gpio.output(6, False)
     time.sleep(tf)
#     gpio.cleanup()
    
def key_input (event):
    key_press = event.char	
    sleep_time = 0.030
    global old_position
    global starting_laser
    init()
    if event.keysym == 'Escape':
        stop(sleep_time)        
	gpio.cleanup()
        command.quit()
    elif event.keysym == 'Up':
	forward(sleep_time)
    elif event.keysym == 'Down':
	reverse(sleep_time)
    elif event.keysym =='Left':
        turn_left(sleep_time)
    elif event.keysym == 'Right':
        turn_right(sleep_time)
    elif event.keysym == 'l':
        laser = laser_toggle(starting_laser)
        starting_laser = laser
    elif event.keysym == 'a':
        new_position = servo_left(old_position,sleep_time)
        old_position = new_position
    elif event.keysym == 'BackSpace':
        stop(sleep_time)
    elif event.keysym == 'd':
        new_position = servo_right(old_position,sleep_time)
        old_position = new_position
    else:
        pass

#print("start")
readchar = curses.initscr()
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(17, False)
pwm.set_pwm(0,0,old_position)
camera.resolution = (1024,768)
camera.start_preview(fullscreen=False, window=(100,50,800,640))

 
while True:
	c = readchar.getch()
	print (c)

#command = tk.Tk()
#command.binKeyPress>', key_input)
#command.mainloop()

