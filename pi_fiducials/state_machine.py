import numpy as np
import RPi.GPIO as io 


class Robot():
    def __init__(self):
        # motor pin definitions (in1, in2, pwm)
        self.Rmotor = Motor(38, 37, 12)
        
        self.setup_gpio()

        self.state = IdleState()
        
    def setup_gpio(self):

    
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

    def set_speed(self, percent):
        self.pwm_control.ChangeDutyCycle(percent)

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


class FollowState(State):
    pass 

class SearchState(State):
    pass 

class FindState(State):
    pass
    
