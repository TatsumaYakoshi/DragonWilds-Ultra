import tkinter as tk
from tkinter import ttk, messagebox
import os
from collections import OrderedDict
import base64

# === LOAD ITEM LIST FROM PYTHON FILE ===
from item_ids import ITEM_LIST

STORAGE_PRESETS = {
    "None": {
        "PersonalInventory": {}
    },
    "Equipment": {
        "PersonalInventory": {
            "0": {"GUID": "", "ItemData": "5PEcXkJHZY9PDqKb9Skqww", "Durability": 1400, "VitalShield": 25},
            "1": {"GUID": "", "ItemData": "0LL6JE9-pi2e3VSDOwqqYw", "Durability": 1500, "VitalShield": 25},
            "2": {"GUID": "", "ItemData": "mkSObERGptKuVly00uIfTQ", "Durability": 1400, "VitalShield": 0},
            "3": {"GUID": "", "ItemData": "RyuOEkWEWdGcvQqo2dPOgA", "Durability": 1300, "VitalShield": 0},
            "4": {"GUID": "", "ItemData": "P3_Aq0nAXu5dlFuBNGgyaw", "Durability": 1300, "VitalShield": 0},
            "5": {"GUID": "", "ItemData": "igveHUWYg2AeXe69EwW1PA", "Count": 5000000},
            "6": {"GUID": "", "ItemData": "QfPOk0c4rF6PIUqOxt0ytg", "Count": 5000000},
            "7": {"GUID": "", "ItemData": "YvBVZjzx_UKN9z1wIPzlrA", "Durability": 2400, "VitalShield": 0},
            "8": {"GUID": "", "ItemData": "gIoZIUIT52OUDkGFuzSBlw", "Durability": 1400, "VitalShield": 25},
            "9": {"GUID": "", "ItemData": "fr5LJkUvJRZ-DbqVbKaB4w", "Durability": 1400, "VitalShield": 25},
            "10": {"GUID": "", "ItemData": "l6qWl0-xTPdrhweMah3eTg", "Durability": 1400, "VitalShield": 0},
            "11": {"GUID": "", "ItemData": "FK7SwEPmPfVFztSXScvKQA", "Durability": 1050, "VitalShield": 0},
            "12": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "13": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "14": {"GUID": "", "ItemData": "TODWPUpA_YR0EnaqhMstcQ", "Count": 5000000},
            "15": {"GUID": "", "ItemData": "VfaynRGcAkammV5YUusfbA", "Durability": 2100, "VitalShield": 0},
            "16": {"GUID": "", "ItemData": "GutTdkwskIsX75i6-CilJA", "Durability": 1400, "VitalShield": 25},
            "17": {"GUID": "", "ItemData": "rXtN2EZOq9NpnL-WyVpF8Q", "Durability": 1500, "VitalShield": 25},
            "18": {"GUID": "", "ItemData": "uDBybUNuv5UipiSXb8BG-A", "Durability": 1400, "VitalShield": 0},
            "MaxSlotIndex": 18
        }
    },
    "Consumables": {
        "PersonalInventory": {
            "0": {"GUID": "", "ItemData": "GC6S207zgsmHryqJEdEQaQ", "Count": 5000000},
            "1": {"GUID": "", "ItemData": "3wV1xUv5zBDHRiaAk2qv7w", "Count": 5000000},
            "2": {"GUID": "", "ItemData": "-jEah0znNr-2UVmbHK-Hqg", "Count": 5000000},
            "3": {"GUID": "", "ItemData": "cZ6va0BSo6_5Dg2Pi23lUQ", "Count": 5000000},
            "4": {"GUID": "", "ItemData": "igveHUWYg2AeXe69EwW1PA", "Count": 5000000},
            "5": {"GUID": "", "ItemData": "ukjoSEXQTWbO6zSJvP5Z4Q", "Count": 5000000},
            "6": {"GUID": "", "ItemData": "-9Zin0B1C7GQgVKwKSR0hQ", "Count": 5000000},
            "7": {"GUID": "", "ItemData": "QfPOk0c4rF6PIUqOxt0ytg", "Count": 5000000},
            "MaxSlotIndex": 7
        }
    }
}

def generate_guid():
    return base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8').rstrip('=')

def build_item_maps(items):
    id_to_name = {}
    name_to_id = {}
    id_to_guids = {}
    id_to_extra = {}
    for item in items:
        name = item.get("SourceString")
        persistence_id = item.get("PersistenceID")
        guids = item.get("GUIDs", [])
        durability = item.get("Durability")
        vital_shield = item.get("VitalShield")
        if name and persistence_id:
            id_to_name[persistence_id] = name
            name_to_id[name] = persistence_id
            id_to_guids[persistence_id] = guids if isinstance(guids, list) else ([guids] if guids else [])
            extra = {}
            if durability is not None:
                extra["Durability"] = durability
            if vital_shield is not None:
                extra["VitalShield"] = vital_shield
            id_to_extra[persistence_id] = extra
    return id_to_name, name_to_id, id_to_guids, id_to_extra

def fix_max_slot_index(storage):
    slot_keys = [int(k) for k in storage.keys() if k.isdigit()]
    max_slot = max(slot_keys) if slot_keys else -1
    items_part = [(k, v) for k, v in storage.items() if k != "MaxSlotIndex"]
    fixed = OrderedDict(sorted(items_part, key=lambda x: int(x[0]) if x[0].isdigit() else -1))
    fixed["MaxSlotIndex"] = max_slot
    storage.clear()
    storage.update(fixed)

def guidify_dict(d):
    out = OrderedDict()
    for k, v in d.items():
        if isinstance(v, dict):
            entry = dict(v)
            if k != "MaxSlotIndex":
                entry["GUID"] = generate_guid()
            out[k] = entry
        else:
            out[k] = v
    return out

def setup_storage_tab(
    tab,
    data,
    refresh_json_preview,
    save_json_func,
    refresh_inventory_and_storage=None,
    storage_slot_count=20,
    storage_slot_start=0,
    storage_slot_end=19
):
    if data is None:
        data = {}
    if "PersonalInventory" not in data or not isinstance(data["PersonalInventory"], OrderedDict):
        if "PersonalInventory" in data and isinstance(data["PersonalInventory"], dict):
            old_st = data["PersonalInventory"]
            st_items = [(k, old_st[k]) for k in sorted(old_st, key=lambda x: int(x) if x.isdigit() else 10**6)]
            data["PersonalInventory"] = OrderedDict(st_items)
        else:
            data["PersonalInventory"] = OrderedDict()
    storage = data["PersonalInventory"]

    # === LOAD ITEM LIST HERE ===
    items = ITEM_LIST
    id_to_name, name_to_id, id_to_guids, id_to_extra = build_item_maps(items)
    all_item_names = sorted(name_to_id.keys())
    item_names = ["Empty"] + all_item_names

    for w in tab.winfo_children():
        w.destroy()

    main_frame = tk.Frame(tab)
    main_frame.pack(fill="both", expand=True)
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="y", padx=16, pady=16, anchor="n")

    # STORAGE PRESET SELECT (start at "None", shows what's currently in storage in dropdown)
    tk.Label(left_frame, text="Storage Presets", font=("Arial", 12, "bold")).pack(pady=(0,8))
    preset_frame = tk.Frame(left_frame)
    preset_frame.pack(anchor="w")
    storage_preset_options = list(STORAGE_PRESETS.keys()) + ["Current (Read from Storage)"]
    storage_preset_var = tk.StringVar(value="None")
    storage_preset_dropdown = ttk.Combobox(
        preset_frame, textvariable=storage_preset_var, values=storage_preset_options, state="readonly", width=22
    )
    storage_preset_dropdown.pack(side="left", padx=(5, 0))

    def show_current_storage_preset():
        # Read data["PersonalInventory"] and show in a popup window
        win = tk.Toplevel(tab)
        win.title("Current Storage Contents")
        text = tk.Text(win, width=70, height=24, font=("Consolas", 10))
        text.pack(fill="both", expand=True)
        if "PersonalInventory" in data and isinstance(data["PersonalInventory"], dict):
            display = json.dumps(data["PersonalInventory"], indent=2)
        else:
            display = "(PersonalInventory is empty)"
        text.insert("1.0", display)
        text.config(state="disabled")
        tk.Button(win, text="Close", command=win.destroy).pack(pady=8)

    def apply_storage_preset():
        preset_name = storage_preset_var.get()
        if preset_name == "None":
            messagebox.showinfo("Info", "Please select a preset to apply.")
            return
        if preset_name == "Current (Read from Storage)":
            show_current_storage_preset()
            return
        preset = STORAGE_PRESETS.get(preset_name)
        if not preset or "PersonalInventory" not in preset:
            messagebox.showerror("Error", "Invalid storage preset.")
            return
        data["PersonalInventory"] = guidify_dict(preset["PersonalInventory"])
        fix_max_slot_index(data["PersonalInventory"])
        save_json_func(data)
        refresh_json_preview()
        if refresh_inventory_and_storage:
            refresh_inventory_and_storage()
        update_storage_items()
        try:
            messagebox.showinfo("Success", f"{preset_name} storage preset applied.")
        except Exception:
            pass
    ttk.Button(preset_frame, text="Apply", command=apply_storage_preset, width=7).pack(side="left", padx=(10, 0))

    # Add/Update Storage Slot
    tk.Label(left_frame, text="Add/Update Storage Slot", font=("Arial", 11, "bold")).pack(pady=(18,0), anchor="w")
    # Slot and Amount fields side-by-side, right above Set Slot button
    slot_amount_frame = tk.Frame(left_frame)
    slot_amount_frame.pack(anchor="w", pady=(4, 0))
    tk.Label(slot_amount_frame, text="Slot:").pack(side="left")
    slot_var = tk.StringVar(value="0")
    slot_options = [str(i) for i in range(storage_slot_start, storage_slot_end + 1)]
    slot_combo = ttk.Combobox(slot_amount_frame, textvariable=slot_var, values=slot_options, width=6, state="readonly")
    slot_combo.pack(side="left", padx=(5, 9))
    tk.Label(slot_amount_frame, text="Amount:").pack(side="left")
    count_var = tk.StringVar(value="1")
    count_entry = tk.Entry(slot_amount_frame, textvariable=count_var, width=8)
    count_entry.pack(side="left", padx=(2, 0))

    # Filterable item list
    tk.Label(left_frame, text="Item:").pack(anchor="w", pady=(8,0))
    filter_frame = tk.Frame(left_frame)
    filter_frame.pack(anchor="w", fill="x")
    tk.Label(filter_frame, text="Filter:", anchor="w").pack(side="left", padx=(0,2))
    item_search_var = tk.StringVar()
    search_entry = tk.Entry(filter_frame, textvariable=item_search_var, width=22)
    search_entry.pack(side="left")
    item_var = tk.StringVar(value="Empty")
    filtered_item_names = ["Empty"] + all_item_names.copy()
    def update_combobox_list(event=None):
        filter_text = item_search_var.get().lower()
        if filter_text == "":
            filtered = all_item_names
        else:
            filtered = [name for name in all_item_names if filter_text in name.lower()]
        filtered_item_names.clear()
        filtered_item_names.extend(["Empty"] + filtered)
        item_combo["values"] = filtered_item_names
        if item_var.get() not in filtered_item_names:
            item_var.set("Empty")
    search_entry.bind("<KeyRelease>", update_combobox_list)
    search_entry.bind("<FocusIn>", update_combobox_list)
    item_combo = ttk.Combobox(left_frame, textvariable=item_var, values=filtered_item_names, width=30, state="readonly")
    item_combo.pack(anchor="w")

    def find_item_id(item_name):
        return name_to_id.get(item_name.strip())
    def get_extra_for_pid(pid):
        return id_to_extra.get(pid, {})
    def save_and_refresh():
        refresh_json_preview()
        save_json_func(data)
    def add_storage_item(data, slot_index, item_id, count):
        slot_key = str(slot_index)
        guid = generate_guid()
        extra = get_extra_for_pid(item_id)
        entry = {
            "GUID": guid,
            "ItemData": item_id,
            "Count": count
        }
        if "Durability" in extra:
            entry["Durability"] = extra["Durability"]
        if "VitalShield" in extra:
            entry["VitalShield"] = extra["VitalShield"]
        storage[slot_key] = entry
        fix_max_slot_index(storage)
    def remove_storage_slot(slot_key):
        if slot_key in storage:
            del storage[slot_key]
            fix_max_slot_index(storage)
    def add_update_slot():
        slot = slot_var.get()
        item_name = item_var.get()
        count_text = count_var.get()
        try:
            slot_index = int(slot)
            if slot_index < storage_slot_start or slot_index > storage_slot_end:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", f"Slot must be an integer between {storage_slot_start} and {storage_slot_end}")
            return
        slot_key = str(slot_index)
        if item_name == "Empty":
            remove_storage_slot(slot_key)
            save_and_refresh()
            update_storage_items()
            return
        try:
            count = int(count_text)
            if count < 1:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", f"Invalid count: '{count_text}' (must be a positive integer)")
            return
        item_id = find_item_id(item_name)
        if not item_id:
            messagebox.showerror("Error", f"Item not found: '{item_name}'.")
            return
        add_storage_item(data, slot_index, item_id, count)
        save_and_refresh()
        update_storage_items()
    tk.Button(left_frame, text="Set Slot", command=add_update_slot, width=20).pack(pady=12)

    # BULK ADD (all slots 0-19)
    bulk_frame = tk.Frame(left_frame)
    bulk_frame.pack(anchor="w", fill="x", pady=(20, 0))
    tk.Label(bulk_frame, text="Bulk Set Storage", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 4))
    tk.Label(bulk_frame, text="Item:").grid(row=1, column=0, sticky="w")
    bulk_item_var = tk.StringVar(value="Empty")
    bulk_item_combo = ttk.Combobox(bulk_frame, textvariable=bulk_item_var, values=item_names, width=22, state="readonly")
    bulk_item_combo.grid(row=1, column=1, sticky="w")
    tk.Label(bulk_frame, text="Amount:").grid(row=1, column=2, sticky="w")
    bulk_count_var = tk.StringVar(value="1")
    bulk_count_entry = tk.Entry(bulk_frame, textvariable=bulk_count_var, width=7)
    bulk_count_entry.grid(row=1, column=3, sticky="w")
    def bulk_apply():
        item_name = bulk_item_var.get()
        count_text = bulk_count_var.get()
        if item_name == "Empty":
            messagebox.showerror("Error", "Bulk: Please select an item.")
            return
        try:
            count = int(count_text)
            if count < 1:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", f"Bulk: Invalid count '{count_text}'")
            return
        item_id = find_item_id(item_name)
        if not item_id:
            messagebox.showerror("Error", f"Bulk: Item not found '{item_name}'")
            return
        for idx in range(storage_slot_start, storage_slot_end + 1):
            add_storage_item(data, idx, item_id, count)
        save_and_refresh()
        update_storage_items()
    tk.Button(bulk_frame, text="Apply to All Slots", command=bulk_apply, width=20).grid(row=2, column=0, columnspan=4, pady=8)

    # BULK INFO AT BOTTOM LEFT
    bulk_info_frame = tk.Frame(left_frame)
    bulk_info_frame.pack(side="bottom", fill="x", pady=(20, 0), anchor="s")
    tk.Label(
        bulk_info_frame,
        text=(
            "Slots 0-19 are your Storage Slots"
        ),
        justify="left",
        anchor="w"
    ).pack(anchor="w")

    # STORAGE LIST
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True, padx=16, pady=16)
    tk.Label(right_frame, text="Your Storage:", font=("Arial", 12, "bold")).pack(anchor="nw", pady=(0,8), padx=4)
    storage_list_frame = tk.Frame(right_frame, borderwidth=1, relief="sunken")
    storage_list_frame.pack(fill="both", expand=True, padx=4, pady=(0,10))
    storage_canvas = tk.Canvas(storage_list_frame, borderwidth=0)
    storage_scrollbar = ttk.Scrollbar(storage_list_frame, orient="vertical", command=storage_canvas.yview)
    storage_inner_frame = tk.Frame(storage_canvas)
    storage_inner_frame.bind(
        "<Configure>",
        lambda e: storage_canvas.configure(scrollregion=storage_canvas.bbox("all"))
    )
    storage_canvas.create_window((0, 0), window=storage_inner_frame, anchor="nw")
    storage_canvas.configure(yscrollcommand=storage_scrollbar.set)
    storage_canvas.pack(side="left", fill="both", expand=True)
    storage_scrollbar.pack(side="right", fill="y")
    def update_storage_items():
        for w in storage_inner_frame.winfo_children():
            w.destroy()
        shown = False
        valid_slots = []
        for idx in storage:
            if idx == "MaxSlotIndex":
                continue
            try:
                i = int(idx)
                valid_slots.append((i, idx))
            except Exception:
                continue
        valid_slots.sort()
        for i, idx in valid_slots:
            entry = storage[idx]
            item_id = entry.get("ItemData", None)
            count = entry.get("Count", 1)
            item_name = id_to_name.get(item_id, f"Unknown ({item_id})")
            guid = entry.get("GUID", "")
            durability = entry.get("Durability", None)
            vital_shield = entry.get("VitalShield", None)
            row = tk.Frame(storage_inner_frame)
            row.pack(fill="x", padx=2, pady=1)
            slot_info = f"Slot {idx} (x{count})"
            tk.Label(row, text=slot_info, width=18, anchor="w").pack(side="left")
            tk.Label(row, text=f"{item_name}", width=28, anchor="w").pack(side="left")
            def clear_slot_closure(idx=idx):
                if idx in storage:
                    del storage[idx]
                    fix_max_slot_index(storage)
                save_json_func(data)
                refresh_json_preview()
                update_storage_items()
            tk.Button(row, text="Remove", command=clear_slot_closure, width=8).pack(side="left", padx=(2,2))
            tk.Label(row, text=f"{guid}", width=26, anchor="w").pack(side="left")
            extras = []
            if durability is not None:
                extras.append(f"Dur: {durability}")
            if vital_shield is not None:
                extras.append(f"Shield: {vital_shield}")
            tk.Label(row, text=" | ".join(extras), width=18, anchor="w").pack(side="left")
            shown = True
        if not shown:
            tk.Label(storage_inner_frame, text="No items in storage.").pack(anchor="w", padx=4, pady=8)

    update_storage_items()