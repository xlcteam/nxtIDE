from api import *


def main():
    while 1:
        
        if SensorUS(IN_2) < 50:
            OnFwd(OUT_A, 80)
            OnRev(OUT_B, 80)
            Wait(1200)
        else:
            OnFwd(OUT_AB, 80)
       
        ticker()#lfixed
