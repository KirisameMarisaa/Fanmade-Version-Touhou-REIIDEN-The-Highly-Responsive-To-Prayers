# -*- coding:utf-8 -*-
from tkinter import *
from math import *
from random import randrange
import random
import time
import threading
import json
import copy
import platform
import globe
import scene.scene_pause as pause_scene
import scene.scene_stats as stats_scene
import scene.scene_gameover as gameover_scene
import scene.scene_emergency as emergency_scene


# Json-Controlled Variables, initialize for failsafe reason
rank = "Easy   "    # total must be 7 chars
timethreshould = 40
bulletrain_time = 8
bulletrain_density = 9
bulletrain_speed = 10
bullet_freq = 17
last_score = 0
bomb_param = 6
hiscore = 9973810
level = "Stage 1"
tiledata = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
bg_filename = "./asset/bg/stage_1.gif"

# ButtonMap
button_bomb = 'Shift_L'
button_left = 'Left'
button_right = 'Right'
button_shoot = 'z'
button_shovel = 'x'

# In-Game Variables, initialize for fail-safe reason
reimu_status_flag = 0        # 0: stay 1: left 2: right 3:pause
reimu_status_flag_action_past = 0
reimu_status_flag_action = 0    # 0:default 3: shoot 4: shovel 5: bomb
ispause = False
framerate = 18
timeremaining = 0
actiontime = 0
enter_bulletrain_count = 0
game_tiledata = copy.deepcopy(tiledata)

# Global variables for assessing
game_init_time = time.time()    # Calculate total elapsed time
life = 5
bomb = 4
game_life = life    # Calculate life remaining
game_bomb = bomb*5    # Calculate bomb remaining
score = 0                   # calculate normal score
bonus_score = 0                 # calculate bonus score
max_bonus = 0                   # Calculate max_bonus


class Scene:
    """
    SUMMARY:
        Define & Maintain Base Scene (With HUD)
    """

    def __init__(self, thewindow, game_state, arg_1=None):
        self.scene = thewindow
        self.width = 1280
        self.height = 720
        self.size = [self.width, self.height]
        self.image_bg = PhotoImage(file="./asset/bg/game_window_bg.gif")
        self.canvas = Canvas(self.scene, width=self.size[0], height=self.size[1], bd=0, highlightthickness=0)
        self.bg = self.canvas.create_image(self.width / 2, self.height / 2, image=self.image_bg)
        self.canvas.place(x=0, y=0)
        self.gamescene = GameScene(self.canvas, game_state)
        self.canvas_game = self.gamescene.canvas
        self.canvas.create_window(465, 345, window=self.gamescene.canvas)
        self.initime = time.time()
        self.arg1 = arg_1
        # STATISTICS INIT

        self.lifecount = game_life
        self.lifeimage = PhotoImage(file="./asset/interface/life.gif")
        self.bombcount = bomb
        self.bombimage = PhotoImage(file="./asset/interface/bomb.gif")
        if platform.system() == 'Darwin':
            self.HiScore = self.canvas.create_text(1180, 239, fill="white", font="Times 40 italic ", text=str(hiscore).zfill(7))  # init hiscore
            self.score = self.canvas.create_text(1180, 310, fill="white",  font="Times 40 italic", text="0000000")
            self.life_onscreen = list(self.canvas.create_image(1222 - 40*i, 381, image=self.lifeimage) for i in range(4))
            self.bomb_onscreen = list(self.canvas.create_image(1222 - 40*i, 452, image=self.bombimage) for i in range(4))
            self.bonus_onscreen = self.canvas.create_text(1210, 524, fill="white", font="Times 40 italic", text="0000")
            self.remaining = self.canvas.create_text(1180, 595, fill="white", font="Times 40 italic", text="0000000")
            self.rank = self.canvas.create_text(130, 660, fill="white", font="Times 30", text=rank)
            self.level = self.canvas.create_text(790, 660, fill="white", font="Times 30", text=level)
        else:
            self.HiScore = self.canvas.create_text(1180, 239, fill="white", font="Times 30 italic ", text=str(hiscore).zfill(7))
            self.score = self.canvas.create_text(1180, 315, fill="white", font="Times 30 italic", text="0000000")
            self.life_onscreen = list(self.canvas.create_image(1222 - 40 * i, 381, image=self.lifeimage) for i in range(4))
            self.bomb_onscreen = list(self.canvas.create_image(1222 - 40 * i, 452, image=self.bombimage) for i in range(4))
            self.bonus_onscreen = self.canvas.create_text(1210, 524, fill="white", font="Times 30 italic", text="0000")
            self.remaining = self.canvas.create_text(1180, 600, fill="white", font="Times 30 italic", text="0000000")
            self.rank = self.canvas.create_text(130, 660, fill="white", font="Times 30", text=rank)
            self.level = self.canvas.create_text(790, 660, fill="white", font="Times 30", text=level)

    # gamestate: 0-reset&coldstart 1: continue from pause
    # gamestate[1]: prev_score
    # gamestate[2]: 255: stage3 254: stage2 253: stage1

    def update_hud(self):
        """
        DESCRIPTION:
            responsible for updating Game HUD info
        """
        global game_life, game_bomb
        a = time.time()
        if (a - self.initime) > 0.25:
            # HiScore Update
            # Score Update
            global bonus_score
            if platform.system() == 'Darwin':
                self.canvas.delete(self.score)
                self.score = self.canvas.create_text(1180, 310, fill="white", font="Times 40 italic", text=str(score).zfill(7))
                if hiscore <= score:
                    self.canvas.delete(self.HiScore)
                    self.HiScore = self.canvas.create_text(1180, 239, fill="white", font="Times 40 italic", text=str(score).zfill(7))
                # LifeCount Update
                for lives in self.life_onscreen:
                    self.canvas.delete(lives)
                self.life_onscreen = list(self.canvas.create_image(1222 - 40*i, 381, image=self.lifeimage) for i in range(game_life-1))
                # BombCount Update
                for bombs in self.bomb_onscreen:
                    self.canvas.delete(bombs)
                self.bomb_onscreen = list(self.canvas.create_image(1222 - 40*i, 452, image=self.bombimage) for i in range(int(game_bomb/5)))
                # Bonus Update
                self.canvas.delete(self.bonus_onscreen)
                self.bonus_onscreen = self.canvas.create_text(1210, 524, fill="white", font="Times 40 italic", text=str(bonus_score).zfill(4))
                # RemainingTime Update
                self.canvas.delete(self.remaining)
                if self.gamescene.bulletsrain:
                    self.remaining = self.canvas.create_text(1215, 595, fill="red", font="Times 40 italic", text=str(int((bulletrain_time - a + self.gamescene.time_enter_bulletrain)) * 4).zfill(3))
                else:
                    self.remaining = self.canvas.create_text(1180, 595, fill="white", font="Times 40 italic", text=str(timeremaining*4).zfill(7))
                self.initime = a
            else:
                self.canvas.delete(self.score)
                self.score = self.canvas.create_text(1180, 315, fill="white", font="Times 30 italic", text=str(score).zfill(7))
                if hiscore <= score:
                    self.canvas.delete(self.HiScore)
                    self.HiScore = self.canvas.create_text(1180, 239, fill="white", font="Times 30 italic", text=str(score).zfill(7))
                # LifeCount Update
                for lives in self.life_onscreen:
                    self.canvas.delete(lives)
                self.life_onscreen = list(self.canvas.create_image(1222 - 40 * i, 381, image=self.lifeimage) for i in range(game_life - 1))
                # BombCount Update
                for bombs in self.bomb_onscreen:
                    self.canvas.delete(bombs)
                self.bomb_onscreen = list(self.canvas.create_image(1222 - 40 * i, 452, image=self.bombimage) for i in range(int(game_bomb / 5)))
                # Bonus Update
                self.canvas.delete(self.bonus_onscreen)
                self.bonus_onscreen = self.canvas.create_text(1210, 524, fill="white", font="Times 30 italic", text=str(bonus_score).zfill(4))
                # RemainingTime Update
                self.canvas.delete(self.remaining)
                if self.gamescene.bulletsrain:
                    self.remaining = self.canvas.create_text(1215, 600, fill="red", font="Times 30 italic", text=str(int((bulletrain_time - a + self.gamescene.time_enter_bulletrain)) * 4).zfill(3))
                else:
                    self.remaining = self.canvas.create_text(1180, 600, fill="white", font="Times 30 italic", text=str(timeremaining * 4).zfill(7))
                self.initime = a

    def update(self):
        """
        DESCRIPTION:
            responsible for updating all scene elements
        """
        if not ispause:
            self.update_hud()
            self.gamescene.update()
            self.canvas_game.update()
            self.canvas.update()

    @staticmethod
    def extpause(arg):
        global ispause
        if arg == 0:
            ispause = True
        elif arg == 1:
            ispause = False


class GameScene:
    """
    SUMMARY:
        Define and maintain the game scene
    """

    def __init__(self, thewindow, game_state):

        self.load(game_state)
        if platform.system() != 'Linux':
            self.fps = 10
        else:
            self.fps = 15
        self.scene = thewindow
        self.width = 806
        self.height = 564
        self.size = [self.width, self.height]
        self.canvas = Canvas(self.scene, width=self.size[0], height=self.size[1], bd=0, highlightthickness=0)
        self.image_bg = PhotoImage(file=bg_filename)
        self.bg = self.canvas.create_image(self.width/2, self.height/2, image=self.image_bg)
        self.bullet_image = PhotoImage(file="./asset/enemy/bullets.gif")
        self.Iscollide = [0]
        self.orb = YingyangOrb(self.canvas, self.scene, self.size)
        self.reimu = Reimu(self.canvas, self.scene, self.size)
        self.tiles = []
        self.bullets = []
        self.initime = time.time()
        self.initime_bullet = time.time()
        self.collision_time = 0
        self.time_enter_bulletrain = 0
        self.bulletsrain = False
        self.isinitialized = False
        self.isloaded = False
        self.last_bombed_time = 0
        self.game_state = game_state
        self.loadtiles()

    def iscollide(self):
        """
        DESCRIPTION:
            responsible for the collision
            detection between Reimu-Orb, Reimu-Bullets
        """
        global game_life
        past_iscollide = self.Iscollide
        self.Iscollide = [0]
        # determine orb-reimu collision
        if abs(sqrt((self.reimu.pos[0] - self.orb.pos[0]) ** 2 + (self.reimu.pos[1] - self.orb.pos[1]) ** 2)) < 20 and (time.time()-self.collision_time) > 1:
            self.Iscollide[0] = 1
            if past_iscollide[0] != self.Iscollide[0]:
                game_life -= 1
            self.collision_time = time.time()
        else:
            self.Iscollide[0] = 0
        for bullet in self.bullets:
            if abs(bullet.x - self.reimu.pos[0]) < 25 and abs(bullet.y - self.reimu.pos[1]) < 60:
                # determine reimu's bullet-driveaway behaviour
                if reimu_status_flag == 0 and reimu_status_flag_action == 4:
                    bullet.isdriven = 1
                else:
                    # determine formal collision with debouncing
                    if (time.time()-self.collision_time) > 1:
                        self.Iscollide[0] = 1
                        game_life -= 1
                        self.collision_time = time.time()
            # determine the collision between orb and bullets
            if abs(bullet.x - self.orb.pos[0]) < 30 and abs(bullet.y - self.orb.pos[1]) < 60:
                self.canvas.delete(bullet.img)
                self.bullets.remove(bullet)

        if reimu_status_flag != 0 or (reimu_status_flag == 0 and reimu_status_flag_action == 4):
            if 10 <= abs(sqrt((self.reimu.pos[0] - self.orb.pos[0])**2 + (self.reimu.pos[1] - self.orb.pos[1])**2)) <= 100:
                self.Iscollide.append(1)
            else:
                self.Iscollide.append(0)
        else:
            self.Iscollide.append(0)
        return self.Iscollide

    def gamemonitor(self, tileslist):
        """
        DESCRIPTION:
            Monitoring the game, detect if the game is finished or gameover,
            also responsible for controlling random
            bulletrain.

        Args:
            tileslist: pass in tileslist for checking its length,
            as an indication of the game is fininshed or not
        """
        global score, bonus_score, max_bonus, ispause, game_life, bomb_param, game_bomb, game_tiledata
        # gamereset
        if not self.isinitialized and self.game_state[0] == 0:
            reset()
            self.bulletsrain = False
            self.initime = time.time()
            self.initime_bullet = time.time()
            self.reimu.pos = [self.reimu.canvasize[0] * 0.5, self.reimu.canvasize[1] - 32]
            self.orb.pos = [self.orb.canvasize[0] * 0.75, self.orb.canvasize[1] * 0.65]
            starts = [-3, -4, -5, 5, 4, 6, 0]
            random.shuffle(starts)
            self.orb.x = starts[0]  # generate orb's x axis loaction randomly
            self.orb.y = -13.5
            self.bulletsclear()
            self.tiles = []
            self.loadtiles()
            self.isinitialized = True
        # jump to next stage
        if len(tileslist) == 0 and (time.time()-game_init_time) > 1:
            print("[console]game end. total score: " + str(score))
            ispause = True
            game_total_time = int(int(time.time())-game_init_time)
            globe.window.switch(stats_scene, [rank, level, game_total_time, game_life, game_bomb, score, bonus_score, max_bonus, 0, game_tiledata])
        if game_life <= 0:
            print("[console]Used all lives, game over!")
            game_total_time = int(int(time.time()) - game_init_time)
            globe.window.switch(gameover_scene, [rank, level, game_total_time, game_life, game_bomb, score, bonus_score, max_bonus, 1])

        if not ispause:
            if (not self.bulletsrain) and (int(timeremaining) <= 0):
                self.bulletsrain = True
                self.time_enter_bulletrain = time.time()
                self.initime_bullet = self.time_enter_bulletrain
                # now running random bullets
                self.rainbullets(0)
            if self.bulletsrain:
                self.rainbullets(0)
            if not self.bulletsrain:
                self.rainbullets(1)
            self.iscollide()

    def tileupdate(self, orb_position, tileslist):
        """
        DESCRIPTION:
            check whether the tiles are getting hit by the orb or not,
            responsible for orb-tile collision detection
            and tile's flip animation

        Args:
           orb_position: pass in the position of Yingyang Orb
           for checking tile-orb collisions
           tileslist:    pass in the list of the tiles for checking the tiles

        """
        global score, bonus_score, max_bonus, ispause, game_life, bomb_param, game_bomb, game_tiledata
        for tile in tileslist:
            if abs((tile.loc[0] - orb_position[0])**2 + (tile.loc[1] - orb_position[1])**2) < 400:
                # self.canvas.delete(tile.image)
                tile.ishit = 1
                game_tiledata[tile.axis[0]][tile.axis[1]] = 0

                score += 120
                bonus_score += 120 * self.orb.bonus_count
                self.orb.bonus_count += 1
                if self.orb.bonus_count > max_bonus:
                    max_bonus = self.orb.bonus_count
            if tile.ishit == 1 or tile.ishit == 0:
                tile.update_image(self.canvas)
            elif tile.ishit == 2:
                tileslist.remove(tile)

        if reimu_status_flag_action == 5:
            if game_bomb > 0:
                if len(tileslist) > 0:
                    index = random.randrange(len(tileslist))
                    if len(tileslist) > bomb_param:
                        for i in range(int(index/bomb_param)):
                            game_tiledata[tileslist[i].axis[0]][tileslist[i].axis[1]] = 0
                            tileslist.pop(i)
                    else:
                        tileslist = tileslist.pop(index)
                    game_bomb -= 1
                    self.bulletsclear()
        return tileslist

    def rainbullets(self, mode):
        """
        DESCRIPTION:
            responsible for the raining of the bullets,
            and the location update of the bullets
        Args:
            mode: 0 = work in raining state, initialize raining state
                      and restart normal counting
                  1 = work in rain ceasing state, cease the rain

        """
        global timeremaining
        # generate random bullets
        now_time = time.time()
        tmp = now_time
        if mode == 0:
            if int(now_time * 100) % bullet_freq == 0 and self.bulletsrain:
                self.bullets.append(Bullets(self.canvas, 0))
                self.bullets.append(Bullets(self.canvas, 1))
                self.bullets.append(Bullets(self.canvas, 2))
            self.initime_bullet = tmp
            # check if the bullets are gone.
            # if gone, then reset self.initime and self.bulletsrain
            # temprorarily do the following jobs
            if (now_time - self.time_enter_bulletrain - bulletrain_time) >= 0:
                # delete all bullets
                self.bulletsrain = False
                self.initime = time.time()
                timeremaining = timethreshould
        # update random bullets
        for bullet in self.bullets:
            if bullet.isdriven == 0:
                bullet.y += bulletrain_speed
                bullet.x += bullet.direction_x
            else:
                bullet.y -= 3 * bulletrain_speed
                bullet.x -= bullet.direction_x
            self.canvas.delete(bullet.img)
            if 0 <= bullet.y <= self.height and 0 <= bullet.x <= self.width:
                bullet.img = self.canvas.create_image(
                    bullet.x, bullet.y, image=self.bullet_image)
            else:
                self.bullets.remove(bullet)

    def bulletsclear(self):
        """
        DESCRIPTION:
            responsible for clearing all on-screen bullets
            when using bombs or the bulletrain cease

        """
        for bullet in self.bullets:
            self.canvas.delete(bullet.image)
        self.bullets = []

    def update(self):
        """
        DESCRIPTION:
            responsible for updating all on-screen, game-scene related objects
        """
        global timethreshould, timeremaining, ispause
        now = time.time()
        self.gamemonitor(self.tiles)
        if not ispause:
            timeremaining = int(timethreshould - (now-self.initime))
            self.tileupdate(self.orb.pos, self.tiles)
            self.scene.after(self.fps, self.orb.update())
            self.scene.after(self.fps, self.reimu.update(self.iscollide(), self.orb.pos))

    @staticmethod
    def pause():
        """
        DESCRIPTION:
            responsible for flipping the state of flag 'ispause'
        """
        global ispause
        if ispause:
            ispause = False
        else:
            ispause = True

    def loadtiles(self):
        """
        DESCRIPTION:
            responsible for loading tile data from game_tiledata
        """
        for r in range(7):
            for c in range(16):
                if game_tiledata[r][c] == 1:
                    position = [44 + 48*c, 60 + 48*r]
                    axis = [r, c]
                    self.tiles.append(
                        Tiles(self.canvas, self.scene, position, axis))
                else:
                    pass

    @staticmethod
    def load(game_state):
        """
        DESCRIPTION:
            responsible for loading the game state from the
            config file (coldstart) or from the continue data(continue)

        Args:
             game_state: a flag indicate the state of the game:
             0 == coldstart, 1 == revive from pause/continue
        """
        global rank, timethreshould, bulletrain_time, bulletrain_density, bulletrain_speed
        global bullet_freq, bomb_param, hiscore, level, tiledata, bg_filename, score, bonus_score
        global button_left, button_right, button_shoot, button_bomb, button_shovel
        # only load when do clean start
        if game_state[0] == 0 or game_state[0] == 1:
            with open('./asset/data/score.json', 'r') as h:
                score_dict = json.load(h)
            with open('./asset/data/continue_data.json', 'r') as j:
                continue_dict = json.load(j)
            with open('./asset/data/settings.json', 'r') as i:
                settings_dict = json.load(i)
            if game_state[0] == 0:  # only load when do clean start
                # Setting dangerous global variables
                rank = settings_dict[0]["Rank"]
                button_bomb = settings_dict[0]["button_bomb"]
                button_left = settings_dict[0]["button_left"]
                button_right = settings_dict[0]["button_right"]
                button_shoot = settings_dict[0]["button_shoot"]
                button_shovel = settings_dict[0]["button_shovel"]
                with open('./asset/data/stage_config.json', 'r') as g:
                    stage_config_dict = json.load(g)
                    hiscore = int(score_dict[0]["Score"])
                    bg_filename = stage_config_dict[(255 - game_state[2])]["bg_filename"]
                    level = stage_config_dict[(255-game_state[2])]["Stage"]
                    tiledata = copy.deepcopy(eval(stage_config_dict[(255-game_state[2])]["tiledata"]))
                if game_state[2] == 255:
                    score = 0
                else:
                    score += int(game_state[1])

            elif game_state[0] == 1:
                tiledata = copy.deepcopy(eval(continue_dict[0]["Tiledata"]))
                reset()
                rank = settings_dict[0]["Rank"]
                level = continue_dict[0]["Stage"]
                score = int(continue_dict[0]["Score"])
                bonus_score = int(continue_dict[0]["Bonus"])
                with open('./asset/data/stage_config.json', 'r') as g:
                    stage_config_dict = json.load(g)
                    bg_filename = stage_config_dict[(int(level[-1])-1)]["bg_filename"]

            with open('./asset/data/rank_config.json', 'r') as f:
                rank_config_dict = json.load(f)
            if rank == "Easy   ":
                timethreshould = int(rank_config_dict[0]["timethreshould"])
                bulletrain_time = int(rank_config_dict[0]["bulletrain_time"])
                bulletrain_density = int(rank_config_dict[0]["bulletrain_density"])
                bulletrain_speed = int(rank_config_dict[0]["bulletrain_speed"])
                bullet_freq = int(rank_config_dict[0]["bullet_freq"])
                bomb_param = int(rank_config_dict[0]["bomb_param"])
            if rank == "Normal ":
                timethreshould = int(rank_config_dict[1]["timethreshould"])
                bulletrain_time = int(rank_config_dict[1]["bulletrain_time"])
                bulletrain_density = int(rank_config_dict[1]["bulletrain_density"])
                bulletrain_speed = int(rank_config_dict[1]["bulletrain_speed"])
                bullet_freq = int(rank_config_dict[1]["bullet_freq"])
                bomb_param = int(rank_config_dict[1]["bomb_param"])
            if rank == "Hard   ":
                timethreshould = int(rank_config_dict[2]["timethreshould"])
                bulletrain_time = int(rank_config_dict[2]["bulletrain_time"])
                bulletrain_density = int(rank_config_dict[2]["bulletrain_density"])
                bulletrain_speed = int(rank_config_dict[2]["bulletrain_speed"])
                bullet_freq = int(rank_config_dict[2]["bullet_freq"])
                bomb_param = int(rank_config_dict[2]["bomb_param"])
            if rank == "Lunatic":
                timethreshould = int(rank_config_dict[3]["timethreshould"])
                bulletrain_time = int(rank_config_dict[3]["bulletrain_time"])
                bulletrain_density = int(rank_config_dict[3]["bulletrain_density"])
                bulletrain_speed = int(rank_config_dict[3]["bulletrain_speed"])
                bullet_freq = int(rank_config_dict[3]["bullet_freq"])
                bomb_param = int(rank_config_dict[3]["bomb_param"])
        else:
            pass


class KeyTracker:
    """
    SUMMARY:
        Custom Key-event Inteceptor, reprocess
        key-press/release events to avoid key repeat problem
    """
    key = ''
    last_press_time = 0
    last_release_time = 0

    def track(self, key=None):
        self.key = key

    def is_pressed(self):
        return time.time() - self.last_press_time < 0.15

    def report_key_press(self, event):
        global game_bomb, game_life, tiledata
        global reimu_status_flag
        global reimu_status_flag_action
        global reimu_status_flag_action_past
        self.last_press_time = time.time()
        if event.keysym == button_left:
            reimu_status_flag = 1
        elif event.keysym == button_right:
            reimu_status_flag = 2
        elif event.keysym == button_shoot:
            reimu_status_flag_action_past = reimu_status_flag_action
            reimu_status_flag_action = 3
        elif event.keysym == button_shovel:
            global actiontime
            actiontime = time.time()    # dangerous time stamp
            reimu_status_flag_action_past = reimu_status_flag_action
            reimu_status_flag_action = 4
        elif event.keysym == button_bomb:
            reimu_status_flag_action_past = reimu_status_flag_action
            reimu_status_flag_action = 5
        elif event.keysym == 'Escape':
            tiledata = copy.deepcopy(game_tiledata)
            isexit = 1      # is_revive_from_pause indicator
            globe.window.switch(pause_scene, [rank, level, score, bonus_score, isexit, game_tiledata])
        elif event.keysym == 'c':
            game_life = 5
            game_bomb = 25
        elif event.keysym == 'b':
            globe.window.switch(emergency_scene, 2)

    def report_key_release(self, event):
        if event.keysym == button_left or button_right or button_shoot or button_shovel or button_bomb:
            timer = threading.Timer(.15, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        global reimu_status_flag
        global reimu_status_flag_action
        global reimu_status_flag_action_past
        if not self.is_pressed():
            reimu_status_flag = 0
            reimu_status_flag_action_past = reimu_status_flag_action
            reimu_status_flag_action = 0
        self.last_release_time = time.time()


class YingyangOrb(object):
    """
    SUMMARY:
        Define Yingyang Orb , maintain its state update
    """

    def __init__(self, canvas, scene, size):
        self.canvas = canvas
        self.canvasize = size
        self.spritesheet = PhotoImage(file="./asset/orb/orb.gif")
        self.num_sprites = 4
        self.images = [self.subimage(40 * i, 0, 40 * (i + 1), 40) for i in range(self.num_sprites)]
        self.last_img = canvas.create_image(self.canvasize[0] * 0.75, self.canvasize[1]*0.65, image=self.images[0])
        self.lastpos = [0, 0]
        self.pos = self.canvas.coords(self.last_img)
        self.scene = scene
        self.gravity = 0.7
        self.bonus_count = 0
        self.istouchground = False
        starts = [-3, -4, -5, 5, 4, 6, 0]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -13.5
        self.updateimage(0)

    def updateimage(self, sprite):
        """
        DESCRIPTION:
            responsible for updating Yingyang Orb's rolling animation

        Args:
            sprite: the number of current playing sprite animation frame
        """
        self.pos = self.canvas.coords(self.last_img)
        self.canvas.delete(self.last_img)
        self.last_img = self.canvas.create_image(
            self.pos[0], self.pos[1], image=self.images[sprite])
        if not ispause:
            if self.x > 0:
                self.scene.after(80, self.updateimage, (sprite-1) % self.num_sprites)
            elif self.x < 0:
                self.scene.after(80, self.updateimage, (sprite+1) % self.num_sprites)
            else:
                self.scene.after(80, self.updateimage, sprite)
        else:
            self.scene.after(80, self.updateimage, sprite)

    def subimage(self, left, top, right, bottom):
        """
        DESCRIPTION:
            a method for wrapping subimage from a larger image

        Args:
             left, top, right, bottom: indicate the
             axis of the image's corresponding position
        """
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from',
                    left, top, right, bottom, '-to', 0, 0)
        return dst

    def update_amulets(self):
        """
        DESCRIPTION:
            responsile for checking the collision between Yingyang Orb-amulets
        """
        for amulet in globe.window.activescene.gamescene.reimu.amulets:
            if abs(amulet.amupos[1] - self.pos[1]) < 35:
                if 8 <= (self.pos[0] - amulet.amupos[0]) < 35:
                    self.x += 13.5
                    self.y -= 12
                elif 8 <= (amulet.amupos[0] - self.pos[0]) < 35:
                    self.x -= 13.5
                    self.y -= 12
                elif abs(self.pos[0] - amulet.amupos[0]) < 8:
                    self.x = 0
                    self.y -= 5

    def update(self):
        """
        DESCRIPTION:
            responsble fot updating the position of the orb
        """
        self.lastpos = self.pos
        self.update_amulets()
        pos = self.pos
        if abs(self.x) >= 35:
            self.x = self.x/abs(self.x) * 25
        if abs(self.y) >= 45:
            self.y = self.y/abs(self.y) * 45
        self.y += self.gravity
        pos[1] += self.y
        self.pos[0] += self.x
        if pos[1] > (self.canvasize[1] - 25):
            pos[1] = self.canvasize[1] - 25
            self.bonus_count = 0
            self.y = -self.y + 10
            if abs(self.y) < 1.2:
                self.y = 0
        if pos[1] < 0:
            pos[1] = 0
            self.y = 5
        if pos[0] > (self.canvasize[0] - 25):
            pos[0] = self.canvasize[0] - 25
            self.x = -self.x
        if pos[0] < 25:
            pos[0] = 25
            self.x = -self.x
        self.canvas.coords(self.last_img, pos[0], pos[1])


class Reimu(object):
    """
    SUMMARY:
        Define & Maintain Reimu
    """

    def __init__(self, canvas, scene, size):
        self.canvas = canvas
        self.canvasize = size
        self.spritesheet = PhotoImage(file="./asset/reimu/reimu.gif")
        self.goheisheet = PhotoImage(file="./asset/reimu/gohei.gif")
        self.shovelsheet = PhotoImage(file="./asset/reimu/shovel.gif")
        self.images = [self.subimage(64 * i, 0, 64 * (i + 1), 64, self.spritesheet) for i in range(9)]
        self.images_g = [self.subimage(88 * i, 0, 88 * (i + 1), 88, self.goheisheet) for i in range(7)]
        self.images_s = [self.subimage(96 * i, 0, 96 * (i + 1), 64, self.shovelsheet) for i in range(2)]
        self.images_l = [self.images[2], self.images[3]]
        self.images_r = [self.images[7], self.images[6]]
        self.last_img = canvas.create_image(self.canvasize[0]*0.5, self.canvasize[1] - 32, image=self.images[0])
        self.pos = [self.canvasize[0] * 0.5, self.canvasize[1] - 32]
        self.scene = scene
        self.isShovel = False
        self.collide = False
        self.tracker = KeyTracker()
        self.canvas.bind_all('<KeyPress>', self.tracker.report_key_press)
        self.canvas.bind_all('<KeyRelease>', self.tracker.report_key_release)
        self.imgcounter = 0
        self.gohei = 0
        self.amulets = list()
        self.tracker.track()

    @staticmethod
    def subimage(left, top, right, bottom, spritesheet):
        """
                DESCRIPTION:
                    a method for wrapping subimage from a larger image

                Args:
                     left, top, right, bottom:
                     indicate the axis of the image's corresponding position
                """
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', left, top, right, bottom, '-to', 0, 0)
        return dst

    def rapidcreate(self):
        """
        DESCRIPTION:
            a way to create one amulet very fast
        """
        self.amulets.append(Amulet(self.canvas, self.scene, self.pos))

    def update(self, iscollide, orb_pos):
        """
        DESCRIPTION:
            responsible for reimu's location & image updating,
            amulets' updating
        """
        delta = time.time()
        global reimu_status_flag
        if iscollide[0] == 0:
            if reimu_status_flag == 1:  # Left
                self.pos[0] -= 12
                if self.pos[0] <= 22:
                    self.pos[0] = 22
                self.canvas.delete(self.last_img)
                if reimu_status_flag_action == 0 \
                        or reimu_status_flag_action == 3:
                    if self.imgcounter == 0:
                        self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images_l[0])
                        self.imgcounter += 1
                    else:
                        self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images_l[1])
                        self.imgcounter = 0
                    if reimu_status_flag_action == 3 \
                            and reimu_status_flag_action_past != 3:
                        self.rapidcreate()
                elif reimu_status_flag_action == 4:
                    if (delta - actiontime) < 0.8:
                        self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images_s[0])
                        self.imgcounter = 0
                    if iscollide[1] == 1:
                        globe.window.activescene.gamescene.x = -18
                        globe.window.activescene.gamescene.orb.y = -30

            if reimu_status_flag == 2:      # Right
                self.pos[0] += 12
                if self.pos[0] >= self.canvasize[0]-22:
                    self.pos[0] = self.canvasize[0]-22
                self.canvas.delete(self.last_img)
                if reimu_status_flag_action == 0 or reimu_status_flag_action == 3:
                    if self.imgcounter == 0:
                        self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images_r[0])
                        self.imgcounter += 1
                    else:
                        self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images_r[1])
                        self.imgcounter = 0
                    if reimu_status_flag_action == 3 and reimu_status_flag_action_past != 3:
                        self.rapidcreate()
                elif reimu_status_flag_action == 4:
                    if (delta - actiontime) < 0.8:
                        self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images_s[1])
                        self.imgcounter = 0
                    if iscollide[1] == 1:
                        globe.window.activescene.gamescene.orb.x = 18
                        globe.window.activescene.gamescene.orb.y = -30

            elif reimu_status_flag == 0:    # Still
                self.canvas.delete(self.last_img)
                if reimu_status_flag_action == 3 and reimu_status_flag_action_past != 3:
                    self.rapidcreate()
                if reimu_status_flag_action == 4:
                    if iscollide[1] == 1:
                        starts = [[-15, -25], [15, -25]]
                        random.shuffle(starts)
                        globe.window.activescene.gamescene.orb.x = globe.window.activescene.gamescene.orb.x * 0.5 + starts[0][0]
                        globe.window.activescene.gamescene.orb.y = starts[0][1]
                    self.gohei = 1
                if self.gohei:
                    self.last_img = self.canvas.create_image(self.pos[0], self.pos[1]-10, image=self.images_g[self.gohei % 7])
                    self.gohei += 1
                    if self.gohei % 8 == 0:
                        self.gohei = 0
                else:
                    # hit animation?
                    self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images[0])
        else:
            self.canvas.delete(self.last_img)
            self.pos = [self.canvasize[0]/2, self.pos[1]]
            self.last_img = self.canvas.create_image(self.pos[0], self.pos[1], image=self.images[0])
            orb_pos[0] = 403
            orb_pos[1] = 100
        if self.amulets:
            for amulet in self.amulets:
                amulet.update(amulet)


class Amulet(object):
    """
    SUMMARY:
        Define & Maintain Amulet Class
    """

    def __init__(self, canvas, scene, position):
        self.scene = scene
        self.amupos = [position[0], 524]
        self.canvas = canvas
        self.amulimg = PhotoImage(file="./asset/reimu/amulet.gif")
        self.amulimage = canvas.create_image(self.amupos[0], self.amupos[1], image=self.amulimg)
        self.vel = 0

    @staticmethod
    def update(amulet):
        """
        DESCRIPTION:
            responsible for updating the location of the amulets
        """
        amulet.canvas.delete(amulet.amulimage)
        amulet.amupos[1] -= 45
        if amulet.amupos[1] >= 0:
            amulet.amulimage = amulet.canvas.create_image(
                amulet.amupos[0], amulet.amupos[1], image=amulet.amulimg)
        else:
            globe.window.activescene.gamescene.reimu.amulets.remove(amulet)


class Tiles(object):

    """
    SUMMARY:
        Define & Maintain Tile Class
        The num of tiles: 16*7
    """

    def __init__(self, canvas, scene, location, axis):
        self.canvas = canvas
        self.scene = scene
        self.loc = location
        self.axis = axis
        self.images = PhotoImage(file="./asset/enemy/tiles.gif")
        self.image = [self.subimage(0, 40*i, 40, 40 * (i + 1), self.images) for i in range(4)]
        self.lastimage = self.canvas.create_image(location[0], location[1], image=self.image[0])
        self.ishit = 0  # 0: not hit 1: hitting 2: switched
        self.image_index = 0
        self.time = 0

    @staticmethod
    def subimage(left, top, right, bottom, spritesheet):
        """
        DESCRIPTION:
            a method for wrapping subimage from a larger image

        Args:
            left, top, right, bottom:
            indicate the axis of the image's corresponding position
        """
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', left, top, right, bottom, '-to', 0, 0)
        return dst

    def update_image(self, canvas):
        """
        DESCRIPTION:
            responsible for tile destroy animation playing
        """
        now_time = time.time()
        if self.ishit == 0:
            pass
        elif self.ishit == 1 and (now_time - self.time) > 0.3:
            self.time = now_time
            if self.image_index != 3:
                self.image_index += 1
                canvas.delete(self.lastimage)
                self.lastimage = self.canvas.create_image(self.loc[0], self.loc[1], image=self.image[self.image_index])
            else:
                self.ishit = 2


class Bullets(object):
    """
    SUMMARY:
        Define & Maintain Bullets Class
    """

    def __init__(self, canvas, loc):
        self.canvas = canvas
        self.image = PhotoImage(file="./asset/enemy/bullets.gif")
        self.x = 268*loc + randrange(0, 268)
        self.y = 0
        self.direction_x = randrange(-5, 5)
        self.isdriven = 0   # 0: not driven 1: being driven
        self.img = self.canvas.create_image(self.x, self.y, image=self.image)


def reset():
    """
    DESCRIPTION:
        a static method for reseting dangerous global variables
    """
    global reimu_status_flag, reimu_status_flag_action
    global reimu_status_flag_action_past, ispause, timeremaining, actiontime
    global enter_bulletrain_count, game_init_time, game_life
    global game_bomb, score, bonus_score, max_bonus, game_tiledata, last_score
    reimu_status_flag = 0  # 0: stay 1: left 2: right 3:pause
    reimu_status_flag_action_past = 0
    reimu_status_flag_action = 0  # 0:default 3: shoot 4: shovel 5: bomb
    ispause = False
    timeremaining = timethreshould
    actiontime = 0
    enter_bulletrain_count = 0

    # Global variables for assessing
    game_init_time = time.time()  # Calculate total elapsed time
    game_life = life  # Calculate life remaining
    game_bomb = bomb * 5  # Calculate bomb remaining
    bonus_score = 0  # calculate bonus score
    max_bonus = 0  # Calculate max_bonus
    game_tiledata = copy.deepcopy(tiledata)
    last_score = 0
