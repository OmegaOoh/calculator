"""
Calculator UI Module
CalculatorUI Class which Construct, Manage and Display the GUI for Calculator
"""


import tkinter as tk
from tkinter import ttk
from pygame import mixer

from keypad import Keypad
from calculatorcontroller import CalculatorController

OPERATOR = ["(", ")", '*', '/', '+', '-', '^', 'mod', '%']


def playsound(filename = 'beep.mp3'):
    """ Function to Play Sound Using Pygame
    :param filename: Name of the Audio file"""
    mixer.music.load(filename)
    mixer.music.play(loops=0)


class CalculatorUI(tk.Tk):
    """ Class for Graphical User Interface of Calculator """
    @staticmethod
    def _isnum(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def __init__(self):
        """ Initialize the attribute of the UI """
        super().__init__()
        mixer.init()
        self.numpad = Keypad(self, list('789456123 0.'), 3)
        operator = ["( )", '*', '/', '+', '-', '^', 'mod', '%']
        self.operator = Keypad(self, operator, 2)
        self.function = ttk.Combobox(self)
        self.exp_his = tk.Listbox(self, height=3)
        self.res_his = tk.Listbox(self, height=3)
        self.b_calculated = False
        self.label = ttk.Label(self, foreground='white', anchor='e')
        self.init_component()
        self.get_mathfunc()

    def init_component(self):
        """ Initialize the tkinter components """
        self.title('Calculator')
        self.minsize(width=200, height=250)

        eq = ttk.Button(self, text='=')
        clr = ttk.Button(self, text='CLR', command=self.clear_handler)
        delete = ttk.Button(self, text='DEL', command=self.del_handler)
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL)

        # Style
        font = ('Arial', 20)
        self.label.config(background="black", font=font)
        style = ttk.Style()
        style.configure("Eq.TButton", foreground="Blue")
        eq.configure(style='Eq.TButton')
        self.function['state'] = 'readonly'

        # Event Handler
        self.numpad.bind('<Button-1>', self.keypad_press_handler)
        self.operator.bind('<Button-1>', self.keypad_press_handler)
        eq.bind('<Button-1>', self.handle_equal)
        self.function.bind('<<ComboboxSelected>>', self.add_function)
        self.exp_his.bind('<MouseWheel>',lambda e: self.scroll_handler(self.res_his, e))
        self.res_his.bind('<MouseWheel>',lambda e: self.scroll_handler(self.exp_his, e))
        scroll.config(command=self.scrollbar_handler)
        self.exp_his.bind('<<ListboxSelect>>', self.load_expression)
        self.res_his.bind('<<ListboxSelect>>', self.load_answer)

        # LayoutManagement
        for i in range(4):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=15)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=25)
        self.rowconfigure(3, weight=200)
        self.rowconfigure(4, weight=80)
        style = {'padx': 2.5, 'pady': 2.5, 'sticky': tk.NSEW}
        self.exp_his.grid(row=0, column=0, columnspan=3, **style)
        self.res_his.grid(row=0, column=3, **style)
        self.exp_his.grid(row=0, column=0, **style)
        scroll.grid(row=0, column=4, **style)
        self.label.grid(row=1, column=0, columnspan=5, **style)
        self.function.grid(row=2, column=0, columnspan=2, **style)
        delete.grid(row=2, column=2, **style)
        clr.grid(row=2, column=3, columnspan=2,**style)
        self.numpad.grid(row=3, column=0, columnspan=3, rowspan=2, **style)
        self.operator.grid(row=3, column=3, columnspan=2, **style)
        eq.grid(row=4, column=3, columnspan=3, **style)

    def scroll_handler(self, sync_listbox, event: tk.Event):
        """ Handle Syncing Listbox scroll events """
        sync_listbox.yview_scroll(int(-4*(event.delta/120)), "units")

    def scrollbar_handler(self, *args):
        """ Handle Scrolling by Scrollbar"""
        if args[0] == 'scroll':
            self.exp_his.yview_scroll(int(args[1]), args[2])
            self.res_his.yview_scroll(int(args[1]), args[2])
        else:
            self.exp_his.yview_moveto(float(args[1]))
            self.res_his.yview_moveto(float(args[1]))

    def get_mathfunc(self):
        """ Set Math Functions to combobox"""
        self.function['values'] = CalculatorController.load_func()
        self.function.current(0)

    def keypad_press_handler(self, event: tk.Event):
        """ Handle Operation and Number Key Press
        Add the key that is pressed onto the screen label
        with some validation to prevent error.
         """
        widget = event.widget
        if str(widget['text']).isspace():
            return

        curr = self.label['text']
        # There is only 0
        b = len(curr) == 1 and curr[0] == '0'
        if self.b_calculated and self._isnum(widget['text']) or b:
            self.label['text'] = ''
            curr = ''
        self.b_calculated = False
        # We Handle Parentheses Another Way
        if widget['text'] == '( )':
            curr = self.label['text']
            open_p = curr.count('(')
            close_p = curr.count(')')
            if close_p < open_p and (self._isnum(curr[-1]) or curr[-1] == ')'):
                self.label['text'] = curr + ')'
            elif self._isnum(curr[-1]) or curr[-1] == ')':
                self.label['text'] = curr + '*('
            else:
                self.label['text'] = curr + '('
            return

        if len(curr) > 2 and curr[-2] in OPERATOR and curr[-1] == '0':
            self.label['text'] = curr[:-1]
            curr = self.label['text']
        self.label['text'] = curr + widget['text']

    def handle_equal(self, *args):
        """ Handle the event that the equal sign button is pressed
        calculate the expression and give a feedback if expression is invalid"""
        self.label.configure(foreground='white')
        curr = self.label['text']
        ans = CalculatorController.get_answer(curr)
        if ans != 'Invalid Format':
            self.exp_his.insert(0, curr + ' =')
            self.res_his.insert(0, ans)
            self.label['text'] = str(ans)
            self.b_calculated = True
        else:
            self.label.configure(foreground='red')
            playsound()

    def add_function(self, *args):
        """ Adding Mathematical Function into the Expression"""
        curr = self.label['text']
        if curr == 'Invalid Format' or self.b_calculated:
            self.label['text'] = ''
            curr = ''
        self.b_calculated = False
        c_func = self.function['values'][self.function.current()]
        if curr == '':
            self.label['text'] = curr + c_func + "("
        elif not self._isnum(curr[-1]):
            self.label['text'] = curr + c_func + "("
        elif self._isnum(curr) or self._isnum(curr[-1]):
            self.label['text'] = c_func + "(" + curr + ")"
        else:
            self.label['text'] = curr + c_func + "("

    def del_handler(self, **args):
        """ Handle Delete Event"""
        if self.b_calculated:
            self.label['text'] = ''
            return
        t = CalculatorController.delete(self.label['text'])
        self.label['text'] = t

    def clear_handler(self, **args):
        """ Clear all Equation on Screen """
        self.label['text'] = ''
        self.b_calculated = False
        self.label.configure(foreground='white')
        self.exp_his.delete(0, tk.END)
        self.res_his.delete(0, tk.END)

    def load_expression(self, *args):
        """ Copy the Selected Expression into the calculation Field"""
        curr = self.exp_his.curselection()
        try:
            t = self.exp_his.get(curr[0])
            self.label['text'] = str(t).removesuffix(' =')
            self.b_calculated = False
        except IndexError:
            return

    def load_answer(self, *args):
        """ Copy the Selected Answer into the Calculation Field"""
        curr = self.res_his.curselection()
        try:
            t = self.res_his.get(curr[0])
            self.label['text'] = str(t)
            self.b_calculated = False
        except IndexError:
            return

    def run(self):
        """ Run the GUI """
        self.mainloop()
