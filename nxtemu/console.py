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
            self.lines.td(gui.Label(str(line), font=font),align=-1)
        self._data = _lines[-1:][0]

class Hack(gui.Spacer):
    def __init__(self, width, height, box):
        gui.Spacer.__init__(self, width, height)
        self.box = box

    def resize(self,width=None,height=None):
        self.box.set_vertical_scroll(65535)
        return 1,1

class ConsoleDialog(gui.Dialog):
    def __init__(self, **params):
        self._locals = {}

        title = gui.Label("Interactive console")

        self.container = gui.Container()

        t = gui.Table(width=env.w + env.WALL_HEIGHT*2 + 360 , height=85)
        t.tr()

        self.lines = gui.Table()

        self.box = gui.ScrollArea(self.lines, env.w + env.WALL_HEIGHT*2 + 300,
                85, hscrollbar=False, vscrollbar=True)
        self.box.set_vertical_scroll(100)
        t.td(self.box)

        font = pygame.font.SysFont("sans", 14)

        t.tr()
        
        it = gui.Table()

        it.td(gui.Label('>>>', font=font))

        self.line = gui.Input(size=113, font=font)
        self.line.connect(gui.KEYDOWN, self.lkey)
        it.td(self.line)


        t.td(it)
        t.tr()

        t.td(Hack(1, 1, self.box))

        self.container.add(t, 0, 0)

        gui.Dialog.__init__(self, title, self.container)

    def lkey(self, _event):
        event = _event
        if event.key == K_RETURN and self.line.value != "":
            _stdout = sys.stdout
            s = sys.stdout = StringStream(self.lines)
            
            val = self.line.value
            self.line.value = ''
            self.line.focus()
            print('>>> '+val)
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
