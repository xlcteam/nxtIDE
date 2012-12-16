def main():
    
    SetSensorLight(IN_1)
    SetSensorLight(IN_4)
    
    while 1:
        if Sensor(IN_4) < 50:
            OnRev(OUT_B , 100)
            OnFwd(OUT_A, 100)
            
        elif Sensor(IN_1) < 50:
            OnRev(OUT_A, 100)
            OnFwd(OUT_B, 100)
        
        else:
            OnFwd(OUT_AB, 80)