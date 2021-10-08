import time
from lib.helpers import *

import pygetwindow as pwin
import pyautogui as pauto


class Phases:
    START = 0
    CASTING = 1
    C_AREA  = (600, 400,100,50)
    REELING = 2
    R_AREA  = (415, 830, 490,10)
    FULL_BASKET = 3


class GameWindow:
    S_ALL_BUTTON = (280, 360)
    SELL_BUTTON = (661, 834)
    CONFIRM_SELL_BUTTON = (772, 714)

    def __init__(self):
        self.win = pwin.getWindowsWithTitle("Fishington.io")[0]
        self.win.size = (1300, 1000)
        self.win.activate()
        self.active = True
        self.phase = Phases.START
        self.fish_count = 0
        time.sleep(0.5)

    def cast(self):
        self.phase = Phases.CASTING
        self.fish_count = 0
        pauto.moveTo(x = self.win.left + 600, y = self.win.top + 800)
        pauto.mouseDown()
        time.sleep(1)
        pauto.mouseUp()

    def getArea(self,pArea):
        return self.win.left + pArea[0], self.win.top + pArea[1], pArea[2], pArea[3]

    def click(self,pos):
        pauto.moveTo(self.win.left + pos[0], self.win.top + pos[1])
        pauto.mouseDown()
        time.sleep(0.1)
        pauto.mouseUp()

    def getMousePos(self):
        x,y = pauto.position()
        return x - self.win.left, y - self.win.top

    def sellAllFish(self):
        self.click((682, 338))
        time.sleep(1)
        self.click(self.S_ALL_BUTTON)
        time.sleep(0.2)
        self.click(self.SELL_BUTTON)
        time.sleep(0.2)
        self.click(self.CONFIRM_SELL_BUTTON)
        time.sleep(0.2)
        self.click((661, 900))
        self.fish_count = 0

    def fishingProcess(self):
        screenArea = pauto.screenshot(region=self.getArea(Phases.R_AREA))
        startX, endX, bobbinX, doneFishing = getFishingDetails(screenArea)
        length = endX - startX
        # print(startX, endX, bobbinX, doneFishing)

        if bobbinX != -1:
            if bobbinX < startX + (length / 2):
                pauto.mouseDown()
            if endX - 30 < bobbinX:
                pauto.mouseUp()
            time.sleep(0.1)
        else:
            pauto.mouseUp()

        if doneFishing:
            time.sleep(2.5)
            self.click((835, 625))
            time.sleep(1)
            self.fish_count += 1
            if self.fish_count > 9:
                self.phase = Phases.FULL_BASKET
                self.fish_count = 0
            else:
                self.phase = Phases.START