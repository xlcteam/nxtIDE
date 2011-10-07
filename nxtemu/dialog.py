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
        table.td(gui.Label("Slot"), align=-1)
        table.td(gui.Label("Sensor"), align=-1)
        table.td(gui.Label("Port"), align=-1)

        sensors = gui.Table()
        sensors.tr()
        sensors.td(gui.Image('icons/light.png'))
        sensors.tr()
        sensors.td(gui.Image('icons/sonic.png'))
        sensors.tr()
        sensors.td(gui.Image('icons/touch.png'))
        
        table.tr()
        table.td(gui.Label("Slot's might be here"))
        table.td(sensors)

        gui.Dialog.__init__(self, title, table)


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
