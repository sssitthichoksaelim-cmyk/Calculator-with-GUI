"""
Modern GUI Calculator
A clean, dark-themed calculator built with tkinter (no external dependencies).
 
Run with:
    python calculator.py
"""
 
import tkinter as tk
from tkinter import font as tkfont
 
 
class Calculator(tk.Tk):
    # ---- Color palette ----
    BG_MAIN = "#1e1e2e"
    BG_DISPLAY = "#181825"
    FG_DISPLAY = "#ffffff"
    FG_EXPRESSION = "#9399b2"
 
    BTN_NUM_BG = "#313244"
    BTN_NUM_FG = "#ffffff"
    BTN_NUM_HOVER = "#45475a"
 
    BTN_OP_BG = "#fab387"
    BTN_OP_FG = "#1e1e2e"
    BTN_OP_HOVER = "#ffb89c"
 
    BTN_FUNC_BG = "#585b70"
    BTN_FUNC_FG = "#ffffff"
    BTN_FUNC_HOVER = "#6c7086"
 
    BTN_EQUALS_BG = "#a6e3a1"
    BTN_EQUALS_FG = "#1e1e2e"
    BTN_EQUALS_HOVER = "#bdf2b8"
 
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(bg=self.BG_MAIN)
        self.resizable(False, False)
        self.geometry("360x540")
 
        # State
        self.expression = ""       # full expression shown above result
        self.current_input = "0"  # current number being typed
        self.just_evaluated = False
 
        self._build_fonts()
        self._build_display()
        self._build_buttons()
        self._bind_keys()
 
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_fonts(self):
        self.font_display = tkfont.Font(family="Helvetica Neue", size=40, weight="bold")
        self.font_expression = tkfont.Font(family="Helvetica Neue", size=14)
        self.font_button = tkfont.Font(family="Helvetica Neue", size=18, weight="bold")
 
    def _build_display(self):
        display_frame = tk.Frame(self, bg=self.BG_DISPLAY, height=140)
        display_frame.pack(fill="x", side="top")
        display_frame.pack_propagate(False)
 
        self.expression_label = tk.Label(
            display_frame,
            text="",
            anchor="e",
            bg=self.BG_DISPLAY,
            fg=self.FG_EXPRESSION,
            font=self.font_expression,
            padx=20,
        )
        self.expression_label.pack(fill="x", pady=(20, 0))
 
        self.result_label = tk.Label(
            display_frame,
            text="0",
            anchor="e",
            bg=self.BG_DISPLAY,
            fg=self.FG_DISPLAY,
            font=self.font_display,
            padx=20,
        )
        self.result_label.pack(fill="x", expand=True)
 
    def _build_buttons(self):
        btn_frame = tk.Frame(self, bg=self.BG_MAIN)
        btn_frame.pack(fill="both", expand=True, padx=12, pady=12)
 
        # row, col, label, type, colspan
        layout = [
            ("C", "func", 0, 0, 1), ("⌫", "func", 0, 1, 1), ("%", "func", 0, 2, 1), ("÷", "op", 0, 3, 1),
            ("7", "num", 1, 0, 1), ("8", "num", 1, 1, 1), ("9", "num", 1, 2, 1), ("×", "op", 1, 3, 1),
            ("4", "num", 2, 0, 1), ("5", "num", 2, 1, 1), ("6", "num", 2, 2, 1), ("−", "op", 2, 3, 1),
            ("1", "num", 3, 0, 1), ("2", "num", 3, 1, 1), ("3", "num", 3, 2, 1), ("+", "op", 3, 3, 1),
            ("±", "func", 4, 0, 1), ("0", "num", 4, 1, 1), (".", "num", 4, 2, 1), ("=", "equals", 4, 3, 1),
        ]
 
        for i in range(5):
            btn_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for j in range(4):
            btn_frame.grid_columnconfigure(j, weight=1, uniform="col")
 
        self.buttons = {}
        for (label, kind, row, col, colspan) in layout:
            bg, fg, hover = self._colors_for(kind)
            btn = tk.Button(
                btn_frame,
                text=label,
                font=self.font_button,
                bg=bg,
                fg=fg,
                activebackground=hover,
                activeforeground=fg,
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda l=label: self.on_button(l),
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                sticky="nsew", padx=6, pady=6, ipadx=4, ipady=10
            )
            btn.bind("<Enter>", lambda e, b=btn, c=hover: b.configure(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
            self.buttons[label] = btn
 
    def _colors_for(self, kind):
        if kind == "num":
            return self.BTN_NUM_BG, self.BTN_NUM_FG, self.BTN_NUM_HOVER
        if kind == "op":
            return self.BTN_OP_BG, self.BTN_OP_FG, self.BTN_OP_HOVER
        if kind == "equals":
            return self.BTN_EQUALS_BG, self.BTN_EQUALS_FG, self.BTN_EQUALS_HOVER
        return self.BTN_FUNC_BG, self.BTN_FUNC_FG, self.BTN_FUNC_HOVER
 
    # ------------------------------------------------------------------
    # Keyboard support
    # ------------------------------------------------------------------
    def _bind_keys(self):
        self.bind("<Key>", self._on_key)
 
    def _on_key(self, event):
        key_map = {
            "*": "×", "/": "÷", "-": "−", "+": "+",
            "\r": "=", "\x08": "⌫", "Escape": "C",
        }
        char = event.char
        keysym = event.keysym
 
        if char.isdigit() or char == ".":
            self.on_button(char)
        elif char in key_map:
            self.on_button(key_map[char])
        elif keysym == "Return":
            self.on_button("=")
        elif keysym == "BackSpace":
            self.on_button("⌫")
        elif keysym == "Escape":
            self.on_button("C")
 
    # ------------------------------------------------------------------
    # Calculator logic
    # ------------------------------------------------------------------
    OP_SYMBOLS = {"÷": "/", "×": "*", "−": "-", "+": "+"}
 
    def on_button(self, label):
        if label.isdigit():
            self._input_digit(label)
        elif label == ".":
            self._input_decimal()
        elif label in self.OP_SYMBOLS:
            self._input_operator(label)
        elif label == "=":
            self._evaluate()
        elif label == "C":
            self._clear()
        elif label == "⌫":
            self._backspace()
        elif label == "±":
            self._toggle_sign()
        elif label == "%":
            self._percent()
 
        self._refresh_display()
 
    def _input_digit(self, digit):
        if self.just_evaluated:
            self.expression = ""
            self.current_input = "0"
            self.just_evaluated = False
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
 
    def _input_decimal(self):
        if self.just_evaluated:
            self.expression = ""
            self.current_input = "0"
            self.just_evaluated = False
        if "." not in self.current_input:
            self.current_input += "."
 
    def _input_operator(self, op_label):
        self.just_evaluated = False
        self.expression += self.current_input + f" {op_label} "
        self.current_input = "0"
 
    def _evaluate(self):
        full_expr = self.expression + self.current_input
        py_expr = full_expr
        for symbol, py_symbol in self.OP_SYMBOLS.items():
            py_expr = py_expr.replace(symbol, py_symbol)
        try:
            # Safe-ish eval: only digits, operators, dot, spaces, parentheses allowed
            allowed = set("0123456789.+-*/() ")
            if not set(py_expr) <= allowed:
                raise ValueError("Invalid characters")
            result = eval(py_expr, {"__builtins__": {}}, {})
            result = self._format_number(result)
            self.expression = full_expr + " ="
            self.current_input = str(result)
            self.just_evaluated = True
        except ZeroDivisionError:
            self.current_input = "Error: ÷0"
            self.expression = ""
            self.just_evaluated = True
        except Exception:
            self.current_input = "Error"
            self.expression = ""
            self.just_evaluated = True
 
    def _clear(self):
        self.expression = ""
        self.current_input = "0"
        self.just_evaluated = False
 
    def _backspace(self):
        if self.just_evaluated:
            self._clear()
            return
        if len(self.current_input) <= 1:
            self.current_input = "0"
        else:
            self.current_input = self.current_input[:-1]
 
    def _toggle_sign(self):
        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        elif self.current_input != "0":
            self.current_input = "-" + self.current_input
 
    def _percent(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = self._format_number(value)
        except ValueError:
            pass
 
    @staticmethod
    def _format_number(value):
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(round(value, 10))
        return str(value)
 
    # ------------------------------------------------------------------
    # Display refresh
    # ------------------------------------------------------------------
    def _refresh_display(self):
        self.expression_label.configure(text=self.expression)
        text = self.current_input
        # Shrink font for long numbers so they still fit
        if len(text) > 9:
            self.result_label.configure(font=tkfont.Font(family="Helvetica Neue", size=26, weight="bold"))
        else:
            self.result_label.configure(font=self.font_display)
        self.result_label.configure(text=text)
 
 
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()