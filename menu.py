import os


class Menu:

    menu: list
    selected: int
    padding: str
    title: str

    def __init__(self, title: str, menu: list = [], padding: int = 8):
        self.title = title
        self.menu = menu
        self.selected = 0
        self.padding = ' ' * padding

    def add(self, title: str):
        self.menu.append(title)

    def view(self, selected: int) -> str:
        os.system('cls')
        output = f'-- {self.title} {"-" * (len(self.padding)*2-len(self.title))}\n'
        for index, item in enumerate(self.menu):
            if index == selected:
                output += f'{self.padding[:-3]}-> {item}\n'  # i know
                continue
            output += f'{self.padding}{item}\n'  # :D
        return output

    def up(self) -> str:
        if self.selected != 0:
            self.selected -= 1
        return self.view(self.selected)

    def down(self) -> str:
        if self.selected != len(self.menu) - 1:
            self.selected += 1
        return self.view(self.selected)
