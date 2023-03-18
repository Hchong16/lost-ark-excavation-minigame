from pyautogui import screenshot, keyUp, keyDown
from matplotlib import pyplot  as plt
from keyboard import is_pressed
from time import sleep
import mss 
import numpy as np
import cv2 as cv2

normal_spacebar = cv2.imread("./assets/normal_spacebar.png", 0)
glow_spacebar = cv2.imread("./assets/glow_spacebar.png", 0)
minigame_arrow = cv2.imread("./assets/minigame_arrow.png", 0)

def automate_space() -> None:
    keyDown('space')
    sleep(0.1)
    keyUp('space')

def search_targets() -> list:
    bar_rgb = np.array(sct.grab({"left": 725, "top": 720, "width": 450, "height": 20}))
    bar_gray = cv2.cvtColor(bar_rgb, cv2.COLOR_BGR2GRAY)

    _, bar_bw = cv2.threshold(bar_gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bar_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    targets = []
    for target in contours:
        if cv2.contourArea(target) >= 100:
            M = cv2.moments(target)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                # cy = int(M['m01']/M['m00']) # We don't care about the y-axis
            targets.append([cx-5, cx+5])

    return targets

targets = []
while is_pressed('=') == False:
    with mss.mss() as sct:
        # To optimize speed, extract specific parts of the screen. The following
        # assumes the program is on a 1080p + fullscreen application. 

        # Tested with minigame difficulty 2+ decreased shovel.
        img_rgb = np.array(sct.grab({"left": 880, "top": 775, "width": 150, "height": 90}))
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # plt.subplot(111), plt.imshow(img_gray)
        # plt.show()

        normal_res = cv2.matchTemplate(img_gray, normal_spacebar, cv2.TM_CCOEFF_NORMED)
        glow_res = cv2.matchTemplate(img_gray, glow_spacebar, cv2.TM_CCOEFF_NORMED)

        _, n_confidence, _, max_loc = cv2.minMaxLoc(normal_res)
        _, g_confidence, _, max_loc = cv2.minMaxLoc(glow_res)

        if n_confidence >= 0.8 or g_confidence >= 0.8:
            game_rgb = np.array(sct.grab({"left": 725, "top": 740, "width": 450, "height": 30}))
            game_gray = cv2.cvtColor(game_rgb, cv2.COLOR_BGR2GRAY)

            if not targets:
                targets = search_targets()

            arrow_res = cv2.matchTemplate(game_gray, minigame_arrow, cv2.TM_CCOEFF_NORMED)
            _, arrow_confidence, _, arrow_loc = cv2.minMaxLoc(arrow_res)
            if arrow_confidence >= 0.75:
                # Offset middle of arrow to trigger spacebar early. This is to account for delays.
                middle = arrow_loc[0] + 15
                for idx, target in enumerate(targets):
                    if middle <= target[1] and middle >= target[0]:
                        targets.remove(targets[idx])
                        automate_space()
                        print("IN RANGE OF: {} ({})".format(target, middle))
                        print("PRESSING SPACE\n")
        else:
            targets = []
