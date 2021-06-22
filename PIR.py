from gpiozero import MotionSensor

pir = MotionSensor(4)

count = 0
 

while True:
    pir.wait_for_motion()
    count + 1
    print("count is", count)
    pir.wait_for_no_motion()