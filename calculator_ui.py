import tkinter as tk
from tkinter import ttk

from keypad import Keypad
from calculatorcontroller import CalculatorController


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
        operator = ["( )", '*', '/', '+', '-', '^', 'mod', '%']
        self.operator = Keypad(self, operator, 2)
        self.function = ttk.Combobox(self)
        self.screen = tk.StringVar()
        self.exp_his = tk.Listbox(self, height=3)
        self.res_his = tk.Listbox(self, height=3)
        self.b_calculated = False
        self.init_component()
        self.get_mathfunc()

    def init_component(self):
        self.title('Calculator')
        self.minsize(width=200, height=250)
        s = ttk.Label(self, textvariable=self.screen, foreground='white', anchor='e')
        eq = ttk.Button(self, text='=')
        clr = ttk.Button(self, text='CLR', command=self.clear_handler)
        delete = ttk.Button(self, text='DEL', command=self.del_handler)
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL)

        # Style
        font = ('Arial', 20)
        s.config(background="black", font=font)
        style = ttk.Style()
        style.configure("Eq.TButton", foreground="Blue")
        eq.configure(style='Eq.TButton')
        self.function['state'] = 'readonly'

        # Event Handler
        self.numpad.bind('<Button-1>', self.keypad_press_handler)
        self.operator.bind('<Button-1>', self.keypad_press_handler)
        eq.bind('<Button-1>', self.keypad_press_handler)
        self.function.bind('<<ComboboxSelected>>', self.add_function)
        self.exp_his.config(yscrollcommand=scroll.set)
        self.res_his.config(yscrollcommand=scroll.set)
        scroll.config(command=self.exp_his.yview)
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
        s.grid(row=1, column=0, columnspan=5, **style)
        self.function.grid(row=2, column=0, columnspan=2, **style)
        delete.grid(row=2, column=2, **style)
        clr.grid(row=2, column=3, columnspan=2,**style)
        self.numpad.grid(row=3, column=0, columnspan=3, rowspan=2, **style)
        self.operator.grid(row=3, column=3, columnspan=2, **style)
        eq.grid(row=4, column=3, columnspan=3, **style)

    def get_mathfunc(self):
        """ Set Math Functions to combobox"""
        self.function['values'] = CalculatorController.load_func()
        self.function.current(0)

    def keypad_press_handler(self, event: tk.Event):
        """ Keypad press handler """
        widget = event.widget
        if str(widget['text']).isspace():
            return
        # Handle Equal Sign
        curr = self.screen.get()
        if widget['text'] == '=':
            ans = CalculatorController.get_answer(curr)
            if ans != 'Invalid Format':
                self.exp_his.insert(0, curr + ' =')
                self.res_his.insert(0, ans)
            self.screen.set(str(ans))
            self.b_calculated = True
            return

        # There is only 0
        b = len(curr) == 1 and curr[0] == '0'
        print(b)
        if self.b_calculated and self._isnum(widget['text']) or b:
            self.screen.set('')
            curr = ''
        self.b_calculated = False
        # We Handle Parentheses Another Way
        if widget['text'] == '( )':
            curr = self.screen.get()
            open_p = curr.count('(')
            close_p = curr.count(')')
            if close_p < open_p and (self._isnum(curr[-1]) or curr[-1] == ')'):
                self.screen.set(curr + ')')
                return
            elif self._isnum(curr[-1]) or curr[-1] == ')':
                self.screen.set(curr + '*(')
                return
            else:
                self.screen.set(curr + '(')
                return

        self.screen.set(curr + widget['text'])

    def add_function(self, event: tk.Event):
        curr = self.screen.get()
        if curr == 'Invalid Format':
            self.screen.set('')
            curr = ''
        c_func = self.function['values'][self.function.current()]
        if not self.b_calculated and not curr == '':
            if not self._isnum(curr[-1]):
                self.screen.set(curr + c_func + "(")
            else:
                self.screen.set(curr + '*' + c_func + "(")
        else:
            self.screen.set(c_func + "(")

    def del_handler(self, **args):
        """ Handle Delete Event"""
        if self.b_calculated:
            self.screen.set('')
            return
        t = CalculatorController.delete(self.screen.get())
        self.screen.set(t)

    def clear_handler(self, **args):
        """ Clear all Equation on Screen """
        self.screen.set('')
        self.b_calculated = False
        self.exp_his.option_clear()
        self.res_his.option_clear()

    def load_expression(self, x,**kwargs):
        curr = self.exp_his.curselection()
        try:
            t = self.exp_his.get(curr[0])
            self.screen.set(str(t).removesuffix(' ='))
            self.b_calculated = False
        except IndexError:
            return

    def load_answer(self, x, **kwargs):
        curr = self.res_his.curselection()
        try:
            t = self.res_his.get(curr[0])
            self.screen.set(str(t))
            self.b_calculated = False
        except IndexError:
            return

    def run(self):
        self.mainloop()
