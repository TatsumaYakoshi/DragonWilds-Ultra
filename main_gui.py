import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
from tab_general import setup_general_tab
from tab_skills import setup_skills_tab
from tab_character import setup_character_tab
from tab_storage import setup_storage_tab
from tab_map import setup_map_tab
from tab_editor import setup_editor_tab

SETTINGS_FILE = "settings.json"

def get_default_save_path():
    # Use the user's real home directory (cross-platform)
    user_dir = os.path.expanduser("~")
    return os.path.join(user_dir, "AppData", "Local", "RSDragonwilds", "Saved", "SaveCharacters")

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception:
        pass

class DragonWildsUltraEditor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.data = None
        self.filepath = None
        self.settings = load_settings()
        self.create_widgets()
        self.show_info_dialog()

    def get_initial_dir(self):
        # Use settings if available, otherwise use the default save path
        return self.settings.get("save_data_path", get_default_save_path())

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

        # Tab order: General, Name, Skills, Inventory, Storage, Map
        self.general_tab = ttk.Frame(self.notebook)
        self.name_tab = ttk.Frame(self.notebook)
        self.skills_tab = ttk.Frame(self.notebook)
        self.editor_tab = ttk.Frame(self.notebook)    # Inventory
        self.storage_tab = ttk.Frame(self.notebook)
        self.map_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.name_tab, text="Name")
        self.notebook.add(self.skills_tab, text="Skills")
        self.notebook.add(self.editor_tab, text="Inventory")
        self.notebook.add(self.storage_tab, text="Storage")
        self.notebook.add(self.map_tab, text="Map")

        # JSON Preview Widget in General Tab
        self.preview_text = tk.Text(self.general_tab, wrap="none", height=20, width=90)
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.preview_text.config(state=tk.DISABLED, font=("Consolas", 10))

        self.setup_tabs()

    def save_json_func(self, data):
        # Only saves if a file is loaded
        if self.filepath:
            try:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Success", f"File saved:\n{self.filepath}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{e}")
        self.refresh_json_preview()

    def setup_tabs(self):
        setup_general_tab(self.general_tab, self)
        setup_character_tab(self.name_tab, self)
        setup_skills_tab(self.skills_tab, self.data, self.refresh_json_preview)
        setup_editor_tab(self.editor_tab, self.data, self.refresh_json_preview, self.save_json_func, self.refresh_inventory_and_storage)
        setup_storage_tab(self.storage_tab, self.data, self.refresh_json_preview, self.save_json_func, self.refresh_inventory_and_storage, storage_slot_end=18)
        setup_map_tab(self.map_tab, self.data, self.refresh_json_preview)

    def refresh_inventory_and_storage(self):
        # Refresh both inventory and storage tabs to reflect any preset changes.
        setup_editor_tab(self.editor_tab, self.data, self.refresh_json_preview, self.save_json_func, self.refresh_inventory_and_storage)
        setup_storage_tab(self.storage_tab, self.data, self.refresh_json_preview, self.save_json_func, self.refresh_inventory_and_storage, storage_slot_end=18)

    def load_save_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.filepath = filepath
            self.setup_tabs()  # Recreate tabs and widgets with the new data
            self.refresh_json_preview()
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load file:\n{e}")

    def load_file_dialog(self):
        initial_dir = self.get_initial_dir()
        filepath = filedialog.askopenfilename(
            title="Select Save File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        if filepath:
            self.load_save_file(filepath)

    def save_file_dialog(self):
        if not self.filepath:
            initial_dir = self.get_initial_dir()
            filepath = filedialog.asksaveasfilename(
                title="Save File As",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir=initial_dir
            )
            if not filepath:
                return
            self.filepath = filepath
        self.save_json_func(self.data)

    def open_settings_dialog(self):
        # Let user set a default save data path
        current_path = self.get_initial_dir()
        new_path = filedialog.askdirectory(
            title="Select Default Save Data Folder",
            initialdir=current_path
        )
        if new_path:
            self.settings["save_data_path"] = new_path
            save_settings(self.settings)
            messagebox.showinfo("Settings Saved", f"Default save data path set to:\n{new_path}")

    def refresh_json_preview(self):
        if self.data is not None:
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, json.dumps(self.data, indent=4))
            self.preview_text.config(state=tk.DISABLED)

    def show_info_dialog(self):
        features = [
            "Features:",
            "• View and edit your save file as JSON",
            "• Change character name and save as new file (Make sure to Delete the old one or you will have issues)",
            "• Fully editable inventory and storage (add, remove, bulk, filter, slot/amount, etc.)",
            "• Apply gear and storage presets",
            "• Editable loadout (inventory tab)",
            "• Filter and search item lists by name",
            "• Live JSON preview for all changes",
            "• Better Orignization..",
            "• User-friendly graphical interface",
            "Shout out to Elleandria for the help",
            "Credits:",
            "DragonWilds Ultra Editor by TatsumaYakoshi"
        ]
        messagebox.showinfo("Features & Credits", "\n".join(features))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wild Editor - Dragon Wilds Ultra")
    app = DragonWildsUltraEditor(root)
    app.mainloop()