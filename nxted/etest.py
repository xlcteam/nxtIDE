from api import *

def main():                                                                        
    print "changing"                                                            
    prnt()
    OnFwd(OUT_AB, 100)                                                           
    #printChar(0, 64, "A")                                                      
   #TextOut(0, 64, "0123456789ABCDEF")                                          
   #TextOut(0, 56, "0123456789ABCDEF")                                          
   #TextOut(0, 48, "0123456789ABCDEF")                                          
   #TextOut(0, 40, "0123456789ABCDEF")                                          
   #TextOut(0, 32, "0123456789ABCDEF")                                          
   #TextOut(0, 24, "0123456789ABCDEF")                                          
   #TextOut(0, 16, "0123456789ABCDEF")                                          
   #TextOut(0,  8, "0123456789ABCDEF")                                          
    #PointOut(50, 50)                                                           
    CircleOut(50, 32, 30)                                                       
    LineOut(0,0,100,64)                                                         
    LineOut(0,64, 100, 0)                                                       
    Wait(6000)                                                                  
    OnRev(OUT_AB, 50)                                                           
    Wait(2000)
    ClearScreen()                                                               
    while 1:
        pass

    for x in range(20):
        prit x
