import tkinter as tk
from tkinter import ttk

SKILL_IDS = [
    'Wf3i7Ha-B06DH719j1vtBw', '4pefO9k1lUqfA6mvHNi1SA', 'waK-8EyQFQ2xEjCGYmuTRQ',
    'Tn7t6DQyX0-Q0cM5K7B90A', '0hreSMRVXUihq9qjDO2CFA', 'jqX0Gh6QI0GFFPCDFK_CJQ',
    'heq7u88Q2UuLXFqLGTVwQw', 'NOqC-z-2ckqi0El22qMFlw', '4zYUGF5u_0KbMLkWJmmBbQ'
]

SKILL_LABELS = [
    "Artisan XP", "Attack XP", "Construction XP", "Cooking XP",
    "Magic XP", "Mining XP", "Ranged XP", "Runecrafting XP", "Woodcutting XP"
]

LEVEL_TO_XP = [
    0, 33, 70, 111, 156, 206, 261, 322, 389, 463,
    545, 636, 736, 847, 969, 1104, 1253, 1417, 1598, 1798,
    2018, 2261, 2529, 2825, 3152, 3512, 3910, 4349, 4833, 5367,
    5957, 6608, 7326, 8118, 8993, 9958, 11023, 12199, 13496, 14929,
    16510, 18255, 20181, 22307, 24654, 27245, 30105, 33262, 36747, 40594
] + [100000000] * (99 - 50)

def get_level_for_xp(xp):
    for i in range(98, -1, -1):
        if xp >= LEVEL_TO_XP[i]:
            return i + 1
    return 1

def setup_skills_tab(tab, data, refresh_preview):
    for widget in tab.winfo_children():
        widget.destroy()
    if not data or not isinstance(data, dict):
        ttk.Label(tab, text="Load a save file to view and edit skills.").pack(padx=10, pady=10)
        return

    skill_dict = {s["Id"]: s for s in data.get("Skills", {}).get("Skills", [])}
    rows = []

    for i, (skill_id, label) in enumerate(zip(SKILL_IDS, SKILL_LABELS)):
        skill_data = skill_dict.get(skill_id, {"Id": skill_id, "Xp": 0})
        xp = int(skill_data.get("Xp", 0))
        level = get_level_for_xp(xp)

        ttk.Label(tab, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)

        level_label = ttk.Label(tab, text=f"Level: {level}")
        level_label.grid(row=i, column=1, sticky="w", padx=5, pady=2)

        xp_var = tk.StringVar(value=str(xp))
        entry = ttk.Entry(tab, textvariable=xp_var, width=12)
        entry.grid(row=i, column=2, padx=5, pady=2)

        rows.append((skill_id, xp_var, level_label))

    def apply_changes():
        skills_list = data.setdefault("Skills", {}).setdefault("Skills", [])
        skill_map = {s["Id"]: s for s in skills_list}

        for skill_id, xp_var, level_label in rows:
            try:
                xp = int(xp_var.get())
            except ValueError:
                xp = 0

            if skill_id in skill_map:
                skill_map[skill_id]["Xp"] = xp
            else:
                skills_list.append({"Id": skill_id, "Xp": xp})

            level_label.config(text=f"Level: {get_level_for_xp(xp)}")

        refresh_preview()

    ttk.Button(tab, text="Apply XP", command=apply_changes).grid(row=len(SKILL_IDS), column=0, columnspan=3, pady=10)