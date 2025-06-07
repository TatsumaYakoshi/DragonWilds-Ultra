import tkinter as tk
from tkinter import ttk, messagebox

def setup_extra_tab(tab, data, refresh_preview, save_json_func):
    # Remove all widgets from the tab
    for widget in tab.winfo_children():
        widget.destroy()

    # --- Map Reveal Section ---
    map_frame = ttk.LabelFrame(tab, text="Reveal Map")
    map_frame.pack(fill="x", padx=10, pady=(10, 0))

    def reveal_map():
        value = {
            "RevealedRegionsBitmap": 4294967295,
            "RevealedRegionsDetectionActive": True
        }
        data["RevealedFog"] = value
        save_json_func(data)
        refresh_preview()
        messagebox.showinfo("Reveal Map", "The entire map has been revealed in the save data.")

    reveal_button = ttk.Button(map_frame, text="Apply", command=reveal_map)
    reveal_button.pack(side="left", padx=8, pady=7)

    # --- Reset Ward Section ---
    ward_frame = ttk.LabelFrame(tab, text="Reset Ward")
    ward_frame.pack(fill="x", padx=10, pady=(10, 0))

    def reset_ward():
        try:
            loadout = data.get("Loadout", {})
            if "1" in loadout and isinstance(loadout["1"], dict):
                loadout["1"]["VitalShield"] = 75
                save_json_func(data)
                refresh_preview()
                messagebox.showinfo("Ward Reset!", "Armour is now Full!")
            else:
                messagebox.showwarning("Ward Reset", "Could not find Loadout key 1.")
        except Exception as e:
            messagebox.showerror("Ward Reset", f"Error resetting ward:\n{e}")

    ward_button = ttk.Button(ward_frame, text="Apply", command=reset_ward)
    ward_button.pack(side="left", padx=8, pady=7)

    # --- Reset Status Effects to 100 Section ---
    status_frame = ttk.LabelFrame(tab, text="Reset Status Effects")
    status_frame.pack(fill="x", padx=10, pady=(10, 0))

    def reset_status_effects():
        character = data.get("Character", {})
        character["Sustenance"] = {
            "SustenanceValue": 100,
            "SustenanceDecayBuffer": 0
        }
        character["Hydration"] = {
            "HydrationValue": 100,
            "HydrationDecayBuffer": 0
        }
        character["Toxicity"] = {
            "ToxicityValue": 0,
            "HighestToxicityValue": 0
        }
        character["Endurance"] = {
            "EnduranceValue": 100,
            "EnduranceDecayBuffer": 0
        }
        save_json_func(data)
        refresh_preview()
        messagebox.showinfo("Reset Status Effects", "Good as NEW!")

    status_btn = ttk.Button(status_frame, text="Apply", command=reset_status_effects)
    status_btn.pack(side="left", padx=8, pady=7)

    # --- Reset Health to 100 Section ---
    health_frame = ttk.LabelFrame(tab, text="Reset Health")
    health_frame.pack(fill="x", padx=10, pady=(10, 0))

    def reset_health():
        character = data.get("Character", {})
        character["Health"] = {
            "CurrentValue": 100
        }
        save_json_func(data)
        refresh_preview()
        messagebox.showinfo("Reset Health", "Health restored to 100!")

    health_btn = ttk.Button(health_frame, text="Apply", command=reset_health)
    health_btn.pack(side="left", padx=8, pady=7)

    # --- Reset Stamina to 100 Section ---
    stamina_frame = ttk.LabelFrame(tab, text="Reset Stamina")
    stamina_frame.pack(fill="x", padx=10, pady=(10, 0))

    def reset_stamina():
        character = data.get("Character", {})
        character["Stamina"] = {
            "CurrentValue": 100
        }
        save_json_func(data)
        refresh_preview()
        messagebox.showinfo("Reset Stamina", "Stamina restored to 100!")

    stamina_btn = ttk.Button(stamina_frame, text="Apply", command=reset_stamina)
    stamina_btn.pack(side="left", padx=8, pady=7)

    # --- Never Hungry, Tired, Thirsty (Infinite Non-Health/Stamina) ---
    infinite_frame = ttk.LabelFrame(tab, text="Never Hungry, Tired, Thirsty")
    infinite_frame.pack(fill="x", padx=10, pady=(10, 0))

    def apply_never_hungry():
        inf = 1e30
        character = data.get("Character", {})
        character["Sustenance"] = {
            "SustenanceValue": inf,
            "SustenanceDecayBuffer": inf
        }
        character["Hydration"] = {
            "HydrationValue": inf,
            "HydrationDecayBuffer": inf
        }
        character["Endurance"] = {
            "EnduranceValue": inf,
            "EnduranceDecayBuffer": inf
        }
        save_json_func(data)
        refresh_preview()
        messagebox.showinfo("Never Hungry, Tired, Thirsty", "Applied.\n\n⚠️ Warning: Resets on Death")

    neverhungry_btn = ttk.Button(infinite_frame, text="Apply", command=apply_never_hungry)
    neverhungry_btn.pack(side="left", padx=8, pady=7)