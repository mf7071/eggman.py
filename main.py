from eggman import EggMan
from menu import Menu
from pynput.keyboard import Listener, Key
import os

# sometimes exit is not working, just repeat it until it works
menu = Menu('EggMan', ['Start', 'Exit'])
listener: Listener
print(menu.view(0))


def on_release(key):
    if key == Key.up:
        print(menu.up())
    elif key == Key.down:
        print(menu.down())
    elif key == Key.space:
        if menu.selected == 0:
            listener.stop()
        elif menu.selected == 1:
            os._exit(0)


with Listener(on_release=on_release) as listener2:
    listener = listener2
    listener.join()
egg = EggMan(30)  # 30 = Camera Width
egg.start()
