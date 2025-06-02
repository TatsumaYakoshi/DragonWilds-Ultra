import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import uuid

def setup_character_tab(tab, editor):
    for widget in tab.winfo_children():
        widget.destroy()

    name_var = tk.StringVar()

    def find_first_char_name(data):
        """Recursively find the first value for 'char_name' in the JSON."""
        if isinstance(data, dict):
            for k, v in data.items():
                if k == "char_name":
                    return v
                result = find_first_char_name(v)
                if result is not None:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = find_first_char_name(item)
                if result is not None:
                    return result
        return None

    def update_all_char_names_and_guids(data, new_name):
        """
        Recursively update all keys named 'char_name' and assign new 'char_guid'
        everywhere in the JSON. Assigns a new GUID for every dict that has both.
        """
        if isinstance(data, dict):
            has_char_name = "char_name" in data
            has_char_guid = "char_guid" in data
            if has_char_name:
                data["char_name"] = new_name
            if has_char_guid and has_char_name:
                data["char_guid"] = uuid.uuid4().hex.upper()
            for k, v in data.items():
                update_all_char_names_and_guids(v, new_name)
        elif isinstance(data, list):
            for item in data:
                update_all_char_names_and_guids(item, new_name)

    def load_name():
        if editor.data and isinstance(editor.data, dict):
            found = find_first_char_name(editor.data)
            name_var.set(found if found is not None else "")
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

        # Recursively update all char_name and char_guid keys
        update_all_char_names_and_guids(editor.data, new_name)

        editor.refresh_json_preview()

        # Always prompt for "Save As" using new name as default filename
        initial_dir = os.path.dirname(getattr(editor, "filepath", "") or os.getcwd())
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
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(editor.data, f, indent=4, ensure_ascii=False)
                editor.filepath = save_path
                messagebox.showinfo("Success", f"Save file saved as:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    ttk.Label(tab, text="Character Name:").pack(pady=10)
    ttk.Entry(tab, textvariable=name_var, width=30).pack(pady=5)
    ttk.Button(tab, text="Apply", command=apply_name).pack(pady=10)

    load_name()