import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json

def setup_character_tab(tab, editor):
    for widget in tab.winfo_children():
        widget.destroy()

    name_var = tk.StringVar()

    def load_name():
        if editor.data and isinstance(editor.data, dict):
            name_var.set(editor.data.get("char_name", ""))
        else:
            name_var.set("")

    def apply_name():
        new_name = name_var.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return
        if not (editor.data and isinstance(editor.data, dict)):
            messagebox.showerror("Error", "No save loaded to update character name.")
            return

        # Update the loaded data
        editor.data["char_name"] = new_name
        editor.refresh_preview()

        # Always prompt for "Save As" using new name as default filename
        initial_dir = os.path.dirname(editor.filepath) if getattr(editor, "filepath", None) else os.getcwd()
        default_filename = f"{new_name}.json"
        save_path = filedialog.asksaveasfilename(
            title="Save your save file as...",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialdir=initial_dir,
            initialfile=default_filename,
        )
        if save_path:
            try:
                with open(save_path, "w") as f:
                    json.dump(editor.data, f, indent=4)
                editor.filepath = save_path
                messagebox.showinfo("Success", f"Save file saved as:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    ttk.Label(tab, text="Character Name:").pack(pady=10)
    ttk.Entry(tab, textvariable=name_var, width=30).pack(pady=5)
    ttk.Button(tab, text="Apply", command=apply_name).pack(pady=10)

    load_name()