import tkinter as tk
from tkinter import ttk, messagebox

# Survival preset - first 8 items only
SURVIVAL_PRESET = {
    "0": {"GUID": "FZB5akuoR90kOQy8RGX3Yg", "ItemData": "GC6S207zgsmHryqJEdEQaQ", "Count": 5000000},
    "1": {"GUID": "6RudxkSDSgVEfnOyMYvALA", "ItemData": "3wV1xUv5zBDHRiaAk2qv7w", "Count": 5000000},
    "2": {"GUID": "FLCDzUSfyYkYEEax9WY9TA", "ItemData": "-jEah0znNr-2UVmbHK-Hqg", "Count": 5000000},
    "3": {"GUID": "XDo09kyyQdo51NuNwW1heA", "ItemData": "cZ6va0BSo6_5Dg2Pi23lUQ", "Count": 5000000},
    "4": {"GUID": "LqPCjE0hG50MXRmZEgoBKg", "ItemData": "igveHUWYg2AeXe69EwW1PA", "Count": 5000000},
    "5": {"GUID": "OHWGUUgsegcKUDqisPivzw", "ItemData": "ukjoSEXQTWbO6zSJvP5Z4Q", "Count": 5000000},
    "6": {"GUID": "BKjZPEod9-XAZ6WIu5gtLw", "ItemData": "-9Zin0B1C7GQgVKwKSR0hQ", "Count": 5000000},
    "7": {"GUID": "TUAwJ0fvuHfPR7CX-XIwKA", "ItemData": "QfPOk0c4rF6PIUqOxt0ytg", "Count": 5000000},
    "MaxSlotIndex": 7
}

# Equipment preset - full data you gave me
EQUIPMENT_PRESET = {
    "0": {"GUID": "aOC0JEgqKEI1AMWBNDRs3g", "ItemData": "5PEcXkJHZY9PDqKb9Skqww", "Durability": 1400, "VitalShield": 25},
    "1": {"GUID": "HQp2TU7j6H7DuIGhkg_8cw", "ItemData": "0LL6JE9-pi2e3VSDOwqqYw", "Durability": 1500, "VitalShield": 25},
    "2": {"GUID": "cXzgL0_1DFRpXsSZtxyq6Q", "ItemData": "mkSObERGptKuVly00uIfTQ", "Durability": 1400, "VitalShield": 0},
    "3": {"GUID": "Cv68wUF_AHIyyTeJXBw_MA", "ItemData": "RyuOEkWEWdGcvQqo2dPOgA", "Durability": 1300, "VitalShield": 0},
    "4": {"GUID": "Md8FO0h5L86bncOGevpQ5g", "ItemData": "P3_Aq0nAXu5dlFuBNGgyaw", "Durability": 1300, "VitalShield": 0},
    "5": {"GUID": "AxTjV0SSUudxl3-CCbFiwQ", "ItemData": "igveHUWYg2AeXe69EwW1PA", "Count": 5000000},
    "6": {"GUID": "C-7u6UVlh-CZo2mwWSnlIg", "ItemData": "QfPOk0c4rF6PIUqOxt0ytg", "Count": 5000000},
    "7": {"GUID": "5S0m50uo0FGHfiClN20TXQ", "ItemData": "YvBVZjzx_UKN9z1wIPzlrA", "Durability": 2400, "VitalShield": 0},
    "8": {"GUID": "UGg4VECN6fj8X6y4Zv1BCw", "ItemData": "gIoZIUIT52OUDkGFuzSBlw", "Durability": 1400, "VitalShield": 25},
    "9": {"GUID": "Pae4okVaM-sM4eKZlh9gdQ", "ItemData": "fr5LJkUvJRZ-DbqVbKaB4w", "Durability": 1400, "VitalShield": 25},
    "10": {"GUID": "u3Dmgkf0M3AbQaqMjW2V8g", "ItemData": "l6qWl0-xTPdrhweMah3eTg", "Durability": 1400, "VitalShield": 0},
    "11": {"GUID": "gLM0fE3XNamlPBuKdgX8wg", "ItemData": "FK7SwEPmPfVFztSXScvKQA", "Durability": 1050, "VitalShield": 0},
    "12": {"GUID": "eeee1330dea14c3f89bc4w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
    "13": {"GUID": "4a31a625df2f475eac430w", "ItemData": "1-eS15sb9UW_8kRzIMyV6g", "Count": 99, "VitalShield": 0},
    "14": {"GUID": "pI0AC0DmD1JkL3e_l5h3bg", "ItemData": "TODWPUpA_YR0EnaqhMstcQ", "Count": 5000000},
    "15": {"GUID": "iypMtkyjTFMgRQ-eXQ2mNw", "ItemData": "VfaynRGcAkammV5YUusfbA", "Durability": 2100, "VitalShield": 0},
    "16": {"GUID": "bbKo70mhc5vO-u639oPxgA", "ItemData": "GutTdkwskIsX75i6-CilJA", "Durability": 1400, "VitalShield": 25},
    "17": {"GUID": "l5Ik2UVtTNVtY4m2yaMYzg", "ItemData": "rXtN2EZOq9NpnL-WyVpF8Q", "Durability": 1500, "VitalShield": 25},
    "18": {"GUID": "-0TOlUutJAPWS1qnJMpoFA", "ItemData": "uDBybUNuv5UipiSXb8BG-A", "Durability": 1400, "VitalShield": 0},
    "19": {"GUID": "csF2vULQsMbh2xiP2R9CLQ", "ItemData": "Hcq0C0UjvN3n8q-X2uqa7w", "Durability": 1300, "VitalShield": 0},
    "MaxSlotIndex": 19
}

def setup_storage_tab(tab, data, refresh_preview_callback):
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_rowconfigure(2, weight=1)

    label = ttk.Label(tab, text="Personal Storage:")
    label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    storage_options = ["Survival", "Equipment"]
    storage_var = tk.StringVar(value=storage_options[0])

    storage_dropdown = ttk.Combobox(tab, values=storage_options, state="readonly", textvariable=storage_var)
    storage_dropdown.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    def apply_storage():
        preset_name = storage_var.get()
        if preset_name == "Survival":
            data["PersonalInventory"] = SURVIVAL_PRESET.copy()
        elif preset_name == "Equipment":
            data["PersonalInventory"] = EQUIPMENT_PRESET.copy()
        else:
            messagebox.showwarning("Storage", "Unknown preset selected.")
            return
        refresh_preview_callback()
        messagebox.showinfo("Storage", f"{preset_name} preset applied to PersonalInventory.")

    apply_button = ttk.Button(tab, text="Apply", command=apply_storage)
    apply_button.grid(row=0, column=2, sticky="ew", padx=10, pady=10)
