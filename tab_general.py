import tkinter as tk
from tkinter import ttk

def setup_general_tab(tab, editor):
    # Clear previous widgets to avoid duplicates
    for widget in tab.winfo_children():
        widget.destroy()

    ttk.Label(tab, text="JSON Preview:").pack(pady=(10, 0))

    editor.preview_text = tk.Text(tab, wrap="none", height=25)
    editor.preview_text.pack(fill="both", expand=True, padx=10, pady=5)
    editor.preview_text.configure(state="disabled")

    editor.refresh_json_preview()