#!/usr/bin/env python


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


class SensorLight(BaseSensor):
    """Light Sensor - measures intensity of the reflected light."""
    type = 'light'
    

    def lightness(self, val):
        """Returns lightness from inputed RGB value."""
        
        R, G, B = val
        
        return int((min([R, G, B])/2.0 + max([R, G, B])/2.0) / 2.55)


    def getValue(self):
        
        return self.lightness((243, 233, 21))



def sensor_generator(type, slot = None):
    if slot == '': slot = None

    if type == 'light':
        return SensorLight(slot) 
    elif type == 'sonic':
        return SensorUS(slot)
    else:
        return BaseSensor(slot)

if __name__ == "__main__":
   s = SensorLight()
   print s.getValue()

