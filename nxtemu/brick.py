from api import *
from glob import glob
import os, os.path, sys

class NXTBrick:
    name = "emulator"
    imgs = {
        'battery': [[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[1, 3],[2, 0],[2, 1],
                    [2, 2],[2, 3],[3, 0],[3, 1],[3, 2],[3, 3],[4, 0],[4, 1],
                    [4, 2],[4, 3],[5, 0],[5, 1],[5, 2],[5, 3],[6, 0],[6, 1],
                    [6, 2],[6, 3],[7, 0],[7, 1],[7, 2],[7, 3],[8, 0],[8, 1],
                    [8, 2],[8, 3]],

        'run': [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12],
                [0, 13], [0, 14], [1, 0], [1, 1], [1, 2], [1, 3],
                [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9],
                [1, 10], [1, 11], [1, 12], [1, 13], [1, 14], [1, 15],
                [2, 0], [2, 1], [2, 14], [2, 15], [3, 0], [3, 1],
                [3, 14], [3, 15], [4, 0], [4, 1], [4, 14], [4, 15],
                [5, 0], [5, 1], [5, 14], [5, 15], [6, 0], [6, 1],
                [6, 6], [6, 7], [6, 8], [6, 9], [6, 14], [6, 15],
                [7, 0], [7, 1], [7, 6], [7, 7], [7, 8], [7, 9],
                [7, 14], [7, 15], [8, 0], [8, 1], [8, 6], [8, 7],
                [8, 8], [8, 9], [8, 14], [8, 15], [9, 0], [9, 1],
                [9, 6], [9, 7], [9, 8], [9, 9], [9, 14], [9, 15],
                [10, 0], [10, 1], [10, 14], [10, 15], [11, 0], [11, 1],
                [11, 14], [11, 15], [12, 0], [12, 1], [12, 14], [12, 15],
                [13, 0], [13, 1], [13, 14], [13, 15], [14, 0], [14, 1],
                [14, 2], [14, 3], [14, 4], [14, 5], [14, 6], [14, 7],
                [14, 8], [14, 9], [14, 10], [14, 11], [14, 12], [14, 13],
                [14, 14], [14, 15], [15, 1], [15, 2], [15, 3], [15, 4],
                [15, 5], [15, 6], [15, 7], [15, 8], [15, 9], [15, 10],
                [15, 11], [15, 12], [15, 13], [15, 14]],

        'swfiles': [[0, 16], [0, 15], [0, 14], [0, 13], [0, 12], [0, 11],
                [0, 10], [0, 9], [0, 8], [0, 7], [0, 6], [0, 5],
                [0, 4], [0, 3], [0, 2], [1, 16], [1, 1], [2, 16],
                [2, 15], [2, 14], [2, 13], [2, 12], [2, 11], [2, 10],
                [2, 9], [2, 8], [2, 0], [3, 16], [3, 7], [3, 0],
                [4, 16], [4, 7], [4, 0], [5, 16], [5, 7], [5, 4],
                [5, 3], [5, 2], [5, 1], [5, 0], [6, 16], [6, 14],
                [6, 13], [6, 12], [6, 11], [6, 10], [6, 9], [6, 7],
                [6, 4], [6, 0], [7, 16], [7, 14], [7, 9], [7, 7],
                [7, 4], [7, 2], [7, 1], [7, 0], [8, 16], [8, 14],
                [8, 12], [8, 11], [8, 7], [8, 4], [8, 2], [8, 1],
                [8, 0], [9, 16], [9, 14], [9, 12], [9, 11], [9, 7],
                [9, 4], [9, 0], [10, 16], [10, 14], [10, 9], [10, 7],
                [10, 4], [10, 0], [11, 16], [11, 14], [11, 13], [11, 12],
                [11, 11], [11, 10], [11, 9], [11, 7], [11, 4], [11, 0],
                [12, 16], [12, 7], [12, 4], [12, 0], [13, 16], [13, 7],
                [13, 4], [13, 3], [13, 2], [13, 1], [13, 0], [14, 16],
                [14, 7], [14, 0], [15, 16], [15, 15], [15, 14], [15, 13],
                [15, 12], [15, 11], [15, 10], [15, 9], [15, 8], [15, 0],
                [16, 16], [16, 0], [17, 16], [17, 15], [17, 14], [17, 13],
                [17, 12], [17, 11], [17, 10], [17, 9], [17, 8], [17, 7],
                [17, 6], [17, 5], [17, 4], [17, 3], [17, 2], [17, 1],],

        'view': [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                    [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12],
                    [1, 0], [1, 1], [1, 12], [1, 13], [2, 0], [2, 13],
                    [3, 0], [3, 13], [4, 0], [4, 13], [5, 0], [5, 11],
                    [5, 13], [6, 0], [6, 10], [6, 11], [6, 13], [7, 0],
                    [7, 9], [7, 11], [7, 13], [8, 0], [8, 8], [8, 11],
                    [8, 12], [8, 13], [8, 14], [8, 15], [8, 16], [9, 0],
                    [9, 7], [9, 16], [10, 0], [10, 7], [10, 16], [11, 0],
                    [11, 8], [11, 11], [11, 12], [11, 13], [11, 14], [11, 15],
                    [11, 16], [12, 0], [12, 9], [12, 11], [12, 13], [13, 0],
                    [13, 10], [13, 11], [13, 13], [14, 0], [14, 11], [14, 13],
                    [15, 0], [15, 13], [16, 0], [16, 13], [17, 0], [17, 13],
                    [18, 0], [18, 1], [18, 12], [18, 13], [19, 1], [19, 2],
                    [19, 3], [19, 4], [19, 5], [19, 6], [19, 7], [19, 8],
                    [19, 9], [19, 10], [19, 11], [19, 12],],

        'myfiles': [[0, 22], [0, 21], [0, 20], [0, 19], [0, 18], [0, 17],
                [0, 16], [0, 15], [0, 14], [0, 13], [0, 12], [0, 11],
                [0, 10], [1, 22], [1, 9], [2, 22], [2, 21], [2, 20],
                [2, 19], [2, 18], [2, 17], [2, 16], [2, 15], [2, 14],
                [2, 13], [2, 12], [2, 11], [2, 10], [2, 9], [2, 8],
                [2, 7], [3, 22], [3, 19], [3, 6], [4, 22], [4, 19],
                [4, 18], [4, 17], [4, 16], [4, 15], [4, 14], [4, 13],
                [4, 12], [4, 11], [4, 10], [4, 9], [4, 8], [4, 7],
                [4, 6], [4, 5], [4, 4], [5, 22], [5, 19], [5, 16],
                [5, 3], [6, 22], [6, 19], [6, 16], [6, 15], [6, 14],
                [6, 13], [6, 12], [6, 11], [6, 10], [6, 9], [6, 8],
                [6, 7], [6, 6], [6, 5], [6, 4], [6, 3], [6, 2],
                [7, 22], [7, 19], [7, 16], [7, 1], [8, 22], [8, 19],
                [8, 16], [8, 15], [8, 14], [8, 13], [8, 12], [8, 11],
                [8, 10], [8, 0], [9, 22], [9, 19], [9, 16], [9, 9],
                [9, 0], [10, 22], [10, 19], [10, 16], [10, 9], [10, 4],
                [10, 3], [10, 2], [10, 1], [10, 0], [11, 22], [11, 19],
                [11, 16], [11, 9], [11, 4], [11, 0], [12, 22], [12, 19],
                [12, 16], [12, 9], [12, 4], [12, 2], [12, 1], [12, 0],
                [13, 22], [13, 19], [13, 16], [13, 9], [13, 4], [13, 0],
                [14, 22], [14, 19], [14, 16], [14, 9], [14, 4], [14, 0],
                [15, 22], [15, 21], [15, 20], [15, 19], [15, 16], [15, 9],
                [15, 4], [15, 0], [16, 22], [16, 19], [16, 16], [16, 9],
                [16, 4], [16, 0], [17, 22], [17, 21], [17, 20], [17, 19],
                [17, 18], [17, 17], [17, 16], [17, 9], [17, 4], [17, 3],
                [17, 2], [17, 1], [17, 0], [18, 19], [18, 16], [18, 9],
                [18, 0], [19, 19], [19, 18], [19, 17], [19, 16], [19, 15],
                [19, 14], [19, 13], [19, 12], [19, 11], [19, 10], [19, 0],
                [20, 16], [20, 0], [21, 16], [21, 15], [21, 14], [21, 13],
                [21, 12], [21, 11], [21, 10], [21, 9], [21, 8], [21, 7],
                [21, 6], [21, 5], [21, 4], [21, 3], [21, 2], [21, 1],],

        'ok': [[0, 5], [0, 4], [1, 7], [1, 6], [1, 3], [2, 8],
                [2, 3], [3, 8], [3, 2], [4, 7], [4, 2], [5, 7],
                [5, 1], [6, 6], [6, 1], [7, 6], [7, 0], [8, 6],
                [8, 0], [9, 8], [9, 7], [9, 2], [9, 1], [10, 10],
                [10, 9], [10, 4], [10, 3], [11, 12], [11, 11], [11, 6],
                [11, 5], [12, 14], [12, 13], [12, 8], [12, 7], [13, 16],
                [13, 15], [13, 10], [13, 9], [14, 17], [14, 12], [14, 11],
                [15, 17], [15, 14], [15, 13], [16, 16], [16, 15],],

        'cross': [[0, 2],[0, 14],[1, 1],[1, 3],[1, 13],[1, 15],[2, 0],
                  [2, 4],[2, 12],[2, 16],[3, 1],[3, 5],[3, 11],[3, 15],
                  [4, 2],[4, 6],[4, 10],[4, 14],[5, 3],[5, 7],[5, 9],[5, 13],
                  [6, 4],[6, 8],[6, 12],[7, 5],[7, 11],[8, 6],[8, 10],[9, 5],
                  [9, 11],[10, 4],[10, 8],[10, 12],[11, 3],[11, 7],[11, 9],
                  [11, 13],[12, 2],[12, 6],[12, 10],[12, 14],[13, 1],[13, 5],
                  [13, 11],[13, 15],[14, 0],[14, 4],[14, 12],[14, 16],[15, 1],
                  [15, 3],[15, 13],[15, 15],[16, 2],[16, 14],],

        'touch': [[0, 5],[0, 13],[0, 14],[1, 4],[1, 13],[1, 14],[2, 4],[2, 14],
                  [2, 15],[3, 3],[3, 14],[3, 15],[4, 2],[4, 5],[4, 14],[4, 15],
                  [5, 2],[5, 5],[5, 12],[5, 14],[5, 15],[6, 1],[6, 4],[6, 5],
                  [6, 8],[6, 10],[6, 12],[6, 14],[6, 15],[7, 0],[7, 3],[7, 4],
                  [7, 5],[7, 8],[7, 10],[7, 12],[7, 13],[7, 14],[8, 1],[8, 2],
                  [8, 3],[8, 5],[8, 8],[8, 9],[8, 10],[8, 11],[8, 12],[9, 5],
                  [9, 8],[9, 9],[10, 5],[10, 8],[10, 9],[11, 5],[11, 8],[11, 9],
                  [12, 5],[12, 8],[12, 9],[13, 5],[13, 8],[13, 9],[14, 6],
                  [14, 7],[14, 8],[17, 5],[17, 6],[17, 7],[17, 8],[17, 9],
                  [18, 4],[18, 10],[19, 1],[19, 2],[19, 3],[19, 4],[19, 5],
                  [19, 6],[19, 7],[19, 8],[19, 9],[19, 10],[19, 11],[19, 12],
                  [19, 13],[19, 14],],
        'light': [[2, 7],[3, 7],[3, 12],[4, 11],[5, 6],[5, 7],[5, 8],[6, 1],
                   [6, 2],[6, 5],[6, 9],[6, 10],[7, 4],[7, 11],[7, 12],[7, 15],
                   [7, 17],[8, 4],[8, 13],[8, 14],[8, 16],[8, 18],[9, 3],
                   [9, 14],[9, 16],[9, 18],[9, 19],[10, 3],[10, 14],[10, 16],
                   [10, 19],[11, 3],[11, 14],[11, 16],[11, 18],[11, 19],[12, 4],
                   [12, 13],[12, 14],[12, 16],[12, 18],[13, 4],[13, 11],
                   [13, 12],[13, 15],[13, 17],[14, 1],[14, 2],[14, 5],[14, 9],
                   [14, 10],[15, 6],[15, 7],[15, 8],[16, 11],[17, 7],[17, 12],
                   [18, 7],],

        'sonic': [[5, 9],[5, 10],[5, 11],[5, 12],[5, 13],[5, 14],[5, 15],[5, 16],
                [5, 17],[5, 18],[5, 19],[5, 20],[6, 6],[6, 7],[6, 8],[6, 9],
                [7, 4],[7, 5],[7, 10],[7, 11],[8, 3],[8, 12],[9, 2],[9, 13],
                [10, 1],[10, 14],[11, 1],[11, 2],[11, 3],[11, 4],[11, 5],
                [11, 6],[11, 7],[11, 8],[11, 9],[11, 10],[11, 11],[11, 12],
                [11, 13],[11, 14],[12, 8],[13, 8],[14, 5],[14, 11],[15, 6],
                [15, 7],[15, 9],[15, 10],[16, 8],[17, 4],[17, 12],[18, 5],
                [18, 6],[18, 10],[18, 11],[19, 7],[19, 8],[19, 9],],

        'delete': [
                [3, 12] , [3, 11] , [4, 13] , [4, 11] , [4, 10] , [4, 9] ,
                [4, 8] , [4, 7] , [4, 6] , [4, 5] , [4, 4] , [4, 3] , [4, 2] , [4, 1] ,
                [5, 13] , [5, 11] , [5, 0] , [6, 13] , [6, 11] , [6, 10] , [6, 9] , [6, 8] ,
                [6, 7] , [6, 6] , [6, 5] , [6, 4] , [6, 3] , [6, 2] , [6, 1] , [6, 0] ,
                [7, 14] , [7, 13] , [7, 11] , [7, 0] , [8, 14] , [8, 13] , [8, 11] , [8, 10] ,
                [8, 9] , [8, 8] , [8, 7] , [8, 6] , [8, 5] , [8, 4] , [8, 3] , [8, 2] ,
                [8, 1] , [8, 0] , [9, 14] , [9, 13] , [9, 11] , [9, 0] , [10, 13] , [10, 11] ,
                [10, 10] , [10, 9] , [10, 8] , [10, 7] , [10, 6] , [10, 5] , [10, 4] , [10, 3] ,
                [10, 2] , [10, 1] , [10, 0] , [11, 13] , [11, 11] , [11, 0] , [12, 13] , [12, 11] ,
                [12, 10] , [12, 9] , [12, 8] , [12, 7] , [12, 6] , [12, 5] , [12, 4] , [12, 3] ,
                [12, 2] , [12, 1] , [13, 12] , [13, 11] ,
]
    }

    screen = 0

    screen_x = 0
    screen_y = 0
    screen_z = 0

    prog = 0
    progs = []
    viewing = False
    scr_running = False
    scr_killed = False
    view_sensors = ['Light', 'UltraSonic', 'Touch']
    view_s_id = 0
    def __init__(self):
        pass
    
    
    def header(self, around = False):
        self.textCenterOut(LCD_LINE1+1, self.name)
        self.imgOut(88, 59, self.imgs['battery'])
        LineOut(0, 56, 100, 56)

        if around:
            self.around()
        
    def around(self):
        LineOut(63, 1, 63, 25)
        LineOut(38, 1, 38, 25)
        LineOut(38, 25, 63, 25)

    def screen0(self):
        self.header(True)
        self.screen_x = self.screen_x % 2        

        # first centeral screen: pos [0, 0, 0] 
        if self.screen_x == 0:
            self.textCenterOut(LCD_LINE5+2, 'My Files')

            self.imgOut(40, 1, self.imgs['myfiles'])
            self.imgOut(70, 1, self.imgs['view'])

        # view screen: pos [1, 0, 0]
        else:
            self.textCenterOut(LCD_LINE5+2, 'View')

            self.imgOut(10, 1, self.imgs['myfiles'])
            self.imgOut(40, 1, self.imgs['view'])
    
    def screen1(self):
        self.header()
        self.textCenterOut(LCD_LINE5+2, "Software files")
        
        self.imgOut(40, 4, self.imgs['swfiles'])
        
        self.progLoad()
        self.prog = 0

    #screen for sensors
    def screen10(self):
        self.header()
        self.textCenterOut(LCD_LINE5+2, self.view_sensors[self.view_s_id])

        if self.view_s_id == 0:
            self.imgOut(10, 1, self.imgs['touch'])
            self.imgOut(40, 1, self.imgs['light'])
            self.imgOut(70, 1, self.imgs['sonic'])
        elif self.view_s_id == 1:
            self.imgOut(10, 1, self.imgs['light'])
            self.imgOut(40, 1, self.imgs['sonic'])
            self.imgOut(70, 1, self.imgs['touch'])
        elif self.view_s_id == 2:
            self.imgOut(10, 1, self.imgs['sonic'])
            self.imgOut(40, 1, self.imgs['touch'])
            self.imgOut(70, 1, self.imgs['light'])
        
    #screen for ports
    def screen100(self):
        self.header()
        self.textCenterOut(LCD_LINE5+2, 'Port ' + str(self.view_port + 1))

        self.imgOut(12, 4, self.imgs['run'])
        self.imgOut(42, 4, self.imgs['run'])
        self.imgOut(72, 4, self.imgs['run'])

    #screen for values
    def screen1000(self):
        self.header()
        
            
    def screen2(self):
        self.header()

        # special case of all items being on the same level
        if self.screen_y == 2 and self.screen_z == 1:
            self.screen_y = 3
            self.screen_x = 0
            self.screen_z = 0
            self.scrout()

            return

        self.screen_x = self.screen_x % len(self.progs)
        self.prog = self.screen_x
        
        self.textCenterOut(LCD_LINE5+2, self.progs[self.prog])

        self.imgOut(40, 4, self.imgs['swfiles'])
        if len(self.progs) > 1:
            if len(self.progs) == 2 and self.prog == 1:
                self.imgOut(10, 4, self.imgs['swfiles'])
            else:
                self.imgOut(70, 4, self.imgs['swfiles'])
        if len(self.progs) > 2:
            self.imgOut(10, 4, self.imgs['swfiles'])

    def screen3(self):
        
        # special case; makes getting back from selected delete possible
        if self.screen_z < 0:
            self.screen_y = 2
            self.screen_x = self.prog
            self.screen_z = 0
            self.scrout()

            return

        self.header()
        self.textCenterOut(LCD_LINE4+2, self.progs[self.prog])

        self.screen_x = self.screen_x % 2

        if self.screen_x == 0:
            self.textCenterOut(LCD_LINE5+2, 'Run')
            self.imgOut(10, 4, self.imgs['delete'])
            self.imgOut(42, 4, self.imgs['run'])
        elif self.screen_x == 1:
            self.textCenterOut(LCD_LINE5+2, 'Delete')
            self.imgOut(42, 4, self.imgs['delete'])
            self.imgOut(70, 4, self.imgs['run'])

    def screen31(self):
        self.header()

        self.textCenterOut(LCD_LINE4, "Are you sure?")
        self.screen_x = self.screen_x % 2

        if self.screen_x == 0:
            self.imgOut(20, 4, self.imgs['ok'])
            self.imgOut(40, 4, self.imgs['cross'])
        else:
            self.imgOut(40, 4, self.imgs['ok'])
            self.imgOut(60, 4, self.imgs['cross'])
    
    def screen_1(self):
        self.header()

        self.textCenterOut(LCD_LINE4, "Turn off?")
        self.screen_x = self.screen_x % 2

        if self.screen_x == 0:
            self.imgOut(40, 4, self.imgs['ok'])
            self.imgOut(60, 4, self.imgs['cross'])
        else:
            self.imgOut(20, 4, self.imgs['ok'])
            self.imgOut(40, 4, self.imgs['cross'])
            
        

    def scrout(self):
        ClearScreen()
        if self.screen_z:
            # YZ
            screen = 'screen%d%d' % (self.screen_y, self.screen_z)
        else:
            screen = 'screen%d' % self.screen_y
        getattr(self, screen.replace('-', '_'))()
    
    def progLoad(self):

        def older_first(x, y):
            return int(os.path.getmtime(y)) - int(os.path.getmtime(x))
        
        prgdir = self.root + os.sep + '__progs__' + os.sep
        #print prgdir
        self.progs = glob(prgdir + 'e*.py')

        progs = sorted(self.progs, cmp=older_first)
        self.progs = []

        for x in range(len(progs)):
            prog = progs[x].replace(prgdir + 'e' , '') \
                        .replace('.py', '')
            if not ('.' in prog):
                self.progs.append(prog)
        
    
    def running(self):
        self.scr_running = True
        #self.header()
        
        #self.imgOut(42, 4, self.imgs['run'])
        pygame.time.delay(200)
        s = ""
        clock = pygame.time.Clock()
        
        while self.scr_running:
            self.header()

            s += "."
            t = (3-len(s))*" "
            # ClearLine(LCD_LINE5)
            TextOut(20, LCD_LINE5, "Running " + s + t)

            #print "'"+s+t+"'"

            if len(s) >= 3:
                s = ""

            clock.tick(3)

    def sensor_viewing(self):
        self.viewing = True
        clock = pygame.time.Clock()

        sensor = self.view_sensors[self.view_s_id]

        if sensor == 'Light' or sensor == 'Touch':
            s = Sensor(self.view_port + 1)
        elif sensor == 'Ultrasonic':
            s = SensorUS(self.view_port + 1)

        while self.viewing:
            self.header()
            refresh = str(s)           

            self.textCenterOut(LCD_LINE4, refresh)

            clock.tick(3)

    def remove_prog(self):
        try:
            os.remove('__progs__/e' + self.progs[self.prog] + '.py')
            try:
                os.remove('__progs__/e' + self.progs[self.prog] + '.pyc')
            except: pass
        except: pass
        
        self.progs.remove(self.progs[self.prog])
        self.prog = (self.prog - 1) % len(self.progs)

        self.screen_x = 0
        self.screen_y = 2
        self.screen_z = 0

    def boot(self):
        Wait(200)
        
        self.scrout()
        
        #TextOut(30, LCD_LINE4, "nxtemu")
        

        #Wait(8000)
        #ClearScreen()
    
    def textCenterOut(self, line, text):
        x = 50 - len(text)*3
        TextOut(x, line, text)


    def imgOut(self, x, y, img):
        for pos in img:
            PointOut(x + pos[0], y + pos[1])
