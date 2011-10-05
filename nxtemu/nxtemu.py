#!/usr/bin/env python


import pygame, random, math, time, sys, os
from pygame.locals import * 
from robothread import *

from pgu import gui 

import imgs

from api import *
from brick import *
from clicker import Clicker

pygame.init() 

w = 640 
h = 480 

WALL_HEIGHT = 3

window = pygame.display.set_mode((w + WALL_HEIGHT*2 + 378,h + WALL_HEIGHT*2)) 
screen = pygame.display.get_surface() 

background = pygame.Surface(screen.get_size()) 
background = background.convert() 
background.fill((255, 255, 255))

pygame.display.set_caption("nxtemu")
background.blit(pygame.image.load("brick.jpg").convert(), (640, 0))
#background.blit(imgs.brick.convert(), (640, 0))

pygame.draw.rect(background, pygame.Color("gray"), ((0, 0), (646, 486)))
pygame.draw.rect(background, pygame.Color("white"), ((3, 3), (640, 480)))

background.blit(pygame.image.load("./line.jpg"), (3, 3))


clock = pygame.time.Clock() 

class Robot(NXTBrick): 
    proc = None
    die = False
    def __init__(self, wboot = True): 
        __builtins__.robot = self

        self.x = w/2 
        self.y = h/2 
        self.angle = 0

        self.mA = 0
        self.mB = 0
        self.mC = 0
        
        self.p = 0

        self.rotA = self.rotB = self.rotC = 0

        self.color = (random.randint(0,255),random.randint  
                      (0,255),random.randint(0,255)) 
        self.radius = 21

        self.dragged = False 
        self.dragoffset = [] 
        #self.image = pygame.image.load("./robot.jpg").convert()
        #path = os.path.dirname(os.path.abspath(sys.argv[0]))
        #self.image = pygame.image.load(path + "/robot.png").convert_alpha()  # imgs.robot.convert()
        self.image = imgs.robot.convert_alpha()
        #self.image = pygame.image.load("black_and_blacker.png").convert_alpha()

        self.lock = Lock()
        
        self.root = os.path.abspath(os.path.dirname(sys.argv[0]))
        # directory with programs to the path
        sys.path.append(self.root + os.sep + '__progs__')


        self.lcd = pygame.Surface((204, 130))
        pygame.draw.rect(self.lcd, pygame.Color(0x43, 0x6c, 0x30), 
            ((0, 0), (204, 130)))

        if wboot:
            #print "booting"
            RoboThread(target=self.boot).start()
        

    
    def getDistanceTo(self, point): 
        dx = point[0] - self.x 
        dy = point[1] - self.y 
        return math.sqrt(dx**2 + dy**2) 

    def mouseOver(self):  
        mpos = pygame.mouse.get_pos() 
        if self.getDistanceTo(mpos) < self.radius: 
            return True 
        else: 
            return False 

    def drag(self): 
        mpos = pygame.mouse.get_pos() 
        self.x = mpos[0] 
        self.y = mpos[1] 

        self.stayIn()
    
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self): 
        screen.blit(background, (0,0)) 
        screen.blit(self.rot_center(self.image, -self.angle), 
                (self.x - 30, self.y - 30))

        screen.blit(self.lcd, ((640 + (378/2 - 100)-2, 90), (204, 130)))

        app.paint()
        pygame.display.flip() 
    
    def stayIn(self):
        if self.x > 640:
            if self.dragged:
                self.x = 640
            else:
                self.x = 0

        if self.x < 0:
            self.x = 640

        if self.y > 480:
            self.y = 0

        if self.y < 0:
            self.y = 480



    def tick(self):
        self.stayIn()
        
        rotA = self.mA / 20.0
        rotB = self.mB / 20.0
        rotC = self.mC / 20.0
               
        angle = (rotA - rotB) / 4

        self.angle += angle
        p = (rotA + rotB) / 2 / 1.8
        
        # #print self.angle, self.mA, self.mB, self

        self.rotA += rotA
        self.rotB += rotB
        self.rotC += rotC

        self.x += math.sin(math.radians(self.angle)) * p
        self.y += -math.cos(math.radians(self.angle)) * p
        

        self.draw()
        # print background.get_at((int(self.x), int(self.y)))

    def onCenter(self):
        if self.screen < 4:
            self.screen += 1
        
        # taking care of empty __progs__ directory
        if self.screen == 2 and len(self.progs) == 0:
            self.screen -= 1

        if self.screen == 4:
            if self.proc == None:

                module = __import__('e' + self.progs[self.prog])                                               
                                                                                         
                self.proc = RoboThread(target=module.main,
                                       cleaner=self.cleaner)        
                ClearScreen()
                self.proc.start()                                                       
        else:
            self.scrout()
        
            
        #print "center"

    def onBack(self):
        
        # exiting
        if self.screen == 0:
            sys.exit(0)

        if self.proc == None:
            self.screen -= 1
            self.scrout()
        else:
            self.die = True

        #print "back"
    
    def onLeft(self):
        #print "left"
        if self.screen == 2:
            self.prog = (self.prog + 1) % len(self.progs)

        self.scrout()

    def onRight(self):
        #print "right"
        if self.screen == 2:
            self.prog = (self.prog - 1) % len(self.progs)

        self.scrout()

    def cleaner(self):
        ClearScreen()
        Off(OUT_ABC)
        ResetTachoCount(OUT_ABC)

        self.proc = None
        

        self.screen -= 1
        self.scrout()
        #print "cleaner"

if __name__ == "__main__":
    app = gui.App() 
    settings = gui.Image("settings.png")
   # settings.connect
    c = gui.Container(align=-1,valign=-1)                                          
    c.add(settings, 970, 400)   
    app.init(c, screen)    

    running = True 

    if len(sys.argv) > 1:
        robot = Robot(wboot = False)         
        robot.draw()


        prog = sys.argv[1]
        robot.progLoad()
        #print robot.progs
       
        robot.prog = robot.progs.index(prog)
        robot.screen = 3
        robot.wboot = False
        
        def runner():
            robot.scrout()
            Wait(800)
            robot.onCenter()

        RoboThread(target=runner).start()
        
    else:
        robot = Robot()
        robot.draw()


    clicker = Clicker()

    clicker.bind(((810, 252), (41, 40)), robot.onCenter)
    clicker.bind(((810, 308), (41, 26)), robot.onBack)
    clicker.bind(((751, 252), (41, 40)), robot.onLeft)
    clicker.bind(((870, 252), (41, 40)), robot.onRight)

    while running: 
        for event in pygame.event.get(): 
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                clicker.process(pygame.mouse.get_pos())
            
            if event.type == QUIT: 
                robot.die = True
                running = False
                sys.exit(0)

            elif event.type == MOUSEBUTTONDOWN and robot.mouseOver(): 

                if event.button == 1:
                    robot.dragged = not robot.dragged
                
                if robot.dragged:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
   

                if event.button == 4:
                    robot.angle += 1
                elif event.button == 5:
                    robot.angle -= 1

            app.event(event)
            

        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        mod = pygame.key.get_mods()

        if keystate[K_LEFT] and mod & KMOD_SHIFT:
            robot.angle -= 1
        elif keystate[K_RIGHT] and mod & KMOD_SHIFT:
            robot.angle += 1

        elif keystate[K_LEFT]:
            robot.x -= 1
        elif keystate[K_RIGHT]:
            robot.x += 1
        elif keystate[K_UP]:
            robot.y -= 1
        elif keystate[K_DOWN]:
            robot.y += 1

        if robot.dragged: 
            robot.draw() 
            robot.drag() 
        else:
            robot.tick()

        clock.tick(40) # Frame rate  
