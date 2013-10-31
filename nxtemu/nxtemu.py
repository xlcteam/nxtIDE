#!/usr/bin/env python2

import pygame, random, math, time, sys, os
from pygame.locals import * 

from pgu import gui 
import imgs

from os.path import abspath, dirname
sys.path.append(os.path.dirname(sys.argv[0]))

def p(path):
    """Nasty monkey patch - shall be removed"""
    import os
    from os.path import abspath, dirname
    return dirname(abspath(sys.argv[0])).replace('library.zip', '') + os.sep \
            + path


from clicker import Clicker

from robot import Robot
from robothread import *

pygame.init() 
icon = pygame.image.load(p('./icons/nxtemu.png')).convert_alpha()
pygame.display.set_icon(icon)
pygame.mixer.pre_init(44100, -16, 2)

import env
env.init()

clock = pygame.time.Clock() 

def main():
    env.app = gui.App(theme=gui.Theme(p("theme/default/"))) 
    settings = gui.Image(p("icons/settings.png"))
    console = gui.Image(p("icons/python.png"))
   # settings.connect
    c = gui.Container(align=-1,valign=-1)
    c.add(console, 970, 10)
    c.add(settings, 960, 400)
    env.app.init(c, env.screen)    

    running = True 

    if len(sys.argv) > 1:
        robot = Robot(wboot = False)         
        robot.draw()


        prog = sys.argv[1]
        robot.progLoad()
       
        robot.prog = robot.progs.index(prog)
        robot.screen = 3
        robot.wboot = False
        
        def runner():
            robot.screen_y = 3
            robot.scrout()
            Wait(800)
            robot.onCenter()

        RoboThread(target=runner).start()
        
    else:
        robot = Robot()
        robot.draw()


    clicker = Clicker()

    clicker.bind(((810, 252), (41, 40)), robot.onCenter)
    clicker.bind(((810, 308), (41, 26)), robot.onBack)
    clicker.bind(((751, 252), (41, 40)), robot.onLeft)
    clicker.bind(((870, 252), (41, 40)), robot.onRight)
    clicker.bind(((970, 10),  (45, 45)), robot.onConsole)

    clicker.bind(((960, 400), (50, 50)), robot.background_dialog)

    # sensor binds
    clicker.bind(((735, 440), (19, 23)), robot.port1)
    clicker.bind(((795, 440), (19, 23)), robot.port2)
    clicker.bind(((855, 440), (19, 23)), robot.port3)
    clicker.bind(((915, 440), (19, 23)), robot.port4)

    robot.load_config('./config.yml')

    while running: 
        for event in pygame.event.get(): 
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                clicker.process(pygame.mouse.get_pos())

            if event.type == KEYDOWN:
                if event.mod & KMOD_CTRL:
                    if event.key == K_h:
                        robot.brick_hidden = not robot.brick_hidden
                        env.check_brick()
                    if event.key == K_d:
                        robot.background_dialog()
                    if event.key == K_c:
                        robot.onConsole()
            
            if event.type == QUIT: 
                robot.die = True
                running = False
                pygame.quit()
                sys.exit(0)

            elif event.type == MOUSEBUTTONDOWN and robot.mouseOver(): 

                if event.button == 1:
                    robot.dragged = not robot.dragged
                
                if robot.dragged:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
   

                if event.button == 4:
                    robot.angle += 1
                    robot.angle = round(robot.angle, 0)
                elif event.button == 5:
                    robot.angle -= 1
                    robot.angle = round(robot.angle, 0)

            env.app.event(event)
            
            
        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        mod = pygame.key.get_mods()

        # rotate robot by keys
        if keystate[K_LEFT] and mod & KMOD_SHIFT:
            robot.angle -= 1
        elif keystate[K_RIGHT] and mod & KMOD_SHIFT:
            robot.angle += 1

        if robot.dragged: 
            robot.draw() 
            robot.drag() 
        else:
            robot.tick()

        clock.tick(40) # Frame rate  

if __name__ == "__main__":
    main()

