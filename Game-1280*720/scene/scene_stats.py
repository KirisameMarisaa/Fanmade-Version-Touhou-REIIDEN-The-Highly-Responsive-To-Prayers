# -*- coding:utf-8 -*-
from tkinter import *
import time
import platform
import globe
import scene.scene_game as game_scene
import scene.scene_reg as reg_scene
import scene.scene_emergency as emergency_scene

ispause = False
extdata = None


class Scene:
    def __init__(self, thewindow, external_data=None, arg_1=None):
        global extdata
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.arg1 = arg_1
        self.size = [self.width, self.height]
        self.image_bg = PhotoImage(file="./asset/bg/stats_window_bg.gif")
        self.canvas = Canvas(
            self.scene, width=self.size[0],
            height=self.size[1], bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(
            self.width / 2, self.height / 2, image=self.image_bg)
        self.canvas.place(x=0, y=0)
        self.initime = time.time()
        self.canvas.bind_all('<KeyPress>', self.jump)
        self.external_data = external_data
        extdata = external_data
        # STAT DATA
        self.totalscore = 0
        self.totaltime = 0
        self.maxbonus = 0
        self.points = 0
        self.rank = "Easy   "
        self.level = "Stage 1"
        self.stats_process()
        if platform.system() == 'Darwin':
            self.totaltime_onscreen = self.canvas.create_text(
                450, 269, fill="red",
                font="Times 49 bold italic", text=str(self.totaltime).zfill(7))
            self.maxbonus_onscreen = self.canvas.create_text(
                523, 339, fill="red",
                font="Times 49 bold italic", text=str(self.maxbonus).zfill(1))
            self.points_onscreen = self.canvas.create_text(
                450, 407, fill="red",
                font="Times 49 bold italic", text=str(self.points).zfill(7))
            self.rank_onscreen = self.canvas.create_text(
                420, 476, fill="red",
                font="Times 49 bold italic", text=self.rank)
            self.totalscore_onscreen = self.canvas.create_text(
                280, 628, fill="purple",
                font="Times 89 bold italic",
                text=str(self.totalscore).zfill(7))
            self.indication = self.canvas.create_text(
                270, 690, fill="black",
                font="Times 30 bold ", text="[Press any key]")
        else:
            self.totaltime_onscreen = self.canvas.create_text(
                450, 274, fill="red",
                font="Times 39 bold italic", text=str(self.totaltime).zfill(7))
            self.maxbonus_onscreen = self.canvas.create_text(
                523, 344, fill="red",
                font="Times 39 bold italic", text=str(self.maxbonus).zfill(1))
            self.points_onscreen = self.canvas.create_text(
                450, 412, fill="red",
                font="Times 39 bold italic", text=str(self.points).zfill(7))
            self.rank_onscreen = self.canvas.create_text(
                420, 481, fill="red",
                font="Times 39 bold italic", text=self.rank)
            self.totalscore_onscreen = self.canvas.create_text(
                280, 638, fill="purple",
                font="Times 79 bold italic",
                text=str(self.totalscore).zfill(7))
            self.indication = self.canvas.create_text(
                270, 690, fill="black",
                font="Times 20 bold ", text="[Press any key]")

    def update(self):
        self.stats_update()
        self.canvas.update()

    # scoring mechanism:
    # finalscore = (score + bonus_score + 500*game_life +
    # 325*game_bomb + 120*max_bonus + time_score) * delta_difficulty
    # delta_difficulty: easy = 0.5 normal = 1.0 hard = 1.2 lunatic = 1.5
    # time_score: if less than 90s: +1200
    # if in range (90, 180): +900 if in range(180+): no reward
    # [rank, level, game_total_time,
    # game_life, game_bomb, score, bonus_score, max_bonus]
    def stats_process(self):
        delta = 1
        time_score = 0
        print(self.external_data)
        if 0 <= self.external_data[2] <= 90:
            time_score = 1200
        elif 90 < self.external_data[2] <= 180:
            time_score = 900
        elif self.external_data[2] > 180:
            time_score = 0
        if self.external_data[1] == "Easy   ":
            delta = 0.5
        elif self.external_data[1] == "Normal ":
            delta = 1.0
        elif self.external_data[1] == "Hard   ":
            delta = 1.2
        elif self.external_data[1] == "Lunatic":
            delta = 1.5
        self.totalscore = delta * (self.external_data[5] +
                                   self.external_data[6] +
                                   500 * self.external_data[3] +
                                   325 * self.external_data[4] +
                                   120 * self.external_data[7] + time_score)
        self.totaltime = self.external_data[2]*10
        self.maxbonus = self.external_data[7]
        self.points = self.external_data[5]
        self.rank = self.external_data[0]
        self.level = self.external_data[1]

    def stats_update(self):
        pass

    @staticmethod
    def extpause(arg):
        global ispause
        if arg == 0:
            ispause = True
        elif arg == 1:
            ispause = False

    def jump(self, event):
        if self.external_data[1] == "Stage 1":
            # globe.window.switch(stats_scene, [rank, totalscore])
            print("[console]now switch to stage 2")
            globe.window.switch(game_scene, [0, self.totalscore, 254, 1])
        elif self.external_data[1] == "Stage 2":
            print("[console]now switch to stage 3")
            globe.window.switch(game_scene, [0, self.totalscore, 253, 1])
        elif self.external_data[1] == "Stage 3" or \
                (self.external_data[1] != "Stage 3" and
                 self.external_data[8] == 1):
            print("[console]switch to hiscore for reg.")
            globe.window.switch(
                reg_scene, [self.totalscore, self.rank, self.level, 1])
        elif event.keysym == 'b':
            globe.window.switch(emergency_scene, 3, extdata)
