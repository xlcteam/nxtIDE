from api import *
from api import *


def main():
    while 1:
        ticker()#lfixed
        
        if SensorUS(IN_2) < 15:
            OnFwd(OUT_A, 90)
            OnRev(OUT_B, 90)
            Wait(1500)
        else:
            OnFwd(OUT_AB, 80)
       
        ticker()#lfixed