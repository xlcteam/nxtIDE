from api import *


def main():
    RotateMotor(OUT_AB, 50, 200)
    # tocenie 
    OnFwd(OUT_A, 100)
    OnRev(OUT_B, 30)
    while 1:
        ticker()#lfixed
        pass    
