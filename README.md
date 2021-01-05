# [Fanmade Version] Touhou REIIDEN: The Highly Responsive To Prayers

This game was made by `10675461 Yi Lu` as `COMP16321-CourseWork_02`. The README file works as a manual that explains how to play the game, code structure and other crucial information. 

<br>

## 0. Rubic Self-Check  

|Objectives|Self-Check|
|:-|:-|
|The use of images|Heavily used inside every scene|
|The use of shapes|draw lines for init animation. (yellow flashing lines)|
|The use of text|The score and the information of in-game HUD are all rendered as text. |
|A Scoring Machanism|See README-5: Scoring Machamism|
|A leader board|See Init Scene - HiScore in game|
|Screen Resolution|`1280x720`, no fullscreen needed|
|The movement of objects|Complete movement of Yingyang Orb and amulets|
|The ability to move an object|Full control of Reimu and Yingyang Orb|
|Some form of collision detection| Complete Collision detection between Reimu-Yingyang Orb, Reimu-Bullets, Yingyang Orb-Amulets, Yingyang Orb-tiles, Yingyang Orb-Bullets|
|In Game Pause / Return|See README-4: PauseScreen|
|Customization|See README-4: Options|
|Special Cheat Codes|See README-2- `c` Key|
|Save/Load Game Feature|See README-4: Continue|
|Boss key|See README-4: Boss Key/README-2-`b` Key|

<br>

## 1. Basic Q & A
- The game is a fan remade version of `Touhou 1: REIIDEN(東方靈異傳) ~ The Highly Responsive To Prayers` :   [WikiPedia](https://zh.wikipedia.org/wiki/東方靈異傳_～_Highly_Responsive_to_Prayers.)
- What is Touhou Project? See [Here](https://en.wikipedia.org/wiki/Touhou_Project)
- About Copyright issues? See [東方Projectの版権を利用する際のガイドライン 2011年版](https://kourindou.exblog.jp/14218252/)
- How to start the game? Locate to the folder where `main.py` stays in Terminal, then execute it using `Python 3`.
- Preferred resulution? `1280*720`, no fullscreen needed. 
- How to play? See README-4-2: GameScreen 
- Too difficult? try `Easy` Rank
- All code was written independently by `10675461 Yi Lu` following `PEP8` Standard, most of the spritesheet was wripped from the original game. 
- All game interface was designed by `10675461 Yi Lu`. However, some bg images was wripped from the original game: 

  1. GameOver/Stats Screen's bg was wripped from the original game's Stats Screen
  2. Reimu's image in GameOver Screen was wripped from the original game's ending screen
  3. Reimu's image in Stats Screen was wripped from the init screen at `Touhou 3: 東方夢時空 ~ Phantasmagoria of Dim. Dream`
  4. The lovely icon was wripped from the original game's Ending Screen. ('DDL' stands for 'Deadline')
- Init Screen and Register Screen Interface design was inspried by the original game. Other game screen designs was made independently by `10675461 Yi Lu`. 
- Abandoned Complex Sprite animations for lack of time
- Abandoned Boss Fight and different types of tiles for lack of time
- Abandoned smooth screen-transioning animation for the image processing limitation
- Abandoned all musical functions due to the Python library using limitation


<br>

## 2. Attentions

For best playing experience, plese use `macOS 10.15 Catalina` for playing the game. Linux and Windows 10 is OK, but due to the limit of Tkinter, Reg Screen's submit button may have incorrect style. (See README-8-3)

<center>

**DO NOT USE BUGGY OS such as macOS BigSur or retro OS like Windows 7!
tkinter may NOT be able to running properly on that OS!**

</center>

<br>

Although key swapping (or key binding customization) is implemented,  It's NOT recommended to customize them: 

**The custom key-events interceptor function is optimized for arrow keys ONLY. If you use other keys to control the character's movement, it may not be able to move smoothly!**


Some key bindings are fixed in case of conflictions:
- `b`   is FIXED for Boss key function
- `c`   is FIXED as cheatcode (cheat button)
- `Esc` is FIXED as pause/exit
- `z`   is FIXED as confirmation in some screens (such as menu screen)
- `Up/Down` is FIXED for menu selection moving

If you really want to customize key bindings, AVOID these keys!

Due to the line width limit of `PEP8`, some parts of the code must be breaked into several lines in order to meet the standard. However, it made the code unreadable for humen. Therefore, I prepared a human-friendly version which has no irritating line-breaks, in the directory `/Game-1280*720(no line length limit)/`. 
 
 
<br>

## 3. Game Goal

You need to control Reimu, the only playable character, using shovel action, Gohei waving or amulets firing to adjust Yingyang Orb's moving pattern, control it to destroy all tiles, and avoid being knocked by the orb or get shot by random bullets if time remaining exceeds. 

Like the original game, I implemented Yingyang Orb's movement with physical emulation. It means it has bouncing effects, and you need to make full use of it.

The amulets shot by Reimu can affect Yingyang Orb's movement: If the amulet shot the orb at one side, the orb will move to the opposite side; if the orb was shot at the bottom center, the orb will stop moving left / right. 

<br>

## 4. Operation Instructions (How to play)

### 1. Init Screen
The initial screen will be displayed with several lines flashing. It is an attempt to remake original game's init animation, using tkinter's `scene.create_line` method. After the animation, you can press any key to pass the welcome screen. The init screen is displayed as below:

![20201129134636](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129134636.png)

In this screen, you use `Up/Down` to move the cursor, use `z` for confirmation. 
The default cursor location is at `START`. 

<BR>

### 2. Game Screen
![20201129130057](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129130057.png)

Under Game Screen presented as above:
- Move Reimu (the playable character) = `Left / Right` key
- Shoot Amulets = `z` key
- Waving Gohei = stay still & button `x` (it can drive both the orb and the bullet near you away. )
- Activate shovel = keep pressing `Left / Right` key, and press key `x`
- Fire bomb = `Left_Shift`
- Cheat = `c` key, reset Lives and Bombs to maximum

The context in the red box is the Game Screen. <br>
HUD information below the Game Screen indicates current rank (`Easy`) and current stage (`Stage 1`). <br>
The HUD information at the right side is:<br>
- HiScore: overall HiScore, read from the record file<br>
- Score: your current non-bonus score
- Player: The number of remaining lives
- Bomb: The number of remaining bombs
- Bonus: The bonus score 
- Time Remain: Your remaining time before entering bulletrain

When the remaining time count down to 0, the digits will be changed to red  bullets rain time. After the countdown, the bulletrain will end, and your time remain will be initialized, bulletrain will stop. 


![20201129135803](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129135803.png)

<br>

### 3. Pause Screen
![20201129133621](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129133621.png)

You can press `Esc` key at the Game Screen to pause. Use `Up/Down` to move the cursor, use `z` for confirmation. 

<br>

### 4. Stats Screen
![20201129133421](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129133421.png)

The stat screen / Gameover Screen shows the statistic information. The Gameover screen is shown as below:

<br>

![20201129133846](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129133846.png)

### 5. Reg Screen
After clearing all 3 stages or game over, you are redirected to the registration Screen:

<br>

![20201129133953](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129133953.png)

In this screen, press any key outside the entry box will pass this screen. Therefore, you need to use mouse to click the entry box and the button. <br>
Notice:
- only top 4 records will be displayed
- The entry box only accept 4 characters. Any exceeding character will be ignored.
- the entry box will only appear under circumstances that needs registration. If you access HiScore option from the init menu, you will only see HiScore, with no entry box or button, just like the screenshot below:
- only by clicking `Esc` key will you pass the scene. 

![20201129134321](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129134321.png)

<br>

### 6. Options Screen
Under Options Screen, you can customize several core key bindings, and the rank of the game: 


![20201129135123](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129135123.png)

This screen is also a full cursor-controlled screen. 

<br>

### 7. Continue Screen
The continue logic is implemented as follow: 
- continue data is stored at `./asset/data/continue_data.json`. It is modified everytime the Pause Screen is called, and current data being stored into it. 
- The Continue Data include Last-time Rank, stage, score, bonus_score and tiledata, time counter will be initialized. You can see it as a fault, or a cheating feature (;;;^_^)
- Only in two circumstances will it be reset to default:
  1. Game Over
  2. All 3 stages completed, Game Finished 

<br>

### 8. Emergency Screen (Implemented for Boss Key)
simplly displays a static screenshot, press `b` (Boss Key) to return to the last scene. 

![20201129145352](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129145352.png)

<br>

## 5. Scoring Mechanism
There are several factors which affect the overall score: 

The scoring mechanism is displayed as below:

    # finalscore = (score + bonus_score + 500*game_life + 325*game_bomb + 120*max_bonus + time_score) * delta_difficulty
    # delta_difficulty: easy = 0.5 normal = 1.0 hard = 1.2 lunatic = 1.5
    # time_score: if less than 90s: +1200 if in range (90, 180): +900 if in range(180+): no reward

The amount of the tiles that Yingyang Orb hits without a single bouncing from the ground is recorded as bonus number, which will be initialized to `0` if the orb bounced to ground. the game will calculate the overall maximum bonus number as max_bonus. The score you get when hitting a tile is recorded as 120 + 120*(bonus_number-1). 

Also, the total time you spend on each stage, life_left and bomb_left will also affect your overall score. 


Therefore, to achieve higher score, you need to:
- try more difficult levels
- try to keep the orb from hitting the ground to get bigger bonus number
- avoid overuse bomb and lives
- avoid being hit by bullets or the orb
- avoid playing in each stage for too long time



<br>

## 6. Rank Control
The different ranks differs in the speed of bulletrain, the number of rained bullets, the bulletrain time and remaining time-threshould. 

The rank was set to `Hard` by default. However, I personally recommend beginners to choose `Easy` Rank to avoid frustrations. 

<br>

## 7. Game structure
The Game is implemented using Scene-Switching framework. All different game scenes are independent (`./scene`), and the method for scene switching is defined inside `main.py`.  data-switching is implemented by using Json file R/W and global Data passing (`globe.py`).

Due to the scale of the project and Tkinter's lack of advanced sprite control, the use of complex animations / spritesheets are avoided in this project. Therefore, there's no need to build resource manager, all image reading are done by different scenes. 

<br>

## 8. Problem explainations
Tkinter is not suitable for building dynamic games due to its event-driving design. To make the game running smoothly, There are several problem we must overcome:

1. Key Repeating Problem<br>
    Modern Operating Systems will interpret continuous key press as high frequency key press & key releases. It will cause laggy playable character moving, therefore must be amended by implementing custom function which reinterprete system events. 

    When the function detected continuous key press and key releases, it will intercept the event reporting: 
    - case1: check key-release <br>
        After it receive a key-release signal, it fire up a timer, and check if there is any corresponding key press event during that time. If not, it will report key-release event. This prevent key-release reporting corruption due to key-repeat issue.
    - case2: check key-press<br>
        With the implementation of key-release checking, we just need to pass key-press event without any checkings.

<br>

2. Refreshing Problem<br>
   In an event-driven framework like Tkinter, we can use two ways to achieve auto screen refreshing:
   - `.after` method: <br>
   use `.after` method to assign specific time delay to specific screen-refresh (update) functions. It is easy to pause, simple to set different framerate (by controlling the time delay), usually implemented with MVC, but need to write very complicated logic for scene switching and key detection. 
   - Using `While loop`: <br>
        put updating functon inside a `While` loop. It's not an officially recommended method, but it's the best way to achieve proper scene-swtching without using `MVC`.  By using `.after` inside the loop. We can also control the refreshing framerate, but to pause the program, we need to set specific pause flags for different updating functions. Also, we need to be very careful of the refreshing function executing order when switching scenes in case of crashing due to the function tries to update a canvas/object that is destoryed by the pause process. 

3. Performance Problem<br>
   Tkinter does not support high-performance sprite drawing & updating, `canvas.create_image` and `canvas.remove()` method eat up too much CPU power, and will drastically slow down the framerate when being used for too many times during one update process. There are three main ways to solve this problem:
   - Reduce the amount of calling these two methods in one iteration
   - Limit the number it is called in one time period by limiting framerate
   - Try to use built-in figure rendering function with `canvas.move` method instead
    

<br>

4. Button style problem<br>

   Tkinter's button style is NOT cross-plaformed. Make different design for different platform is the only way under the limitation of coursework instructions. 

   ![20201129143238](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129143238.png)

   <center>(left: WSL right: Windows Native, running the exact same program, partially amended)</center>

    <br>

    ![20201129151624](https://cdn.jsdelivr.net/gh/KirisameMarisaa/KirisameMarisaa.github.io/img/blogpost_images/20201129151624.png)
    <center>(The problematic button rendering under Windows)</center>

    If you use Windows to run this program and noticed this problem, do not blame me! The same program runs with barely no problem on Linux and macOS, blame Tkinter and Windows instead. 
