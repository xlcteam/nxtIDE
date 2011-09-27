import pygame, sys, os.path
from robothread import RoboException

def _makeXY(x, y):                                                     
    """ Generates real x,y from NXT like x,y """                            
    if x*2+2 <= 200:
        rx = x*2+2
    else:
        rx = 200

    if y <= 64:                                                             
        return (rx, abs(y - 64)*2+1) 
    else:                                                                   
        return (rx, y*2+1)  

# font adapted form
# http://www.openobject.org/opensourceurbanism/Bike_POV_Beta_4
chars =[[0x00,0x00,0x00,0x00,0x00],
    [0x00,0x00,0x6f,0x00,0x00],  
    [0x00,0x07,0x00,0x07,0x00],  
    [0x14,0x7f,0x14,0x7f,0x14],  
    [0x00,0x07,0x04,0x1e,0x00],  
    [0x23,0x13,0x08,0x64,0x62],  
    [0x36,0x49,0x56,0x20,0x50],  
    [0x00,0x00,0x07,0x00,0x00],  
    [0x00,0x1c,0x22,0x41,0x00],  
    [0x00,0x41,0x22,0x1c,0x00],  
    [0x14,0x08,0x3e,0x08,0x14],  
    [0x08,0x08,0x3e,0x08,0x08],  
    [0x00,0x50,0x30,0x00,0x00],  
    [0x08,0x08,0x08,0x08,0x08],  
    [0x00,0x60,0x60,0x00,0x00],  
    [0x20,0x10,0x08,0x04,0x02],  
    [0x3e,0x51,0x49,0x45,0x3e],  
    [0x00,0x42,0x7f,0x40,0x00],  
    [0x42,0x61,0x51,0x49,0x46],  
    [0x21,0x41,0x45,0x4b,0x31],  
    [0x18,0x14,0x12,0x7f,0x10],  
    [0x27,0x45,0x45,0x45,0x39],  
    [0x3c,0x4a,0x49,0x49,0x30],  
    [0x01,0x71,0x09,0x05,0x03],  
    [0x36,0x49,0x49,0x49,0x36],  
    [0x06,0x49,0x49,0x29,0x1e],  
    [0x00,0x36,0x36,0x00,0x00],  
    [0x00,0x56,0x36,0x00,0x00],  
    [0x08,0x14,0x22,0x41,0x00],  
    [0x14,0x14,0x14,0x14,0x14],  
    [0x00,0x41,0x22,0x14,0x08],  
    [0x02,0x01,0x51,0x09,0x06],  
    [0x3e,0x41,0x5d,0x49,0x4e],  
    [0x7e,0x09,0x09,0x09,0x7e],  
    [0x7f,0x49,0x49,0x49,0x36],  
    [0x3e,0x41,0x41,0x41,0x22],  
    [0x7f,0x41,0x41,0x41,0x3e],  
    [0x7f,0x49,0x49,0x49,0x41],  
    [0x7f,0x09,0x09,0x09,0x01],  
    [0x3e,0x41,0x49,0x49,0x7a],  
    [0x7f,0x08,0x08,0x08,0x7f],  
    [0x00,0x41,0x7f,0x41,0x00],  
    [0x20,0x40,0x41,0x3f,0x01],  
    [0x7f,0x08,0x14,0x22,0x41],  
    [0x7f,0x40,0x40,0x40,0x40],  
    [0x7f,0x02,0x0c,0x02,0x7f],  
    [0x7f,0x04,0x08,0x10,0x7f],  
    [0x3e,0x41,0x41,0x41,0x3e],  
    [0x7f,0x09,0x09,0x09,0x06],  
    [0x3e,0x41,0x51,0x21,0x5e],  
    [0x7f,0x09,0x19,0x29,0x46],  
    [0x46,0x49,0x49,0x49,0x31],  
    [0x01,0x01,0x7f,0x01,0x01],  
    [0x3f,0x40,0x40,0x40,0x3f],  
    [0x0f,0x30,0x40,0x30,0x0f],  
    [0x3f,0x40,0x30,0x40,0x3f],  
    [0x63,0x14,0x08,0x14,0x63],  
    [0x07,0x08,0x70,0x08,0x07],  
    [0x61,0x51,0x49,0x45,0x43],  
    [0x3c,0x4a,0x49,0x29,0x1e],  
    [0x02,0x04,0x08,0x10,0x20],  
    [0x00,0x41,0x7f,0x00,0x00],  
    [0x04,0x02,0x01,0x02,0x04],  
    [0x40,0x40,0x40,0x40,0x40],  
    [0x00,0x00,0x03,0x04,0x00],  
    [0x20,0x54,0x54,0x54,0x78],  
    [0x7f,0x48,0x44,0x44,0x38],  
    [0x38,0x44,0x44,0x44,0x20],  
    [0x38,0x44,0x44,0x48,0x7f],  
    [0x38,0x54,0x54,0x54,0x18],  
    [0x08,0x7e,0x09,0x01,0x02],  
    [0x0c,0x52,0x52,0x52,0x3e],  
    [0x7f,0x08,0x04,0x04,0x78],  
    [0x00,0x44,0x7d,0x40,0x00],  
    [0x20,0x40,0x44,0x3d,0x00],  
    [0x00,0x7f,0x10,0x28,0x44],  
    [0x00,0x41,0x7f,0x40,0x00],  
    [0x7c,0x04,0x18,0x04,0x78],  
    [0x7c,0x08,0x04,0x04,0x78],  
    [0x38,0x44,0x44,0x44,0x38],  
    [0x7c,0x14,0x14,0x14,0x08],  
    [0x08,0x14,0x14,0x18,0x7c],  
    [0x7c,0x08,0x04,0x04,0x08],  
    [0x48,0x54,0x54,0x54,0x20],  
    [0x04,0x3f,0x44,0x40,0x20],  
    [0x3c,0x40,0x40,0x20,0x7c],  
    [0x1c,0x20,0x40,0x20,0x1c],  
    [0x3c,0x40,0x30,0x40,0x3c],  
    [0x44,0x28,0x10,0x28,0x44],  
    [0x0c,0x50,0x50,0x50,0x3c],  
    [0x44,0x64,0x54,0x4c,0x44],  
    [0x00,0x08,0x36,0x41,0x41],  
    [0x00,0x00,0x7f,0x00,0x00],  
    [0x41,0x41,0x36,0x08,0x00],  
    [0x04,0x02,0x04,0x08,0x04],  
    ]


def _dieTest():
    with robot.lock:
        if robot.die:
            robot.die = False
            raise RoboException


def PointOut(x, y):
    _dieTest()
    x, y = _makeXY(x, y)
    
    #print y
    with robot.lock:
        robot.lcd.set_at((x, y), (0, 0, 0))
        robot.lcd.set_at((x + 1, y), (0, 0, 0))
        robot.lcd.set_at((x + 1, y + 1), (0, 0, 0))
        robot.lcd.set_at((x, y + 1), (0, 0, 0))

   


def _printChar(x, y, char):                                            
    """ Low level function for printing chars on the Surface"""                 

    char = ord(char)                                                        
    if char < 32 or char > 126:                                             
        char = 32                                                           
                                                                            
    char -= 32                                                              
                                                                            
    data = chars[char]                                                 
                                                                            
    for line in data:                                                       
        for z in range(0,8):                                                
            if line << z & 0b10000000:                                      
                PointOut(x,y- (8 - z))                                       
        x += 1   


LCD_LINE1 = 64
LCD_LINE2 = 56
LCD_LINE3 = 48
LCD_LINE4 = 40
LCD_LINE5 = 32
LCD_LINE6 = 24
LCD_LINE7 = 16
LCD_LINE8 =  8

def TextOut(x, y, text):
    """ High level function for printing text on surface """
    for char in list(text):
        _printChar(x, y, char)
        x += 6

def NumOut(x, y, num):
    """ The same as TextOut but for integers """
    
    num = str(num)
    TextOut(x, y, num)
    

def LineOut(x0, y0, x1, y1):
    """ 
    Function for printing line from [x1,y1] to [x2,y2] 
    It is just a simple implementation of Bresenham's algorithm 
    """

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, x1 = y0, y1

    if x0 > x1:
        x0, y0 = x1, y1

    deltax = x1 - x0
    deltay = abs(y1 - y0)
    error = deltax / 2.0


    y = y0
    if y0 < y1:
        ystep = 1
    else:
        ystep = -1

    for x in range(x0, x1):
        if steep:
            PointOut(y,x)
        else:
            PointOut(x,y)
        

        error = error - deltay
        if error < 0:
            y += ystep
            error += deltax
    

def CircleOut(x, y, radius):
    #x,y = _makeXY(x, y)
    #pygame.draw.circle(robot.lcd, (0, 0, 0), (x, y), radius*2+1, 1)
    #pygame.draw.circle(robot.lcd, (0, 0, 0), (x, y), radius*2+2, 1)
    #pygame.draw.circle(robot.lcd, (0, 0, 0), (x, y), radius*2+3, 1)
    
    f = 1 - radius
    ddF_x = 1
    ddF_y = -2 * radius

    xx = 0
    yy = radius

    PointOut(x, y + radius)
    PointOut(x, y - radius)
    PointOut(x + radius, y)
    PointOut(x - radius, y)

    while xx < yy:
        if f >= 0:
            yy -= 1
            ddF_y += 2
            f += ddF_y

        xx += 1
        ddF_x += 2
        f += ddF_x
        PointOut(x + xx, y + yy)
        PointOut(x - xx, y + yy)
        PointOut(x + xx, y - yy)
        PointOut(x - xx, y - yy)
        PointOut(x + yy, y + xx)
        PointOut(x - yy, y + xx)
        PointOut(x + yy, y - xx)
        PointOut(x - yy, y - xx)

# TODO
def RectOut(x, y, width, height):
    LineOut(x, y, x + width, y )
    LineOut(x, y - height, x + width, y - height)
    LineOut(x + width, y, x + width, y - height )


def ClearScreen():
    with robot.lock:
        pygame.draw.rect(robot.lcd, pygame.Color(0x43, 0x6c, 0x30), 
            ((0, 0), (204, 130)))

def Wait(sec):
    while sec > 1:
        sec -= pygame.time.delay(100)
        _dieTest()


OUT_A = 1
OUT_B = 2
OUT_C = 4
OUT_AB = 3
OUT_BC = 6
OUT_ABC = 7


def OnFwd(motor, speed):
    _dieTest()

    if speed <= -100:
        speed = -100

    if speed >= 100:
        speed = 100

    with robot.lock:
        if motor & OUT_A:
            robot.mA = speed

        if motor & OUT_B:
            robot.mB = speed

        if motor & OUT_C:
            robot.mC = speed

def OnRev(motor, speed):
    _dieTest()
    speed = -speed
    
    if speed <= -100:
        speed = -100

    if speed >= 100:
        speed = 100

    with robot.lock:
        if motor & OUT_A:
            robot.mA = speed

        if motor & OUT_B:
            robot.mB = speed

        if motor & OUT_C:
            robot.mC = speed

def Off(motor):
    _dieTest()
    with robot.lock:
        if motor & OUT_A:
            robot.mA = 0

        if motor & OUT_B:
            robot.mB = 0

        if motor & OUT_C:
            robot.mC = 0

def Float(motor):
    return Off(motor)

def Coast(motor):
    return Off(motor)

def MotorTachoCount(motor):
    _dieTest()
    if motor & OUT_A:
        return robot.rotA

    if motor & OUT_B:
        return robot.rotB

    if motor & OUT_C:
        return robot.rotC


def RotateMotor(motor, speed, angle):
    OnFwd(motor, speed)
    clock = pygame.time.Clock()
    while MotorTachoCount(motor) < angle:
        _dieTest()
        clock.tick(20)

def ResetTachoCount(motor):
    _dieTest()
    with robot.lock:
        if motor & OUT_A:
            robot.rotA = 0

        if motor & OUT_B:
            robot.rotB = 0

        if motor & OUT_C:
            robot.rotC = 0


def Random(a = None):
    import random
    if a is None:
        return random.randint(-32767, 32767)
    else:
        return random.randint(0, a-1)
    

__clock__ = pygame.time.Clock()
def ticker():
    __clock__.tick(20)
    _dieTest()
    

#   def tracer(frame, a, b):
#       #_dieTest()
#       f = os.path.basename(frame.f_back.f_code.co_filename)
#       print f

#       if f.startswith('e'):
#           _dieTest()
#       return tracer

#   import threading
#   threading.settrace(tracer)
