#!/usr/bin/env python
import pygame
from pygame.locals import *

from pgu import gui


class SettingsDialog(gui.Dialog):
    
    def __init__(self, **params):
        title = gui.Label("Settings")
        self.value = gui.Form()

        table = gui.Table()
        table.tr()
        table.td(gui.Label("Slot"))
        table.td(gui.Label("Sensor"))
        table.td(gui.Label("Port"))
        
        
        self.sensors_group = gui.Group(value='')
        sensors = gui.Table()
        sensors.tr()
        sensors.td(gui.Tool(self.sensors_group, 
                        gui.Image('icons/light.png'), value='light'))
        sensors.td(gui.Tool(self.sensors_group, 
                        gui.Image('icons/sonic.png'), value='sonic'))
        sensors.td(gui.Tool(self.sensors_group, 
                        gui.Image('icons/touch.png'), value='touch'))
        
        self.sensors_group.connect(gui.CHANGE, self.change)
        
        ports = gui.Select()
        ports.add('Port 1', 1)
        ports.add('Port 2', 2)
        ports.add('Port 3', 3)
        ports.add('Port 4', 4)



        table.tr()
        table.td(gui.Spacer(width=160,height=8))
        table.td(gui.Spacer(width=220,height=8))
        table.td(gui.Spacer(width=200,height=8))
        table.tr()
        table.td(gui.Label("Slot's might be here"))
        table.td(sensors)
        table.td(ports)

        gui.Dialog.__init__(self, title, table)
    
    def change(self, **params):
        print self.sensors_group.value

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
