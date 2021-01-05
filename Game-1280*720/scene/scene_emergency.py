# -*- coding:utf-8 -*-
from tkinter import *
import globe
import scene.scene_init as game_init
import scene.scene_game as game_scene
import scene.scene_reg as game_reg
import scene.scene_menu as game_menu
import scene.scene_pause as pause_scene
import scene.scene_stats as stats_scene
import scene.scene_gameover as gameover_scene

ispause = False


class Scene:
    def __init__(self, thewindow, arg, arg1=None):
        """
        SUMMARY:
            Carrying out emergency scene

        ATTRIBUTES:
            self.scene:             pass mainwindow to Emergency Scene
            self.width & height:    fix screen width & height
            self.size:              fix window size
            self.image_bg:          fix window background
            self.canvas:            create a canvas for placing the bg
            self.arg & arg1:        store the passed in arguments:
                                    self.arg store the previous scene
                                    self.arg_1 store the extended info
                                    from the previous scene
        """
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.size = [self.width, self.height]
        self.image_bg = PhotoImage(file="./asset/bg/emergency.gif")
        self.canvas = Canvas(
            self.scene, width=self.size[0],
            height=self.size[1], bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(
            self.width / 2, self.height / 2, image=self.image_bg)
        self.canvas.pack()
        self.canvas.bind_all('<KeyPress>', self.jump)
        self.arg = arg
        self.arg1 = arg1

    def update(self):
        """
        DESCRIPTION:            simplly do updating
        """
        self.canvas.update()

    def jump(self, event):
        """
        DESCRIPTION:
            Event function intercepting key press event. read in self.arg,
            and preform scene-switching:
            0: init 1: menu 2:game 3: stat 4: hiscore 6: pause 7: gameover

        """
        if self.arg == 0:   # go to init
            globe.window.switch(game_init, None)
        if self.arg == 1:
            globe.window.switch(game_menu, None)
        if self.arg == 2:
            globe.window.switch(game_scene, [2, 0, 1])
        if self.arg == 3:
            globe.window.switch(stats_scene, self.arg1, None)
        if self.arg == 4:
            globe.window.switch(game_reg, self.arg1)
        if self.arg == 6:
            globe.window.switch(pause_scene, self.arg1, None)
        if self.arg == 7:
            globe.window.switch(gameover_scene, self.arg1, None)

    @staticmethod
    def extpause(arg):
        global ispause
        if arg == 0:
            ispause = True
        elif arg == 1:
            ispause = False
