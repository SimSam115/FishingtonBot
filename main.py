import time
from PIL import Image
from lib.helpers import *
from lib.gameWindow import *

import pyautogui as pauto


def main():
    gameCon = GameWindow()
    gameCon.setFishCount()
    print(gameCon)
    castTime = 0

    while gameCon.active:

        if gameCon.phase == Phases.START:
            #todo: move to location
            gameCon.cast()
            castTime = 0

        if gameCon.phase == Phases.CASTING:
            gameCon.setFishCount()
            alertArea = pauto.screenshot(region=gameCon.getArea(Phases.C_AREA))
            time.sleep(0.001)
            castTime += 1
            if canPull(alertArea):
                pauto.leftClick()
                gameCon.phase = Phases.REELING
                time.sleep(0.2)
            if castTime > 200:
                gameCon.cast()

        if gameCon.phase == Phases.REELING:
            gameCon.fishingProcess()

        if gameCon.phase == Phases.FULL_BASKET:
            pauto.keyDown('w')
            time.sleep(0.6)
            pauto.keyUp('w')
            gameCon.sellAllFish()
            pauto.keyDown('s')
            time.sleep(1)
            pauto.keyUp('s')
            gameCon.phase = Phases.START
        print(gameCon)





main()