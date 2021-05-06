import numpy as np
import RPi.GPIO as io 


class Robot():
    def __init__(self):
        # motor pin definitions (in1, in2, pwm)
        print('here1')
        self.Rmotor = Motor(38, 37, 12)
        print('here2')
        self.setup_gpio()
        print('here3')
        self.state = IdleState()

    def setup_gpio(self):
	# set motor pins
        io.setmode(io.BCM)
        print('here4')
        io.setup(self.Rmotor.pins[0], io.OUT)
        io.setup(self.Rmotor.pins[1], io.OUT)
        io.setup(self.Rmotor.pins[2], io.OUT)
        print('here5')

        # define starting output of motor pins (forward with 0 speed)
        io.output(self.Rmotor.pins[0], io.HIGH)
        io.output(self.Rmotor.pins[1], io.LOW)
        print('here6')
        self.Rmotor.start_pwm()
        print('here7')

    def change_state(self, detections):
        pass

    def act(self, detections):
        self.state.act(detections, self.Rmotor)


class Motor():
    def __init__(self, in1, in2, pwm):
        self.pins = (in1, in2, pwm)
        self.speed = 0

    def start_pwm(self):
        self.pwm_control = io.PWM(self.pins[2], 1000)
        self.pwm_control.start(self.speed)
        print("started pwm")

    def set_speed(self, percent):
        self.pwm_control.ChangeDutyCycle(percent)
        print("speed changed")

# super class
class State():
    def __init__(self):
        pass

    def change_state(self, markers):
        pass

    def act(self):
        pass


# subclasses of state
class IdleState(State):
    def __init__(self):
        print('entering idle state')

    def change_state(self, detections):
        pass

    def act(self, detections, Rmotor):
        Rmotor.set_speed(50)
        print("completed action")


class FollowState(State):
    pass 

class SearchState(State):
    pass 

class FindState(State):
    pass

