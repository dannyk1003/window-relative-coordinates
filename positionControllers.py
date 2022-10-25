from positionModel import  Model
from positionView import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def main(self):
        self.view.main()

    
    def on_combobox_click(self, title):
        result = self.model.combobox_click(title)
        self.model.window = result


    def on_combobox_content(self):
        content = self.model.combobox_content() 
        return content

    
    def on_add_history(self, window):
        hwnd = self.model.get_inner_hwnd(window)
        position = self.model.positionInWindow(hwnd)
        color = self.model.get_color()
        self.view.position = position
        self.view.color = color
