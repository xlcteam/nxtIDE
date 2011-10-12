#!/usr/bin/env python
import pygame
from pygame.locals import *

from pgu import gui


class SettingsDialog(gui.Dialog):
    port = None   
    ports = {}
    inputs = {}
    def __init__(self, **params):
        title = gui.Label("Settings")
        self.value = gui.Form()

        self.container = gui.Container()

        table = gui.Table()
        table.tr()
        
        self.sensors_img = gui.Image('icons/sensors.jpg')

        table.td(self.sensors_img, cellspan=3)

        spacer = gui.Spacer(300, 100)
        self.box = gui.ScrollArea(spacer)
        table.tr()
        table.td(self.box, style={'border': 1})
        
        save = gui.Button('Save')
        save.connect(gui.CLICK, self.send, gui.CHANGE)

        table.tr()
        table.td(save, align=1)

        self.container.add(table, 0, 0)

        self.init_ports()
        gui.Dialog.__init__(self, title, self.container)
    
    def init_ports(self):
        for x in range(1, 5):
            self.ports[x] = {}
            self.ports[x]['img'] = gui.Image('icons/port%d.png' % x)
            self.ports[x]['img'].connect(gui.CLICK, self.change, x)
            
            self.ports[x]['sensors'] = self.build_sensors()
            self.ports[x]['slots'] = self.build_slots()

            self.container.add(self.ports[x]['img'], 30+(60*x), 90)

            self.inputs[x] = {'type': None, 'slot': None}


    def port_select(self, port, prev=None):
        
        if prev is not None:
            img = 'icons/port%d.png' % (prev)
            self.ports[prev]['img'].value = pygame.image.load(img).convert()
        
        img = 'icons/w_port%d.png' % (port)
        self.ports[port]['img'].value = pygame.image.load(img).convert()

    def build_sensors(self):
        sensors_group = gui.Group(value='')
        sensors = gui.Table()
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, 
                        gui.Image('icons/light.png'), value='light'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, 
                        gui.Image('icons/sonic.png'), value='sonic'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, 
                        gui.Image('icons/touch.png'), value='touch'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, gui.Label('None'), value=''))

        sensors_group.connect(gui.CHANGE, self.sensor_change, sensors_group)
        
        return sensors

    def build_slots(self):
        slots_group = gui.Group(value='')
        slots = gui.Table()
        slots.tr()
        slots.td(gui.Tool(slots_group, 
                        gui.Image('icons/slot1.png'), value=1))
        slots.tr()
        slots.td(gui.Tool(slots_group, 
                        gui.Image('icons/slot2.png'), value=2))
        slots.tr()
        slots.td(gui.Tool(slots_group, 
                        gui.Image('icons/slot3.png'), value=3))
        slots.tr()
        slots.td(gui.Tool(slots_group, gui.Label('None'), value=''))
        
        slots_group.connect(gui.CHANGE, self.slot_change, slots_group)
        
        return slots 



    def change(self, port):
        # changing the image
        self.port_select(port, self.port)
        self.port = port
        
        spacer = gui.Spacer(200, 100)

        table = gui.Table()
        table.tr()
        table.td(self.ports[port]['sensors'])
        table.td(gui.Image('icons/arrow.png'))
        table.td(self.ports[port]['slots'])
        table.tr()

        self.box.widget = table
    
    def port_connected(self):
        return self.inputs[self.port]['type'] is not None and \
                self.inputs[self.port]['slot'] is not None
    
    def port_connect_update(self):
        if self.port_connected():
            pygame.draw.rect(self.sensors_img.value, (0, 0, 0), 
                    (28+(60*self.port), 116, 26, 34))
            
            self.container.repaint()
            print "drawing"

    
    def sensor_change(self, g):
        self.inputs[self.port]['type'] = g.value
        self.port_connect_update()
    
    def slot_change(self, g):


        self.inputs[self.port]['slot'] = g.value
        self.port_connect_update()



if __name__ == '__main__':                                                     
    app = gui.Desktop()                                                        
    app.connect(gui.QUIT,app.quit,None)                                        
                                                                               
    c = gui.Table(width=640,height=480)   
    dialog = SettingsDialog()    

    def ret(d):
        print d.inputs
        d.close()

    dialog.connect(gui.CHANGE, ret, dialog)

    e = gui.Button("New")                                                      
    e.connect(gui.CLICK,dialog.open,None)                                      
    c.tr()                                                                     
    c.td(e)                                                                    
                                                                               
    app.run(c)  
