#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# An interactive console for live programming

import api

import traceback

import env

from pgu import gui
from pgu import html

import pygame
from pygame.locals import *
import sys

class StringStream:
    def __init__(self, lines):
        self._data = ''
        self.lines = lines

    def write(self, data):
        self._data = self._data+data
        _lines = self._data.split("\n")
        
        font = pygame.font.SysFont("sans", 14)

        for line in _lines[:-1]:
            self.lines.tr()
            self.lines.td(gui.Label(str(line), font=font),
                            align=-1)
        self._data = _lines[-1:][0]

class Hack(gui.Spacer):
    def __init__(self, width, height, box):
        gui.Spacer.__init__(self, width, height)
        self.box = box

    def resize(self,width=None,height=None):
        self.box.set_vertical_scroll(65535)
        return 1,1

class ConsoleDialog(gui.Dialog):
    def __init__(self, init_code=None, init_text=None, ps1='>>>', **params):
        
        self._locals = {}

        self.commands = []
        self.lastcmd = 0

        title = gui.Label("Interactive console")

        self.container = gui.Container(background= (255, 255, 255))

        t = gui.Table(width=env.w + env.WALL_HEIGHT*2 + 300 , height=85)
        t.tr()

        self.lines = gui.Table(background=(255, 255, 255))

        self.box = gui.ScrollArea(self.lines, env.w + env.WALL_HEIGHT*2 + 300,
                85, hscrollbar=False, vscrollbar=True, background=(255, 255, 255))
        self.box.set_vertical_scroll(100)
        t.td(self.box)

        font = pygame.font.SysFont("sans", 14)

        t.tr()
        
        it = gui.Table()

        it.td(gui.Label(ps1 + ' ', font=font))

        self.line = gui.Input(size=(117 - len(ps1)), font=font)
        self.line.connect(gui.KEYDOWN, self.lkey)
        #self.line.connect(gui.MOUSEBUTTONDOWN, self.lkey)
        it.td(self.line)


        t.td(it)
        t.tr()

        t.td(Hack(1, 1, self.box))

        self.container.add(t, 0, 0)

        if init_code is not None :
            code = compile(init_code, '<string>', 'single')
            eval(code,globals(),self._locals)
 
        if init_text is not None:
            _stdout = sys.stdout
            s = sys.stdout = StringStream(self.lines)
            
            val = self.line.value
            print(init_text)

            sys.stdout = _stdout
 
        self.ps1 = ps1

        gui.Dialog.__init__(self, title, self.container)

    def own_focus(self, x, y):
        e = pygame.event.Event(pygame.MOUSEBUTTONDOWN ,{"button": 1, "pos": (x,y)})
        pygame.event.post(e)

    def lkey(self, _event):
        event = _event

        if event.key == K_UP:
            if len(self.commands):
                if self.lastcmd > 0:
                    self.lastcmd -= 1
                self.line.value = self.commands[self.lastcmd]
            
            x = int(self.rect.x) + 86 + 100
            y = int(self.rect.y) + 86 + 38
            self.own_focus(x,y)

        elif event.key == K_DOWN:
            if len(self.commands):
                if self.lastcmd < len(self.commands) - 1:
                    self.lastcmd += 1
                self.line.value = self.commands[self.lastcmd]

            
            x = int(self.rect.x) + 86 + 100
            y = int(self.rect.y) + 86 + 38
            self.own_focus(x,y)

            
        elif event.key == K_RETURN and self.line.value != "":
            _stdout = sys.stdout
            s = sys.stdout = StringStream(self.lines)
            
            val = self.line.value

            self.commands.append(val)
            self.lastcmd = len(self.commands) - 1

            self.line.value = ''

            print(self.ps1 + ' ' + val)
            try:
                code = compile(val,'<string>','single')
                eval(code,globals(),self._locals)
            except: 
                e_type,e_value,e_traceback = sys.exc_info()
                print('Traceback (most recent call last):')
                traceback.print_tb(e_traceback,None,s)
                print(e_type,e_value)

            sys.stdout = _stdout


if __name__ == "__main__":
    app = gui.Desktop()
    app.connect(gui.QUIT,app.quit,None)

    dialog = ConsoleDialog()

    dialog.connect(gui.QUIT,dialog.close,None)

    c = gui.Table(width=640,height=480)   
    e = gui.Button("New")                                                      
    e.connect(gui.CLICK,dialog.open)                                      
    c.tr()                                                                     
    c.td(e)    

    app.run(c)
