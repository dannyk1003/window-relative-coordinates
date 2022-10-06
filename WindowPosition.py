import tkinter as tk
from tkinter import END, ttk
import win32api, win32gui, win32ui
import numpy as np


def get_all_windows():
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


    return [hwnds_list, hwnds_dict]


def get_inner_windows(hwnd):
    '''
    Return all inner hwnds
    '''
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)] = hwnd
        return True
    hwnds_dict = {}
    hwnds_list = []
    win32gui.EnumChildWindows(hwnd, callback, hwnds_dict)

    for hwnd, title in hwnds_dict.items():
        hwnds_list.append([hwnd, title])
    return [hwnds_list, hwnds_dict]


def get_hwnd(window_name):
    '''
    Use window name get it's hwnd
    '''
    hwnd = win32gui.FindWindow(None, window_name)
    return hwnd


def get_inner_hwnd(window_name, inner_window_name):
    '''
    Use inner window name gwt it's hwnd
    '''
    hwnd = get_hwnd(window_name)
    hwnd = get_inner_windows(hwnd)[1][inner_window_name]
    return hwnd


def positionInWindow(hwnd):
    '''
    Get the position in specific window
    '''
    tempt = win32api.GetCursorPos()
    windowRec = win32gui.GetWindowRect(hwnd)

    x = tempt[0] - windowRec[0]
    y = tempt[1] - windowRec[1]
    return [x, y]


def positionInScreen():
    tempt = win32api.GetCursorPos()
    x, y = tempt[0], tempt[1]
    return [x, y]


def positionColor(window_name, x, y):
    w = win32ui.FindWindow(None, window_name)
    dc = w.GetWindowDC()
    color = dc.GetPixel(x, y)
    Blue =  color & 255
    Green = (color >> 8) & 255
    Red =   (color >> 16) & 255
    return color


def hwnd_combobox_func(event):
    print(hwnd_combobox.current(), hwnd_combobox_Text.get())
    hwnd_Text.set('the window name is \n' + hwnd_combobox_Text.get())
    inner_hwnd_combobox_list = get_inner_windows(get_hwnd(hwnd_combobox_Text.get()))[0]
    if inner_hwnd_combobox_list == []:
        inner_hwnd_combobox_list = [hwnd_combobox_Text.get()]
    else:
        inner_hwnd_combobox_list = list(np.array(get_inner_windows(get_hwnd(hwnd_combobox_Text.get()))[0])[:,0])
        
    inner_hwnd_combobox['values'] = inner_hwnd_combobox_list


def inner_hwnd_combobox_func(event):
    print(inner_hwnd_combobox.current(), inner_hwnd_combobox_Text.get())
    inner_hwnd_Text.set('the inner window name is \n' + inner_hwnd_combobox_Text.get())


n = 0
def position_func(event):
    global n
    n += 1
    if hwnd_combobox.get() == inner_hwnd_combobox.get():
        position = positionInWindow(get_hwnd(hwnd_combobox_Text.get()))
    else:
        position = positionInWindow(get_inner_hwnd(hwnd_combobox.get(), inner_hwnd_combobox.get()))
    print(f'{n}. {position}')
    position_Text.set(f'position is : {position}, position history as below')
    position_history.configure(state='normal')
    position_history.insert('insert', f'{n}. position : {position} \n')
    position_history.configure(state='disabled')
    

def clear_func(event):
    global n
    n = 0
    position_history.configure(state='normal')
    position_history.delete("1.0",END)
    position_history.configure(state='disabled')



root = tk.Tk()
root.title('my window position detector')
root.geometry('380x500')


# all hwnds combobox
hwnd_combobox_Text = tk.StringVar()
hwnd_combobox = ttk.Combobox(root, textvariable=hwnd_combobox_Text, state='readonly', width=40)
hwnd_combobox['values'] = list(np.array(get_all_windows()[0])[:,1])
hwnd_combobox.grid(row=1, column=1)

hwnd_Text = tk.StringVar()
hwnd_label = tk.Label(root, textvariable=hwnd_Text, font=('Arial', 12), wraplength=400)
hwnd_label.grid(row=2, column=1)


# all inner hwnds combobox
inner_hwnd_combobox_Text = tk.StringVar()
inner_hwnd_combobox = ttk.Combobox(root, textvariable=inner_hwnd_combobox_Text, state='readonly', width=40)
inner_hwnd_combobox.grid(row=3, column=1)

hwnd_combobox.bind("<<ComboboxSelected>>", hwnd_combobox_func)

inner_hwnd_Text = tk.StringVar()
inner_hwnd_label = tk.Label(root, textvariable=inner_hwnd_Text,font=('Arial', 12), wraplength=400)
inner_hwnd_label.grid(row=4, column=1)

inner_hwnd_combobox.bind("<<ComboboxSelected>>", inner_hwnd_combobox_func)


position_title = tk.StringVar()
position_title.set('press ctrl + s to remember, ctrl + z to clear!!')
position_title_label = tk.Label(root, textvariable=position_title, font=('Arial', 12))
position_title_label.grid(row=5, column=1)


# return the position
position_Text = tk.StringVar()
positionlabel = tk.Label(root, textvariable=position_Text,font=('Arial', 12))
positionlabel.grid(row=6, column=1)


root.bind('<Control-s>', position_func)
root.bind('<Control-z>', clear_func)


position_history = tk.Text(root, width=50, height=50)
position_history.grid(row=7, column=1)
position_history.configure(state='disabled')


# main()
root.mainloop()