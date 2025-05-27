import tkinter as tk
from tkinter import ttk, messagebox

GEAR_LOADOUTS = {
"Melee": {
"Inventory": {
"0": {"GUID": "Cv68wUF_AHIyyTeJXBw_MA", "ItemData": "RyuOEkWEWdGcvQqo2dPOgA", "Durability": 1300, "VitalShield": 0},
"1": {"GUID": "Md8FO0h5L86bncOGevpQ5g", "ItemData": "P3_Aq0nAXu5dlFuBNGgyaw", "Durability": 1300, "VitalShield": 0},
"MaxSlotIndex": 1
},
"Loadout": {
"0": {"GUID": "aOC0JEgqKEI1AMWBNDRs3g", "ItemData": "5PEcXkJHZY9PDqKb9Skqww", "Durability": 1400, "VitalShield": 25},
"1": {"GUID": "HQp2TU7j6H7DuIGhkg_8cw", "ItemData": "0LL6JE9-pi2e3VSDOwqqYw", "Durability": 1500, "VitalShield": 25},
"2": {"GUID": "cXzgL0_1DFRpXsSZtxyq6Q", "ItemData": "mkSObERGptKuVly00uIfTQ", "Durability": 1400, "VitalShield": 0},
"3": {"GUID": "BQ1--EsJwE1_A9uHVGXmIQ", "ItemData": "24_UV0P2zlDAbcy48UOCkA", "VitalShield": 0},
"7": {"PlayerInventoryItemIndex": 1},
"8": {"PlayerInventoryItemIndex": 0},
"MaxSlotIndex": 8
}
},
"Magic": {
"Inventory": {
"0": {"GUID": "csF2vULQsMbh2xiP2R9CLQ", "ItemData": "Hcq0C0UjvN3n8q-X2uqa7w", "Durability": 1300, "VitalShield": 0},
"32": {"GUID": "BG8nXU9N-zT-0Ker3c9pcw", "ItemData": "iKbF7k2XvufGqqyg5rK-vQ", "Count": 999},
"33": {"GUID": "1C8fWkY1ZgoOlm2xQaufqg", "ItemData": "bbLdJRhwPEWt1ScENYRUCg", "Count": 999},
"34": {"GUID": "d2BgQU6F0U4Z7yaCVv44-g", "ItemData": "Dvo6TE2d7YNnoni8XbKYzw", "Count": 999, "VitalShield": 0},
"35": {"GUID": "_FQtZEEtOcjiy3es0ezX_g", "ItemData": "4wdYZE-FFMhS9Iia0ftWDg", "Count": 999},
"36": {"GUID": "oHCovEXVOy_Y5HS1mwT0bA", "ItemData": "lCE7i3iXGUuHv7FphIOcXg", "Count": 999},
"37": {"GUID": "03KtLEnQZ13C-reyLYAhOQ", "ItemData": "_QMgbMYhjU-9jAD_euFbyQ", "Count": 999, "VitalShield": 0},
"38": {"GUID": "niM85U6UFYDXEGi9avM87w", "ItemData": "_c9JTkwKy8s88GWv586hbQ", "Count": 999},
"MaxSlotIndex": 38
},
"Loadout": {
"0": {"GUID": "bbKo70mhc5vO-u639oPxgA", "ItemData": "GutTdkwskIsX75i6-CilJA", "Durability": 1400, "VitalShield": 25},
"1": {"GUID": "l5Ik2UVtTNVtY4m2yaMYzg", "ItemData": "rXtN2EZOq9NpnL-WyVpF8Q", "Durability": 1500, "VitalShield": 25},
"2": {"GUID": "-0TOlUutJAPWS1qnJMpoFA", "ItemData": "uDBybUNuv5UipiSXb8BG-A", "Durability": 1400, "VitalShield": 0},
"3": {"GUID": "kdI9nUGyn6PB1vu3WKZgcA", "ItemData": "71LhGUmAvrlALY6KcS8W3Q", "VitalShield": 0},
"6": {"PlayerInventoryItemIndex": 34},
"7": {"PlayerInventoryItemIndex": 0},
"8": {"PlayerInventoryItemIndex": 0},
"MaxSlotIndex": 8
}
},
"Ranged": {
"Inventory": {
"0": {"GUID": "gLM0fE3XNamlPBuKdgX8wg", "ItemData": "FK7SwEPmPfVFztSXScvKQA", "Durability": 1025, "VitalShield": 0},
"1": {"GUID": "54e3bbbc5d8949fe9a9a7w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 95, "VitalShield": 0},
"2": {"GUID": "eeee1330dea14c3f89bc4w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
"3": {"GUID": "4a31a625df2f475eac430w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
"4": {"GUID": "b01bbc8c435c4096b6fe6Q", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
"5": {"GUID": "a4298b8bba34490cb06a5w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
"6": {"GUID": "46f140f3e8a7478ca0c55Q", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
"7": {"GUID": "2939ece4daa543b1bcf30w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
"MaxSlotIndex": 7
},
"Loadout": {
"0": {"GUID": "UGg4VECN6fj8X6y4Zv1BCw", "ItemData": "gIoZIUIT52OUDkGFuzSBlw", "Durability": 1400, "VitalShield": 25},
"1": {"GUID": "Pae4okVaM-sM4eKZlh9gdQ", "ItemData": "fr5LJkUvJRZ-DbqVbKaB4w", "Durability": 1400, "VitalShield": 25},
"2": {"GUID": "u3Dmgkf0M3AbQaqMjW2V8g", "ItemData": "l6qWl0-xTPdrhweMah3eTg", "Durability": 1400, "VitalShield": 0},
"3": {"GUID": "KuYmXkRhDdb1fIezDi6lQw", "ItemData": "qANQGE8VKB_lSNeI-PHxGQ", "VitalShield": 0},
"5": {"PlayerInventoryItemIndex": 1},
"7": {"PlayerInventoryItemIndex": 0},
"8": {"PlayerInventoryItemIndex": 0},
"MaxSlotIndex": 8
}
}
}


def setup_gear_tab(tab, data, refresh_preview):
    for widget in tab.winfo_children():
        widget.destroy()
    frame = ttk.Frame(tab)
    frame.pack(fill="both", expand=True)
    
    style_label = ttk.Label(frame, text="Style:")
    style_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    style_var = tk.StringVar(value="Melee")
    style_dropdown = ttk.Combobox(frame, textvariable=style_var, values=list(GEAR_LOADOUTS.keys()), state="readonly")
    style_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    def apply_gear():
        style = style_var.get()
        loadout = GEAR_LOADOUTS.get(style)
        if not loadout:
            messagebox.showerror("Error", "Invalid style selected.")
            return
    
        data["Inventory"] = loadout.get("Inventory", {})
        data["Loadout"] = loadout.get("Loadout", {})
    
        refresh_preview()
        try:
            messagebox.showinfo("Success", f"{style} gear applied.")
        except Exception:
            pass
    
    apply_button = ttk.Button(frame, text="Apply", command=apply_gear)
    apply_button.grid(row=1, column=0, columnspan=2, pady=10)