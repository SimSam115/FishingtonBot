import time
from PIL import Image
from lib.helpers import *
from lib.gameWindow import *

import pyautogui as pauto


def main():
    gameCon = GameWindow()

    total = 0; count = 0;
    last_phase = Phases.START
    while gameCon.active:
        if last_phase != gameCon.phase:
            last_phase = gameCon.phase
            print(last_phase)

        if gameCon.phase == Phases.START:
            #todo: move to location
            gameCon.cast()

        if gameCon.phase == Phases.CASTING:

            alertArea = pauto.screenshot(region=gameCon.getArea(Phases.C_AREA))
            time.sleep(0.001)
            if canPull(alertArea):
                pauto.leftClick()
                gameCon.phase = Phases.REELING
                time.sleep(0.2)

        if gameCon.phase == Phases.REELING:
            gameCon.fishingProcess()

        if gameCon.phase == Phases.FULL_BASKET:
            pauto.keyDown('w')
            time.sleep(0.6)
            pauto.keyUp('w')

            total += count
            gameCon.sellAllFish()
            count = 0

            pauto.keyDown('s')
            time.sleep(1)
            pauto.keyUp('s')
            gameCon.phase = Phases.START

    print(total)





main()