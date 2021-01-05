# -*- coding:utf-8 -*-
from tkinter import *
import time
import threading
import json
import globe
import scene.scene_game as game_scene
import scene.scene_init as init_scene
import scene.scene_emergency as emergency_scene


ispause = False
cursurloc = 0   # 0: start 1:continue 2: hiscore 3: settings 4:exit
reset = False
gloarg = None


class Scene:
    def __init__(self, thewindow, arg, arg_1=None):
        global gloarg
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.arg1 = arg_1
        self.size = [self.width, self.height]
        self.image_bg = PhotoImage(file="./asset/bg/game_paused_deactive.gif")
        self.images_menu_active = PhotoImage(file="./asset/bg/game_paused_active.gif")
        self.menu_active = [self.subimage( 0, 353+64*i, 1280, 353+64*(i+1), self.images_menu_active) for i in range(2)]
        self.canvas = Canvas(self.scene, width=self.size[0], height=self.size[1], bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(640, 360, image=self.image_bg)
        self.canvas.pack()
        self.initime = time.time()
        self.tracker = KeyTracker()
        self.canvas.bind_all('<KeyPress>', self.tracker.report_key_press)
        self.canvas.bind_all('<KeyRelease>', self.tracker.report_key_release)
        # print default cursurs
        self.cursur = self.canvas.create_image(640, 385, image=self.menu_active[cursurloc])
        self.arg = arg
        gloarg = arg

    def menupdate(self):
        self.canvas.delete(self.cursur)
        self.cursur = self.canvas.create_image(640, 385 + 64*cursurloc, image=self.menu_active[cursurloc])

    @staticmethod
    def subimage(left, top, right, bottom, spritesheet):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', left, top, right, bottom, '-to', 0, 0)
        return dst

    def update(self):
        self.menupdate()
        self.canvas.update()
        self.canvas.update_idletasks()
        self.scene.update()
        self.scene.update_idletasks()

    def gotoscene(self, arg):
        if arg == 0:
            self.savedata()
            globe.window.switch(game_scene, [1, 0, 0], None)
        if arg == 1:
            self.savedata()
            globe.window.switch(init_scene, None, None)

    def savedata(self):
        stage = self.arg[1]
        score = self.arg[2]
        bonus = self.arg[3]
        tiledata = str(self.arg[5])
        with open('./asset/data/continue_data.json', 'r') as f:
            continue_dict = json.load(f)
            insert_dict = {"Stage": stage, "Score": score, "Bonus": bonus, "Tiledata": tiledata}
            list_towrite = [insert_dict] + [continue_dict[1]]
            with open('./asset/data/continue_data.json', 'w') as g:
                json.dump(list_towrite, g)

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
        global cursurloc
        self.last_press_time = time.time()
        if event.keysym == 'Up':
            cursurloc = (cursurloc - 1) % 2
        elif event.keysym == 'Down':
            cursurloc = (cursurloc + 1) % 2
        elif event.keysym == 'z':
            globe.window.activescene.gotoscene(cursurloc)
        elif event.keysym == 'b':
            globe.window.switch(emergency_scene, 6, gloarg)

    def report_key_release(self, event):
        if event.keysym == 'Up' or 'Down' or 'z':
            timer = threading.Timer(.15, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed():
            pass
            # work on params
        self.last_release_time = time.time()


pass
