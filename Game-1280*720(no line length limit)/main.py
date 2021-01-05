from tkinter import *
import tkinter
# import scene.scene_game as game_scene
import scene.scene_init as init_scene
import globe
import time


class MainWindow:
    """
    SUMMARY:
        The main game window, for carrying all different scenes

    Attributes:
        self.window             Define tkinter window objecct
        self.window.title       Set the title of the window
        self.activescene        Initialize the scene which is updated & displayed inside the window
        self.stack              Initialize the scene stack for rapid scene switching
    """

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title(
            "東方靈異伝 ～ Highly Responsive to Prayers [FanMade Version]")
        self.window.resizable(0, 0)
        self.window.iconphoto(True, PhotoImage(file="asset/icon.gif"))
        self.window.configure(background='black')

        self.activescene = None
        self.stack = []

    def coldstart(self, scene):
        """
        DESCRIPTION:
            start one specific scene inside the window for the first time

        Args:
            scene: The scene to be started

        Return:
            None
        """
        self.stack.append(scene)
        self.activescene = scene
        self.activescene.extpause(1)

    def switch(self, scene, arg=None, arg1=None):
        """
        DESCRIPTION:
            switch from one scene to another. WARNING: Will kill old one,
            save all relevent states before switching


        Args:
            scene: The destination scene to be switched to
            arg: conditional data passing
            arg1: conditional data passing
        """
        self.activescene.extpause(0)            # Pause the current scene
        self.stack.append(scene)  # Append destination scene into the stack
        # Remove all objects on the canvas, do NOT preserve states
        self.activescene.canvas.destroy()

        # Set activescene to destionation scene
        self.activescene = scene.Scene(self.window, arg, arg1)
        time.sleep(0.1)
        self.activescene.extpause(1)

    def run(self):
        """
        DESCRIPTION:
            run the main window framework

        Args:
            /
        """
        self.coldstart(init_scene.Scene(self.window, None))   # coldstart init scene

        while True:        # go into while loop for scene updates
            self.activescene.update()

    @staticmethod
    def kill():
        """
        DESCRIPTION:
            kill the program

        Args:
            /
        """
        globe.window.window.destroy()


globe.ispause = False
# Instanciate MainWindow class, set & initialize window
globe.window = MainWindow()
globe.window.run()         # Call function run(), start running init_scene
globe.window.window.mainloop()             # tkinter mainloop
