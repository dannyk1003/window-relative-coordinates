import tkinter as tk
from tkinter import ttk, END
import numpy as np


class View():

    def __init__(self, controller):

        self.controller = controller
        
        self.root = tk.Tk()
        self.PAD = 10
        self.window = ''
        self.windows = list()
        self.inner_windows = list()
        self.inner_window = ''
        self.count = 0
        self.position = [0, 0]
        self.color = [0, 0, 0]

        
        self.root.title('my window position detector')
        self.root.geometry('380x500')

        self._make_main_frame()
        hwnds_list = list(np.array(self.controller.on_combobox_content())[:,1])
        self._make_combobox_and_innerWindows(hwnds_list)
        self._make_textbox()



    def main(self):
        self.root.mainloop()


    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self.root)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD)

    
    def _make_combobox(self, content):

        def combobox_func(event):
            print(combobox.current(), combobox_Text.get())

            label_Text.set(f'the window is : \n {combobox_Text.get()}')
            title = combobox_Text.get()
            self.controller.on_combobox_click(title)
            self.inner_windows = list(np.array(self.controller.on_combobox_content())[:,1])
            print('view:', self.inner_windows)
            self._make_combobox_innerWindow(self.inner_windows)


        frm = ttk.Frame(self.main_frm)
        frm.pack()
        combobox_Text = tk.StringVar()
        combobox = ttk.Combobox(frm, textvariable=combobox_Text, state='readonly')
        # combobox['values'] = list(np.array(self.controller.on_combobox_content())[:,1])
        combobox['values'] = content
        combobox.pack()

        label_Text = tk.StringVar()
        label = tk.Label(frm, textvariable=label_Text, font=('Arial', 12), wraplength=400)

        label.pack()

        combobox.bind("<<ComboboxSelected>>", combobox_func)

    
    def _make_combobox_innerWindow(self, content):

        def combobox_func(event):
            print(combobox.current(), combobox_Text.get())
            label_Text.set(f'the inner window is : \n {combobox_Text.get()}' )
            title = combobox.get()
            self.controller.on_combobox_click(title)


        frm = ttk.Frame(self.main_frm)
        frm.pack()
        combobox_Text = tk.StringVar()
        combobox = ttk.Combobox(frm, textvariable=combobox_Text, state='readonly')
        combobox['values'] = content
        combobox.pack()

        label_Text = tk.StringVar()
        label = tk.Label(frm, textvariable=label_Text, font=('Arial', 12), wraplength=400)
        label.pack()

        combobox.bind("<<ComboboxSelected>>", combobox_func)


    def _make_combobox_and_innerWindows(self, content):
        
        def combobox_func(event):
            print(combobox.current(), combobox_Text.get())
            label_Text.set(f'the window is : \n {combobox_Text.get()}' )
            title = combobox.get()
            self.window = combobox.get()
            self.controller.on_combobox_click(title)
            self.inner_windows = list(np.array(self.controller.on_combobox_content())[:,1])
            inner_combobox['values'] = self.inner_windows


        def inner_combobox_func(event):
            print(inner_combobox.current(), inner_combobox_Text.get())
            inner_label_Text.set(f'the inner window is : \n {inner_combobox_Text.get()}')
            self.inner_window = inner_combobox_Text.get()



        frm = ttk.Frame(self.main_frm)
        frm.pack()
        combobox_Text = tk.StringVar()
        combobox = ttk.Combobox(frm, textvariable=combobox_Text, state='readonly')
        combobox['values'] = content
        combobox.pack()

        label_Text = tk.StringVar()
        label = tk.Label(frm, textvariable=label_Text, font=('Arial', 12), wraplength=400)

        label.pack()

        combobox.bind("<<ComboboxSelected>>", combobox_func)

        
        inner_combobox_Text = tk.StringVar()
        inner_combobox = ttk.Combobox(frm, textvariable=inner_combobox_Text, state='readonly')
        inner_combobox.pack()

        inner_label_Text = tk.StringVar()
        inner_label = tk.Label(frm, textvariable=inner_label_Text, font=('Arial', 12), wraplength=400)

        inner_combobox.bind("<<ComboboxSelected>>", inner_combobox_func)

        inner_label.pack()


    def _item_grid():
        return 0


    def _make_textbox(self):

        def position_func(event):
            self.controller.on_add_history(self.inner_window)
            self.count += 1
            textbox.configure(state='normal')
            textbox.insert('insert', f'{self.count}. position : {self.position}, ')
            textbox.insert('insert', f'color : {self.color} \n')
            # textbox.config(fg = "#%02x%02x%02x" % tuple(self.color))
            box.config(bg = "#%02x%02x%02x" % tuple(self.color))
            print(f'{self.count}. position : {self.position}, color : {self.color}')
            textbox.configure(state='disabled')


        def clear_func(event):
            self.count = 0
            textbox.configure(state='normal')
            textbox.delete("1.0", END)
            textbox.configure(state='disabled')


        frm = ttk.Frame(self.main_frm)
        frm.pack()

        label_Text = tk.StringVar()
        label = tk.Label(frm, textvariable=label_Text, font=('Arial', 12), wraplength=400)
        label_Text.set('position history as below: \n please press ctrl + A to Add, ctrl + C to clean')
        label.pack()

        textbox = tk.Text(self.root, width=60, height=20)
        textbox.configure(state='disabled')
        textbox.pack()

        box = tk.Label(self.root, width=5, height=2)
        box.configure(state='disabled')
        box.config(bg = "#%02x%02x%02x" % tuple(self.color))
        box.pack()

        self.root.bind('<Control-a>', position_func)
        self.root.bind('<Control-c>', clear_func)

        
    def _make_colorBox(self):

        box = tk.Text(self.root, width=5, height=5)

        box.config(bg = "#%02x%02x%02x" % tuple(self.color))