import win32api, win32gui
import pyautogui

class Model:

    def __init__(self):
        self.hwnd = 0
        self.hwnds_list = list() # window list
        self.inner_hwnds_list = list() # self.window 的 inner window list
        self.inner_hwnds_dict = dict()
        self.window = '' # 選哪個window
        self.is_window_exist = 0

        self.get_all_windows()
        


    def combobox_content(self):
        if self.is_window_exist == 0:
            content = self.hwnds_list
            self.is_window_exist = 1
        else:
            content = self.inner_hwnds_list
        
        return content

    
    def combobox_click(self, title):
        self.window = title
        self.get_hwnd(self.window)
        self.get_inner_windows(self.hwnd)
        if self.window != '':
            return title
        else:
            self.window = title
            return title


    def get_all_windows(self):
        '''
        Return all hwnds
        '''
        all_hwnds_dict = dict()
        hwnds_dict = dict()
        hwnds_list = list()
        def get_all_title(hwnd, mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                all_hwnds_dict.update({hwnd:win32gui.GetWindowText(hwnd)})
        mouse = 0
        win32gui.EnumWindows(get_all_title,mouse)

        for hwnd, title in all_hwnds_dict.items():
            if title != "":
                hwnds_list.append([hwnd, title])
                hwnds_dict.update({hwnd: title})

        self.hwnds_list = hwnds_list
        self.hwnds_dict = hwnds_dict


    def get_inner_windows(self, hwnd):
        '''
        Return all inner hwnds
        '''
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                hwnds[win32gui.GetClassName(hwnd)] = hwnd
            return True
        hwnds_dict = dict()
        hwnds_list = list()
        win32gui.EnumChildWindows(hwnd, callback, hwnds_dict)

        for title, hwnd in hwnds_dict.items():
            hwnds_list.append([hwnd, title])
        
        if hwnds_list == []:
            self.inner_hwnds_list = [[self.hwnd, self.window]]
        else:
            self.inner_hwnds_list = hwnds_list
            self.inner_hwnds_dict = hwnds_dict


    def get_hwnd(self, window_name):
        '''
        Use window name get it's hwnd
        '''
        self.hwnd = win32gui.FindWindow(None, window_name)


    def positionInWindow(self, hwnd):
        '''
        Get the position in specific window
        '''
        tempt = win32api.GetCursorPos()
        if hwnd == 0:
            windowRec = [0, 0]
        else:
            windowRec = win32gui.GetWindowRect(hwnd)

        x = tempt[0] - windowRec[0]
        y = tempt[1] - windowRec[1]
        print(self.hwnd, hwnd)
        return [x, y]

    
    def get_inner_hwnd(self, inner_window_name):
        '''
        Use inner window name gwt it's hwnd
        '''
        if inner_window_name == self.window or inner_window_name == '':
            hwnd = self.hwnd
        else:
            hwnd = self.inner_hwnds_dict[inner_window_name]
        return hwnd


    def get_color(self):
        x = win32api.GetCursorPos()[0]
        y = win32api.GetCursorPos()[1]
        rgb = pyautogui.screenshot().getpixel((x, y))
        r = int(str(rgb[0]).rjust(3))
        g = int(str(rgb[1]).rjust(3))
        b = int(str(rgb[2]).rjust(3))
        # hex_c = rgb2hex(int(r), int(g), int(b))
        return [r, g, b]


