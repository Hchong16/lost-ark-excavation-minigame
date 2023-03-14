from pyautogui import screenshot, keyUp, keyDown
from matplotlib import pyplot  as plt
from keyboard import is_pressed
from time import sleep
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
    sleep(0.5)
    bar = screenshot('bar.png', region=(740, 720, 430, 20))
    bar_rgb = np.array(bar)
    bar_gray = cv2.cvtColor(bar_rgb, cv2.COLOR_BGR2GRAY)

    _, bar_bw = cv2.threshold(bar_gray, 95, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bar_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    targets = []
    for target in contours:
        if cv2.contourArea(target) >= 100:
            M = cv2.moments(target) # Middle x coord of target
            targets.append(int(M['m10']/M['m00']))

    targets.sort()

    times = []
    curr, prev = None, None
    for idx, target in enumerate(targets):
        curr = target

        if idx == 0:
            prev = curr
            times.append(curr/214)
        else:
            times.append((curr - prev)/214)
            prev = curr

        # print("idx: {}, curr: {}, prev: {}, time: {}".format(idx, curr, prev, times[-1]))

    assert len(times) == 3
    return times

counter = 3
targets = []
skip_first = True
while is_pressed('q') == False:
    # To optimize speed, extract specific parts of the screen. The following
    # assumes the program is on a 1080p + fullscreen application. 

    # Must have minigame difficulty 2+ decreased shovel.
    im = screenshot(region=(880, 775, 150, 90))
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    normal_res = cv2.matchTemplate(img_gray, normal_spacebar, cv2.TM_CCOEFF_NORMED)
    glow_res = cv2.matchTemplate(img_gray, glow_spacebar, cv2.TM_CCOEFF_NORMED)

    _, n_confidence, _, max_loc = cv2.minMaxLoc(normal_res)
    _, g_confidence, _, max_loc = cv2.minMaxLoc(glow_res)

    if n_confidence >= 0.8 or g_confidence >= 0.8:
        if not targets: 
            targets = search_targets()
        print(targets)
        sleep(2.80) # Config value?
        print("ARROW MOVED")

        sleep(targets[0])
        automate_space()
 
        sleep(targets[1])
        automate_space()

        sleep(targets[2])
        automate_space()
        
        







    else:
        counter = 3
        targets = []
        skip_first = True
