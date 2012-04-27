from api import *
def main():
    
    SetSensorLight(IN_1)
    SetSensorLight(IN_3)
    
    while 1:
        ticker()#lfixed
        if Sensor(IN_3) < 50:
            OnRev(OUT_B, 100)
            OnFwd(OUT_A, 100)
            
        elif Sensor(IN_1) < 50:
            OnRev(OUT_A, 100)
            OnFwd(OUT_B, 100)
        
        else:
            OnFwd(OUT_AB, 80)