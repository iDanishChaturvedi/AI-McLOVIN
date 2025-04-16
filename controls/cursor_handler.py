import pyautogui as gui
import time

SPEED_MAP = {
    "slightly": 50,
    "normal": 100,
    "fast": 200
}
def move_cursor(direction, speed="normal"):
    step = SPEED_MAP.get(speed, 100)

    if direction == "up":
        gui.moveRel(0, -step)
    elif direction == "down":
        gui.moveRel(0, step)
    elif direction == "left":
        gui.moveRel(-step, 0)
    elif direction == "right":
        gui.moveRel(step, 0)
