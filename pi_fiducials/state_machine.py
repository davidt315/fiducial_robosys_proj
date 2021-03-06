# import numpy as np
# from scipy.interpolate import interp1d 
import time
import RPi.GPIO as io

class Robot():
    def __init__(self):
        # motor pin definitions (in1, in2, pwm)
        self.Rmotor = Motor(15, 16, 12)
        self.Lmotor = Motor(21, 22, 13)
        self.setup_gpio()
        self.state = IdleState()

    def setup_gpio(self):
	    # set motor pins
        io.cleanup()
        io.setmode(io.BOARD)
        io.setup(self.Rmotor.pins[0], io.OUT)
        io.setup(self.Rmotor.pins[1], io.OUT)
        io.setup(self.Rmotor.pins[2], io.OUT)
        io.setup(self.Lmotor.pins[0], io.OUT)
        io.setup(self.Lmotor.pins[1], io.OUT)
        io.setup(self.Lmotor.pins[2], io.OUT)

        # define starting output of motor pins (forward with 0 speed)
        io.output(self.Rmotor.pins[0], io.HIGH)
        io.output(self.Rmotor.pins[1], io.LOW)
        io.output(self.Lmotor.pins[0], io.HIGH)
        io.output(self.Lmotor.pins[1], io.LOW)
        self.Rmotor.start_pwm()
        self.Lmotor.start_pwm()

    def change_state(self, detections):
        self.state = self.state.change_state(detections)

    def act(self, detections):
        self.state.act(detections, self.Rmotor, self.Lmotor)


class Motor():
    def __init__(self, in1, in2, pwm):
        self.pins = (in1, in2, pwm)
        self.speed = 0
        self.base_speed = 50

    def start_pwm(self):
        self.pwm_control = io.PWM(self.pins[2], 500)
        self.pwm_control.start(self.speed)

    def set_speed(self, speed):
        self.speed = speed
        self.pwm_control.ChangeDutyCycle(self.speed)


# super class
class State():
    def __init__(self):
        # fiducial IDs 
        self.follow_id = 17
        self.search_id = 24
        self.search_bool = False
        # PID inputs
        self.setpoint = 504
        self.cutoff_width = 250

    def change_state(self, detections):
        pass


# subclasses of state
class IdleState(State):
    def __init__(self, pause = 0):
        super().__init__()
        self.pause = pause
        self.start_time = time.time()

    def change_state(self, detections):
        # enables a pause in the state
        if self.pause and (time.time() - self.start_time < self.pause):
            return self

        # search fiducial detected and unsearched
        if not self.search_bool and self.search_id in detections[0]:
            return SearchState()
        # some other condition, enter find state
        return FindState()

    def act(self, detections, Rmotor, Lmotor):
        # check if the motor speeds were already set
        if Rmotor.speed is 0 and Lmotor.speed is 0:
            pass

        # set the motor speeds to 0
        Rmotor.set_speed(50)
        Lmotor.set_speed(50)
        print(f"Rmotor speed: {Lmotor.speed}")



class FollowState(State):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.cum_error = 0
        self.last_error = 0
        self.last_time = time.time()*1000.0
        self.kp = 0.01
        self.ki = 0.000000
        self.kd = 0.00000001

    def change_state(self, detections):
        # search fiducial detected and not searched
        if self.search_id in detections[0] and not self.search_bool:
            return SearchState()
        
        # no detections or only detect search point that has already been searched:
        if (self.follow_id not in detections[0]):
            self.count += 1
            if self.count >= 5:
                return FindState()
            return self
        
        # must have seen the follow tag again, reset count and continue
        self.count = 0
        return self
        

    def act(self, detections, Rmotor, Lmotor):
        # if for a frame we don't see the follow tag, skip the iteration this loop
        if self.follow_id not in detections[0]:
            return

        # if too close, don't move
        width = detections[2][detections[0].index(self.follow_id)]
        if width > self.cutoff_width:
            Lmotor.set_speed(0)
            Rmotor.set_speed(0)
            self.last_error = 0
            self.last_time = time.time()*1000.0
            return

        x_pos = detections[1][detections[0].index(self.follow_id)]
        error = self.setpoint - x_pos
        print(f"error: {error}")
        elapsed_time = time.time()*1000.0 - self.last_time
        self.cum_error += error * elapsed_time
        rate_error = (error - self.last_error) / elapsed_time
        output = self.kp*error + self.ki*self.cum_error - self.kd*rate_error
        print(f"output: {output}")
        
        Lmotor.set_speed(Lmotor.base_speed - int(output))
        Rmotor.set_speed(Rmotor.base_speed + int(output))

        print(f"Lmotorspd: {Lmotor.speed}")
        print(f"Rmotorspd: {Rmotor.speed}")
        
        self.last_error = error
        self.last_time = time.time()*1000.0


        
class SearchState(State):
    def change_state(self):
        return IdleState(3)



class FindState(State):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()*1000

    def change_state(self, detections):
        # search fiducial detected and not searched
        if self.search_id in detections[0] and not self.search_bool:
            return SearchState()
        
        # now see follow ID
        if self.follow_id in detections[0]:
            return FollowState()

        # no detections or only detect search point that has already been searched:
        return self

    def act(self, detections, Rmotor, Lmotor):
        curr_time = time.time()*1000
        diff = curr_time - self.start_time

        # turn around to start
        if (diff < 500): 
            Rmotor.set_speed(0)
            Lmotor.set_speed(0)
            return

        # go towards center
        if (diff >= 500 and diff < 2000): 
            Rmotor.set_speed(0)
            Lmotor.set_speed(0)
            return

        # once back in mid, just rotate to search
        Rmotor.set_speed(0)
        Lmotor.set_speed(0)


        

