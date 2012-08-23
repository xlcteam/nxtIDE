# -*- coding: utf-8 -*-
import pygame, sys, os.path, threading, pygame.sndarray
from numpy import sin, array, arange, resize, pi
from robothread import RoboException

sensors = {}

def makeXY(x, y):                                                     
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


def dieTest():
    with robot.lock:
        if robot.die:
            robot.die = False
            raise RoboException


def screenTest():
    with robot.lock:
        if threading.current_thread().name == "brick":
            if robot.scr_running:
                robot.scr_running = False
                robot.scr_killed = True
                pygame.time.delay(200)
                
            robot.scr_running = False



def PointOut(x, y):
    """PointOut(x, y)
    
    Draw a point on the screen at (x, y)

    :param int x: The x coordinate of the point
    :param int y: The y coordinate of the point
    
    .. [sk]
    PointOut(x, y)
    
    Nakreslí bod na obrazovke na pozíciach (x, y)

    :param int x: X-ová pozícia bodu
    :param int y: Y-ová pozícia bodu
    """
    screenTest()
    dieTest()
    x, y = makeXY(x, y)
    
    #print y
    with robot.lock:
        robot.lcd.set_at((x, y), (0, 0, 0))
        robot.lcd.set_at((x + 1, y), (0, 0, 0))
        robot.lcd.set_at((x + 1, y + 1), (0, 0, 0))
        robot.lcd.set_at((x, y + 1), (0, 0, 0))

def clearPoint(x, y):
    dieTest()
    x, y = makeXY(x, y)

    with robot.lock:
        robot.lcd.set_at((x, y), (0x43, 0x6c, 0x30))
        robot.lcd.set_at((x + 1, y), (0x43, 0x6c, 0x30))
        robot.lcd.set_at((x + 1, y + 1), (0x43, 0x6c, 0x30))
        robot.lcd.set_at((x, y + 1), (0x43, 0x6c, 0x30))



def printChar(x, y, char):                                            
    """ Low level function for printing chars on the Surface"""                 

    char = ord(char)                                                        
    if char < 32 or char > 126:                                             
        char = 32                                                           
                                                                            
    char -= 32                                                              
                                                                            
    data = chars[char]                                                 
                                                                            
    for line in data:                                                       
        for z in range(0,8):                                                
            if line << z & 0b10000000:                                      
                PointOut(x,y-(8-z))                                       
            else:
                clearPoint(x, y-(8-z))
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
    """TextOut(x, y, text)
    
    Print text on the screen.
    
    :param int x: X coordinate of the text
    :param int y: Y coordinate or the text
    :param str text: The text to print

    .. [sk]
    TextOut(x, y, text)
    
    Vypíše text na obrazovku.
    
    :param int x: X-ová pozícia textu.
    :param int y: Y-ová pozícia textu.
    :param str text: Text, ktorý sa má vypísať.
    """

    for char in list(text):
        printChar(x, y, char)
        x += 6

def NumOut(x, y, num):
    """NumOut(x, y, num)
    
    Print number on the screen.
 
    :param int x: X coordinate of the text
    :param int y: Y coordinate or the text
    :param int num: The number to print

    .. [sk]
    NumOut(x, y, číslo)
    
    Vypíše číslo na obrazovku.
 
    :param int x: X-ová pozícia textu.
    :param int y:  Y-ová pozícia textu.
    :param int num: Číslo, ktorá chceme vypísať.
    """

    
    num = str(num)
    TextOut(x, y, num)
    
#TODO
def LineOut(x0, y0, x1, y1):
    """LineOut(x0, y0, x1, y1)
    
    Draw a line from [x0, y0] to [x1, y1].

    :param int x0: X coordinate of the start point of the line
    :param int y0: Y coordinate of the start point of the line
    :param int x1: X coordinate of the end point of the line
    :param int y1: Y coordinate of the start point of the line

    .. [sk]
    LineOut(x0, y0, x1, y1)
    
    Funkcia na vykreslovanie čiary od [x0, y0] do [x1, y1].

    :param int x0: X-ová pozíca začiatku čiary.
    :param int y0: Y-ová pozíca začiatku čiary.
    :param int x1: X-ová pozíca konca čiary.
    :param int y1: Y-ová pozíca konca čiary.
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
    """CircleOut(x, y, radius)

    Draw a circle with center at [x, y] and specified radius.

    :param int x: X coordinate of the center of the circle.
    :param int x: Y coordinate of the center of the circle.
    :param int radius: The radius of the circle.

    .. [sk]
    CircleOut(x, y, polomer)

    Vykreslí kruh, ktorého stred je [x, y] s daným polomerom.

    :param int x: X-ová pozícia stredu kruhu.
    :param int x: Y-ová pozícia stredu kruhu.
    :param int radius: Polomer kruhu.
    """
    #x,y = makeXY(x, y)
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
    """RectOut(x, y, width, height)
    
    Draw a rectangle from [x, y] with specified width and height.

    :param int x: X coordinate of the start point of the rectangle.
    :param int y: Y coordinate of the start point of the rectangle.
    :param int width: The width of the rectangle.
    :param int height: The height of the rectangle.

    .. [sk]
    RectOut(x, y, šírka, výška)
    
    Vykreslí obdĺžnik z [x, y] a podľa špecifikovanej šírky a výšky.

    :param int x: X-ová pozícía ľavého horného rohu.
    :param int y: Y-ová pozícia ľavého horného rohu.
    :param int width: Šírka obdĺžnika.
    :param int height: Výška obldĺžnika.
    """

    LineOut(x, y, x + width, y )
    LineOut(x, y - height, x + width, y - height)
    LineOut(x + width, y, x + width, y - height )


def ClearScreen():
    """ClearScreen()
    
    Clear the screen.

    .. [sk]
    ClearScreen()

    Vyčistí obrazovku.
    """
    screenTest()

    with robot.lock:
        pygame.draw.rect(robot.lcd, pygame.Color(0x43, 0x6c, 0x30), 
            ((0, 0), (204, 130)))

def ClearLine(line):
    """ClearLine(line)
    
    Clear one line on the screen.
    
    :param int line: line we want to clear.

    .. [sk]
    ClearLine(riadok)
    
    Vyčistí jeden riadok na obrazovke.
    
    :param int line: riadok, ktorý chceme vyčistiť.
    """
    
    #x, y = makeXY(0, line)
    #x1, y1 = makeXY(100, line-8)

    #with robot.lock:
    #    pygame.draw.rect(robot.lcd, pygame.Color(0x43, 0x6c, 0x30),
    #        ((x, y), (x1, y1)))
    TextOut(0, line, 16*" ")


def Wait(milisec):
    """Wait(milisec)
    
    Waits for given number of miliseconds.

    :param int milisec: number of miliseconds

    .. [sk]
    Wait(milisekundy)
    
    Počká na daný čas v milisekundách.

    :param int milisec: číslo v milisekundách.
    """
    

    while milisec > 1:
        step = 100 if milisec > 500 else milisec 
        milisec -= pygame.time.delay(step)
        dieTest()


def sine_array_onecycle(hz, peak):
    length = 44100 / float(hz)
    omega = pi * 2 / length
    xvalues = arange(int(length)) * omega
    return (peak * sin(xvalues))
    
def sine_array(hz, peak, n_samples = 200):
    return resize(sine_array_onecycle(hz, peak), (n_samples,))

def PlayTone(freq, duration):
    """PlayTone(freq, duration)
    
    Play a tone.

    :param int freq: Frequency of the tone in Hz.
    :param int duration: For how long should the brick play this tone.

    .. [sk]
    PlayTone(frekvencia, dĺžka)
    
    Prehrá tón.

    :param int freq: Frekvencia tónu v Hz.
    :param int duration: Dĺžka prehrávania tónu v milisekundách.
    """

    f = sine_array(freq, 1, duration*6)
    f = array(zip(f, f))

    sound = pygame.sndarray.make_sound(f)
    channel = sound.play(-1)
    channel.set_volume(0.2, 0.2)

    Wait(duration)
    sound.stop()



OUT_A = 1
OUT_B = 2
OUT_C = 4
OUT_AB = 3
OUT_BC = 6
OUT_AC = 5
OUT_ABC = 7


def OnFwd(motor, speed):
    """OnFwd(motor, speed)
  
    Set motor to forward direction and turn it on.
    
    :param int motor: motor we want to run.
    :param int speed: speed we want to run the motor at from 0 to 100. Negative value reverses direction.   

    .. [sk]
    OnFwd(motor, rýchlosť)
  
    Nastaví motor aby išiel dopredu, a pustí ho
    
    :param int motor: motor, ktorý chceme spustiť.
    :param int speed: Rýchlosť, ktorou chceme poslať robota dopredu od 0 do 100. Záporná rýchlosť zmení smer chodu motora.   
    """

    dieTest()

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
    """OnRev(motor, speed)
    
    Set motor to reverse direction and turn it on.
    
    :param int motor: motor we want to run.
    :param int speed: speed we want to run the motor at from 0 to 100. Negative value reverses direction.

    .. [sk]
    OnRev(motor, rýchlosť)
    
    Nastaví motor, aby išiel dozadu a zapne ho.
    
    :param int motor: motor, ktorý chceme spustiť.
    :param int speed: rýchlosť, ktorou pôjde motor od 0 do 100. Záporná rýchlosť zmení smer chodu motora.
    """

    dieTest()
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
    """Off(motor)
    
    Turn the motor off (with break).
    
    :param int motor: motor we want to stop.

    .. [sk]
    Off(motor)
    
    Vypne motor (bez zotvrvačnosti).
    
    :param int motor: motor, ktorý chceme zastaviť.
    """

    dieTest()
    with robot.lock:
        if motor & OUT_A:
            robot.mA = 0

        if motor & OUT_B:
            robot.mB = 0

        if motor & OUT_C:
            robot.mC = 0

def Float(motor):
    """Float(motor)
    
    Kill power for the motor.

    :param int motor: motor we want to stop.

    .. [sk]
    Float(motor)
    
    Vypne motor (so zotrvačnosťou).

    :param int motor: motor, ktorý chceme zastaviť.
    """

    return Off(motor)

def MotorTachoCount(motor):
    """MotorTachoCount(motor)
    
    Get motor tachometer counter value.

    :param int motor: motor we want to get tachometer count from.

    .. [sk]
    MotorTachoCount(motor)
    
    Načítavanie otáčok motora.

    :param int motor: motor, z ktorého chceme načítavať.
    """

    dieTest()
    if motor & OUT_A:
        return robot.rotA

    if motor & OUT_B:
        return robot.rotB

    if motor & OUT_C:
        return robot.rotC


def RotateMotor(motor, speed, angle):
    """RotateMotor(motor, speed, angle)
    
    Rotate motor in specified direction at specified speed for the specified
    number of degrees.

    :param int motor: motor we want to rotate
    :param int speed: speed we want to run the motor at, from 0 to 100. Negative value reverses direction.
    :param int angle: number of degrees we want to rotate the motor. Negative value reverses direction.
    
    .. [sk]
    RotateMotor(motor, rýchlosť, uhol)
    
    Otočí motor v špecifikovanom smere na špecifikovanj rýchlosti a špecifikovanom čísle stupňov.

    :param int motor: motor, ktorý chceme točiť
    :param int speed: rýchlosť, ktorou chceme točiť motor od 0 do 100. Záporná hodnota otočí smer chodu motora.
    :param int angle: počet stupňov pre otáčanie motora. Záporná hodnota otočí smer chodu motorra.
    """

    OnFwd(motor, speed)
    clock = pygame.time.Clock()
    start = MotorTachoCount(motor)
    while (MotorTachoCount(motor) - start) < angle:
        dieTest()
        clock.tick(40)

    Off(motor)

def ResetTachoCount(motor):
    """ResetTachoCount(motor)
    
    Reset tachometer counter. 

    :param int motor: desired motor output.

    .. [sk]
    ResetTachoCount(motor)
    
    Zresetuje tachometer. 

    :param int motor: motor, ktorého tachometer chceme zresetovať.
    """

    dieTest()
    with robot.lock:
        if motor & OUT_A:
            robot.rotA = 0

        if motor & OUT_B:
            robot.rotB = 0

        if motor & OUT_C:
            robot.rotC = 0


IN_1 = 1
IN_2 = 2
IN_3 = 3
IN_4 = 4

SENSOR_TOUCH = 1
SENSOR_LIGHT = 2


def SetSensor(sensor, type):
    """SetSensor(sensor, type)"""
    sensor = 1

def SetSensorType(sensor, type):
    """SetSensorType(sensor, type)"""
    sensor = 1

def SetSensorLowspeed(sensor):
    """SetSensorLowspeed(sensor)"""
    sensor = 1

def SetSensorLight(sensor):
    """SetSensorLight(sensor)"""
    sensor = 1

def SetSensorTouch(sensor):
    """SetSensorTouch(sensor)"""
    sensor = 1

def Sensor(sensor):
    """Sensor(sensor)
    
    Read value from given sensor.
    
    :param int sensor: sensor we want to read from

    .. [sk]
    Sensor(sensor)
    
    Načíta hodnotu z daného senzoru.
    
    :param int sensor: senzor, z ktorého chceme čítať.
    """
    
    return robot.sensors[sensor].getValue()

def SensorUS(sensor):
    """SensorUS(sensor)

    Read value from given lowspeed sensor (e.g. Ultrasonic). The input port 
    has to be configured as a Lowspeed before using this function.
    
    :param int sensor: sensor we want to read from

    .. [sk]
    SensorUS(sensor)

    Načíta hodnotu z lowspeed sensoru (e.g. Ultrasonic). Input port
    by mal byt nastaveny ako lowspeed pred použitím.
    
    :param int sensor: senzor, z ktorého chceme čítať.
    """
    
    return robot.sensors[sensor].getValue()



def Random(n = None):
    """Random(n = 0)
    
    Returns a random number

    :param int n: the maximal value this function should return

    .. [sk]
    Random(n = 0)
    
    Vráti náhodné číslo
    
    :param int n: najväčšia hodnota , ktorú má táto funkcia vrátiť. 
    """

    import random
    if n is None:
        return random.randint(-32767, 32767)
    else:
        return random.randint(0, n-1)
    

S1 = 0
S2 = 1
S3 = 2
S4 = 3



__clock__ = pygame.time.Clock()
def ticker():
    dieTest()
    __clock__.tick(20)
    

#   def tracer(frame, a, b):
#       #dieTest()
#       f = os.path.basename(frame.f_back.f_code.co_filename)
#       print f

#       if f.startswith('e'):
#           dieTest()
#       return tracer

#   import threading
#   threading.settrace(tracer)
