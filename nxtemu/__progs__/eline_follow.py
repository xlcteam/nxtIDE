from api import *
def main():
    SetSensorLight(IN_1)
    SetSensorLight(IN_3)
    
    while 1:
        ticker()#lfixed
        if Sensor(IN_1) < 50:
            OnFwd(OUT_B, 90)
            OnRev(OUT_A, 90)
            
        elif Sensor(IN_3) < 50:
            OnFwd(OUT_A, 90)
            OnRev(OUT_B, 90)
        
        else:
            OnFwd(OUT_AB, 80)