from gpiozero import Button, LEDBoard, AngularServo
from omxplayer.player import OMXPlayer
from pathlib import Path
from signal import pause
from time import sleep

## Model Specific LED Colour Groups
body_leds = LEDBoard(6, 5, 13, 19, 16, 26, 20, 21, pwm=True)
hull_led = LEDBoard(18, pwm=True)
left_red_thruster = LEDBoard(27, pwm=True)
left_green_thruster = LEDBoard(22, pwm=True)
right_red_thruster = LEDBoard(4, pwm=True)
right_green_thruster = LEDBoard(17, pwm=True)
boosters = LEDBoard(24, 25, pwm=True)

# Thruster Servos
myCorrection=0.0
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
left_thruster = AngularServo(12, min_pulse_width=minPW, max_pulse_width=maxPW)
#right_thruster = AngularServo(, min_angle=-90, max_angle=90)

## Setup the audio files
explode_path = Path("/home/pi/ship-codes/audio/explode.ogg")

## Light sequences for the different modes
def leds_off():
	body_leds.off()
	hull_led.off()
	left_red_thruster.off()
	left_green_thruster.off()
	right_red_thruster.off()
	right_green_thruster.off()
	boosters.off()

def static_display():
	body_leds.on()
	hull_led.on()
	left_red_thruster.on()
	left_green_thruster.on()
	right_red_thruster.on()
	right_green_thruster.on()
	boosters.on()

def cruising_display():
	body_leds.on()
	boosters.on()
	hull_led.pulse(1.5,1.5)
	left_red_thruster.pulse(.5,.5)
	sleep(.25)
	left_green_thruster.pulse(.5,.5)
	sleep(.25)
	right_red_thruster.pulse(.5,.5)
	sleep(.25)
	right_green_thruster.pulse(.5,.5)

def orbital_display():
	body_leds.on()
	hull_led.pulse(.25,.25)
	for value in range(0,21):
		thrusterMove=(float(value)-10)/10
		left_thruster.value=thrusterMove
		sleep(0.02)
	#right_thruster.angle = 90
	left_red_thruster.pulse(.25,.25)
	left_green_thruster.pulse(.25,.25)
	right_red_thruster.pulse(.25,.25)
	right_green_thruster.pulse(.25,.25)
	boosters.blink(0.1,0.1)
	sleep(.2)
	boosters.blink(0.05,0.05)
	explode_player = OMXPlayer(explode_path)
	sleep(.1)
	boosters.blink(0.03,0.03)
	sleep(.2)
	boosters.blink(0.1,0.1)
	sleep(.1)
	boosters.blink(0.03,0.03)
	sleep(.1)
	boosters.blink(0.03,0.03)
	sleep(.3)
	boosters.blink(0.02,0.02)

## Define the buttons
static_button = Button(2)
cruising_button = Button(8)
orbital_button = Button(15)

# Define the states of the LED sequences
running = dict.fromkeys(["static", "cruising", "orbital"], False)

def set_sequences(btn):
	global running
	if btn==static_button and running["static"] == False:
		static_display()
		running.update(dict(dict.fromkeys(["cruising", "orbital"], False), **dict.fromkeys(["static"], True)))
	elif btn==cruising_button and running["cruising"] == False:
		cruising_display()
		running.update(dict(dict.fromkeys(["static", "orbital"], False), **dict.fromkeys(["cruising"], True)))
	elif btn==orbital_button and running["orbital"] == False:
		orbital_display()
		running.update(dict(dict.fromkeys(["static", "cruising"], False), **dict.fromkeys(["orbital"], True)))
	else:
		if running["orbital"] == True:
			for value in range(20,-1,-1):
				thrusterMove=(float(value)-10)/10
				left_thruster.value=thrusterMove
				sleep(0.02)
			#right_thruster.angle = -90
		running.update(dict.fromkeys(["static", "cruising", "orbital"], False))
		leds_off()

for button in (static_button, cruising_button, orbital_button):
    button.when_pressed = set_sequences

pause()