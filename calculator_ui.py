import tkinter as tk
from tkinter import ttk

from keypad import Keypad


class CalculatorUI(tk.Tk):
    @staticmethod
    def _isnum(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def __init__(self):
        super().__init__()
        self.numpad = Keypad(self, list('789456123 0.'), 3)
        self.operator = Keypad(self, list('*/+-^='), 1)
        self.screen = tk.StringVar()
        self.b_calculated = False
        self.init_component()

    def init_component(self):
        self.title('Calculator')
        s = ttk.Label(self, textvariable=self.screen, width=100, foreground='white', anchor='e')

        # Style
        s.config(background="black")

        # Event Handler
        self.numpad.bind('<Button-1>', self.keypad_press_handler)
        self.operator.bind('<Button-1>', self.keypad_press_handler)

        # LayoutManagement
        for i in range(3):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        style = {'padx': 2.5, 'pady': 2.5, 'sticky': tk.NSEW}
        s.grid(row=0, column=0, columnspan=3, **style)
        self.numpad.grid(row=1, column=0, columnspan=2, **style)
        self.operator.grid(row=1, column=2, columnspan=1, **style)

    def keypad_press_handler(self, event=tk.Event):
        """ Keypad press handler """
        widget = event.widget
        if widget['text'] != '=':
            if not self.b_calculated:
                curr = self.screen.get()
                self.screen.set(curr + widget['text'])
            else:
                self.screen.set(widget['text'])
                self.b_calculated = False
        else:
            curr = self.screen.get()
            curr.replace("^", "**")
            self.screen.set(str(eval(curr)))
            self.b_calculated = True

    def run(self):
        self.mainloop()
