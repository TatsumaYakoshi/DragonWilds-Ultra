RUN WITH LAUNCHER.PY


## ✨ Features

- **Inventory Editor:**  
  View, add, remove, or update any item in your character’s inventory. Includes search and filter for items, slot management, and bulk editing features.

- **Stats and Player Tab:**  
  Adjust your player’s stats, levels, experience, and more.

- **Equipment Manager:**  
  Edit your equipped items, durability, and special gear properties.

 **Gear & Storage:**  
  Full support for injecting personal storage supplies, gear.

- **Automatic Save Protection:**  
  The editor keeps your save structure valid, including fields like `MaxSlotIndex`, to prevent in-game errors.

- **Live Preview:**  
  Instantly see all changes before saving to avoid mistakes.

## 🖥️ How to Use

1. **Backup your save file.** (Always recommended!)
2. Launch the save editor.
3. Open your save file.
4. Use the tabs to edit inventory, stats, gear, quests, and more.
5. Click **Save** to write your changes back to the file.
6. Load your game and enjoy!

## 🛠️ Requirements

- Python 3.x
- Tkinter (usually included with Python)
`ItemID.txt` or item database file in `data/`

## 📁 File Structure

- `tab_editor.py` – The main editor logic.
- `data/ItemID.txt` – JSON database of all items (required for item search/filter).
- Other supporting scripts and assets as needed.

## ⚠️ Disclaimer

- **Always back up your saves.**  
- This tool is provided as-is. Use at your own risk.
- Not affiliated with or endorsed by Jagex.

## 💡 Credits

Me, Elleandria for allowing me use of their stuff, google

---

