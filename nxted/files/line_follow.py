def main():
    
    SetSensorLight(IN_1)
    SetSensorLight(IN_4)
    
    while 1:
        if Sensor(IN_4) < 50:
            OnRev(OUT_B, 90)
            OnFwd(OUT_A, 90)
            
        elif Sensor(IN_1) < 50:
            OnRev(OUT_A, 90)
            OnFwd(OUT_B, 90)
        
        else:
            OnFwd(OUT_AB, 80)