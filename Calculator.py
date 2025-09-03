#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import math
from tkinter import ttk

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cihanın kalkulyatoru")
        self.resizable(True, True)
        self.geometry("420x520")
        self.theme = "dark"
        self.font_size = 22

        self.apply_theme()

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 14, "bold"), padding=8, borderwidth=0)
        style.map("TButton",
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#2b88ff'), ('!active', self.btn_color)])

        menubar = tk.Menu(self, bg="#333333", fg="white", tearoff=0)
        filemenu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Settings menyusu
        settingsmenu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        settingsmenu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        settingsmenu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Small Font", command=lambda: self.change_font(16))
        settingsmenu.add_command(label="Normal Font", command=lambda: self.change_font(22))
        settingsmenu.add_command(label="Large Font", command=lambda: self.change_font(28))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Clear Screen", command=self.clear_screen)
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        # Help menyusu
        helpmenu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="white")
        helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "CIHANIN SON MODEL KALKULYATORU!!"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

        self.display_frame = tk.Frame(self, bg=self.bg_color, bd=3, relief="ridge")
        self.display_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

        self.display = tk.Entry(self.display_frame, font=("Segoe UI", self.font_size, "bold"), bd=0, relief="flat",
                                justify="right", bg=self.bg_color, fg=self.fg_color, insertbackground="white")
        self.display.pack(fill="both", expand=True, padx=5, pady=5)

        # Düymələr
        buttons = [
            ["MC", "MR", "MS", "M+", "M-"],
            ["←", "CE", "C", "±", "√"],
            ["7", "8", "9", "/", "%"],
            ["4", "5", "6", "*", "1/x"],
            ["1", "2", "3", "-", "xˣ"],
            ["0", ".", "=", "+"]
        ]

        self.buttons_list = []
        for r, row in enumerate(buttons, 1):
            for c, text in enumerate(row):
                btn = self.create_button(text, r, c)
                self.buttons_list.append(btn)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.grid_columnconfigure(j, weight=1)

        self.memory = 0.0
        self.last_result = None

        # Ekran animasiyası
        self.animate_display_bg()

    def animate_display_bg(self):
        # Rəng keçidi animasiyası
        colors = ["#2c2c2c", "#1a73e8", "#2c2c2c"]
        def loop(idx=0):
            self.display_frame.config(bg=colors[idx % len(colors)])
            self.display.config(bg=colors[idx % len(colors)])
            self.after(1200, loop, idx+1)
        loop()

    def apply_theme(self):
        if self.theme == "dark":
            self.bg_color = "#222831"
            self.btn_color = "#393e46"
            self.fg_color = "#eeeeee"
        else:
            self.bg_color = "#f0f0f0"
            self.btn_color = "#ffffff"
            self.fg_color = "#222831"
        self.configure(bg=self.bg_color)

    def change_theme(self, theme):
        self.theme = theme
        self.apply_theme()
        self.update_ui()

    def change_font(self, size):
        self.font_size = size
        self.display.config(font=("Segoe UI", self.font_size, "bold"))

    def clear_screen(self):
        self.display.delete(0, tk.END)

    def update_ui(self):
        self.display.config(bg=self.bg_color, fg=self.fg_color)
        for btn in self.buttons_list:
            btn.config(style="TButton")

    def create_button(self, text, row, col):
        btn = ttk.Button(self, text=text, style="TButton",
                         command=lambda t=text: self.on_button_click(t))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

        # Hover animasiyası
        def on_enter(e):
            btn.state(['active'])
        def on_leave(e):
            btn.state(['!active'])
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def on_button_click(self, char):
        if char == "xˣ":
            self.display.insert(tk.END, "**")
        elif char == "C":
            self.display.delete(0, tk.END)
        elif char == "CE":
            self.display.delete(0, tk.END)
        elif char == "←":
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current[:-1])
        elif char == "=":
            try:
                expr = self.display.get()
                result = eval(expr, {"__builtins__": None}, {"sqrt": math.sqrt, "pi": math.pi, "e": math.e})
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                self.last_result = result
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif char == "√":
            try:
                value = float(self.display.get())
                result = math.sqrt(value)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif char == "1/x":
            try:
                value = float(self.display.get())
                result = 1 / value
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif char == "±":
            try:
                value = float(self.display.get())
                result = -value
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except Exception:
                pass
        else:
            self.display.insert(tk.END, char)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

