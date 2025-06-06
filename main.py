import tkinter as tk
from Login import LoginWindow
from bd import init_db

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()