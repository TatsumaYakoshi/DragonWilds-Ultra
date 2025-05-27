import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import getpass

SETTINGS_PATH = os.path.expanduser("~/.dragonwilds_editor_settings.json")

def get_default_save_folder():
    username = getpass.getuser()
    return os.path.join("C:\\Users", username, "AppData", "Local", "RSDragonwilds", "Saved", "SaveCharacters")

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f)
    except Exception:
        pass

from tab_general import setup_general_tab
from tab_skills import setup_skills_tab
from tab_character import setup_character_tab
from tab_gear import setup_gear_tab
from tab_storage import setup_storage_tab
from tab_map import setup_map_tab
from tab_editor import setup_editor_tab

class DragonWildsUltraEditor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.data = None
        self.filepath = None
        self.settings = load_settings()
        self.preview_text = None  # for General tab JSON preview
        self.create_widgets()
        self.show_info_dialog()

    def create_widgets(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=5, pady=5)

        load_btn = ttk.Button(button_frame, text="Load", command=self.load_file_dialog)
        load_btn.pack(side="left", padx=(0, 5))
        save_btn = ttk.Button(button_frame, text="Save", command=self.save_file_dialog)
        save_btn.pack(side="left")
        settings_btn = ttk.Button(button_frame, text="Settings", command=self.open_settings_dialog)
        settings_btn.pack(side="right", padx=(10,0))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.general_tab = ttk.Frame(self.notebook)
        self.skills_tab = ttk.Frame(self.notebook)
        self.name_tab = ttk.Frame(self.notebook)
        self.gear_tab = ttk.Frame(self.notebook)
        self.storage_tab = ttk.Frame(self.notebook)
        self.map_tab = ttk.Frame(self.notebook)
        self.editor_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.skills_tab, text="Skills")
        self.notebook.add(self.name_tab, text="Name")
        self.notebook.add(self.gear_tab, text="Gear")
        self.notebook.add(self.storage_tab, text="Storage")
        self.notebook.add(self.map_tab, text="Map")
        self.notebook.add(self.editor_tab, text="Editor")

        self.setup_tabs()

    def save_json_func(self, data):
        if self.filepath:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        self.refresh_json_preview()

    def setup_tabs(self):
        setup_general_tab(self.general_tab, self)
        setup_skills_tab(self.skills_tab, self.data, self.refresh_json_preview)
        setup_character_tab(self.name_tab, self)
        setup_gear_tab(self.gear_tab, self.data, self.refresh_json_preview)
        setup_storage_tab(self.storage_tab, self.data, self.refresh_json_preview)
        setup_map_tab(self.map_tab, self.data, self.refresh_json_preview)
        setup_editor_tab(self.editor_tab, self.data, self.refresh_json_preview, self.save_json_func)
        # No need to call refresh_json_preview() here because setup_general_tab does it after creating the widget

    def load_save_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.filepath = filepath
            self.setup_tabs()  # this will recreate the tabs and the preview widget
            # refresh_json_preview is called by setup_general_tab during this
            messagebox.showinfo("Loaded", "Save loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load save file:\n{e}")

    def save_to_file(self, filepath):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            self.filepath = filepath
            messagebox.showinfo("Saved", "Save file saved.")
            self.refresh_json_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def load_file_dialog(self):
        initial_dir = self.settings.get("save_folder") or get_default_save_folder()
        filepath = filedialog.askopenfilename(
            title="Open Save File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        if filepath:
            self.load_save_file(filepath)

    def save_file_dialog(self):
        initial_dir = self.settings.get("save_folder") or get_default_save_folder()
        filepath = filedialog.asksaveasfilename(
            title="Save Save File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        if filepath:
            self.save_to_file(filepath)

    def refresh_json_preview(self):
        if hasattr(self, "preview_text") and self.preview_text and self.preview_text.winfo_exists():
            self.preview_text.configure(state="normal")
            self.preview_text.delete("1.0", "end")
            if self.data is None:
                self.preview_text.insert("1.0", "Save not Loaded")
            else:
                try:
                    pretty = json.dumps(self.data, indent=4, ensure_ascii=False)
                except Exception as e:
                    pretty = f"Error displaying JSON: {e}"
                self.preview_text.insert("1.0", pretty)
            self.preview_text.configure(state="disabled")

    def show_info_dialog(self):
        message = (
            "DragonWilds: Ultra Editor\n"
            "------------------------\n"
            "• Load: Open an existing save file (JSON)\n"
            "• Save: Save your changes to a file\n"
            "• Features: Adding items, changing name, editing skills, updating personal chest, revealing map etc"
            "• Settings: Set your default folder for loading/saving saves\n"
            "• Gear gives you set gear, Storage updates personal chest with surival items or extra gear"
            "• Credits: TatsumaYakoshi, Elleandria, Google"
        )
        messagebox.showinfo("Info", message)

    def open_settings_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Settings")
        dialog.grab_set()
        dialog.geometry("400x140")

        tk.Label(dialog, text="Default Save Folder:").pack(pady=(10,2))
        folder_var = tk.StringVar(value=self.settings.get("save_folder", get_default_save_folder()))
        entry = tk.Entry(dialog, textvariable=folder_var, width=40)
        entry.pack(padx=10, fill="x")

        def browse_folder():
            folder = filedialog.askdirectory(title="Choose Save Folder", initialdir=folder_var.get() or get_default_save_folder())
            if folder:
                folder_var.set(folder)

        browse_btn = ttk.Button(dialog, text="Browse...", command=browse_folder)
        browse_btn.pack(pady=5)

        def save_settings_and_close():
            self.settings["save_folder"] = folder_var.get()
            save_settings(self.settings)
            dialog.destroy()

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        save_btn = ttk.Button(button_frame, text="Save", command=save_settings_and_close)
        save_btn.pack(side="left", padx=5)
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side="left", padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DragonWilds: Ultra Editor")
    root.geometry("900x600")
    app = DragonWildsUltraEditor(root)
    root.mainloop()