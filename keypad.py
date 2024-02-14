import tkinter as tk
from tkinter import ttk


class Keypad(ttk.Frame):

    def __init__(self, parent, keynames=[], columns=1, **kwargs):
        super().__init__(parent, **kwargs)
        self.keynames = keynames
        self.buttons = []
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        for i in range(len(self.keynames)):
            row = i // columns
            col = i % columns
            self.columnconfigure(col, weight=1)
            self.rowconfigure(row, weight=1)
            style = {'padx': 2, 'pady': 2,
                     'sticky': 'NSEW'}
            b = ttk.Button(self, text=self.keynames[i])
            b.grid(row=row, column=col, **style)
            self.buttons.append(b)

    def bind(self, sequence=None, func=None, add=None):
        """Bind an event handler to an event sequence."""
        for i in self.buttons:
            i.bind(sequence=sequence, func=func, add=add)
    
    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for i in self.buttons:
            i[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        return self.buttons[0][key]

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        for i in self.buttons:
            i.configure(cnf=cnf, **kwargs)

    @property
    def frame(self):
        """ returns a reference to superclass object"""
        return ttk.Frame(self)


if __name__ == '__main__':
    keys = list('789456123 0.')  # = ['7','8','9',...]
    root = tk.Tk()
    root.title("Keypad Demo")
    keypad = Keypad(root, keynames=keys, columns=3)
    keypad.pack(expand=True, fill=tk.BOTH)
    keypad.bind('<Button-1>', lambda x:print('a'))
    root.mainloop()
