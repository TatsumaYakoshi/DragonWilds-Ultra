import tkinter as tk
from tkinter import ttk, messagebox

def setup_map_tab(tab, data, refresh_preview):
    # Clear tab content
    for widget in tab.winfo_children():
        widget.destroy()

    label = ttk.Label(tab, text="Unlock the entire map:")
    label.pack(pady=(10, 5))

    def reveal_map():
        try:
            data["RevealedFog"] = {
                "RevealedRegionsBitmap": 4294967295,
                "RevealedRegionsDetectionActive": True
            }

            refresh_preview()
            messagebox.showinfo("Map Revealed", "The entire map has been revealed in the save data.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unlock map: {e}")

    reveal_button = ttk.Button(tab, text="Reveal Map", command=reveal_map)
    reveal_button.pack(pady=10)
