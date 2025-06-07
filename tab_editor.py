import tkinter as tk
from tkinter import ttk, messagebox
import os
from collections import OrderedDict
import base64

# === LOAD ITEM LIST FROM PYTHON FILE ===
from item_ids import ITEM_LIST

def generate_guid():
    return base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8').rstrip('=')

GEAR_LOADOUTS = {
    "Melee": {
        "Inventory": {
            "0": {"GUID": "", "ItemData": "RyuOEkWEWdGcvQqo2dPOgA", "Durability": 1300, "VitalShield": 0},
            "1": {"GUID": "", "ItemData": "P3_Aq0nAXu5dlFuBNGgyaw", "Durability": 1300, "VitalShield": 0},
            "MaxSlotIndex": 1
        },
        "Loadout": {
            "0": {"GUID": "", "ItemData": "5PEcXkJHZY9PDqKb9Skqww", "Durability": 1400, "VitalShield": 25},
            "1": {"GUID": "", "ItemData": "0LL6JE9-pi2e3VSDOwqqYw", "Durability": 1500, "VitalShield": 25},
            "2": {"GUID": "", "ItemData": "mkSObERGptKuVly00uIfTQ", "Durability": 1400, "VitalShield": 0},
            "3": {"GUID": "", "ItemData": "24_UV0P2zlDAbcy48UOCkA", "VitalShield": 0},
            "7": {"PlayerInventoryItemIndex": 1},
            "8": {"PlayerInventoryItemIndex": 0},
            "MaxSlotIndex": 8
        }
    },
    "Magic": {
        "Inventory": {
            "0": {"GUID": "", "ItemData": "Hcq0C0UjvN3n8q-X2uqa7w", "Durability": 1300, "VitalShield": 0},
            "32": {"GUID": "", "ItemData": "iKbF7k2XvufGqqyg5rK-vQ", "Count": 999},
            "33": {"GUID": "", "ItemData": "bbLdJRhwPEWt1ScENYRUCg", "Count": 999},
            "34": {"GUID": "", "ItemData": "Dvo6TE2d7YNnoni8XbKYzw", "Count": 999, "VitalShield": 0},
            "35": {"GUID": "", "ItemData": "4wdYZE-FFMhS9Iia0ftWDg", "Count": 999},
            "36": {"GUID": "", "ItemData": "lCE7i3iXGUuHv7FphIOcXg", "Count": 999},
            "37": {"GUID": "", "ItemData": "_QMgbMYhjU-9jAD_euFbyQ", "Count": 999, "VitalShield": 0},
            "38": {"GUID": "", "ItemData": "_c9JTkwKy8s88GWv586hbQ", "Count": 999},
            "MaxSlotIndex": 38
        },
        "Loadout": {
            "0": {"GUID": "", "ItemData": "GutTdkwskIsX75i6-CilJA", "Durability": 1400, "VitalShield": 25},
            "1": {"GUID": "", "ItemData": "rXtN2EZOq9NpnL-WyVpF8Q", "Durability": 1500, "VitalShield": 25},
            "2": {"GUID": "", "ItemData": "uDBybUNuv5UipiSXb8BG-A", "Durability": 1400, "VitalShield": 0},
            "3": {"GUID": "", "ItemData": "71LhGUmAvrlALY6KcS8W3Q", "VitalShield": 0},
            "6": {"PlayerInventoryItemIndex": 34},
            "7": {"PlayerInventoryItemIndex": 0},
            "8": {"PlayerInventoryItemIndex": 0},
            "MaxSlotIndex": 8
        }
    },
    "Ranged": {
        "Inventory": {
            "0": {"GUID": "", "ItemData": "FK7SwEPmPfVFztSXScvKQA", "Durability": 1025, "VitalShield": 0},
            "1": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 95, "VitalShield": 0},
            "2": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "3": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "4": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "5": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "6": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "7": {"GUID": "", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
            "MaxSlotIndex": 7
        },
        "Loadout": {
            "0": {"GUID": "", "ItemData": "gIoZIUIT52OUDkGFuzSBlw", "Durability": 1400, "VitalShield": 25},
            "1": {"GUID": "", "ItemData": "fr5LJkUvJRZ-DbqVbKaB4w", "Durability": 1400, "VitalShield": 25},
            "2": {"GUID": "", "ItemData": "l6qWl0-xTPdrhweMah3eTg", "Durability": 1400, "VitalShield": 0},
            "3": {"GUID": "", "ItemData": "qANQGE8VKB_lSNeI-PHxGQ", "VitalShield": 0},
            "5": {"PlayerInventoryItemIndex": 1},
            "7": {"PlayerInventoryItemIndex": 0},
            "8": {"PlayerInventoryItemIndex": 0},
            "MaxSlotIndex": 8
        }
    }
}

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

def fix_max_slot_index(inventory):
    slot_keys = [int(k) for k in inventory.keys() if k.isdigit()]
    max_slot = max(slot_keys) if slot_keys else -1
    items_part = [(k, v) for k, v in inventory.items() if k != "MaxSlotIndex"]
    fixed = OrderedDict(sorted(items_part, key=lambda x: int(x[0]) if x[0].isdigit() else -1))
    fixed["MaxSlotIndex"] = max_slot
    inventory.clear()
    inventory.update(fixed)

def is_rune_or_quest_slot(idx):
    idx = int(idx)
    return (32 <= idx <= 55 or 56 <= idx <= 72)

def setup_editor_tab(
    tab,
    data,
    refresh_json_preview,
    save_json_func,
    refresh_inventory_and_storage=None,
    inv_slot_count=80,
    inv_slot_start=0,
    inv_slot_end=79
):
    if data is None:
        data = {}

    # === LOAD ITEM LIST HERE ===
    items = ITEM_LIST
    id_to_name, name_to_id, id_to_guids, id_to_extra = build_item_maps(items)
    all_item_names = sorted(name_to_id.keys())
    item_names = ["Empty"] + all_item_names

    for w in tab.winfo_children():
        w.destroy()

    if "Inventory" not in data or not isinstance(data["Inventory"], OrderedDict):
        if "Inventory" in data and isinstance(data["Inventory"], dict):
            old_inv = data["Inventory"]
            inv_items = [(k, old_inv[k]) for k in sorted(old_inv, key=lambda x: int(x) if x.isdigit() else 10**6)]
            data["Inventory"] = OrderedDict(inv_items)
        else:
            data["Inventory"] = OrderedDict()
    inventory = data["Inventory"]
    if "Loadout" not in data or not isinstance(data["Loadout"], OrderedDict):
        if "Loadout" in data and isinstance(data["Loadout"], dict):
            old_ld = data["Loadout"]
            ld_items = [(k, old_ld[k]) for k in sorted(old_ld, key=lambda x: int(x) if x.isdigit() else 10**6)]
            data["Loadout"] = OrderedDict(ld_items)
        else:
            data["Loadout"] = OrderedDict()
    loadout = data["Loadout"]

    main_frame = tk.Frame(tab)
    main_frame.pack(fill="both", expand=True)
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="y", padx=16, pady=16, anchor="n")

    # GEAR PRESET SELECT (start at "None")
    tk.Label(left_frame, text="Gear Loadouts", font=("Arial", 12, "bold")).pack(pady=(0,8))
    preset_frame = tk.Frame(left_frame)
    preset_frame.pack(anchor="w")
    gear_preset_options = ["None"] + list(GEAR_LOADOUTS.keys())
    gear_loadout_var = tk.StringVar(value="None")
    gear_loadout_dropdown = ttk.Combobox(
        preset_frame, textvariable=gear_loadout_var, values=gear_preset_options, state="readonly", width=12
    )
    gear_loadout_dropdown.pack(side="left", padx=(5, 0))
    def guidify_dict(d):
        out = OrderedDict()
        for k, v in d.items():
            if isinstance(v, dict):
                entry = dict(v)
                if "PlayerInventoryItemIndex" not in entry and k != "MaxSlotIndex":
                    entry["GUID"] = generate_guid()
                out[k] = entry
            else:
                out[k] = v
        return out
    def apply_gear_loadout():
        preset_name = gear_loadout_var.get()
        if preset_name == "None":
            messagebox.showinfo("Info", "Please select a preset to apply.")
            return
        gear = GEAR_LOADOUTS.get(preset_name)
        if not gear:
            messagebox.showerror("Error", "Invalid gear loadout preset.")
            return
        data["Inventory"] = guidify_dict(gear["Inventory"])
        data["Loadout"] = guidify_dict(gear["Loadout"])
        fix_max_slot_index(data["Inventory"])
        fix_max_slot_index(data["Loadout"])
        save_json_func(data)
        refresh_json_preview()
        if refresh_inventory_and_storage:
            refresh_inventory_and_storage()
        update_your_items()
        update_loadout_items()
        try:
            messagebox.showinfo("Success", f"{preset_name} gear loadout applied.")
        except Exception:
            pass
    ttk.Button(preset_frame, text="Apply", command=apply_gear_loadout, width=7).pack(side="left", padx=(10, 0))

    # Add/Update Inventory Slot
    tk.Label(left_frame, text="Add/Update Inventory Slot", font=("Arial", 11, "bold")).pack(pady=(18,0), anchor="w")
    # Slot and Amount fields side-by-side, right above Set Slot button
    slot_amount_frame = tk.Frame(left_frame)
    slot_amount_frame.pack(anchor="w", pady=(4, 0))
    tk.Label(slot_amount_frame, text="Slot:").pack(side="left")
    slot_var = tk.StringVar(value="0")
    slot_options = [str(i) for i in range(inv_slot_start, inv_slot_end + 1)]
    slot_combo = ttk.Combobox(slot_amount_frame, textvariable=slot_var, values=slot_options, width=6, state="readonly")
    slot_combo.pack(side="left", padx=(5, 9))
    tk.Label(slot_amount_frame, text="Amount:").pack(side="left")
    count_var = tk.StringVar(value="1")
    count_entry = tk.Entry(slot_amount_frame, textvariable=count_var, width=8)
    count_entry.pack(side="left", padx=(2, 0))

    # Filterable item list - Filter ABOVE ComboBox now
    filter_item_frame = tk.Frame(left_frame)
    filter_item_frame.pack(anchor="w", fill="x", pady=(8, 0))
    tk.Label(filter_item_frame, text="Filter:", anchor="w").pack(side="top", anchor="w")
    item_search_var = tk.StringVar()
    search_entry = tk.Entry(filter_item_frame, textvariable=item_search_var, width=22)
    search_entry.pack(side="top", anchor="w", pady=(0, 2))
    tk.Label(left_frame, text="Item:").pack(anchor="w")
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
    def add_inventory_item(data, slot_index, item_id, count):
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
        inventory[slot_key] = entry
        fix_max_slot_index(inventory)
    def remove_inventory_slot(slot_key):
        if slot_key in inventory:
            del inventory[slot_key]
            fix_max_slot_index(inventory)
    def add_update_slot():
        slot = slot_var.get()
        item_name = item_var.get()
        count_text = count_var.get()
        try:
            slot_index = int(slot)
            if slot_index < inv_slot_start or slot_index > inv_slot_end:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", f"Slot must be an integer between {inv_slot_start} and {inv_slot_end}")
            return
        slot_key = str(slot_index)
        if item_name == "Empty":
            remove_inventory_slot(slot_key)
            save_and_refresh()
            update_your_items()
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
        add_inventory_item(data, slot_index, item_id, count)
        save_and_refresh()
        update_your_items()
    tk.Button(left_frame, text="Set Slot", command=add_update_slot, width=20).pack(pady=12)

    # BULK ADD (no slot selection, always over main slots only)
    bulk_frame = tk.Frame(left_frame)
    bulk_frame.pack(anchor="w", fill="x", pady=(20, 0))
    tk.Label(bulk_frame, text="Bulk Set Inventory", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 4))

    # Filter row (on its own line)
    filter_row = tk.Frame(bulk_frame)
    filter_row.pack(anchor="w", fill="x")
    tk.Label(filter_row, text="Filter:").pack(side="left")
    bulk_filter_var = tk.StringVar()
    bulk_filter_entry = tk.Entry(filter_row, textvariable=bulk_filter_var, width=24)
    bulk_filter_entry.pack(side="left", padx=(4, 0))

    # Item row (on its own line)
    item_row = tk.Frame(bulk_frame)
    item_row.pack(anchor="w", fill="x", pady=(4, 0))
    tk.Label(item_row, text="Item:").pack(side="left")
    bulk_item_var = tk.StringVar(value="Empty")
    filtered_bulk_item_names = ["Empty"] + all_item_names.copy()
    bulk_item_combo = ttk.Combobox(item_row, textvariable=bulk_item_var, values=filtered_bulk_item_names, width=28, state="readonly")
    bulk_item_combo.pack(side="left", padx=(4,0))

    # Amount row (on its own line)
    amount_row = tk.Frame(bulk_frame)
    amount_row.pack(anchor="w", fill="x", pady=(4, 0))
    tk.Label(amount_row, text="Amount:").pack(side="left")
    bulk_count_var = tk.StringVar(value="1")
    bulk_count_entry = tk.Entry(amount_row, textvariable=bulk_count_var, width=10)
    bulk_count_entry.pack(side="left", padx=(4, 0))

    def update_bulk_item_list(event=None):
        filter_text = bulk_filter_var.get().lower()
        if filter_text == "":
            filtered = all_item_names
        else:
            filtered = [name for name in all_item_names if filter_text in name.lower()]
        filtered_bulk_item_names.clear()
        filtered_bulk_item_names.extend(["Empty"] + filtered)
        bulk_item_combo["values"] = filtered_bulk_item_names
        if bulk_item_var.get() not in filtered_bulk_item_names:
            bulk_item_var.set("Empty")
    bulk_filter_entry.bind("<KeyRelease>", update_bulk_item_list)
    bulk_filter_entry.bind("<FocusIn>", update_bulk_item_list)
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
        # Only main slots: 0-7 (action bar) and 8-31 (main inv), skip runes/quest slots entirely
        for idx in list(range(0, 8)) + list(range(8, 32)):
            add_inventory_item(data, idx, item_id, count)
        save_and_refresh()
        update_your_items()
    tk.Button(bulk_frame, text="Apply to Main Slots", command=bulk_apply, width=24).pack(pady=8)

    # BULK INFO AT BOTTOM LEFT
    bulk_info_frame = tk.Frame(left_frame)
    bulk_info_frame.pack(side="bottom", fill="x", pady=(20, 0), anchor="s")
    tk.Label(
        bulk_info_frame,
        text=(
            "Slots 0-7 are your Action Bar Slots\n"
            "Slots 8-31 are your Main Inventory Slots\n"
            "Slots 32-55 are your Rune Inventory Slots\n"
            "Slots 56-72 are your Quest Inventory slots"
        ),
        justify="left",
        anchor="w"
    ).pack(anchor="w")

    # INVENTORY LIST
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True, padx=16, pady=16)
    tk.Label(right_frame, text="Your Inventory:", font=("Arial", 12, "bold")).pack(anchor="nw", pady=(0,8), padx=4)
    items_list_frame = tk.Frame(right_frame, borderwidth=1, relief="sunken")
    items_list_frame.pack(fill="both", expand=True, padx=4, pady=(0,10))
    items_canvas = tk.Canvas(items_list_frame, borderwidth=0)
    items_scrollbar = ttk.Scrollbar(items_list_frame, orient="vertical", command=items_canvas.yview)
    items_inner_frame = tk.Frame(items_canvas)
    items_inner_frame.bind(
        "<Configure>",
        lambda e: items_canvas.configure(scrollregion=items_canvas.bbox("all"))
    )
    items_canvas.create_window((0, 0), window=items_inner_frame, anchor="nw")
    items_canvas.configure(yscrollcommand=items_scrollbar.set)
    items_canvas.pack(side="left", fill="both", expand=True)
    items_scrollbar.pack(side="right", fill="y")
    def update_your_items():
        for w in items_inner_frame.winfo_children():
            w.destroy()
        shown = False
        valid_slots = []
        for idx in inventory:
            if idx == "MaxSlotIndex":
                continue
            try:
                i = int(idx)
                valid_slots.append((i, idx))
            except Exception:
                continue
        valid_slots.sort()
        for i, idx in valid_slots:
            entry = inventory[idx]
            item_id = entry.get("ItemData", None)
            count = entry.get("Count", 1)
            item_name = id_to_name.get(item_id, f"Unknown ({item_id})")
            guid = entry.get("GUID", "")
            durability = entry.get("Durability", None)
            vital_shield = entry.get("VitalShield", None)
            row = tk.Frame(items_inner_frame)
            row.pack(fill="x", padx=2, pady=1)
            slot_info = f"Slot {idx} (x{count})"
            tk.Label(row, text=slot_info, width=18, anchor="w").pack(side="left")
            tk.Label(row, text=f"{item_name}", width=28, anchor="w").pack(side="left")
            def clear_slot_closure(idx=idx):
                if idx in inventory:
                    del inventory[idx]
                    fix_max_slot_index(inventory)
                save_json_func(data)
                refresh_json_preview()
                update_your_items()
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
            tk.Label(items_inner_frame, text="No items in inventory.").pack(anchor="w", padx=4, pady=8)

    # LOADOUT LIST
    tk.Label(right_frame, text="Your Loadout:", font=("Arial", 12, "bold")).pack(anchor="nw", pady=(14,8), padx=4)
    loadout_list_frame = tk.Frame(right_frame, borderwidth=1, relief="sunken")
    loadout_list_frame.pack(fill="both", expand=True, padx=4, pady=(0,10))
    loadout_canvas = tk.Canvas(loadout_list_frame, borderwidth=0)
    loadout_scrollbar = ttk.Scrollbar(loadout_list_frame, orient="vertical", command=loadout_canvas.yview)
    loadout_inner_frame = tk.Frame(loadout_canvas)
    loadout_inner_frame.bind(
        "<Configure>",
        lambda e: loadout_canvas.configure(scrollregion=loadout_canvas.bbox("all"))
    )
    loadout_canvas.create_window((0, 0), window=loadout_inner_frame, anchor="nw")
    loadout_canvas.configure(yscrollcommand=loadout_scrollbar.set)
    loadout_canvas.pack(side="left", fill="both", expand=True)
    loadout_scrollbar.pack(side="right", fill="y")
    def update_loadout_items():
        for w in loadout_inner_frame.winfo_children():
            w.destroy()
        shown = False
        valid_slots = []
        for idx in loadout:
            if idx == "MaxSlotIndex":
                continue
            try:
                i = int(idx)
                valid_slots.append((i, idx))
            except Exception:
                continue
        valid_slots.sort()
        for i, idx in valid_slots:
            entry = loadout[idx]
            if "PlayerInventoryItemIndex" in entry:
                row = tk.Frame(loadout_inner_frame)
                row.pack(fill="x", padx=2, pady=1)
                tk.Label(row, text=f"Slot {idx}", width=7, anchor="w").pack(side="left")
                tk.Label(row, text=f"Ref Inv Slot {entry['PlayerInventoryItemIndex']}", width=30, anchor="w", fg="#0a0").pack(side="left")
                continue
            item_id = entry.get("ItemData", None)
            count = entry.get("Count", 1)
            item_name = id_to_name.get(item_id, f"Unknown ({item_id})")
            guid = entry.get("GUID", "")
            durability = entry.get("Durability", None)
            vital_shield = entry.get("VitalShield", None)
            row = tk.Frame(loadout_inner_frame)
            row.pack(fill="x", padx=2, pady=1)
            tk.Label(row, text=f"Slot {idx}", width=7, anchor="w").pack(side="left")
            tk.Label(row, text=f"{item_name}", width=22, anchor="w").pack(side="left")
            tk.Label(row, text=f"x{count}", width=7, anchor="w").pack(side="left")
            tk.Label(row, text=f"{guid}", width=26, anchor="w").pack(side="left")
            extras = []
            if durability is not None:
                extras.append(f"Dur: {durability}")
            if vital_shield is not None:
                extras.append(f"Shield: {vital_shield}")
            tk.Label(row, text=" | ".join(extras), width=18, anchor="w").pack(side="left")
            shown = True
        if not shown:
            tk.Label(loadout_inner_frame, text="No items in loadout.").pack(anchor="w", padx=4, pady=8)

    update_your_items()
    update_loadout_items()