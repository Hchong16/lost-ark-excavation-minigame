from pyautogui import screenshot, keyUp, keyDown
from matplotlib import pyplot  as plt
from keyboard import is_pressed
from time import sleep
import numpy as np
import cv2 as cv2

normal_spacebar = cv2.imread("./asset/normal_spacebar.png", 0)
glow_spacebar = cv2.imread("./asset/glow_spacebar.png", 0)
minigame_arrow = cv2.imread("./asset/minigame_arrow.png", 0)

def automate_space() -> None:
    keyDown('space')
    sleep(0.1)
    keyUp('space')

def search_targets() -> list:
    bar = screenshot("b.png", region=(725, 720, 450, 20))
    bar_rgb = np.array(bar)
    bar_gray = cv2.cvtColor(bar_rgb, cv2.COLOR_BGR2GRAY)

    ret, bar_bw = cv2.threshold(bar_gray, 95, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bar_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # plt.subplot(121),plt.imshow(bar_bw, cmap = 'gray')
    # plt.show()

    targets = []
    for target in contours:
        if cv2.contourArea(target) >= 100:
            M = cv2.moments(target)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                # cy = int(M['m01']/M['m00']) # We don't care about the y-axis
            targets.append([cx-15, cx+15])

    return targets

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
        if not targets and skip_first:
            sleep(1)

        game = screenshot(region=(725, 740, 450, 30))
        game_rgb = np.array(game)
        game_gray = cv2.cvtColor(game_rgb, cv2.COLOR_BGR2GRAY)

        if not targets:
            targets = search_targets()

        arrow_res = cv2.matchTemplate(game_gray, minigame_arrow, cv2.TM_CCOEFF_NORMED)
        _, arrow_confidence, _, arrow_loc = cv2.minMaxLoc(arrow_res)
        if arrow_confidence >= 0.8:
            # Offset middle of arrow to trigger spacebar early. This is to account for delays.
            middle = arrow_loc[0] + 15
            for idx, target in enumerate(targets):
                if middle <= target[1] and middle >= target[0] and counter > 0:
                    targets.remove(targets[idx])
                    automate_space()
                    counter -= 1
                    print("IN RANGE OF: {} ({})".format(target, middle))
                    print("PRESSING SPACE")
    else:
        counter = 3
        targets = []
        skip_first = True
