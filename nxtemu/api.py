# -*- coding: utf-8 -*-
import pygame
import sys
import os.path
import threading
import pygame.sndarray
from numpy import sin, array, arange, resize, pi
from robothread import RoboException, RoboThread

sensors = {}


def makeXY(x, y):
    """ Generates real x,y from NXT like x,y """
    if x * 2 + 2 <= 200:
        rx = x * 2 + 2
    else:
        rx = 200

    if y <= 64:
        return (rx, abs(y - 64) * 2 + 1)
    else:
        return (rx, y * 2 + 1)

# font adapted from
# http://www.openobject.org/opensourceurbanism/Bike_POV_Beta_4
chars = [[0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x6f, 0x00, 0x00],
        [0x00, 0x07, 0x00, 0x07, 0x00],
        [0x14, 0x7f, 0x14, 0x7f, 0x14],
        [0x00, 0x07, 0x04, 0x1e, 0x00],
        [0x23, 0x13, 0x08, 0x64, 0x62],
        [0x36, 0x49, 0x56, 0x20, 0x50],
        [0x00, 0x00, 0x07, 0x00, 0x00],
        [0x00, 0x1c, 0x22, 0x41, 0x00],
        [0x00, 0x41, 0x22, 0x1c, 0x00],
        [0x14, 0x08, 0x3e, 0x08, 0x14],
        [0x08, 0x08, 0x3e, 0x08, 0x08],
        [0x00, 0x50, 0x30, 0x00, 0x00],
        [0x08, 0x08, 0x08, 0x08, 0x08],
        [0x00, 0x60, 0x60, 0x00, 0x00],
        [0x20, 0x10, 0x08, 0x04, 0x02],
        [0x3e, 0x51, 0x49, 0x45, 0x3e],
        [0x00, 0x42, 0x7f, 0x40, 0x00],
        [0x42, 0x61, 0x51, 0x49, 0x46],
        [0x21, 0x41, 0x45, 0x4b, 0x31],
        [0x18, 0x14, 0x12, 0x7f, 0x10],
        [0x27, 0x45, 0x45, 0x45, 0x39],
        [0x3c, 0x4a, 0x49, 0x49, 0x30],
        [0x01, 0x71, 0x09, 0x05, 0x03],
        [0x36, 0x49, 0x49, 0x49, 0x36],
        [0x06, 0x49, 0x49, 0x29, 0x1e],
        [0x00, 0x36, 0x36, 0x00, 0x00],
        [0x00, 0x56, 0x36, 0x00, 0x00],
        [0x08, 0x14, 0x22, 0x41, 0x00],
        [0x14, 0x14, 0x14, 0x14, 0x14],
        [0x00, 0x41, 0x22, 0x14, 0x08],
        [0x02, 0x01, 0x51, 0x09, 0x06],
        [0x3e, 0x41, 0x5d, 0x49, 0x4e],
        [0x7e, 0x09, 0x09, 0x09, 0x7e],
        [0x7f, 0x49, 0x49, 0x49, 0x36],
        [0x3e, 0x41, 0x41, 0x41, 0x22],
        [0x7f, 0x41, 0x41, 0x41, 0x3e],
        [0x7f, 0x49, 0x49, 0x49, 0x41],
        [0x7f, 0x09, 0x09, 0x09, 0x01],
        [0x3e, 0x41, 0x49, 0x49, 0x7a],
        [0x7f, 0x08, 0x08, 0x08, 0x7f],
        [0x00, 0x41, 0x7f, 0x41, 0x00],
        [0x20, 0x40, 0x41, 0x3f, 0x01],
        [0x7f, 0x08, 0x14, 0x22, 0x41],
        [0x7f, 0x40, 0x40, 0x40, 0x40],
        [0x7f, 0x02, 0x0c, 0x02, 0x7f],
        [0x7f, 0x04, 0x08, 0x10, 0x7f],
        [0x3e, 0x41, 0x41, 0x41, 0x3e],
        [0x7f, 0x09, 0x09, 0x09, 0x06],
        [0x3e, 0x41, 0x51, 0x21, 0x5e],
        [0x7f, 0x09, 0x19, 0x29, 0x46],
        [0x46, 0x49, 0x49, 0x49, 0x31],
        [0x01, 0x01, 0x7f, 0x01, 0x01],
        [0x3f, 0x40, 0x40, 0x40, 0x3f],
        [0x0f, 0x30, 0x40, 0x30, 0x0f],
        [0x3f, 0x40, 0x30, 0x40, 0x3f],
        [0x63, 0x14, 0x08, 0x14, 0x63],
        [0x07, 0x08, 0x70, 0x08, 0x07],
        [0x61, 0x51, 0x49, 0x45, 0x43],
        [0x3c, 0x4a, 0x49, 0x29, 0x1e],
        [0x02, 0x04, 0x08, 0x10, 0x20],
        [0x00, 0x41, 0x7f, 0x00, 0x00],
        [0x04, 0x02, 0x01, 0x02, 0x04],
        [0x40, 0x40, 0x40, 0x40, 0x40],
        [0x00, 0x00, 0x03, 0x04, 0x00],
        [0x20, 0x54, 0x54, 0x54, 0x78],
        [0x7f, 0x48, 0x44, 0x44, 0x38],
        [0x38, 0x44, 0x44, 0x44, 0x20],
        [0x38, 0x44, 0x44, 0x48, 0x7f],
        [0x38, 0x54, 0x54, 0x54, 0x18],
        [0x08, 0x7e, 0x09, 0x01, 0x02],
        [0x0c, 0x52, 0x52, 0x52, 0x3e],
        [0x7f, 0x08, 0x04, 0x04, 0x78],
        [0x00, 0x44, 0x7d, 0x40, 0x00],
        [0x20, 0x40, 0x44, 0x3d, 0x00],
        [0x00, 0x7f, 0x10, 0x28, 0x44],
        [0x00, 0x41, 0x7f, 0x40, 0x00],
        [0x7c, 0x04, 0x18, 0x04, 0x78],
        [0x7c, 0x08, 0x04, 0x04, 0x78],
        [0x38, 0x44, 0x44, 0x44, 0x38],
        [0x7c, 0x14, 0x14, 0x14, 0x08],
        [0x08, 0x14, 0x14, 0x18, 0x7c],
        [0x7c, 0x08, 0x04, 0x04, 0x08],
        [0x48, 0x54, 0x54, 0x54, 0x20],
        [0x04, 0x3f, 0x44, 0x40, 0x20],
        [0x3c, 0x40, 0x40, 0x20, 0x7c],
        [0x1c, 0x20, 0x40, 0x20, 0x1c],
        [0x3c, 0x40, 0x30, 0x40, 0x3c],
        [0x44, 0x28, 0x10, 0x28, 0x44],
        [0x0c, 0x50, 0x50, 0x50, 0x3c],
        [0x44, 0x64, 0x54, 0x4c, 0x44],
        [0x00, 0x08, 0x36, 0x41, 0x41],
        [0x00, 0x00, 0x7f, 0x00, 0x00],
        [0x41, 0x41, 0x36, 0x08, 0x00],
        [0x04, 0x02, 0x04, 0x08, 0x04],
         ]


def dieTest():
    while robot.paused:  # pauses execution of the emulated program
        __clock__.tick(20)

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
    """
    .. [en]
    PointOut(x, y)

    Draw a point on the screen at (x, y)

    :param int x: The x coordinate of the point
    :param int y: The y coordinate of the point

    .. [/en]
    .. [sk]
    PointOut(x, y)

    Nakreslí bod na obrazovke na pozíciach (x, y)

    :param int x: X-ová pozícia bodu
    :param int y: Y-ová pozícia bodu
    .. [/sk]
    """
    screenTest()
    dieTest()
    x, y = makeXY(x, y)

    # print y
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


def _printChar(x, y, char):
    """ Low level function for printing chars on the Surface"""

    char = ord(char)
    if char < 32 or char > 126:
        char = 32

    char -= 32

    data = chars[char]

    for line in data:
        for z in range(0, 8):
            if line << z & 0b10000000:
                PointOut(x, y - (8 - z))
            else:
                clearPoint(x, y - (8 - z))
        x += 1


LCD_LINE1 = 64
LCD_LINE2 = 56
LCD_LINE3 = 48
LCD_LINE4 = 40
LCD_LINE5 = 32
LCD_LINE6 = 24
LCD_LINE7 = 16
LCD_LINE8 = 8


def ClearScreen():
    """
    .. [en]
    ClearScreen()

    Clear the screen.

    .. [/en]
    .. [sk]
    ClearScreen()

    Vyčistí obrazovku.
    .. [/sk]
    """
    screenTest()

    with robot.lock:
        pygame.draw.rect(robot.lcd, pygame.Color(0x43, 0x6c, 0x30),
                        ((0, 0), (204, 130)))

    robot._cur_lcd_line = 7


def lcd_clear():
    """
    .. [en]
    lcd_clear()

    Clear the screen.

    .. [/en]
    .. [sk]
    lcd_clear()

    Vyčistí obrazovku.
    .. [/sk]
    """

    ClearScreen()


def TextOut(x, y, text, clear=False):
    """
    .. [en]
    TextOut(x, y, text)

    Print text on the screen.

    :param int x: X coordinate of the text
    :param int y: Y coordinate or the text
    :param str text: The text to print

    .. [/en]
    .. [sk]
    TextOut(x, y, text)

    Vypíše text na obrazovku.

    :param int x: X-ová pozícia textu.
    :param int y: Y-ová pozícia textu.
    :param str text: Text, ktorý sa má vypísať.
    .. [/sk]
    """

    if clear:
        ClearScreen()

    for char in list(text):
        _printChar(x, y, char)
        x += 6


def NumOut(x, y, num, clear=False):
    """
    .. [en]
    NumOut(x, y, num)

    Print number on the screen.

    :param int x: X coordinate of the text
    :param int y: Y coordinate or the text
    :param int num: The number to print

    .. [/en]
    .. [sk]
    NumOut(x, y, číslo)

    Vypíše číslo na obrazovku.

    :param int x: X-ová pozícia textu.
    :param int y:  Y-ová pozícia textu.
    :param int num: Číslo, ktorá chceme vypísať.
    """

    num = str(num)
    TextOut(x, y, num, clear)

# TODO

def lcd_print(text):
    """
    .. [en]
    lcd_print(text)

    Print one or multiple lines of text on the LCD screen. Every line can have
    at most 16 characters -- others will be omitted. 
    
    Lines are separated in text by the newline sign (\\n). Every line is printed
    separately. 

    :param string text: text to be printed on the LCD screen
    .. [/en]
    .. [sk]
    lcd_print(text)

    Vypíše jeden alebo viac riadkov textu na LCD obrazovku. Na jeden riadok
    vypíše najviac 16 znakov -- ostatné budú ignorované. 

    Riadky sú v texte oddelené znakom nového riadku (\\n). Každý riadok je
    vypísaný samostatne. 
    
    :param string text: text, ktorý sa má vypísať na LCD obrazovku
    .. [/sk]
    """
    lines = text.split('\n')
    for line in lines:
        if robot._cur_lcd_line == 7:
            lcd_clear()
            robot._cur_lcd_line = 0
        else:
            robot._cur_lcd_line += 1

        line_position = 64 - robot._cur_lcd_line* 8
        TextOut(0, line_position, line)


def LineOut(x0, y0, x1, y1):
    """
    .. [en]
    LineOut(x0, y0, x1, y1)

    Draw a line from [x0, y0] to [x1, y1].

    :param int x0: X coordinate of the start point of the line
    :param int y0: Y coordinate of the start point of the line
    :param int x1: X coordinate of the end point of the line
    :param int y1: Y coordinate of the start point of the line

    .. [/en]
    .. [sk]
    LineOut(x0, y0, x1, y1)

    Funkcia na vykreslovanie čiary od [x0, y0] do [x1, y1].

    :param int x0: X-ová pozíca začiatku čiary.
    :param int y0: Y-ová pozíca začiatku čiary.
    :param int x1: X-ová pozíca konca čiary.
    :param int y1: Y-ová pozíca konca čiary.
    .. [/sk]
    """

    tmp = []
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        tmp = [x0, x1]
        x0 = y0
        x1 = y1
        y0 = tmp[0]
        y1 = tmp[1]

    if x0 > x1:
        tmp = [x0, y0]
        x0 = x1
        y0 = y1
        x1 = tmp[0]
        y1 = tmp[1]

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
            PointOut(y, x)
        else:
            PointOut(x, y)

        error = error - deltay
        if error < 0:
            y += ystep
            error += deltax


def CircleOut(x, y, radius):
    """
    .. [en]
    CircleOut(x, y, radius)

    Draw a circle with center at [x, y] and specified radius.

    :param int x: X coordinate of the center of the circle.
    :param int y: Y coordinate of the center of the circle.
    :param int radius: The radius of the circle.

    .. [/en]
    .. [sk]
    CircleOut(x, y, polomer)

    Vykreslí kruh, ktorého stred je [x, y] s daným polomerom.

    :param int x: X-ová pozícia stredu kruhu.
    :param int y: Y-ová pozícia stredu kruhu.
    :param int radius: Polomer kruhu.
    .. [/sk]
    """
    # x,y = makeXY(x, y)
    # pygame.draw.circle(robot.lcd, (0, 0, 0), (x, y), radius*2+1, 1)
    # pygame.draw.circle(robot.lcd, (0, 0, 0), (x, y), radius*2+2, 1)
    # pygame.draw.circle(robot.lcd, (0, 0, 0), (x, y), radius*2+3, 1)

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
    """
    .. [en]
    RectOut(x, y, width, height)

    Draw a rectangle from [x, y] with specified width and height.

    :param int x: X coordinate of the start point of the rectangle.
    :param int y: Y coordinate of the start point of the rectangle.
    :param int width: The width of the rectangle.
    :param int height: The height of the rectangle.

    .. [/en]
    .. [sk]
    RectOut(x, y, šírka, výška)

    Vykreslí obdĺžnik z [x, y] a podľa špecifikovanej šírky a výšky.

    :param int x: X-ová pozícía ľavého horného rohu.
    :param int y: Y-ová pozícia ľavého horného rohu.
    :param int width: Šírka obdĺžnika.
    :param int height: Výška obldĺžnika.
    .. [/sk]
    """

    LineOut(x, y, x + width + 1, y)
    LineOut(x, y, x, y - height)
    LineOut(x, y - height, x + width, y - height)
    LineOut(x + width, y, x + width, y - height)


def lcd_draw_polygon(vertices):
    """
    .. [en]
    lcd_draw_polygon(vertices)

    Draw a polygon with specified vertices.

    :param 2D array vertices: [[x,y]] coordinates of the vertices.

    .. [/en]
    .. [sk]
    lcd_draw_polygon(vrcholy)

    Vykreslí polygón podľa zadaných vrcholov.

    :param 2D array vertices: [[x,y]] súradnice vrcholov.
    .. [/sk]
    """

    for i in range(len(vertices)):
        if i == len(vertices)-1:
            LineOut(vertices[i][0], vertices[i][1], vertices[0][0], vertices[0][1])
        else:
            LineOut(vertices[i][0], vertices[i][1], vertices[i+1][0], vertices[i+1][1])


def ResetScreen():
    """
    .. [en]
    ResetScreen()

    Return the screen to Running... state.

    .. [/en]
    .. [sk]
    ResetScreen()

    Vráti obrazovku do stavu Running... .
    .. [/sk]
    """
    if not robot.scr_running:
        robot.scr_running = True
        scr_runner = RoboThread(target=robot.running)
        scr_runner.start()


def lcd_reset():
    """
    .. [en]
    lcd_reset()

    Return the screen to Running... state.

    .. [/en]
    .. [sk]
    lcd_reset()

    Vráti obrazovku do stavu Running... .
    .. [/sk]
    """

    ResetScreen()
 

def ClearLine(line):
    """
    .. [en]
    ClearLine(line)

    Clear one line on the screen.

    :param int line: line we want to clear.

    .. [/en]
    .. [sk]
    ClearLine(riadok)

    Vyčistí jeden riadok na obrazovke.

    :param int line: riadok, ktorý chceme vyčistiť.
    .. [/sk]
    """

    # x, y = makeXY(0, line)
    # x1, y1 = makeXY(100, line-8)

    # with robot.lock:
    #    pygame.draw.rect(robot.lcd, pygame.Color(0x43, 0x6c, 0x30),
    #        ((x, y), (x1, y1)))
    TextOut(0, line, 16 * " ")


def Wait(milisec):
    """
    .. [en]
    Wait(milisec)

    Waits for given number of miliseconds.

    :param int milisec: number of miliseconds

    .. [/en]
    .. [sk]
    Wait(milisekundy)

    Počká na daný čas v milisekundách.

    :param int milisec: číslo v milisekundách.
    .. [/sk]
    """

    while milisec > 1:
        step = 100 if milisec > 500 else milisec
        milisec -= pygame.time.delay(step)
        dieTest()


def wait(milisec):
    """
    .. [en]
    wait(milisec)

    Waits for given number of miliseconds.

    :param int milisec: number of miliseconds

    .. [/en]
    .. [sk]
    wait(milisekundy)

    Počká na daný čas v milisekundách.

    :param int milisec: číslo v milisekundách.
    .. [/sk]
    """

    return Wait(milisec)


def _sine_array_onecycle(hz, peak):
    length = 44100 / float(hz)
    omega = pi * 2 / length
    xvalues = arange(int(length)) * omega
    return (peak * sin(xvalues))


def _sine_array(hz, peak, n_samples=200):
    return resize(_sine_array_onecycle(hz, peak), (n_samples,))


def PlayTone(freq, duration):
    """
    .. [en]
    PlayTone(freq, duration)

    Play a tone.

    :param int freq: Frequency of the tone in Hz.
    :param int duration: For how long should the brick play this tone.

    .. [/en]
    .. [sk]
    PlayTone(frekvencia, dĺžka)

    Prehrá tón.

    :param int freq: Frekvencia tónu v Hz.
    :param int duration: Dĺžka prehrávania tónu v milisekundách.
    .. [/sk]
    """

    f = _sine_array(freq, 1, duration * 6)
    f = array(zip(f, f))

    sound = pygame.sndarray.make_sound(f)
    channel = sound.play(-1)
    channel.set_volume(0.2, 0.2)

    Wait(duration)
    sound.stop()


def Beep(duration):
    """
    .. [en]
    Beep(duration)

    Beeps for a number of miliseconds.

    :param int duration: For how long should the brick beeps in milliseconds.

    .. [/en]
    .. [sk]
    Beep(dížka)

    Pípne.

    :param int duration: Ako dlho potrvá pípnutie v milisekundách.
    .. [/sk]
    """

    PlayTone(2600, duration)


OUT_A = 1
OUT_B = 2
OUT_C = 4
OUT_AB = 3
OUT_AC = 5
OUT_BC = 6
OUT_ABC = 7


def OnFwd(motor, speed):
    """
    .. [en]
    OnFwd(motor, speed)

    Set motor to forward direction and turn it on.

    :param int motor: motor we want to run.  
    :param int speed: speed we want to run the motor at from 0 to 100. Negative 
                      value reverses direction.

    .. [/en]
    .. [sk]
    OnFwd(motor, rychlost)

    Nastaví motor tak, aby sa pohyboval vpred a spustí ho

    :param int motor: motor, ktorý chceme spustiť.
    :param int rychlost: Rýchlosť, ktorou chceme poslať robota dopredu od 0 do
                         100. Záporná rýchlosť zmení smer chodu motora.
    .. [/sk]
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
    """
    .. [en]
    OnRev(motor, speed)

    Set motor to reverse direction and turn it on.

    :param int motor: motor we want to run.
    :param int speed: speed we want to run the motor at from 0 to 100. Negative 
                      value reverses direction.

    .. [/en]
    .. [sk]
    OnRev(motor, rychlost)

    Nastaví motor nastaví motor na pohyb vzad a spustí ho.

    :param int motor: motor, ktorý chceme spustiť.
    :param int rychlost: rýchlosť, ktorou pôjde motor od 0 do 100. 
                         Záporná rýchlosť zmení smer chodu motora.
    .. [/sk]
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
    """
    .. [en]
    Off(motor)

    Turn the motor off (with break).

    :param int motor: motor we want to stop.

    .. [/en]
    .. [sk]
    Off(motor)

    Vypne motor (a zabrzdí).

    :param int motor: motor, ktorý chceme zastaviť.
    .. [/sk]
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
    """
    .. [en]
    Float(motor)

    Make the motor float. 

    :param int motor: motor we want to stop.

    .. [/en]
    .. [sk]
    Float(motor)

    Vypne motor (so zotrvačnosťou).

    :param int motor: motor, ktorý chceme zastaviť.
    .. [/sk]
    """

    return Off(motor)


def off(motor=None):
    """
    .. [en]
    off(motor)

    Turn the motor off (with break).

    :param int motor: motor we want to stop.

    .. [/en]
    .. [sk]
    off(motor)

    Vypne motor (a zabrzdí).

    :param int motor: motor, ktorý chceme zastaviť.
    .. [/sk]
    """

    if motor is None:
        return Off(OUT_ABC)
    else:
        return Off(motor)


def MotorTachoCount(motor):
    """
    .. [en]
    MotorTachoCount(motor)

    Get motor tachometer counter value.

    :param int motor: motor we want to get tachometer count from.

    .. [/en]
    .. [sk]
    MotorTachoCount(motor)

    Načíta hodnotu otáčkomeru motora.

    :param int motor: motor, z ktorého chceme načítavať.
    .. [/sk]
    """

    dieTest()
    if motor & OUT_A:
        return robot.rotA

    if motor & OUT_B:
        return robot.rotB

    if motor & OUT_C:
        return robot.rotC

def MotorRotationCount(motor):
    """
    .. [en]
    MotorRotationCount(motor)

    Get motor tachometer counter value.

    :param int motor: motor we want to get tachometer count from.

    .. [/en]
    .. [sk]
    MotorRotationCount(motor)

    Načíta hodnotu otáčkomeru motora.

    :param int motor: motor, z ktorého chceme načítavať.
    .. [/sk]
    """

    return MotorTachoCount(motor)

def RotateMotor(motor, speed, angle):
    """
    .. [en]
    RotateMotor(motor, speed, angle)

    Rotate motor in specified direction at specified speed for the specified
    number of degrees.

    :param int motor: motor we want to rotate
    :param int speed: speed we want to run the motor at, from 0 to 100. 
                      Negative value reverses direction.
    :param int angle: number of degrees we want to rotate the motor. Negative 
                      value reverses direction.

    .. [/en]
    .. [sk]
    RotateMotor(motor, rýchlosť, uhol)

    Otočí motor v danom smere danou rýchlosťou a o istý počet stupňov. 

    :param int motor: motor, ktorý chceme točiť
    :param int speed: rýchlosť, ktorou chceme točiť motor od 0 do 100. Záporná 
                      hodnota otočí smer chodu motora.
    :param int angle: počet stupňov pre otáčanie motora. Záporná hodnota otočí 
                      smer chodu motora.
    .. [/sk]
    """

    OnFwd(motor, speed)
    clock = pygame.time.Clock()
    start = MotorTachoCount(motor)
    while (MotorTachoCount(motor) - start) < angle:
        dieTest()
        clock.tick(40)

    Off(motor)

def rotate_motor(motor, speed, angle):
    """
    .. [en]
    rotate_motor(motor, speed, angle)

    Rotate motor in specified direction at specified speed for the specified
    number of degrees.

    :param int motor: motor we want to rotate
    :param int speed: speed we want to run the motor at, from 0 to 100. 
                      Negative value reverses direction.
    :param int angle: number of degrees we want to rotate the motor. Negative 
                      value reverses direction.

    .. [/en]
    .. [sk]
    rotate_motor(motor, rýchlosť, uhol)

    Otočí motor v danom smere danou rýchlosťou a o istý počet stupňov. 

    :param int motor: motor, ktorý chceme točiť
    :param int speed: rýchlosť, ktorou chceme točiť motor od 0 do 100. Záporná 
                      hodnota otočí smer chodu motora.
    :param int angle: počet stupňov pre otáčanie motora. Záporná hodnota otočí 
                      smer chodu motora.
    .. [/sk]
    """

    return RotateMotor(motor, speed, angle)


def ResetTachoCount(motor):
    """
    .. [en]
    ResetTachoCount(motor)

    Reset tachometer counter.

    :param int motor: motor we want to reset.

    .. [/en]
    .. [sk]
    ResetTachoCount(motor)

    Zresetuje tachometer.

    :param int motor: motor, ktorého tachometer chceme zresetovať.
    .. [/sk]
    """

    dieTest()
    with robot.lock:
        if motor & OUT_A:
            robot.rotA = 0

        if motor & OUT_B:
            robot.rotB = 0

        if motor & OUT_C:
            robot.rotC = 0


IN_1 = S1 = 1
IN_2 = S2 = 2
IN_3 = S3 = 3
IN_4 = S4 = 4

SENSOR_TOUCH = 1
SENSOR_LIGHT = 2
SENSOR_SOUND = 3
SENSOR_ULTRASONIC = 4

MIC = SENSOR_SOUND
EYES = SENSOR_ULTRASONIC


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
    """
    .. [en]
    Sensor(sensor)

    Read value from given sensor.

    :param int sensor: sensor we want to read from

    .. [/en]
    .. [sk]
    Sensor(sensor)

    Načíta hodnotu z daného senzoru.

    :param int sensor: senzor, z ktorého chceme čítať.
    .. [/sk]
    """

    return robot.sensors[sensor].getValue()


def SensorUS(sensor):
    """
    .. [en]
    SensorUS(sensor)

    Read value from given lowspeed sensor (e.g. Ultrasonic). The input port
    has to be configured as lowspeed via :func:`api.SetSensorLowspeed` function before 
    using this function.

    :param int sensor: sensor we want to read from

    .. [/en]
    .. [sk]
    SensorUS(sensor)

    Načíta hodnotu z lowspeed sensoru (e.g. Ultrasonic). Input port
    by mal byť pred použitím nastavený ako lowspeed funkciou 
    :func:`api.Lowspeed.

    :param int sensor: senzor, z ktorého chceme načítať hodnotu
    .. [/sk]
    """

    return robot.sensors[sensor].getValue()


def SensorHTCompass(sensor):
    """
    .. [en]
    SensorHTCompass(sensor)

    Read value from given Compass sensor. Returns deviation from north.

    :param int sensor: sensor we want to read from

    .. [/en]
    .. [sk]
    SensorHTCompass(sensor)

    Načíta hodnotu z kompasu. Vrati odchýlku od severu.

    :param int sensor: senzor, z ktorého chceme čítať
    .. [/sk]
    """

    return robot.sensors[sensor].getValue()


def SensorHTIRSeeker(sensor, direction, val1, val2, val3, val4, val5):
    """
    SensorHTIRSeeker(sensor, direction, val1, val2, val3, val4, val5)

    Read value from the HiTechnic IR sensor which can be used to find the IR
    ball used in RoboCupJunior Soccer competition.

    :param int sensor: sensor to read from
    :param int direction: the ball's direction
    :param int val1: value in the first part
    :param int val2: value in the second part
    :param int val3: value in the third part
    :param int val4: value in the fourth part
    :param int val5: value in the fifth part
    """
    pass


def Random(n=None):
    """
    .. [en]
    Random(n = 0)

    Returns a random number

    :param int n: the maximal value this function should return

    .. [/en]
    .. [sk]
    Random(n = 0)

    Vráti náhodné číslo

    :param int n: najväčšia hodnota , ktorú má táto funkcia vrátiť.
    .. [/sk]
    """

    import random
    if n is None:
        return random.randint(-32767, 32767)
    else:
        return random.randint(0, n - 1)


def StopAllTasks():
    """
    .. [en]
    StopAllTasks()

    Stops all running tasks.

    .. [/en]
    .. [sk]
    StopAllTasks()

    Zastaví program a všetky jeho časti.
    .. [/sk]
    """

    robot.scr_running = False
    robot.die = True

def motor_tacho_count(motor):
    """
    .. [en]
    motor_tacho_count(motor)

    Get motor tachometer counter value.

    :param int motor: motor we want to get tachometer count from.

    .. [/en]
    .. [sk]
    motor_tacho_count(motor)

    Načíta hodnotu otáčkomeru motora.

    :param int motor: motor, z ktorého chceme načítavať.
    .. [/sk]
    """

    return MotorTachoCount(motor)


def motor_rotation_count(motor):
    """
    .. [en]
    motor_rotation_count(motor)

    Get motor tachometer counter value.

    :param int motor: motor we want to get tachometer count from.

    .. [/en]
    .. [sk]
    motor_rotation_count(motor)

    Načíta hodnotu otáčkomeru motora.

    :param int motor: motor, z ktorého chceme načítavať.
    .. [/sk]
    """

    return motor_tacho_count(motor)


def on_fwd(motor, speed):
    """
    .. [en]
    on_fwd(motor, speed)

    Set motor to forward direction and turn it on.

    :param int motor: motor we want to run.
    :param int speed: speed we want to run the motor at from 0 to 100. Negative 
                      value reverses direction.

    .. [/en]
    .. [sk]
    on_fwd(motor, rychlost)

    Nastaví motor tak, aby sa pohyboval vpred a spustí ho

    :param int motor: motor, ktorý chceme spustiť.
    :param int rychlost: Rýchlosť, ktorou chceme poslať robota dopredu od 0 do 
                         100. Záporná rýchlosť zmení smer chodu motora.

    .. [/sk]
    """
    return OnFwd(motor, speed)


def on_rev(motor, speed):
    """
    .. [en]
    on_rev(motor, speed)

    Set motor to reverse direction and turn it on.

    :param int motor: motor we want to run.
    :param int speed: speed we want to run the motor at from 0 to 100. Negative 
                      value reverses direction.

    .. [/en]
    .. [sk]
    OnRev(motor, rychlost)

    Nastaví motor nastaví motor na pohyb vzad a spustí ho.

    :param int motor: motor, ktorý chceme spustiť.
    :param int rychlost: rýchlosť, ktorou pôjde motor od 0 do 100. 
                         Záporná rýchlosť zmení smer chodu motora.

    .. [/sk]
    """

    return OnRev(motor, speed)


def set_sensor(port, type):
    """
    .. [en]
    set_sensor(port, type) 

    Sets the port to a given type. 
    .. [/en]

    """

    return SetSensor(port, type)


def set_sensors(port1, port2, port3, port4):
    """set_sensors(port1, port2, port3, port4)"""

    SetSensor(IN_1, port1)
    SetSensor(IN_2, port2)
    SetSensor(IN_3, port3)
    SetSensor(IN_4, port4)

    return True


def random(n=None):
    """
    .. [en]
    random(n = 0)

    Returns a random number

    :param int n: the maximal value this function should return

    .. [/en]
    .. [sk]
    random(n = 0)

    Vráti náhodné číslo

    :param int n: najväčšia hodnota , ktorú má táto funkcia vrátiť.
    .. [/sk]
    """

    return Random(n)

def lcd_print_at(xpos, ypos, text):
    """
    .. [en]
    lcd_print_at(xpos, ypos, text)

    Prints text on given y-th line, starting on the position of the x-th
    character.

    :param int xpos: the x coordinate (line)
    :param int ypos: the y coordinate (line)
    :param string text: text to be printed on the LCD screen
    .. [/en]
    .. [sk]
    lcd_print_at(xpos, ypos, text)

    Vypíše text na daný y-ty riadok, začínajúc na pozícii x-tého znaku. 
    
    :param int xpos: X-ová súradnica (riadok)
    :param int ypos: Y-ová súradnica (riadok)
    :param string text: text, ktorý sa má vypísať na LCD obrazovku
     .. [/sk]
    """
 
    TextOut(xpos*6, 64 - ypos*8, text)


def lcd_draw(obj, pA, pB, pC=None, pD=None):
    """
    .. [en]
    lcd_draw(obj, pA, pB, pC, pD)

    Draw obj given some parameters.

    :param int pA: parameter A.
    :param int pB: parameter B.
    :param int pC: parameter C.
    :param int pD: parameter D.

    .. [/en]
    .. [sk]
    lcd_draw(obj, pA, pB, pC, pD)

    Vykresli obj v závislosti od daných parametrov.

    :param int pA: parameter A.
    :param int pB: parameter B.
    :param int pC: parameter C.
    :param int pD: parameter D.
    .. [/sk]
    """

    if obj == "line":
        LineOut(pA, pB, pC, pD)
    elif obj == "rectangle":
        RectOut(pA, pB, pC, pD)


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
