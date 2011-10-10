#!/usr/bin/env python
import pygame
from pygame.locals import *

from pgu import gui


class SettingsDialog(gui.Dialog):
    
    def __init__(self, **params):
        title = gui.Label("Settings")
        self.value = gui.Form()

        container = gui.Container()

        table = gui.Table()
        table.tr()

        table.td(gui.Image('icons/sensors.jpg'), cellspan=3)
        

        self.port1 = gui.Image('icons/port1.png')
        self.port1.connect(gui.CLICK, self.change, (self.port1))
        self.port2 = gui.Image('icons/port2.png')
        self.port3 = gui.Image('icons/port3.png')
        self.port4 = gui.Image('icons/port4.png')
        
        spacer = gui.Spacer(200, 100)
        self.box = gui.ScrollArea(spacer)
        table.tr()
        table.td(self.box, style={'border': 1})

#       table.tr()
#       table.td(gui.Label("Slot"))
#       table.td(gui.Label("Sensor"))
#       table.td(gui.Label("Port"))
#       
#       
        self.sensors_group = gui.Group(value='')
        self.sensors = gui.Table()
        self.sensors.tr()
        self.sensors.td(gui.Tool(self.sensors_group, 
                        gui.Image('icons/light.png'), value='light'))
        self.sensors.tr()
        self.sensors.td(gui.Tool(self.sensors_group, 
                        gui.Image('icons/sonic.png'), value='sonic'))
        self.sensors.tr()
        self.sensors.td(gui.Tool(self.sensors_group, 
                        gui.Image('icons/touch.png'), value='touch'))
        
#       self.sensors_group.connect(gui.CHANGE, self.change)
#       
#       ports = gui.Select()
#       ports.add('Port 1', 1)
#       ports.add('Port 2', 2)
#       ports.add('Port 3', 3)
#       ports.add('Port 4', 4)



#       table.tr()
#       table.td(gui.Spacer(width=160,height=8))
#       table.td(gui.Spacer(width=220,height=8))
#       table.td(gui.Spacer(width=200,height=8))
#       table.tr()
#       table.td(gui.Label("Slot's might be here"))
#       table.td(sensors)
#       table.td(ports)
        
        container.add(table, 0, 0)
        container.add(self.port1, 90, 90)
        container.add(self.port2, 150, 90)
        container.add(self.port3, 210, 90)
        container.add(self.port4, 270, 90)
        gui.Dialog.__init__(self, title, container)
    
    def change(self, e):
        print e
        self.box.widget = self.sensors

if __name__ == '__main__':                                                     
    app = gui.Desktop()                                                        
    app.connect(gui.QUIT,app.quit,None)                                        
                                                                               
    c = gui.Table(width=640,height=480)   
    dialog = SettingsDialog()    

    e = gui.Button("New")                                                      
    e.connect(gui.CLICK,dialog.open,None)                                      
    c.tr()                                                                     
    c.td(e)                                                                    
                                                                               
    app.run(c)  
