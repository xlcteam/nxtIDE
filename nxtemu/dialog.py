#!/usr/bin/env python
import pygame, sys, os
from pygame.locals import *

from pgu import gui

def p(path):
    """Nasty monkey patch - shall be removed"""
    import os
    from os.path import abspath, dirname
    return dirname(abspath(sys.argv[0])).replace('library.zip', '') + os.sep \
            + path


class BackgroundDialog(gui.Dialog):

    def __init__(self, bckg = "None"):
        self.bckg = bckg

        title = gui.Label("Set background")
        self.value = gui.Form()

        self.container = gui.Container()

        table = gui.Table()
        
        table.tr()
        table.td(self.build_background_select(), 
                    style={'padding_top': 10, 'padding_bottom': 10})

        save = gui.Button('Save')
        save.connect(gui.CLICK, self.send, gui.CHANGE)

        table.tr()
        table.td(save, align=1)

        self.container.add(table, 0, 0)

        gui.Dialog.__init__(self, title, self.container)

    def build_background_select(self):
        background = gui.Table()
        background.td(gui.Label("Room background:"), 
                      style={'padding_right': 6})
        self.background_input = gui.Input(size=16)
        inp = gui.Button('...')
        inp.connect(gui.CLICK, self.file_dialog_open, None)

        self.bckg_group = gui.Group(name='background', value='')
        t = gui.Table()
        t.tr()
        t.td(gui.Radio(self.bckg_group, value=''))
        t.td(gui.Label('None'), align=-1, style={'padding_left': 4})
        t.tr()
        custom_bckg = gui.Radio(self.bckg_group, value='custom')
        t.td(custom_bckg)
        t.td(self.background_input, style={'padding_left': 4})
        t.td(inp, style={'padding_left': 4})
        
        if self.bckg is not None and self.bckg != "None"\
                and os.path.exists(self.bckg):
            self.background_input.value = self.bckg
            custom_bckg.click()

        background.td(t)

        return background

    def file_dialog_open(self, arg):
        d = gui.FileDialog()                                                       
        d.connect(gui.CHANGE, self.file_dialog_handle, d)                       
        d.open()   

    def file_dialog_handle(self, dlg):
        if dlg.value: 
            self.background_input.value = dlg.value  
            self.bckg_group.value = 'custom'

    def out(self):
        return self.background_input.value


class SensorDialog(gui.Dialog):
    pt = {}
    inp = {}
    slots = [1, 2, 3]
    
    def __init__(self, bckg="None", port=None, **params):
        self.bckg = bckg
        self.port = port

        title = gui.Label("Sensor of port %d" % int(self.port))
        self.value = gui.Form()

        self.container = gui.Container()

        table = gui.Table()
        table.tr()
        
        self.sensors_img = gui.Image(p('icons/sensors.jpg'))
        table.td(self.sensors_img, cellspan=3)

        spacer = gui.Spacer(200, 100)
        self.box = gui.ScrollArea(spacer)
        table.tr()
        table.td(self.box, style={'border': 1})

        save = gui.Button('Save')
        save.connect(gui.CLICK, self.send, gui.CHANGE)

        table.tr()
        table.td(save, align=1)

        self.container.add(table, 0, 0)

        self.init_ports()
        self.change()
        gui.Dialog.__init__(self, title, self.container)

    def init_ports(self):
        self.pt = {}
        self.pt['img'] = gui.Image(p('icons/w_port%d.png' % int(self.port)))
        
        self.pt['sensors'] = self.build_sensors()

        self.container.add(self.pt['img'], 30+(60*self.port), 24)

        self.inp = {'type': None, 'slot': ''}

    def change(self):
        # changing the image
        
        spacer = gui.Spacer(200, 100)

        table = gui.Table()
        table.tr()
        table.td(self.pt['sensors'])
        table.td(gui.Image(p('icons/arrow.png')))

        slots = self.build_slots()

        table.td(slots)
        table.tr()

        self.box.widget = table

    def build_sensors(self):
        sensors_group = gui.Group(value='')
        sensors = gui.Table()
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, 
                        gui.Image(p('icons/light.png')), value='light'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, 
                        gui.Image(p('icons/sonic.png')), value='sonic'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, 
                        gui.Image(p('icons/touch.png')), value='touch'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group,
                        gui.Image(p('icons/compass.png')), value='compass'))
        sensors.tr()
        sensors.td(gui.Tool(sensors_group, gui.Label('None'), value=''))

        sensors_group.connect(gui.CHANGE, self.sensor_change, sensors_group)
        
        return sensors

    def build_slots(self):
        slots_group = gui.Group(value=self.inp['slot'])
        slots = gui.Table()
        
        wslots = self.slots
        for slot in [1, 2, 3]:
            slots.tr()
            if slot in wslots:
                slots.td(gui.Tool(slots_group, 
                                  gui.Image(p('icons/slot%d.png' % (slot))), 
                                  value=slot))
            else:
                slots.td(gui.Image(p('icons/slot%d.png' % (slot))))
 
        
        slots.tr()
        slots.td(gui.Tool(slots_group, gui.Label('None'), value=''))
        
        slots_group.connect(gui.CHANGE, self.slot_change, slots_group)
        
        return slots
    
    def port_connected(self):
        return self.inp['type'] is not None and \
                self.inp['slot'] is not ''
    
    def port_connect_update(self):
        if self.port_connected():
            pygame.draw.rect(self.sensors_img.value, (0, 0, 0), 
                    (28+(60*self.port), 51, 26, 34))
            
        else:
            pygame.draw.rect(self.sensors_img.value, (0xff, 0xff, 0xff), 
                    (28+(60*self.port), 51, 26, 34))
                    
        self.container.repaint()
    
    def sensor_change(self, g):
        self.inp['type'] = g.value
        self.port_connect_update()
    
    def slot_change(self, g):
        
        if g.value != '':
            self.slots.remove(g.value)
        else:
            self.slots.append(self.inp['slot'])

        self.inp['slot'] = g.value
        self.port_connect_update()

    def out(self):
        return self.inp



if __name__ == '__main__':                                                     
    app = gui.Desktop()                                                        
    app.connect(gui.QUIT,app.quit,None)                                        
                                                                               
    c = gui.Table(width=640,height=480)   
    dialog = SensorDialog(port=1)    
    #dialog = BackgroundDialog()
    def ret(d):
        print d.out()
        d.close()

    dialog.connect(gui.CHANGE, ret, dialog)

    e = gui.Button("New")                                                      
    e.connect(gui.CLICK,dialog.open)                                      
    c.tr()                                                                     
    c.td(e)                                                                    
                                                                               
    app.run(c)  
