import pyautogui
import time
import sys
from datetime import datetime

pyautogui.FAILSAFE = False
minutes_to_keep_awake = None

SLEEP_INTERVAL = 5

if len(sys.argv) < 2 or sys.argv[1].isalpha() or int(sys.argv[1]) < 1:
    minutes_to_keep_awake = float("inf")
else:
    minutes_to_keep_awake = int(sys.argv[1])

while True:
    x = 0
    while x < (minutes_to_keep_awake * 60):
        time.sleep(SLEEP_INTERVAL)
        x += SLEEP_INTERVAL
        for i in range(0, 200):
            pyautogui.moveTo(0, i * 4)
        pyautogui.moveTo(1, 1)
        for i in range(0, 3):
            pyautogui.press("shift")
        print("Movement made at {}".format(datetime.now().time()))
