# -*- coding:utf-8 -*-
from tkinter import *
import time
import threading
import globe
from random import randrange
import scene.scene_game as game_scene
import scene.scene_reg as game_reg
import scene.scene_menu as game_menu
import scene.scene_emergency as emergency_scene

ispause = False
cursurloc = 0   # 0: start 1:continue 2: hiscore 3: settings 4:exit
# 0: not played 1: playing
# 2: play finished, need to be deleted 3: play finished, deleted
anim_played = 0
initime = time.time()
wait_press = 0


class Scene:
    def __init__(self, thewindow, arg, arg_1=None):
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.arg = arg
        self.arg1 = arg_1
        self.size = [self.width, self.height]
        self.image_bg = PhotoImage(file="./asset/bg/init_window_1_bg.gif")
        self.image_bg_open = PhotoImage(file="./asset/bg/init_window_0_bg.gif")
        self.images_menu_active = PhotoImage(
            file="./asset/interface/init_window_menu_active.gif")
        self.images_bg_open_press = PhotoImage(
            file="./asset/bg/init_window_2_bg.gif")
        self.animate_lines = []
        self.menu_active = [self.subimage(0, 40*i, 224, 40*(i+1), self.images_menu_active) for i in range(5)]
        self.canvas = Canvas(self.scene, width=self.size[0], height=self.size[1], bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(self.width / 2, self.height / 2, image=self.image_bg)
        self.bg_anim = None
        self.bg_press = None
        self.canvas.pack()
        self.initime = time.time()
        self.tracker = KeyTracker()
        self.canvas.bind_all('<KeyPress>', self.tracker.report_key_press)
        self.canvas.bind_all('<KeyRelease>', self.tracker.report_key_release)
        # print default cursurs
        # self.canvas.create_image(644, 438, image=self.menu_active[cursurloc])
        self.cursur = None

    def menupdate(self):

        if anim_played == 4:
            self.canvas.delete(self.cursur)
            self.cursur = self.canvas.create_image(644, 438 + 40*cursurloc, image=self.menu_active[cursurloc])

    def animate(self):
        global anim_played, initime, wait_press
        now_time = time.time()
        if anim_played == 0 and (now_time - initime) > 0.1:
            initime = now_time
            self.bg_anim = self.canvas.create_image(
                self.width / 2, self.height / 2, image=self.image_bg_open)
            rand_y = randrange(20, 250)
            self.animate_lines.append(self.canvas.create_line(0, rand_y, 1280, rand_y, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 25, 1280, rand_y+25, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 85, 1280, rand_y + 85, width=2, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 10, 1280, rand_y + 10, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 60, 1280, rand_y + 60, width=2, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 55, 1280, rand_y + 55, width=3, fill='yellow'))
            rand_y = randrange(250, 450)
            self.animate_lines.append(self.canvas.create_line(0, rand_y, 1280, rand_y, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 25, 1280, rand_y + 25, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 85, 1280, rand_y + 85, width=2, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 10, 1280, rand_y + 10, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 60, 1280, rand_y + 60, width=2, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 55, 1280, rand_y + 55, width=3, fill='yellow'))
            rand_y = randrange(450, 700)
            self.animate_lines.append(self.canvas.create_line(0, rand_y, 1280, rand_y, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 25, 1280, rand_y + 25, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 45, 1280, rand_y + 45, width=2, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 10, 1280, rand_y + 10, width=3, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 30, 1280, rand_y + 30, width=2, fill='yellow'))
            self.animate_lines.append(self.canvas.create_line(0, rand_y + 55, 1280, rand_y + 55, width=3, fill='yellow'))
            if len(self.animate_lines) > 80:
                anim_played = 2
                self.bg_press = self.canvas.create_image(
                    self.width / 2, self.height / 2,
                    image=self.images_bg_open_press)

        if anim_played == 2:
            for line in self.animate_lines:
                self.canvas.delete(line)
            anim_played = 3

        if anim_played == 3 and wait_press == 1:
            self.bg = self.canvas.create_image(
                self.width / 2, self.height / 2, image=self.image_bg)
            anim_played = 4

    @staticmethod
    def subimage(left, top, right, bottom, spritesheet):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', left, top, right, bottom, '-to', 0, 0)
        return dst

    def update(self):
        self.animate()
        self.menupdate()
        self.canvas.update()

    @staticmethod
    def gotoscene(arg):
        if arg == 0:
            globe.window.switch(game_scene, [0, 0, 255, 0])
        if arg == 1:
            globe.window.switch(game_scene, [1, 0, 1, 0])
        if arg == 2:
            globe.window.switch(game_reg, [0, 0, 0, 0])
        if arg == 3:
            globe.window.switch(game_menu, None)
        if arg == 4:
            globe.window.kill()

    @staticmethod
    def extpause(arg):
        global ispause
        if arg == 0:
            ispause = True
        elif arg == 1:
            ispause = False


class KeyTracker:
    key = ''
    last_press_time = 0
    last_release_time = 0

    def track(self, key=None):
        self.key = key

    def is_pressed(self):
        return time.time() - self.last_press_time < 0.15

    def report_key_press(self, event):
        global cursurloc, wait_press
        self.last_press_time = time.time()

        if event.keysym == 'Up' and wait_press == 1:
            cursurloc = (cursurloc - 1) % 5
        elif event.keysym == 'Down' and wait_press == 1:
            cursurloc = (cursurloc + 1) % 5
        elif event.keysym == 'z' and wait_press == 1:
            globe.window.activescene.gotoscene(cursurloc)
        elif event.keysym == 'b' and wait_press == 1:
            globe.window.switch(emergency_scene, 0)
        wait_press = 1

    def report_key_release(self, event):
        if event.keysym == 'Up' or 'Down' or 'z' or 'b':
            timer = threading.Timer(.15, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed():
            pass
            # work on params
        self.last_release_time = time.time()
