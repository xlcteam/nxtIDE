from brick import *

from pgu import gui 

import env

import math

import imgs
from robothread import *
from dialog import SettingsDialog

class Robot(NXTBrick): 
    proc = None
    die = False
    inputs = {}
    others = {}
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
        
        rotA = self.mA / 40.0
        rotB = self.mB / 40.0
        rotC = self.mC / 40.0
               
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
        # Turning off
        if self.screen == -1 and self.btn_x == 0:
            sys.exit(0)

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
                self.proc.setName("brick")

                ClearScreen()
                self.scr_runner = RoboThread(target=robot.running)

                self.scr_runner.start()
                self.proc.start()                                                       
        else:
            self.scrout()
        
            
        #print "center"

    def onBack(self):
        
        # exiting
       #if self.screen == 0:
       #    sys.exit(0)
        
        if self.screen == -1:
            self.screen += 2

        if self.proc == None:
            self.screen -= 1
            self.scrout()
        else:
            self.die = True
            self.scr_running = False

        #print "back"
    
    def onLeft(self):
        #print "left"
        if self.screen == 2:
            self.prog = (self.prog + 1) % len(self.progs)
        
        if self.screen == -1:
            self.btn_x = 0 

        self.scrout()

    def onRight(self):
        #print "right"
        if self.screen == 2:
            self.prog = (self.prog - 1) % len(self.progs)

        if self.screen == -1:
            self.btn_x = 1 


        self.scrout()

    def cleaner(self):
        ClearScreen()

        self.scr_running = False

        Off(OUT_ABC)
        ResetTachoCount(OUT_ABC)

        self.proc = None
        

        self.screen -= 1
        self.scrout()
        #print "cleaner"

    def onDialog(self):
        self.dialog.connect(gui.CHANGE, self.dialogReturn, self.dialog)
        self.dialog.open()
        self.dialog.rect.x = 120

    def dialogReturn(self, d):
        out = d.out()
        
        robot.inputs = out['inputs']
        robot.others = out['others']
        
        robot.background = out['others'][0][1]
        robot.back = out['others'][0][1]
        

        d.close()


