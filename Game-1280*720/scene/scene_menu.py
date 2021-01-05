# -*- coding:utf-8 -*-
from tkinter import *
import tkinter as tk
import json
import platform
import copy
import globe
import scene.scene_init as init_scene
import scene.scene_emergency as emergency_scene


ispause = False


class Scene:
    def __init__(self, thewindow, arg, arg_1=None):
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.arg = arg
        self.arg_1 = arg_1
        self.image_bg = PhotoImage(
            file="./asset/bg/init_window_options_bg.gif")
        self.canvas = Canvas(self.scene, width=1280,
                             height=720, bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(640, 360, image=self.image_bg)
        self.canvas.pack()
        self.canvas.bind_all('<KeyPress>', self.report_key_press)
        self.detecting = 255
        self.count = 0

        self.difficulty_data = None
        self.set_shoot_data = None
        self.set_shovel_data = None
        self.set_bomb_data = None
        self.set_left_data = None
        self.set_right_data = None
        self.default_settings = None
        self.last_level = None

        self.readin_configurations()

        self.difficulty_text = tk.StringVar()
        self.set_shoot_text = tk.StringVar()
        self.set_shovel_text = tk.StringVar()
        self.set_bomb_text = tk.StringVar()
        self.set_left_text = tk.StringVar()
        self.set_right_text = tk.StringVar()
        self.difficulty_text.set(self.difficulty_data)
        self.set_shoot_text.set(self.set_shoot_data)
        self.set_shovel_text.set(self.set_shovel_data)
        self.set_bomb_text.set(self.set_bomb_data)
        self.set_left_text.set(self.set_left_data)
        self.set_right_text.set(self.set_right_data)
        if platform.system() == 'Darwin':
            self.difficulty = tk.Button(textvariable=self.difficulty_text,
                                        command=lambda: self.getdifficulty(),
                                        highlightbackground='red',
                                        fg="#b01000", font="Times 25 bold",
                                        bd=0, width="18")
            self.canvas.create_window(850, 220, window=self.difficulty)
            self.set_shoot = tk.Button(textvariable=self.set_shoot_text,
                                       command=lambda: self.getshoot(),
                                       highlightbackground='red',
                                       fg="#b01000", font="Times 22 bold",
                                       bd=0, width="18")
            self.canvas.create_window(850, 353, window=self.set_shoot)
            self.set_shovel = tk.Button(textvariable=self.set_shovel_text,
                                        command=lambda: self.getshovel(),
                                        highlightbackground='red',
                                        fg="#b01000", font="Times 22 bold",
                                        bd=0, width="18")
            self.canvas.create_window(850, 395, window=self.set_shovel)
            self.set_bomb = tk.Button(textvariable=self.set_bomb_text,
                                      command=lambda: self.getbomb(),
                                      highlightbackground='red',
                                      fg="#b01000",
                                      font="Times 22 bold", bd=0, width="18")
            self.canvas.create_window(850, 437, window=self.set_bomb)
            self.set_left = tk.Button(textvariable=self.set_left_text,
                                      command=lambda: self.getleft(),
                                      highlightbackground='red',
                                      fg="#b01000",
                                      font="Times 22 bold", bd=0, width="18")
            self.canvas.create_window(850, 479, window=self.set_left)
            self.set_right = tk.Button(textvariable=self.set_right_text,
                                       command=lambda: self.getright(),
                                       highlightbackground='red',
                                       fg="#b01000", font="Times 22 bold",
                                       bd=0, width="18")
            self.canvas.create_window(850, 521, window=self.set_right)

            self.saveandexit = tk.Button(text="Save and exit",
                                         command=lambda: self.save_and_exit(),
                                         highlightbackground='red',
                                         fg="#b01000",
                                         font="Times 32 bold italic",
                                         bd=0, width="16")
            self.canvas.create_window(500, 590, window=self.saveandexit)
            self.reset = tk.Button(text="Reset Default",
                                   command=lambda: self.optionsreset(),
                                   highlightbackground='red', fg="#b01000",
                                   font="Times 32 bold italic",
                                   bd=0, width="16")
            self.canvas.create_window(750, 590, window=self.reset)
        else:
            self.difficulty = tk.Button(textvariable=self.difficulty_text,
                                        command=lambda: self.getdifficulty(),
                                        highlightbackground='red',
                                        fg="#b01000", font="Times 15 bold",
                                        bd=0, width="18")
            self.canvas.create_window(850, 220, window=self.difficulty)
            self.set_shoot = tk.Button(textvariable=self.set_shoot_text,
                                       command=lambda: self.getshoot(),
                                       highlightbackground='red', fg="#b01000",
                                       font="Times 12 bold", bd=0, width="18")
            self.canvas.create_window(850, 353, window=self.set_shoot)
            self.set_shovel = tk.Button(textvariable=self.set_shovel_text,
                                        command=lambda: self.getshovel(),
                                        highlightbackground='red',
                                        fg="#b01000", font="Times 12 bold",
                                        bd=0, width="18")
            self.canvas.create_window(850, 395, window=self.set_shovel)
            self.set_bomb = tk.Button(textvariable=self.set_bomb_text,
                                      command=lambda: self.getbomb(),
                                      highlightbackground='red', fg="#b01000",
                                      font="Times 12 bold", bd=0, width="18")
            self.canvas.create_window(850, 437, window=self.set_bomb)
            self.set_left = tk.Button(textvariable=self.set_left_text,
                                      command=lambda: self.getleft(),
                                      highlightbackground='red', fg="#b01000",
                                      font="Times 12 bold", bd=0, width="18")
            self.canvas.create_window(850, 479, window=self.set_left)
            self.set_right = tk.Button(textvariable=self.set_right_text,
                                       command=lambda: self.getright(),
                                       highlightbackground='red', fg="#b01000",
                                       font="Times 12 bold", bd=0, width="18")
            self.canvas.create_window(850, 521, window=self.set_right)

            self.saveandexit = tk.Button(text="Save and exit",
                                         command=lambda: self.save_and_exit(),
                                         highlightbackground='red',
                                         fg="#b01000",
                                         font="Times 22 bold italic", bd=0,
                                         width="16")
            self.canvas.create_window(500, 590, window=self.saveandexit)
            self.reset = tk.Button(text="Reset Default",
                                   command=lambda: self.optionsreset(),
                                   highlightbackground='red',
                                   fg="#b01000", font="Times 22 bold italic",
                                   bd=0, width="16")
            self.canvas.create_window(750, 590, window=self.reset)
        self.readin_configurations()

    def readin_configurations(self):
        with open('./asset/data/settings.json', 'r') as f:
            settings_dict = json.load(f)
            self.difficulty_data = settings_dict[0]["Rank"]
            self.set_shoot_data = settings_dict[0]["button_shoot"]
            self.set_shovel_data = settings_dict[0]["button_shovel"]
            self.set_bomb_data = settings_dict[0]["button_bomb"]
            self.set_left_data = settings_dict[0]["button_left"]
            self.set_right_data = settings_dict[0]["button_right"]
            self.last_level = settings_dict[0]["LastLevel"]
            self.default_settings = copy.deepcopy(settings_dict[1])

    def getdifficulty(self):
        levelist = \
            ['Easy   ', 'Normal ', 'Hard   ', 'Lunatic']
        self.difficulty_data = levelist[self.count % 4]
        self.difficulty_text.set(self.difficulty_data)
        self.count += 1

    def getshoot(self):
        self.set_shoot_text.set("Recording")
        self.detecting = 0

    def getshovel(self):
        self.set_shovel_text.set("Recording")
        self.detecting = 1

    def getbomb(self):
        self.set_bomb_text.set("Recording")
        self.detecting = 2

    def getleft(self):
        self.set_left_text.set("Recording")
        self.detecting = 3

    def getright(self):
        self.set_right_text.set("Recording")
        self.detecting = 4

    def optionsreset(self):
        self.difficulty_data = self.default_settings["Rank"]
        self.set_shoot_data = self.default_settings["button_shoot"]
        self.set_shovel_data = self.default_settings["button_shovel"]
        self.set_bomb_data = self.default_settings["button_bomb"]
        self.set_left_data = self.default_settings["button_left"]
        self.set_right_data = self.default_settings["button_right"]
        self.difficulty_text.set(self.difficulty_data)
        self.set_shoot_text.set(self.set_shoot_data)
        self.set_shovel_text.set(self.set_shovel_data)
        self.set_bomb_text.set(self.set_bomb_data)
        self.set_left_text.set(self.set_left_data)
        self.set_right_text.set(self.set_right_data)

    def save_and_exit(self):
        with open('./asset/data/settings.json', 'r') as f:
            settings_dict = json.load(f)
            insert_dict = {'Rank': self.difficulty_data,
                           "button_bomb": self.set_bomb_data,
                           "button_left": self.set_left_data,
                           "button_right": self.set_right_data,
                           "button_shoot": self.set_shoot_data,
                           "button_shovel": self.set_shovel_data,
                           "LastLevel": self.last_level
                           }
            list_to_write = [insert_dict] + [settings_dict[1]]
            with open('./asset/data/settings.json', 'w') as g:
                json.dump(list_to_write, g)
                self.gotoscene()

    def update(self):
        self.canvas.update()
        self.canvas.update_idletasks()

    @staticmethod
    def gotoscene():
        # and also save settings files
        globe.window.switch(init_scene, None)

    @staticmethod
    def extpause(arg):
        global ispause
        if arg == 0:
            ispause = True
        elif arg == 1:
            ispause = False

    def report_key_press(self, event):
        if event.keysym == 'Escape':
            globe.window.activescene.gotoscene()
        if event.keysym == 'b':
            globe.window.switch(emergency_scene, 1)
        else:
            if self.detecting == 0:
                self.set_shoot_data = event.keysym
                self.set_shoot_text.set(self.set_shoot_data)
                self.detecting = 255
            if self.detecting == 1:
                self.set_shovel_data = event.keysym
                self.set_shovel_text.set(self.set_shovel_data)
                self.detecting = 255
            if self.detecting == 2:
                self.set_bomb_data = event.keysym
                self.set_bomb_text.set(self.set_bomb_data)
                self.detecting = 255
            if self.detecting == 3:
                self.set_left_data = event.keysym
                self.set_left_text.set(self.set_left_data)
                self.detecting = 255
            if self.detecting == 4:
                self.set_right_data = event.keysym
                self.set_right_text.set(self.set_right_data)
                self.detecting = 255
