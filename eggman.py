from pynput.keyboard import Listener, Key
from threading import Thread
import os, time


class EggMan:

    # the world.txt converted into a list
    world: list

    # every hurdle position
    hurdle_position: list

    # you will die if you touch one of them
    hurdle_list: list = ['[', ']', '^']

    # do not change if you don't know what are you doing
    # (this will result to infinite loop)
    floor: str = '='

    is_jumping: bool

    # eggman position, this only hold two values which is [x, y]
    eggman_position: list

    # camera position
    camera_pos: int

    # world visibility distance
    camera_width: int

    # do not modify, this depend on world.txt
    camera_height: int

    # the eggman character, only support single character
    eggman: str = '0'

    friend_positon: list

    def __init__(self, camera_width: int = 15):
        self.world = []
        self.hurdle_position = []
        self.is_jumping = False
        self.camera_pos = 0
        self.camera_width = camera_width
        with open('world.txt', 'r') as file:
            content = file.read().split('\n')
            self.camera_height = len(content) - 2
            self.eggman_position = [5, 0]
            for line_index, line in enumerate(content):
                chars = list(line)
                self.world.append(chars)
                for char_index, char in enumerate(chars):
                    if char in self.hurdle_list:
                        self.hurdle_position.append([char_index, line_index])
                    elif char == self.eggman:
                        self.friend_position = [char_index, line_index]

    def clear(self):
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

    def print_game(self):
        self.clear()
        print(self.game_view())

    def check_lose(self):
        if self.eggman_position in self.hurdle_position:
            print('Game over')
            os._exit(0)

    def check_win(self):
        if self.eggman_position == self.friend_position:
            print('You win!')
            os._exit(0)

    def move(self, key_direction: Key):
        if key_direction == Key.left and self.world[self.eggman_position[1]][self.eggman_position[0] - 1] !=\
                    self.floor:
            if self.eggman_position[0] != 0:
                self.eggman_position[0] -= 1
                if not self.is_jumping:
                    self.fall_down()
                    self.clear()
            if self.camera_pos != 0:
                self.camera_pos -= 1
        elif key_direction == Key.right and self.world[self.eggman_position[1]][self.eggman_position[0] + 1] !=\
                self.floor:
            self.eggman_position[0] += 1
            if self.eggman_position[0] > self.camera_width / 3:
                self.camera_pos += 1
            if not self.is_jumping:
                self.fall_down()
                self.clear()
        elif key_direction == Key.up and not self.is_jumping:
            self.jump(3)
            self.clear()
        else:
            self.print_game()
            return
        self.print_game()
        self.check_lose()

    def jump(self, height: int):
        Thread(target=self.__jump, args=[height]).start()

    def __jump(self, height: int):
        self.is_jumping = True
        for _ in range(height):
            if self.world[self.eggman_position[1] - 1][self.eggman_position[0]] == self.floor:
                break
            self.eggman_position[1] -= 1
            self.print_game()
            self.check_lose()
            self.check_win()
            time.sleep(0.2)
        self.__fall_down()

    def fall_down(self):
        if self.world[self.eggman_position[1] + 1][self.eggman_position[0]] != self.floor:
            Thread(target=self.__fall_down).start()

    def __fall_down(self):
        while self.world[self.eggman_position[1] + 1][self.eggman_position[0]] != self.floor:
            self.eggman_position[1] += 1
            self.print_game()
            self.check_lose()
            time.sleep(0.3)
        self.is_jumping = False

    def start(self):
        self.print_game()
        self.fall_down()
        with Listener(on_press=self.move) as listener:
            listener.join()

    def game_view(self) -> str:
        view = ''
        combined_world = []
        for line in self.world:
            combined_world.append(line[self.camera_pos:self.camera_pos + self.camera_width])
        combined_world[self.eggman_position[1]][self.eggman_position[0] - self.camera_pos] = self.eggman
        for line in combined_world:
            for char in line:
                view += char
            view += '\n'
        return view
