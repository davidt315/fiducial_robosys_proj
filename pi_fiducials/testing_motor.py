import time
import RPi.GPIO as io

start = time.time()*1000
pins = (15, 16, 12)
speed = 0

io.cleanup()
io.setmode(io.BOARD)

io.setup(pins[0], io.OUT)
io.setup(pins[1], io.OUT)
io.setup(pins[2], io.OUT)

io.output(pins[0], io.HIGH)
io.output(pins[1], io.LOW)

pwm_control = io.PWM(pins[2], 500)
pwm_control.start(0)
time.sleep(5)
pwm_control.ChangeDutyCycle(50)



while True:
    diff = time.time()*1000 - start
    if diff > 60000:
        io.cleanup()
        print("cleaning up!")
        break