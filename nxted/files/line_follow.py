def main():
    
    SetSensorLight(IN_1)
    SetSensorLight(IN_3)
    
    while 1:
        if Sensor(IN_3) < 50:
            OnFwd(OUT_A, 100)
            OnRev(OUT_C, 100)
            
        elif Sensor(IN_1) < 50:
            OnFwd(OUT_C, 100)
            OnRev(OUT_A, 100)
        
        else:
            OnFwd(OUT_AC, 80)