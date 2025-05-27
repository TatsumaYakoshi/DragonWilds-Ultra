import tkinter as tk
from main_gui import DragonWildsUltraEditor

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DragonWilds: Ultra Editor")
    root.geometry("900x600")
    app = DragonWildsUltraEditor(root)
    root.mainloop()