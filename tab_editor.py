import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from collections import OrderedDict

def get_itemid_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data", "ItemID.txt")

def load_items_from_file(itemfile_path):
    with open(itemfile_path, "r", encoding="utf-8") as f:
        raw = f.read()
        if raw.lstrip().startswith("["):
            items = json.loads(raw)
        else:
            raw = "\n".join(line.split("|",1)[1].strip() if "|" in line else line for line in raw.splitlines())
            items = json.loads(raw)
        return items

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

def setup_editor_tab(
    tab,
    data,
    refresh_json_preview,
    save_json_func,
    slot_count=56,
    rune_slot_start=32,
    rune_slot_end=55,
    quest_slot_start=56,
    quest_slot_end=72
):
    if data is None:
        data = {}
    itemfile_path = get_itemid_path()
    if not os.path.isfile(itemfile_path):
        messagebox.showerror("Error", f"ItemID.txt not found at:\n{itemfile_path}")
        return

    items = load_items_from_file(itemfile_path)
    id_to_name, name_to_id, id_to_guids, id_to_extra = build_item_maps(items)
    all_item_names = sorted(name_to_id.keys())
    item_names = ["Empty"] + all_item_names

    for w in tab.winfo_children():
        w.destroy()

    # Always use OrderedDict for inventory
    if "Inventory" not in data or not isinstance(data["Inventory"], OrderedDict):
        # If loading from a save, retain the slot ordering
        if "Inventory" in data and isinstance(data["Inventory"], dict):
            old_inv = data["Inventory"]
            inv_items = [(k, old_inv[k]) for k in sorted(old_inv, key=lambda x: int(x) if x.isdigit() else 10**6)]
            data["Inventory"] = OrderedDict(inv_items)
        else:
            data["Inventory"] = OrderedDict()
    inventory = data["Inventory"]

    main_frame = tk.Frame(tab)
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="y", padx=16, pady=16, anchor="n")

    tk.Label(left_frame, text="Add or Update Slot", font=("Arial", 12, "bold")).pack(pady=(0,8))

    tk.Label(left_frame, text="Slot:").pack(anchor="w")
    slot_var = tk.StringVar(value="0")
    slot_options = [str(i) for i in range(quest_slot_end+1)]
    slot_combo = ttk.Combobox(left_frame, textvariable=slot_var, values=slot_options, width=6, state="readonly")
    slot_combo.pack(anchor="w")

    # --- Searchable Item Box ---
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
        # If current selection doesn't match, reset to "Empty"
        if item_var.get() not in filtered_item_names:
            item_var.set("Empty")
    search_entry.bind("<KeyRelease>", update_combobox_list)
    search_entry.bind("<FocusIn>", update_combobox_list)

    item_combo = ttk.Combobox(left_frame, textvariable=item_var, values=filtered_item_names, width=30, state="readonly")
    item_combo.pack(anchor="w")

    tk.Label(left_frame, text="Amount:").pack(anchor="w", pady=(8,0))
    count_var = tk.StringVar(value="1")
    count_entry = tk.Entry(left_frame, textvariable=count_var, width=8)
    count_entry.pack(anchor="w")

    def find_item_id(item_name):
        return name_to_id.get(item_name.strip())

    def get_first_guid_for_pid(pid):
        guids = id_to_guids.get(pid, [])
        return guids[0] if guids else ""

    def get_extra_for_pid(pid):
        return id_to_extra.get(pid, {})

    def save_and_refresh():
        refresh_json_preview()
        save_json_func(data)

    def add_inventory_item(data, slot_index, item_id, count):
        slot_key = str(slot_index)
        guid = get_first_guid_for_pid(item_id)
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
            if slot_index < 0 or slot_index > quest_slot_end:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", f"Slot must be an integer between 0 and {quest_slot_end}")
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

    add_btn = tk.Button(left_frame, text="Set Slot", command=add_update_slot, width=20)
    add_btn.pack(pady=12)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True, padx=16, pady=16)

    tk.Label(right_frame, text="Your Items:", font=("Arial", 12, "bold")).pack(anchor="nw", pady=(0,8), padx=4)

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
        # Show all slots in inventory except MaxSlotIndex, sorted by slot number
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
            tk.Label(row, text=f"Slot {idx}", width=7, anchor="w").pack(side="left")
            tk.Label(row, text=f"{item_name}", width=28, anchor="w").pack(side="left")
            def clear_slot_closure(idx=idx):
                remove_inventory_slot(idx)
                save_and_refresh()
                update_your_items()
            tk.Button(row, text="Remove", command=clear_slot_closure, width=8).pack(side="left", padx=(2,2))
            tk.Label(row, text=f"x{count}", width=7, anchor="w").pack(side="left")
            tk.Label(row, text=f"{guid}", width=26, anchor="w").pack(side="left")
            extra_info = []
            if durability is not None:
                extra_info.append(f"Dur: {durability}")
            if vital_shield is not None:
                extra_info.append(f"Shield: {vital_shield}")
            tk.Label(row, text=" | ".join(extra_info), width=20, anchor="w").pack(side="left")
            shown = True
        if not shown:
            tk.Label(items_inner_frame, text="No items in inventory.").pack(anchor="w", padx=4, pady=8)

    bulk_info_frame = tk.Frame(right_frame)
    bulk_info_frame.pack(fill="x", pady=(4,0), anchor="w")

    info_label = tk.Label(
        bulk_info_frame,
        text=(
            "Slots 0-7 are your Action Bar Slots\n"
            "Slots 8-31 are your Main Inventory Slots\n"
            "Slots 32-55 are your Rune Inventory Slots\n"
            "Slots 56-72 are your Quest Inventory slots"
        ),
        justify="left",
        anchor="w"
    )
    info_label.pack(side="left", padx=(0,16), pady=0)

    bulk_frame = tk.Frame(bulk_info_frame)
    bulk_frame.pack(side="left", fill="x")

    tk.Label(bulk_frame, text="Bulk Set", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0,4))

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
        for idx in range(quest_slot_end+1):
            if rune_slot_start <= idx <= rune_slot_end:
                continue
            if quest_slot_start <= idx <= quest_slot_end:
                continue
            add_inventory_item(data, idx, item_id, count)
        save_and_refresh()
        update_your_items()

    tk.Button(bulk_frame, text="Apply to All", command=bulk_apply, width=20).grid(row=2, column=0, columnspan=4, pady=8)

    update_your_items()