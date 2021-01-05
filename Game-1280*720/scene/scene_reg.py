# -*- coding:utf-8 -*-
from tkinter import *
import tkinter as tk
import time
import json
import platform
import threading
import globe
import scene.scene_init as init_scene
import scene.scene_emergency as emergency_scene


ispause = False
reset = False
extarg = None


class Scene:
    def __init__(self, thewindow, arg, arg_1=None):
        global extarg
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.arg1 = arg_1
        self.image_bg = PhotoImage(file="./asset/bg/reg_window_bg.gif")
        self.canvas = Canvas(self.scene, width=1280,
                             height=720, bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(640, 360, image=self.image_bg)
        self.canvas.pack()
        self.tracker = KeyTracker()
        self.canvas.bind_all('<KeyPress>', self.tracker.report_key_press)
        self.canvas.bind_all('<KeyRelease>', self.tracker.report_key_release)
        self.score_dict = None
        extarg = arg
        self.hiscore_score = []
        self.hiscore_name = []
        self.hiscore_rank = []
        self.file_r = None
        self.entry = None
        self.var = None
        self.name = None
        self.score = arg[0]
        self.rank = arg[1]
        self.level = arg[2]
        self.button = None
        self.list_towrite = []
        self.dataprocessing(arg)

    @staticmethod
    def s_formatting(string, k):
        if len(string) == 0 or string is None:
            return "    "
        elif len(string) >= k:
            return str(string[0:k])
        elif len(string) < k:
            while len(string) < k:
                string += ' '
            return str(string)

    def dataprocessing(self, arg):
        with open('./asset/data/score.json', 'r') as self.file_r:
            score_dict = json.load(self.file_r)
            for i in range(4):
                if platform.system() == 'Darwin':
                    self.canvas.create_text(
                        335, 328 + 82 * i, fill="black",
                        font="Times  50 bold", text=str(score_dict[i]["Name"]))
                    self.canvas.create_text(
                        600, 328 + 82 * i, fill="red",
                        font="Times 50 italic",
                        text=str(score_dict[i]["Score"]))
                    self.canvas.create_text(
                        924, 328 + 82 * i, fill="purple",
                        font="Times 50 italic",
                        text=str(score_dict[i]["Rank"]))
                    self.canvas.create_text(
                        1080, 328 + 82 * i, fill="purple",
                        font="Times 50 bold", text=str(score_dict[i]["Level"]))
                else:
                    self.canvas.create_text(
                        335, 333 + 82 * i, fill="black",
                        font="Times  40 bold", text=str(score_dict[i]["Name"]))
                    self.canvas.create_text(
                        600, 333 + 82 * i, fill="red",
                        font="Times 40 italic",
                        text=str(score_dict[i]["Score"]))
                    self.canvas.create_text(
                        924, 333 + 82 * i, fill="purple",
                        font="Times 40 italic",
                        text=str(score_dict[i]["Rank"]))
                    self.canvas.create_text(
                        1080, 333 + 82 * i, fill="purple",
                        font="Times 40 bold", text=str(score_dict[i]["Level"]))

            if arg[3] == 1:
                self.registration()

    def registration(self):
        self.var = tk.StringVar()
        if platform.system() == 'Darwin':
            self.entry = Entry(
                self.scene, font="Times 50 italic", justify="center",
                width=32, bg="purple", fg="yellow",
                disabledbackground="#1E6FBA", disabledforeground="black",
                highlightbackground="black", highlightcolor="red",
                highlightthickness=1, bd=0)
            self.entry.place(width=20, height=500)
            self.canvas.create_window(550, 660, window=self.entry)
            self.entry.insert(0, "Enter your name: (4 chars limit)")
            self.button = tk.Button(text="Submit",
                                    command=lambda: self.getvalue(),
                                    bg="#cbd020", fg="purple",
                                    font="Times 50 bold", bd=0)
            self.canvas.create_window(1035, 660, window=self.button)
        else:
            self.entry = Entry(
                self.scene, font="Times 40 italic", justify="center",
                width=32, bg="purple", fg="yellow",
                disabledbackground="#1E6FBA", disabledforeground="black",
                highlightbackground="black", highlightcolor="red",
                highlightthickness=1, bd=0)
            self.entry.place(width=20, height=500)
            self.canvas.create_window(550, 660, window=self.entry)
            self.entry.insert(0, "Enter your name: (4 chars limit)")
            self.button = tk.Button(text="Submit",
                                    command=lambda: self.getvalue(),
                                    bg="#cbd020", fg="purple",
                                    font="Times 36 bold", bd=0)
            self.canvas.create_window(1035, 660, window=self.button)

    def getvalue(self):
        self.name = self.entry.get()
        self.name = self.s_formatting(self.name, 4)
        self.datastoring()

    def datastoring(self):
        # open, cmp, insert, exit
        with open('./asset/data/score.json', 'r') as f:
            score_dict = json.load(f)
            insert_dict = {"Rank": self.rank, "Name": self.name,
                           "Score": str(self.score).zfill(7),
                           "Level": self.level[-1]}
            for i in range(len(score_dict)):
                if int(score_dict[i]["Score"]) <= int(insert_dict["Score"]):
                    list_0 = score_dict[0:i]
                    list_1 = score_dict[i: len(score_dict)]
                    self.list_towrite = list_0 + [insert_dict] + list_1
                    break
            else:
                self.list_towrite = score_dict + [insert_dict]
            with open('./asset/data/score.json', 'w') as g:
                json.dump(self.list_towrite, g)
                with open('./asset/data/continue_data.json', 'r') as h:
                    continue_dict = json.load(h)
                    insert_dict = continue_dict[1]
                    list_towrite = [insert_dict] + [continue_dict[1]]
                    with open('./asset/data/continue_data.json', 'w') as i:
                        json.dump(list_towrite, i)
                self.gotoscene()

    def update(self):
        self.canvas.update()
        self.canvas.update_idletasks()

    @staticmethod
    def gotoscene():
        globe.window.switch(init_scene, None)

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
        self.last_press_time = time.time()
        if event.keysym == 'b':
            globe.window.switch(emergency_scene, 4, extarg)
        elif event.keysym == 'Escape':
            globe.window.activescene.gotoscene()

    def report_key_release(self, event):
        if event.keysym == 'z':
            timer = threading.Timer(.15,
                                    self.report_key_release_callback,
                                    args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed():
            pass
            # work on params
        self.last_release_time = time.time()


pass
