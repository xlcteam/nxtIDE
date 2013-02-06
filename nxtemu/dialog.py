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
  
ports = {}
inputs = {}
slots = [1, 2, 3]

for x in range(1, 5):
    ports[x] = {}


class BackgroundDialog(gui.Dialog):
    port = None
    def __init__(self, bckg = "None", **params):
        self.bckg = bckg

        title = gui.Label("Settings")
        self.value = gui.Form()

        self.container = gui.Container()

        table = gui.Table()
        table.tr()
        
        self.sensors_img = gui.Image(p('icons/sensors.jpg'))
        

        table.td(self.sensors_img, cellspan=3)

        spacer = gui.Image(p('icons/choose_port.png'))
        self.box = gui.ScrollArea(spacer)
        table.tr()
        table.td(self.box, style={'border': 1})
        
        table.tr()
        table.td(self.build_background_select(), 
                    style={'padding_top': 10, 'padding_bottom': 10})

        save = gui.Button('Save')
        save.connect(gui.CLICK, self.send, gui.CHANGE)

        table.tr()
        table.td(save, align=1)

        self.container.add(table, 0, 0)

        self.init_ports()
        gui.Dialog.__init__(self, title, self.container)
    
    def init_ports(self):
        for x in range(1, 5):
            ports[x]['img'] = gui.Image(p('icons/port%d.png' % x))

            ports[x]['img'].connect(gui.CLICK, self.change, x)
            
            ports[x]['sensors'] = self.build_sensors()

            self.container.add(ports[x]['img'], 30+(60*x), 24)

            inputs[x] = {'type': None, 'slot': ''}

    
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
        
        if self.bckg != "None" and os.path.exists(self.bckg):
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


    def port_select(self, port, prev=None):
        
        if prev is not None:
            img = p('icons/port%d.png' % (prev))
            ports[prev]['img'].value = pygame.image.load(img).convert()
        
        img = p('icons/w_port%d.png' % (port))
        ports[port]['img'].value = pygame.image.load(img).convert()

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
        slots_group = gui.Group(value=inputs[self.port]['slot'])
        _slots = gui.Table()
        
        wslots = [inputs[self.port]['slot']] + slots

        for slot in [1, 2, 3]:
            _slots.tr()
            if slot in wslots:
                _slots.td(gui.Tool(slots_group, 
                                  gui.Image(p('icons/slot%d.png' % (slot))), 
                                  value=slot))
            else:
                _slots.td(gui.Image(p('icons/slot%d.png' % (slot))))
 
        
        _slots.tr()
        _slots.td(gui.Tool(slots_group, gui.Label('None'), value=''))
        
        slots_group.connect(gui.CHANGE, self.slot_change, slots_group)
        
        return _slots 



    def change(self, port):
        # changing the image
        self.port_select(port, self.port)
        self.port = port
        
        spacer = gui.Spacer(200, 100)

        table = gui.Table()
        table.tr()
        table.td(ports[self.port]['sensors'])
        table.td(gui.Image(p('icons/arrow.png')))

        _slots = self.build_slots()

        table.td(_slots)
        table.tr()

        self.box.widget = table
    
    def port_connected(self):
        return inputs[self.port]['type'] is not None and \
                inputs[self.port]['slot'] is not ''
    
    def port_connect_update(self):
        if self.port_connected():
            pygame.draw.rect(self.sensors_img.value, (0, 0, 0), 
                    (28+(60*self.port), 51, 26, 34))
            
        else:
            pygame.draw.rect(self.sensors_img.value, (0xff, 0xff, 0xff), 
                    (28+(60*self.port), 51, 26, 34))
                    
        self.container.repaint()
    
    def sensor_change(self, g):
        inputs[self.port]['type'] = g.value
        self.port_connect_update()
    
    def slot_change(self, g):
        
        if g.value != '':
            slots.remove(g.value)
        else:
            slots.append(inputs[self.port]['slot'])

        inputs[self.port]['slot'] = g.value
        self.port_connect_update()

    def out(self):

        value = dict(self.value.items())
        if value['background'] == '':
            background = None
        else:
            background = self.background_input.value

        return {'inputs': inputs, 
                'others': {'background': background}} 


class SensorDialog(gui.Dialog):
    
    def __init__(self, port = None, **params):
        self.port = port

        title = gui.Label("Connect sensor to port %d" % int(self.port))
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
        ports[self.port] = {}
        ports[self.port]['img'] = gui.Image(p('icons/w_port%d.png' % int(self.port)))
        
        ports[self.port]['sensors'] = self.build_sensors()

        self.container.add(ports[self.port]['img'], 30+(60*self.port), 24)

        inputs[self.port] = {'type': None, 'slot': ''}

    def change(self):
        # changing the image
        
        spacer = gui.Spacer(200, 100)

        table = gui.Table()
        table.tr()
        table.td(ports[self.port]['sensors'])
        table.td(gui.Image(p('icons/arrow.png')))

        _slots = self.build_slots()

        table.td(_slots)
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
        slots_group = gui.Group(value=inputs[self.port]['slot'])
        _slots = gui.Table()
        
        wslots = [inputs[self.port]['slot']] + slots

        for slot in [1, 2, 3]:
            _slots.tr()
            if slot in wslots:
                _slots.td(gui.Tool(slots_group, 
                                  gui.Image(p('icons/slot%d.png' % (slot))), 
                                  value=slot))
            else:
                _slots.td(gui.Image(p('icons/slot%d.png' % (slot))))
 
        
        _slots.tr()
        _slots.td(gui.Tool(slots_group, gui.Label('None'), value=''))
        
        slots_group.connect(gui.CHANGE, self.slot_change, slots_group)
        
        return _slots
    
    def port_connected(self):
        return inputs[self.port]['type'] is not None and \
                inputs[self.port]['slot'] is not ''
    
    def port_connect_update(self):
        if self.port_connected():
            pygame.draw.rect(self.sensors_img.value, (0, 0, 0), 
                    (28+(60*self.port), 51, 26, 34))
            
        else:
            pygame.draw.rect(self.sensors_img.value, (0xff, 0xff, 0xff), 
                    (28+(60*self.port), 51, 26, 34))
                    
        self.container.repaint()
    
    def sensor_change(self, g):
        inputs[self.port]['type'] = g.value
        self.port_connect_update()
    
    def slot_change(self, g):
        
        if g.value != '' and g.value in slots:
            slots.remove(g.value)
        else:
            slots.append(inputs[self.port]['slot'])

        inputs[self.port]['slot'] = g.value
        self.port_connect_update()

    def out(self):
        return inputs[self.port]


if __name__ == '__main__':                                                     
    app = gui.Desktop()                                                        
    app.connect(gui.QUIT,app.quit,None)                                        
                                                                               
    c = gui.Table(width=640,height=480)   
    #dialog = SensorDialog(port=1)    
    dialog = BackgroundDialog()
    def ret(d):
        print d.out()
        d.close()

    dialog.connect(gui.CHANGE, ret, dialog)

    e = gui.Button("New")                                                      
    e.connect(gui.CLICK,dialog.open)                                      
    c.tr()                                                                     
    c.td(e)                                                                    
                                                                               
    app.run(c)  
