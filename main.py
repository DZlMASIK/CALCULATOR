import tkinter as tk
from calckulator import ModernCalculator


def main():
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()