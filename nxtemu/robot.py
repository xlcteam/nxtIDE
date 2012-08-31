from brick import *

from pgu import gui

import env

import os

import math

import imgs
from robothread import *
from dialog import SettingsDialog

from sensors import *

class Robot(NXTBrick):
    proc = None
    die = False
    inputs = {}
    background = None
    bckg = None
    sensors = {}
    touchPoints = {
        "topleft": [
            [29.0, -133.60281897270363],
            [28.319604517012593, -132.13759477388825],
            [27.65863337187866, -130.6012946450045],
        ],
        "left": [
            [-29, 42.721999467666336],
            [-28.319604517012593, 41.389942632819086],
        ],
        "topright": [
            [27.018512172212592, -51.00900595749453],
            [27.65863337187866, -49.398705354995535],
            [28.319604517012593, -47.862405226111754],
        ],
        "right": [
            [29.698484809834994, -43.97583689433345],
            [29, -42.721999467666336],
            [29, -47.278000532333664],
            [28.319604517012593, -41.389942632819086],
            [28.319604517012593, -48.610057367180914],
        ]
    }

    def __init__(self, wboot = True):
        __builtins__['robot']= self

        self.x = env.w/2
        self.y = env.h/2
        self.angle = 0

        self.mA = 0
        self.mB = 0
        self.mC = 0

        self.p = 0

        self.rotA = self.rotB = self.rotC = 0

        self.radius = 21

        self.dragged = False
        self.dragoffset = []
        #self.image = pygame.image.load("./robot.jpg").convert()
        #path = os.path.dirname(os.path.abspath(sys.argv[0]))
        #self.image = pygame.image.load(path + "/robot.png").convert_alpha() # imgs.robot.convert()
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
        
        self.sensors = {1: BaseSensor(1),
                        2: BaseSensor(2),
                        3: BaseSensor(3),
                        4: BaseSensor(4)}

        self.dialog = SettingsDialog()

    
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
        

        #pygame.image.save(self.image, "robot_.png")

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

        env.screen.blit(env.background, (0,0))
        env.screen.blit(self.rot_center(self.image, -self.angle),
                (self.x - 30, self.y - 30))

        env.screen.blit(self.lcd, ((640 + (378/2 - 100)-2, 90), (204, 130)))

        env.app.paint()
        pygame.display.flip()

    def touchesAt(self, positions):
        
        for pos in positions:
            dx = cos(radians(pos[1] + robot.angle)) * pos[0]
            dy = sin(radians(pos[1] + robot.angle)) * pos[0]
            
            #print 30 + round(dx), 30 + round(dy)

            x = int(self.x + round(dx))
            y = int(self.y + round(dy))

            #env.background.set_at((x, y), (0, 0, 255, 0))

            try:
                o = env.background.get_at((x, y))
            except IndexError:
                return True

            if o == (190, 190, 190, 255):
                return True

        return False

    def touches(self):
        out = {}
        for p in self.touchPoints:
            out[p] = self.touchesAt(p)

        return out

    def stayIn(self):
        if self.x > 623:
            self.x = 623

        if self.x < 23:
            self.x = 23

        if self.y > 463:
            self.y = 463

        if self.y < 23:
            self.y = 23


    def tick(self):
        # self.stayIn()
        angle = 0
        rotA = rotB = 0
        touchedA = touchedB = False

        if not self.touchesAt(self.touchPoints["topleft"]):
            rotA = self.mA / 30.0
        else:
            touchedA = True
            rotA -= self.mA / 40.0 

        if not self.touchesAt(self.touchPoints["topright"]):
            rotB = self.mB / 30.0
        else:
            touchedB = True
            rotB -= self.mB / 40.0

        rotC = self.mC / 30.0
               
        angle += (rotA - rotB) / 3

        self.angle += angle
        p = (rotA + rotB) / 2 / 1.8
        
        # #print self.angle, self.mA, self.mB, self
        
        self.rotA += rotA
        self.rotB += rotB
        self.rotC += rotC

        self.x += math.sin(math.radians(self.angle)) * p
        self.y += -math.cos(math.radians(self.angle)) * p
        
        self.angle = round(self.angle)

        self.draw()
        
        if touchedA:
            self.rotA += -2*rotA
        if touchedB:
            self.rotB += -2*rotB

        # print background.get_at((int(self.x), int(self.y)))

    def onCenter(self):
        #print "onCenter"

        # Turning off ? yes/no
        if self.screen_y == -1:
            if self.screen_x == 0:
                sys.exit(0)
            else:
                self.screen_y += 1
                self.screen_x = 0
                self.scrout()
                return

        # delete prog from nxtemu
       #if [self.screen_x, self.screen_y] == [1, 3]:
       #    if self.screen_x == 1:
       #        self.remove_prog()
       #    else:
       #        self.screen_x, self.screen_y, self.screen_z = 0, 3, 0
       #    self.scrout()
       #    return
           
        if [self.screen_x, self.screen_y, self.screen_z] == [0, 3, 0]:
            if self.proc == None:

                module = __import__('e' + self.progs[self.prog])
                                                                                         
                self.proc = RoboThread(target=module.main,
                                       cleaner=self.cleaner)
                self.proc.setName("brick")

                ClearScreen()
                self.scr_runner = RoboThread(target=robot.running)

                self.scr_runner.start()
                self.proc.start()
            return
        
        if self.screen_x == 0:
            self.screen_y += 1
        else:
            self.screen_z += 1
            self.screen_x = 0
        
        # taking care of empty __progs__ directory
        if self.screen_y == 2 and len(self.progs) == 0:
            self.screen_y -= 1

        
        #print self.screen_x, self.screen_y, self.screen_z
        self.scrout()

    def onBack(self):
        #taking care of turning off screen
        if self.screen_y == -1:
            self.screen_y += 1
            self.screen_x = 0
            self.scrout()
            return

        if self.proc == None:
            if self.scr_view == None:
                if self.screen_z:
                    self.screen_z -= 1
                else:
                    self.screen_y -= 1
            else:
                self.viewing = False
                self.scr_view = None
                self.screen_z -= 1
            self.screen_x = 0
            self.scrout()
        else:
            self.die = True
            self.scr_running = False

    def onLeft(self):
        if self.proc == None and self.scr_view == None:
            self.screen_x -= 1
        self.scrout()

    def onRight(self):
        if self.proc == None and self.scr_view == None:
            self.screen_x += 1
        self.scrout()

    def cleaner(self):
        ClearScreen()

        self.scr_running = False

        Off(OUT_ABC)
        ResetTachoCount(OUT_ABC)

        self.proc = None
        

        #self.screen_y -= 1
        self.scrout()
        #print "cleaner"

    def onDialog(self):
        self.dialog.connect(gui.CHANGE, self.dialogReturn, self.dialog)
        self.dialog.open()
        self.dialog.rect.x = 120
    
    def imgUpdate(self):
        image = imgs.robot.convert_alpha()
        
        for x in self.inputs:
            inp = self.inputs[x]
            if inp['slot'] != '':
                dx = inp['slot']*7
                if inp['slot'] == 3:
                    dx += 1
                
                dw = 1 if inp['slot'] == 2 else 0
                pygame.draw.rect(image, (0xfa, 0x70, 0x0d),
                                 (13+dx, 9, 5+dw, 5))
                


       #pygame.draw.rect(image, (0xfa, 0x70, 0x0d), (20, 9, 5, 5))
       #pygame.draw.rect(image, (0xfa, 0x70, 0x0d), (27, 9, 6, 5))
       #pygame.draw.rect(image, (0xfa, 0x70, 0x0d), (35, 9, 5, 5))

        self.image = image

    def dialogReturn(self, d):
        out = d.out()

        robot.inputs = out['inputs']
        
        for i in out['inputs']:
            inp = out['inputs'][i]
            
            self.sensors[i] = sensor_generator(inp['type'], inp['slot'])
        
        if out['others']['background'] is not None:
            robot.background = out['others']['background']
            env.init()
            
            img = pygame.image.load(robot.background)
            if img.get_alpha() != None:
                img = img.convert_alpha()
            else:
                img = img.convert()


            env.background.blit(img, (3, 3))
        else:
            robot.background = None
            env.init()
        
        self.imgUpdate()

        d.close()
