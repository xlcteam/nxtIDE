#!/usr/bin/env python
import env
from math import cos, sin, radians

class BaseSensor(object):
    """BaseSensor is the wrapper object for all other sensors."""
    
    type = None
    slot = None

    def __init__(self, slot):
        
        self.slot = slot
    
    def getValue(self):
        return 0


class SensorUS(BaseSensor):
    """Ultrasonic Sensor - measures distance from nearest object."""
    type = 'sonic'
    pos = {1: [19.697715603592208, 66.03], 
           2: [-18, 270], 
           3: [-19.697715603592208, -66.03]}
    

    def getValue(self):
        pos = self.pos[self.slot]

        dx = cos(radians(pos[1] + robot.angle)) * pos[0]
        dy = sin(radians(pos[1] + robot.angle)) * pos[0]

        (x, y) = (robot.x - dx, robot.y - dy)
        for z in xrange(800):
            x += sin(radians(robot.angle))
            y += -cos(radians(robot.angle))
            
            o = env.background.get_at((int(round(x)), int(round(y))))
            if o == (190, 190, 190, 255):
                break
            #else:
            #    env.background.set_at((int(round(x)), int(round(y))), (255, 0, 0))
                
        return z//2.5


class SensorLight(BaseSensor):
    """Light Sensor - measures intensity of the reflected light."""
    type = 'light'
    pos = {1: [19.697715603592208, 66.03], 
           2: [-18, 270], 
           3: [-19.697715603592208, -66.03]}
    

    def lightness(self, val):
        """Returns lightness from inputed RGB value."""
        
        R, G, B, A = val
        
        return int((min([R, G, B])/2.0 + max([R, G, B])/2.0) / 2.55)


    def getValue(self):
        
        pos = self.pos[self.slot]
        
        dx = cos(radians(pos[1] + robot.angle)) * pos[0]
        dy = sin(radians(pos[1] + robot.angle)) * pos[0]

        x = int(round(robot.x - dx))
        y = int(round(robot.y - dy))

        rgb = env.background.get_at((x, y))
        #env.background.set_at((x, y), (0, 0, 0xff))
        #print (dx, dy), rgb
        return self.lightness(rgb)


class SensorTouch(BaseSensor):
    """Touch Sensor"""
    type = 'touch'
    pos = {1: [23.615528128088304, 70.54801085509538], 
           2: [-22, 270], 
           3: [-23.615528128088304, -70.54801085509538]}

    def getValue(self):

        pos = self.pos[self.slot]

        dx = cos(radians(pos[1] + robot.angle)) * pos[0]
        dy = sin(radians(pos[1] + robot.angle)) * pos[0]

        x = int(round(robot.x - dx))
        y = int(round(robot.y - dy))

        o = env.background.get_at((x, y))
        #env.background.set_at((x, y), (0, 0, 0xff))

        if o == (190, 190, 190, 255):
            return 1 
        else:
            return 0


class SensorHTCompass(BaseSensor):
    """HTCompass sensor - measures robot's rotation from north (0 - 359)"""
    type = 'compass'
    #TODO: make a slot at the top of robot for it

    def getValue(self):
        return robot.angle % 360



def sensor_generator(type, slot = None):
    if slot == '': slot = None

    if type == 'light':
        return SensorLight(slot) 
    elif type == 'sonic':
        return SensorUS(slot)
    elif type == 'touch':
        return SensorTouch(slot)
    elif type == 'compass':
        return SensorHTCompass(slot)
    else:
        return BaseSensor(slot)

if __name__ == "__main__":
   s = SensorLight()
   print s.getValue()

