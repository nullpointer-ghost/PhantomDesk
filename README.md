# PhantomDesk 🛡️

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue?style=flat-square&logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/UI-CustomTkinter-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-emerald?style=flat-square)
![Release](https://img.shields.io/badge/Release-v4.5--beta-indigo?style=flat-square)

**A high-performance, minimalist Windows system privacy and optimization engine.**  
Cloak installed games and sensitive applications from Windows Control Panel/Settings, apply kernel-level stealth attributes to files, and run batched system performance tweaks with two-way reversibility.

[Download Beta (.exe)](#-download--installation) • [Key Features](#-core-features) • [Run From Source](#-running-from-source) • [Safety & Privacy](#-privacy--security-guarantee)

</div>

---

## ⚡ Core Features

### 🛡️ Application Cloaking Studio
* **Zero-Impact Cloaking:** Mask installed software and games from the Windows Control Panel and Settings app without touching save files, configs, or game directories.
* **Stealth Shortcut Camouflage:** Disguise game and application shortcuts as ordinary documents (e.g., `.docx`, `.calc`).
* **Registry Backup Engine:** Instantly export original application uninstall keys to standalone `.reg` files before modifying any parameters.
* **Direct Binary Launcher:** Launch hidden applications directly from disk even when masked from system menus.

### ⚡ Batched & Reversible Tweaks Hub
* **100+ Windows Configurations:** Deep optimizations across Windows 11 De-Bloat, Gaming Latency, Privacy/Telemetry, Junk Purge, and Diagnostics.
* **Zero-Lag Pagination:** Tweaks are split into lightweight, batched pages with category filtering to prevent UI freezes.
* **Two-Way Reversibility:** Every supported tweak features independent **Apply** and **Revert** actions with local state tracking (`phantomdesk_state.json`).

### 📁 Universal File & Locker Shield
* **Kernel Stealth Flags:** Apply `+s +h` (System + Hidden) attributes to arbitrary paths, keeping them invisible even when "Show Hidden Files" is active.
* **File Handle Breaker:** Terminate hanging processes holding locks over files and directories to bypass *"File in use by another program"* errors.
* **Take Full Ownership:** Execute recursive `takeown` and `icacls` commands to grant administrative access over protected paths.
* **Zero-Byte Shredder:** Overwrite sectors with random byte buffers before deletion to prevent file-recovery tools from reconstructing contents.

### 🎨 Modern Minimalist Architecture
* **React/Tailwind-Inspired Aesthetic:** Polished Zinc & Slate color palette with sharp contrast, responsive card grids, and status pills.
* **Dynamic Theme Engine:** Synchronized Dark and Light modes with zero visual artifacts or unreadable text.
* **Threaded Scanning:** Registry scanning executes asynchronously on a background worker thread, ensuring the app opens in milliseconds.
* **Desktop Quality-of-Life:** Smooth recursive mouse-wheel scrolling and full-screen support (**F11**).

---

## 📥 Download & Installation

### Option 1: Standalone Binary (Recommended for most users)
No Python installation or dependencies required.

1. Head over to the **[Latest Releases](https://github.com/nullpointer-ghost/PhantomDesk/releases)** page.
2. Download `PhantomDesk-v4.5-beta.exe`.
3. Right-click the `.exe` and select **Run as administrator** (required for system registry and attribute access).

---

## 🛠️ Running from Source

For developers who want to run or build PhantomDesk locally:

### 1. Clone the Repository
```bash
git clone https://github.com/nullpointer-ghost/PhantomDesk.git
cd PhantomDesk
```

### 2. Install Dependencies
```bash
pip install customtkinter
```

### 3. Run the Application
```bash
python app.py
```

### 4. Build Standalone `.exe`
To compile a single executable with embedded administrator elevation prompts:
```bash
pip install pyinstaller
pyinstaller --clean --onefile --noconsole --uac-admin --name "PhantomDesk" app.py
```
The compiled output will be located in the `dist/` directory.

---

## 🔒 Privacy & Security Guarantee

* **100% Local Execution:** PhantomDesk runs entirely offline. Zero network calls, telemetry beacons, analytics, or background tracking services.
* **Non-Destructive Operations:** Game save folders, user directories, and registry hives are left completely intact.
* **Full Transparency:** Every system command (such as `taskkill`, `attrib`, `sc`, or `reg`) is completely open-source and reviewable directly inside `app.py`.

---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/57097dd7-b43c-4ba9-aaec-3e1f72f46dff" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/73d180f1-875b-4fad-9284-f00c8a5211e3" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/23edd8ae-6ec8-43a0-b36c-1e57e359bc70" />


## 🗺️ Roadmap

- [ ] Steam / Epic Games / Ubisoft Connect auto-detector integration
- [ ] Automated system restore point creation before batch tweaks
- [ ] Exportable stealth profiles (portable configurations)
- [ ] Custom CLI mode for headless background scripting

---

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` for more information

