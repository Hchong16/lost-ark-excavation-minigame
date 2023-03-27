import cv2 as cv2
import mss as mss
import numpy as np
from configparser import ConfigParser
from keyboard import is_pressed
from matplotlib import pyplot  as plt
from pyautogui import keyUp, keyDown
from time import sleep

config = ConfigParser()
config.read('config.ini')

starting_delay_seconds = float(config["DEFAULT"]['starting_delay_seconds'])
arrow_middle_offset = float(config["DEFAULT"]['arrow_middle_offset'])
target_range_left_offset = float(config["DEFAULT"]['target_range_left_offset'])
target_range_right_offset = float(config["DEFAULT"]['target_range_right_offset'])

MINIGAME_ARROW = cv2.imread("./assets/minigame_arrow.png", 0)
NORMAL_SACEBAR = cv2.imread("./assets/normal_spacebar.png", 0)
GLOW_SPACEBAR = cv2.imread("./assets/glow_spacebar.png", 0)

print("""
██      ██████  ███████ ████████      █████  ██████  ██   ██ 
██     ██    ██ ██         ██        ██   ██ ██   ██ ██  ██  
██     ██    ██ ███████    ██        ███████ ██████  █████   
██     ██    ██      ██    ██        ██   ██ ██   ██ ██  ██  
███████ ██████  ███████    ██        ██   ██ ██   ██ ██   ██                                                                                                                                                
""")
print("Program has started... looking for excavation minigames. Press the '=' key to quit anytime!")

def automate_space() -> None:
    keyDown('space')
    sleep(0.1)
    keyUp('space')

def search_targets() -> list:
    """
    Search for the target zones within the excavation bar by returning the x-ranges
    for each individual zones. Add offsets to account for latency between the program and
    the game. 
    """
    excavation_bar_rgb = np.array(sct.grab({"left": 725, "top": 720, "width": 450, "height": 20}))
    excavation_bar_gray = cv2.cvtColor(excavation_bar_rgb, cv2.COLOR_BGR2GRAY)

    _, bar_bw = cv2.threshold(excavation_bar_gray, 70, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bar_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    targets = []
    for target in contours:
        if cv2.contourArea(target) >= 100:
            M = cv2.moments(target)
            x = int(M['m10']/M['m00'])
            targets.append(
                [
                    x-target_range_left_offset, 
                    x+target_range_right_offset
                ]
            )
    return targets

targets = []
searched = False
while is_pressed('=') == False:
    with mss.mss() as sct:
        spacebar_img_rgb = np.array(sct.grab({"left": 880, "top": 775, "width": 150, "height": 90}))
        spacebar_img_gray = cv2.cvtColor(spacebar_img_rgb, cv2.COLOR_BGR2GRAY)

        # Determine whether the game have started  by searching for the spacebar assets.
        normal_res = cv2.matchTemplate(spacebar_img_gray, NORMAL_SACEBAR, cv2.TM_CCOEFF_NORMED)
        glow_res = cv2.matchTemplate(spacebar_img_gray, GLOW_SPACEBAR, cv2.TM_CCOEFF_NORMED)

        _, n_confidence, _, max_loc = cv2.minMaxLoc(normal_res)
        _, g_confidence, _, max_loc = cv2.minMaxLoc(glow_res)

        if n_confidence >= 0.8 or g_confidence >= 0.8:
            # Let the game load before we do anything
            if not targets:
                sleep(starting_delay_seconds)

            arrow_rgb = np.array(sct.grab({"left": 725, "top": 740, "width": 450, "height": 30}))
            arrow_gray = cv2.cvtColor(arrow_rgb, cv2.COLOR_BGR2GRAY)

            if not searched:
                searched = True
                targets = search_targets()

            arrow_res = cv2.matchTemplate(arrow_gray, MINIGAME_ARROW, cv2.TM_CCOEFF_NORMED)
            _, arrow_confidence, _, arrow_loc = cv2.minMaxLoc(arrow_res)
            if arrow_confidence >= 0.75:
                # Offset to the middle of arrow coordinate.
                location = arrow_loc[0] + arrow_middle_offset
                for idx, target in enumerate(targets):
                    if location <= target[1] and location >= target[0]:
                        targets.remove(targets[idx])
                        automate_space()
                        print("PRESSING SPACE\n")
        else:
            targets = []
            searched = False
