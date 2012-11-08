from api import *
def main():
    speed = 0
    while 1:
        ticker()#lfixed
        value = SensorHTCompass(IN_1)
        
        if  value > 0 and  value < 180:
            speed = -100
        elif value < 360 and  value >= 180:
                speed = 100
        OnFwd(OUT_A, speed)
        OnRev(OUT_B, speed)