"""
PhantomDesk v4.5 Pro // High-Performance Windows Cloaking & Optimization Hub
Architecture: Threaded Asynchronous Scanning, Batched UI Rendering & Reversible Tweaks
Engine: Direct Native Win32 / Kernel32 / Winreg Integration
License: MIT
"""

import os
import sys
import json
import shutil
import ctypes
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import winreg
import customtkinter as ctk

# Import the native Win32 engine
import win32_engine as engine

# Windows creation flag to suppress any console window spawning
CREATE_NO_WINDOW = 0x08000000

# -----------------------------------------------------------------------------
# Dynamic Theme Palette: (Light Mode Color, Dark Mode Color)
# -----------------------------------------------------------------------------
T_BG_ROOT       = ("#f8fafc", "#09090b")  # Slate 50 / Zinc 950
T_SURFACE       = ("#ffffff", "#121215")  # Pure White / Zinc 900
T_SURFACE_ALT   = ("#f1f5f9", "#18181c")  # Slate 100 / Zinc 800
T_BORDER        = ("#cbd5e1", "#27272a")  # Slate 300 / Zinc 700
T_BORDER_ACTIVE = ("#4f46e5", "#6366f1")  # Indigo Focus
T_TEXT          = ("#0f172a", "#fafafa")  # Slate 900 / Zinc 50
T_TEXT_MUTED    = ("#64748b", "#a1a1aa")  # Slate 500 / Zinc 400
T_ACCENT        = ("#4f46e5", "#6366f1")  # Indigo Primary
T_ACCENT_HOV    = ("#4338ca", "#4f46e5")
T_DANGER        = ("#e11d48", "#ef4444")  # Rose Red
T_DANGER_HOV    = ("#be123c", "#dc2626")
T_SUCCESS       = ("#059669", "#10b981")  # Emerald Green
T_SUCCESS_HOV   = ("#047857", "#059669")
T_WARNING       = ("#d97706", "#f59e0b")  # Amber
T_WARNING_HOV   = ("#b45309", "#d97706")
T_ROW_HOVER     = ("#e2e8f0", "#1f1f26")
T_ROW_SELECTED  = ("#e0e7ff", "#262638")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

STATE_FILE = os.path.join(os.environ.get("LOCALAPPDATA", "."), "phantomdesk_state.json")

# -----------------------------------------------------------------------------
# Categorized & Reversible Tweaks Database
# -----------------------------------------------------------------------------
TWEAKS_CATALOG = [
    # Win 11 De-Bloat
    {"id": "win11_classic_menu", "cat": "Win 11 De-Bloat", "name": "Classic Windows 10 Context Menu", "desc": "Bypasses the 'Show More Options' sub-menu in Windows 11.", "reversible": True},
    {"id": "win11_taskbar_left", "cat": "Win 11 De-Bloat", "name": "Align Taskbar to Left", "desc": "Moves Windows 11 taskbar icons to the classic left position.", "reversible": True},
    {"id": "win11_taskbar_center", "cat": "Win 11 De-Bloat", "name": "Align Taskbar to Center", "desc": "Restores modern centered taskbar icon layout.", "reversible": True},
    {"id": "win11_disable_widgets", "cat": "Win 11 De-Bloat", "name": "Disable Widgets Feed", "desc": "Turns off background news widgets & MSN service feeds.", "reversible": True},
    {"id": "win11_disable_copilot", "cat": "Win 11 De-Bloat", "name": "Disable Windows Copilot", "desc": "Disables integrated Copilot AI features across the OS.", "reversible": True},
    {"id": "win11_disable_recall", "cat": "Win 11 De-Bloat", "name": "Disable Windows Recall History", "desc": "Blocks Windows automatic snapshot & AI indexing telemetry.", "reversible": True},
    {"id": "win11_disable_bing", "cat": "Win 11 De-Bloat", "name": "Disable Bing Search in Start Menu", "desc": "Prevents Start Menu from sending keystrokes to Bing servers.", "reversible": True},
    {"id": "win11_show_hidden", "cat": "Win 11 De-Bloat", "name": "Show Hidden System Files", "desc": "Sets File Explorer to display all hidden and system files.", "reversible": True},
    {"id": "win11_show_extensions", "cat": "Win 11 De-Bloat", "name": "Show Known File Extensions", "desc": "Forces File Explorer to always show extensions like .exe, .bat, .txt.", "reversible": True},
    {"id": "win11_this_pc", "cat": "Win 11 De-Bloat", "name": "Open Explorer to 'This PC'", "desc": "Changes default Explorer launch window from Home to This PC.", "reversible": True},
    {"id": "win11_compact_view", "cat": "Win 11 De-Bloat", "name": "Enable Compact File List View", "desc": "Reduces vertical padding in File Explorer list items.", "reversible": True},
    {"id": "win11_disable_sticky", "cat": "Win 11 De-Bloat", "name": "Disable Sticky Keys Popups", "desc": "Prevents 5-Shift key trigger from interrupting full-screen games.", "reversible": True},
    {"id": "win11_hide_chat", "cat": "Win 11 De-Bloat", "name": "Hide Teams / Chat Taskbar Icon", "desc": "Removes Microsoft Teams icon from the Windows 11 taskbar.", "reversible": True},
    {"id": "win11_hide_taskview", "cat": "Win 11 De-Bloat", "name": "Hide Task View Icon", "desc": "Removes virtual desktops icon button from taskbar.", "reversible": True},

    # Gaming & Latency
    {"id": "game_ultimate_power", "cat": "Gaming & Latency", "name": "Activate Ultimate Performance Plan", "desc": "Unlocks workstation power scheme that disables CPU core sleep.", "reversible": True},
    {"id": "game_disable_dvr", "cat": "Gaming & Latency", "name": "Disable GameDVR Background Capture", "desc": "Turns off background video recording to eliminate a 10-15% FPS hit.", "reversible": True},
    {"id": "game_disable_gamebar", "cat": "Gaming & Latency", "name": "Disable Xbox Game Bar Overlays", "desc": "Stops Win+G hooks from creating DirectX overlay latency.", "reversible": True},
    {"id": "game_mouse_accel", "cat": "Gaming & Latency", "name": "Disable Mouse Acceleration", "desc": "Enforces 1:1 linear mouse input without acceleration curves.", "reversible": True},

    # Privacy & Telemetry
    {"id": "priv_diagtrack", "cat": "Privacy & Telemetry", "name": "Disable DiagTrack Telemetry Service", "desc": "Stops Connected User Experiences and Telemetry background service.", "reversible": True},
    {"id": "priv_wer", "cat": "Privacy & Telemetry", "name": "Disable Windows Error Reporting (WER)", "desc": "Blocks crash telemetry and diagnostic dump generation.", "reversible": True},
    {"id": "priv_ad_id", "cat": "Privacy & Telemetry", "name": "Disable Advertising ID Profile", "desc": "Prevents applications from tracking ad preferences across software.", "reversible": True},
    {"id": "priv_location", "cat": "Privacy & Telemetry", "name": "Disable Location Tracking Sensors", "desc": "Shuts off Windows system location querying APIs.", "reversible": True},
    {"id": "priv_wipe_clipboard", "cat": "Privacy & Telemetry", "name": "Purge Clipboard & History Memory", "desc": "Wipes current copy buffer and the Win+V history clipboard cache.", "reversible": False},
    {"id": "priv_clear_recent", "cat": "Privacy & Telemetry", "name": "Clear Recent Documents & JumpLists", "desc": "Wipes all recent file records from %APPDATA%\\Recent.", "reversible": False},

    # Junk & Purge
    {"id": "junk_clean_temp", "cat": "Junk & Purge", "name": "Purge User & System Temp Directories", "desc": "Empties %TEMP% scratch files to free storage drives.", "reversible": False},
    {"id": "junk_empty_recycle", "cat": "Junk & Purge", "name": "Silently Empty All Recycle Bins", "desc": "Empties all drive bins without showing OS confirmation boxes.", "reversible": False},

    # Diagnostics & Shell
    {"id": "diag_restart_explorer", "cat": "Diagnostics & Fixes", "name": "Refresh Windows Explorer Shell", "desc": "Refreshes icon, desktop, and shell notification cache natively.", "reversible": False},
    {"id": "diag_flush_dns", "cat": "Diagnostics & Fixes", "name": "Flush DNS Resolver Cache", "desc": "Flushes system DNS cache to resolve inaccessible network paths.", "reversible": False}
]


class PhantomDesk(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PhantomDesk v4.5 Pro // Fast System & Privacy Hub")
        self.geometry("1200x820")
        self.minsize(1060, 700)
        self.configure(fg_color=T_BG_ROOT)

        # Fullscreen bindings
        self.is_fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        self.bind_all("<MouseWheel>", self._universal_mousewheel)

        # State storage for reversions
        self.applied_tweaks = self.load_state()

        # Batching / Pagination state for Tweaks Hub
        self.current_tweak_cat = "All"
        self.current_tweak_page = 0
        self.tweaks_per_page = 12

        # In-memory App Catalog
        self.all_apps = {}
        self.filtered_apps = {}
        self.selected_app_name = None
        self.is_scanning = True

        # Render scaffolding first (loads instantly)
        self.setup_scaffolding()
        self.show_app_cloaker()

        # Run Registry Scanning in Background Thread (Does not freeze the GUI)
        threading.Thread(target=self._threaded_scan_apps, daemon=True).start()

    # -------------------------------------------------------------------------
    # State Management
    # -------------------------------------------------------------------------
    def load_state(self):
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r") as f:
                    return set(json.load(f))
        except Exception:
            pass
        return set()

    def save_state(self):
        try:
            with open(STATE_FILE, "w") as f:
                json.dump(list(self.applied_tweaks), f)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Threaded Async Registry Scanning
    # -------------------------------------------------------------------------
    def _threaded_scan_apps(self):
        """Scans Windows Registry in the background without blocking the UI thread."""
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]

        found_apps = {}
        for root_key, key_path in registry_paths:
            try:
                base_key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)
                for i in range(winreg.QueryInfoKey(base_key)[0]):
                    try:
                        sub_name = winreg.EnumKey(base_key, i)
                        full_route = f"{key_path}\\{sub_name}"
                        target_key = winreg.OpenKey(root_key, full_route, 0, winreg.KEY_READ)

                        is_cloaked = False
                        try:
                            sys_comp, _ = winreg.QueryValueEx(target_key, "SystemComponent")
                            if sys_comp == 1:
                                is_cloaked = True
                        except FileNotFoundError:
                            pass

                        try:
                            app_name, _ = winreg.QueryValueEx(target_key, "DisplayName")
                        except FileNotFoundError:
                            try:
                                app_name, _ = winreg.QueryValueEx(target_key, "QuietDisplayName")
                                is_cloaked = True
                            except FileNotFoundError:
                                app_name = None

                        try:
                            install_dir, _ = winreg.QueryValueEx(target_key, "InstallLocation")
                        except FileNotFoundError:
                            install_dir = ""

                        if app_name and isinstance(app_name, str) and app_name.strip():
                            clean_name = app_name.strip()
                            if not any(x in clean_name.lower() for x in ["kb", "security update", "package_for"]):
                                found_apps[clean_name] = {
                                    "root": root_key,
                                    "route": full_route,
                                    "directory": install_dir.strip() if isinstance(install_dir, str) else "",
                                    "is_cloaked": is_cloaked
                                }
                        winreg.CloseKey(target_key)
                    except OSError:
                        continue
                winreg.CloseKey(base_key)
            except OSError:
                continue

        self.after(0, lambda: self._on_scan_completed(found_apps))

    def _on_scan_completed(self, found_apps):
        self.all_apps = found_apps
        self.filtered_apps = found_apps.copy()
        self.is_scanning = False
        if hasattr(self, "app_count_lbl"):
            self.app_count_lbl.configure(text=f"{len(self.all_apps)} applications detected")
        if self.active_tab == "apps":
            self.render_app_list()

    # -------------------------------------------------------------------------
    # Layout Framework
    # -------------------------------------------------------------------------
    def setup_scaffolding(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        brand_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_box.pack(anchor="w", padx=20, pady=(24, 18))

        self.brand_title = ctk.CTkLabel(brand_box, text="PhantomDesk", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=T_TEXT)
        self.brand_title.pack(anchor="w")

        self.brand_sub = ctk.CTkLabel(brand_box, text="v4.5 PRO HUB", font=ctk.CTkFont(family="Consolas", size=10, weight="bold"), fg_color=T_SURFACE_ALT, text_color=T_TEXT_MUTED, corner_radius=4)
        self.brand_sub.pack(anchor="w", pady=(4, 0))

        # Nav Buttons
        self.nav_buttons = {}
        self.create_nav_btn("apps", "🛡️  App Cloaker", self.show_app_cloaker)
        self.create_nav_btn("hub", "⚡  Tweaks Hub (Batched)", self.show_tweaks_hub)
        self.create_nav_btn("files", "📁  File & Locker Shield", self.show_file_shield)

        # Sidebar Footer
        self.sidebar_foot = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_foot.pack(side="bottom", fill="x", padx=16, pady=20)

        self.theme_btn = ctk.CTkButton(
            self.sidebar_foot,
            text="☀️ Switch to Light Mode",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=T_SURFACE_ALT,
            text_color=T_TEXT,
            hover_color=T_ROW_HOVER,
            border_color=T_BORDER,
            border_width=1,
            height=36,
            corner_radius=8,
            command=self.toggle_theme
        )
        self.theme_btn.pack(fill="x", pady=(0, 10))

        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        admin_str = "● ADMIN ACTIVE" if is_admin else "○ LIMITED PRIVILEGES"
        admin_col = T_SUCCESS if is_admin else T_DANGER

        self.admin_lbl = ctk.CTkLabel(self.sidebar_foot, text=admin_str, font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=admin_col)
        self.admin_lbl.pack(anchor="w", pady=(0, 2))

        self.fs_hint = ctk.CTkLabel(self.sidebar_foot, text="F11: Toggle Fullscreen", font=ctk.CTkFont(size=11), text_color=T_TEXT_MUTED)
        self.fs_hint.pack(anchor="w")

        # Main Workspace Container
        self.main_container = ctk.CTkFrame(self, fg_color=T_BG_ROOT, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

    def create_nav_btn(self, key, label, cmd):
        btn = ctk.CTkButton(
            self.sidebar,
            text=label,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="transparent",
            text_color=T_TEXT_MUTED,
            hover_color=T_SURFACE_ALT,
            height=42,
            corner_radius=8,
            command=cmd
        )
        btn.pack(fill="x", padx=12, pady=4)
        self.nav_buttons[key] = btn

    def set_active_nav(self, key):
        self.active_tab = key
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=T_SURFACE_ALT, text_color=T_TEXT)
            else:
                btn.configure(fg_color="transparent", text_color=T_TEXT_MUTED)

    def clear_viewport(self):
        for w in self.main_container.winfo_children():
            w.destroy()

    def toggle_theme(self):
        cur = ctk.get_appearance_mode()
        new_mode = "Light" if cur == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.theme_btn.configure(text="🌙 Switch to Dark Mode" if new_mode == "Light" else "☀️ Switch to Light Mode")
        if self.active_tab == "apps": self.show_app_cloaker()
        elif self.active_tab == "hub": self.show_tweaks_hub()
        elif self.active_tab == "files": self.show_file_shield()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.fs_hint.configure(text="Esc: Exit Fullscreen" if self.is_fullscreen else "F11: Toggle Fullscreen")

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)
            self.fs_hint.configure(text="F11: Toggle Fullscreen")

    def _universal_mousewheel(self, event):
        x, y = event.x_root, event.y_root
        widget = self.winfo_containing(x, y)
        curr = widget
        while curr:
            if isinstance(curr, tk.Canvas):
                curr.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return
            curr = getattr(curr, "master", None)

    # -------------------------------------------------------------------------
    # VIEW 1: Application Cloaking Studio
    # -------------------------------------------------------------------------
    def show_app_cloaker(self):
        self.set_active_nav("apps")
        self.clear_viewport()

        head = ctk.CTkFrame(self.main_container, fg_color="transparent")
        head.pack(fill="x", pady=(0, 14))

        title = ctk.CTkLabel(head, text="Application Cloaking Studio", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=T_TEXT)
        title.pack(anchor="w")

        sub = ctk.CTkLabel(head, text="Mask installed software from Windows Control Panel & Settings without breaking saves.", font=ctk.CTkFont(size=13), text_color=T_TEXT_MUTED)
        sub.pack(anchor="w")

        split = ctk.CTkFrame(self.main_container, fg_color="transparent")
        split.pack(fill="both", expand=True)
        split.grid_columnconfigure(0, weight=5)
        split.grid_columnconfigure(1, weight=5)
        split.grid_rowconfigure(0, weight=1)

        # Left Column: Catalog
        left_card = ctk.CTkFrame(split, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=10)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_card.grid_rowconfigure(2, weight=1)
        left_card.grid_columnconfigure(0, weight=1)

        search_wrap = ctk.CTkFrame(left_card, fg_color="transparent")
        search_wrap.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))

        self.app_search_var = tk.StringVar()
        self.app_search_var.trace_add("write", self.filter_app_cards)

        search_in = ctk.CTkEntry(
            search_wrap,
            placeholder_text="Type to search (e.g. Far Cry, Steam, Discord)...",
            textvariable=self.app_search_var,
            height=38,
            fg_color=T_SURFACE_ALT,
            border_color=T_BORDER,
            text_color=T_TEXT,
            placeholder_text_color=T_TEXT_MUTED
        )
        search_in.pack(fill="x")

        status_init = "Scanning registry in background..." if self.is_scanning else f"{len(self.all_apps)} applications detected"
        self.app_count_lbl = ctk.CTkLabel(left_card, text=status_init, font=ctk.CTkFont(family="Consolas", size=11), text_color=T_TEXT_MUTED)
        self.app_count_lbl.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 6))

        self.app_list_box = ctk.CTkScrollableFrame(left_card, fg_color="transparent", corner_radius=0)
        self.app_list_box.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 10))

        # Right Column: Inspector & Actions
        right_card = ctk.CTkFrame(split, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=10)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        insp_scroll = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        insp_scroll.pack(fill="both", expand=True, padx=14, pady=14)

        insp_title = ctk.CTkLabel(insp_scroll, text="APPLICATION DIAGNOSTICS", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=T_TEXT_MUTED)
        insp_title.pack(anchor="w", pady=(0, 6))

        self.info_box = ctk.CTkTextbox(insp_scroll, height=130, fg_color=T_SURFACE_ALT, border_color=T_BORDER, border_width=1, text_color=T_TEXT, font=ctk.CTkFont(family="Consolas", size=12))
        self.info_box.pack(fill="x", pady=(0, 16))
        self.info_box.configure(state="disabled")

        # Cloak / Restore Buttons
        b_grid1 = ctk.CTkFrame(insp_scroll, fg_color="transparent")
        b_grid1.pack(fill="x", pady=(0, 8))
        b_grid1.grid_columnconfigure((0, 1), weight=1)

        self.btn_cloak = ctk.CTkButton(b_grid1, text="🙈 Cloak Program", fg_color=T_DANGER, hover_color=T_DANGER_HOV, text_color="#ffffff", font=ctk.CTkFont(size=13, weight="bold"), height=44, corner_radius=8, command=self.execute_hide_app)
        self.btn_cloak.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_restore = ctk.CTkButton(b_grid1, text="🐵 Restore App", fg_color=T_SUCCESS, hover_color=T_SUCCESS_HOV, text_color="#ffffff", font=ctk.CTkFont(size=13, weight="bold"), height=44, corner_radius=8, command=self.execute_restore_app)
        self.btn_restore.grid(row=0, column=1, padx=4, sticky="ew")

        # Directory & Reg Backup
        b_grid2 = ctk.CTkFrame(insp_scroll, fg_color="transparent")
        b_grid2.pack(fill="x", pady=(0, 8))
        b_grid2.grid_columnconfigure((0, 1), weight=1)

        self.btn_open = ctk.CTkButton(b_grid2, text="📁 Open Directory", fg_color=T_SURFACE_ALT, hover_color=T_ROW_HOVER, text_color=T_TEXT, border_color=T_BORDER, border_width=1, font=ctk.CTkFont(size=12, weight="bold"), height=40, corner_radius=8, command=self.open_selected_folder)
        self.btn_open.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_backup = ctk.CTkButton(b_grid2, text="💾 Backup .reg Key", fg_color=T_SURFACE_ALT, hover_color=T_ROW_HOVER, text_color=T_TEXT, border_color=T_BORDER, border_width=1, font=ctk.CTkFont(size=12, weight="bold"), height=40, corner_radius=8, command=self.export_registry_key)
        self.btn_backup.grid(row=0, column=1, padx=4, sticky="ew")

        # Stealth Shortcut & Startup Tweaks
        b_grid3 = ctk.CTkFrame(insp_scroll, fg_color="transparent")
        b_grid3.pack(fill="x", pady=(0, 8))
        b_grid3.grid_columnconfigure((0, 1), weight=1)

        self.btn_startup = ctk.CTkButton(b_grid3, text="🛑 Cloak Startup Key", fg_color=T_SURFACE_ALT, hover_color=T_ROW_HOVER, text_color=T_TEXT, border_color=T_BORDER, border_width=1, font=ctk.CTkFont(size=12, weight="bold"), height=40, corner_radius=8, command=self.toggle_startup_state)
        self.btn_startup.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_camou = ctk.CTkButton(b_grid3, text="🎭 Camouflage Shortcut", fg_color=T_SURFACE_ALT, hover_color=T_ROW_HOVER, text_color=T_TEXT, border_color=T_BORDER, border_width=1, font=ctk.CTkFont(size=12, weight="bold"), height=40, corner_radius=8, command=self.camouflage_shortcut)
        self.btn_camou.grid(row=0, column=1, padx=4, sticky="ew")

        # Direct Launch
        self.btn_launch = ctk.CTkButton(insp_scroll, text="🚀 Direct Stealth Launch Binary", fg_color=T_ACCENT, hover_color=T_ACCENT_HOV, text_color="#ffffff", font=ctk.CTkFont(size=13, weight="bold"), height=42, corner_radius=8, command=self.direct_launch_app)
        self.btn_launch.pack(fill="x", padx=4, pady=(8, 0))

        if not self.is_scanning:
            self.render_app_list()

    def render_app_list(self):
        for w in self.app_list_box.winfo_children():
            w.destroy()

        sorted_names = sorted(list(self.filtered_apps.keys()))
        if hasattr(self, "app_count_lbl"):
            self.app_count_lbl.configure(text=f"{len(sorted_names)} applications listed")

        if not sorted_names:
            msg = "Scanning applications..." if self.is_scanning else "No matching apps found"
            none_lbl = ctk.CTkLabel(self.app_list_box, text=msg, text_color=T_TEXT_MUTED)
            none_lbl.pack(pady=20)
            self.display_app_details(None)
            return

        if not self.selected_app_name or self.selected_app_name not in sorted_names:
            self.selected_app_name = sorted_names[0]

        for name in sorted_names:
            is_selected = (name == self.selected_app_name)
            meta = self.filtered_apps[name]
            is_cloaked = meta.get("is_cloaked", False)

            row_bg = T_ROW_SELECTED if is_selected else T_SURFACE_ALT
            row_border = T_BORDER_ACTIVE if is_selected else T_BORDER

            row = ctk.CTkFrame(self.app_list_box, fg_color=row_bg, border_color=row_border, border_width=1, corner_radius=8, height=46)
            row.pack(fill="x", pady=2, padx=2)
            row.pack_propagate(False)

            title_txt = name if len(name) < 32 else f"{name[:29]}..."
            name_lbl = ctk.CTkLabel(row, text=title_txt, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=T_TEXT)
            name_lbl.pack(side="left", padx=12)

            badge_text = "● CLOAKED" if is_cloaked else "● VISIBLE"
            badge_color = T_DANGER if is_cloaked else T_SUCCESS

            badge_lbl = ctk.CTkLabel(row, text=badge_text, font=ctk.CTkFont(family="Consolas", size=10, weight="bold"), text_color=badge_color)
            badge_lbl.pack(side="right", padx=12)

            def _bind_click(w, n=name):
                w.bind("<Button-1>", lambda e: self.select_app(n))
                w.bind("<Enter>", lambda e: row.configure(fg_color=T_ROW_HOVER))
                w.bind("<Leave>", lambda e: row.configure(fg_color=T_ROW_SELECTED if n == self.selected_app_name else T_SURFACE_ALT))

            _bind_click(row)
            _bind_click(name_lbl)
            _bind_click(badge_lbl)

        self.display_app_details(self.selected_app_name)

    def select_app(self, name):
        self.selected_app_name = name
        self.render_app_list()

    def filter_app_cards(self, *args):
        q = self.app_search_var.get().lower()
        if not q:
            self.filtered_apps = self.all_apps.copy()
        else:
            self.filtered_apps = {k: v for k, v in self.all_apps.items() if q in k.lower()}
        self.render_app_list()

    def display_app_details(self, selection):
        if not selection or selection not in self.filtered_apps:
            self.info_box.configure(state="normal")
            self.info_box.delete("1.0", tk.END)
            self.info_box.insert(tk.END, "Select an application on the left to view diagnostics.")
            self.info_box.configure(state="disabled")
            return

        meta = self.filtered_apps[selection]
        has_dir = meta['directory'] and os.path.exists(meta['directory'])
        status = "DISK VALIDATED" if has_dir else "REGISTRY ONLY / UNKNOWN"
        cloaked_str = "HIDDEN FROM CONTROL PANEL" if meta.get("is_cloaked") else "VISIBLE IN CONTROL PANEL"

        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", tk.END)
        self.info_box.insert(tk.END, f"Target:    {selection}\n")
        self.info_box.insert(tk.END, f"State:     [{cloaked_str}]\n")
        self.info_box.insert(tk.END, f"Registry:  {meta['route']}\n")
        self.info_box.insert(tk.END, f"Directory: {meta['directory'] if meta['directory'] else 'N/A'}\n")
        self.info_box.insert(tk.END, f"Integrity: [{status}]")
        self.info_box.configure(state="disabled")

    # -------------------------------------------------------------------------
    # VIEW 2: Batched & Reversible Tweaks Hub (Fast Pagination)
    # -------------------------------------------------------------------------
    def show_tweaks_hub(self):
        self.set_active_nav("hub")
        self.clear_viewport()

        head = ctk.CTkFrame(self.main_container, fg_color="transparent")
        head.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(head, text="System Tweaks & Optimization Hub", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=T_TEXT)
        title.pack(anchor="w")

        sub = ctk.CTkLabel(head, text="Execute system configurations with two-way reversibility. Divided into batches for instant responsiveness.", font=ctk.CTkFont(size=13), text_color=T_TEXT_MUTED)
        sub.pack(anchor="w")

        cat_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        cat_frame.pack(fill="x", pady=(0, 10))

        categories = ["All", "Win 11 De-Bloat", "Gaming & Latency", "Privacy & Telemetry", "Junk & Purge", "Diagnostics & Fixes"]
        for cat in categories:
            is_active = (self.current_tweak_cat == cat)
            btn = ctk.CTkButton(
                cat_frame,
                text=cat,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=T_ROW_SELECTED if is_active else T_SURFACE,
                hover_color=T_ROW_HOVER,
                text_color=T_TEXT,
                border_color=T_BORDER_ACTIVE if is_active else T_BORDER,
                border_width=1,
                height=32,
                corner_radius=6,
                command=lambda c=cat: self.set_tweak_category(c)
            )
            btn.pack(side="left", padx=(0, 6))

        search_card = ctk.CTkFrame(self.main_container, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=8)
        search_card.pack(fill="x", pady=(0, 10), ipady=4, ipadx=8)

        self.tweak_search_var = tk.StringVar()
        self.tweak_search_var.trace_add("write", lambda *args: self.reset_and_render_tweaks())

        search_in = ctk.CTkEntry(
            search_card,
            placeholder_text="Filter active batch by keyword...",
            textvariable=self.tweak_search_var,
            height=34,
            fg_color=T_SURFACE_ALT,
            border_color=T_BORDER,
            text_color=T_TEXT,
            placeholder_text_color=T_TEXT_MUTED
        )
        search_in.pack(fill="x", padx=6, pady=4)

        self.tweaks_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.tweaks_scroll.pack(fill="both", expand=True)

        self.page_footer = ctk.CTkFrame(self.main_container, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=8, height=44)
        self.page_footer.pack(fill="x", pady=(10, 0))
        self.page_footer.pack_propagate(False)

        self.prev_btn = ctk.CTkButton(self.page_footer, text="◀ Previous Batch", width=120, height=30, fg_color=T_SURFACE_ALT, hover_color=T_ROW_HOVER, text_color=T_TEXT, border_color=T_BORDER, border_width=1, command=self.prev_tweak_page)
        self.prev_btn.pack(side="left", padx=12)

        self.page_lbl = ctk.CTkLabel(self.page_footer, text="Batch 1 of 1", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"), text_color=T_TEXT)
        self.page_lbl.pack(side="left", expand=True)

        self.next_btn = ctk.CTkButton(self.page_footer, text="Next Batch ▶", width=120, height=30, fg_color=T_SURFACE_ALT, hover_color=T_ROW_HOVER, text_color=T_TEXT, border_color=T_BORDER, border_width=1, command=self.next_tweak_page)
        self.next_btn.pack(side="right", padx=12)

        self.render_tweaks_batch()

    def set_tweak_category(self, cat):
        self.current_tweak_cat = cat
        self.current_tweak_page = 0
        self.show_tweaks_hub()

    def reset_and_render_tweaks(self):
        self.current_tweak_page = 0
        self.render_tweaks_batch()

    def prev_tweak_page(self):
        if self.current_tweak_page > 0:
            self.current_tweak_page -= 1
            self.render_tweaks_batch()

    def next_tweak_page(self):
        self.current_tweak_page += 1
        self.render_tweaks_batch()

    def render_tweaks_batch(self):
        for w in self.tweaks_scroll.winfo_children():
            w.destroy()

        q = self.tweak_search_var.get().lower() if hasattr(self, "tweak_search_var") else ""

        filtered = []
        for t in TWEAKS_CATALOG:
            if self.current_tweak_cat != "All" and t["cat"] != self.current_tweak_cat:
                continue
            if q and (q not in t["name"].lower() and q not in t["desc"].lower() and q not in t["cat"].lower()):
                continue
            filtered.append(t)

        total_items = len(filtered)
        total_pages = max(1, (total_items + self.tweaks_per_page - 1) // self.tweaks_per_page)

        if self.current_tweak_page >= total_pages:
            self.current_tweak_page = total_pages - 1

        start_idx = self.current_tweak_page * self.tweaks_per_page
        end_idx = min(start_idx + self.tweaks_per_page, total_items)
        current_batch = filtered[start_idx:end_idx]

        self.page_lbl.configure(text=f"Batch {self.current_tweak_page + 1} of {total_pages} ({total_items} items total)")
        self.prev_btn.configure(state="normal" if self.current_tweak_page > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_tweak_page < total_pages - 1 else "disabled")

        if not current_batch:
            none_lbl = ctk.CTkLabel(self.tweaks_scroll, text="No tweaks matched the active filters.", text_color=T_TEXT_MUTED)
            none_lbl.pack(pady=30)
            return

        for tweak in current_batch:
            t_id = tweak["id"]
            is_applied = t_id in self.applied_tweaks

            card = ctk.CTkFrame(self.tweaks_scroll, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=10)
            card.pack(fill="x", pady=4, ipady=8, ipadx=10)

            box = ctk.CTkFrame(card, fg_color="transparent")
            box.pack(side="left", fill="both", expand=True, padx=10)

            top_row = ctk.CTkFrame(box, fg_color="transparent")
            top_row.pack(anchor="w")

            cat_badge = ctk.CTkLabel(top_row, text=f" {tweak['cat'].upper()} ", font=ctk.CTkFont(family="Consolas", size=9, weight="bold"), fg_color=T_SURFACE_ALT, text_color=T_TEXT_MUTED, corner_radius=4)
            cat_badge.pack(side="left", padx=(0, 8))

            name_lbl = ctk.CTkLabel(top_row, text=tweak["name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=T_TEXT)
            name_lbl.pack(side="left")

            if tweak["reversible"]:
                state_txt = "● APPLIED" if is_applied else "○ DEFAULT"
                state_col = T_SUCCESS if is_applied else T_TEXT_MUTED
                state_lbl = ctk.CTkLabel(top_row, text=f"  {state_txt}", font=ctk.CTkFont(family="Consolas", size=10, weight="bold"), text_color=state_col)
                state_lbl.pack(side="left")

            desc_lbl = ctk.CTkLabel(box, text=tweak["desc"], font=ctk.CTkFont(size=12), text_color=T_TEXT_MUTED)
            desc_lbl.pack(anchor="w", pady=(2, 0))

            action_box = ctk.CTkFrame(card, fg_color="transparent")
            action_box.pack(side="right", padx=10)

            apply_btn = ctk.CTkButton(
                action_box,
                text="Apply",
                width=80,
                height=32,
                fg_color=T_ACCENT,
                hover_color=T_ACCENT_HOV,
                text_color="#ffffff",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda t=tweak: self.execute_tweak_toggle(t, action="apply")
            )
            apply_btn.pack(side="left", padx=4)

            if tweak["reversible"]:
                revert_btn = ctk.CTkButton(
                    action_box,
                    text="Revert",
                    width=80,
                    height=32,
                    fg_color=T_SURFACE_ALT if is_applied else T_SURFACE_ALT,
                    hover_color=T_WARNING_HOV,
                    text_color=T_WARNING if is_applied else T_TEXT_MUTED,
                    border_color=T_WARNING if is_applied else T_BORDER,
                    border_width=1,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda t=tweak: self.execute_tweak_toggle(t, action="revert")
                )
                revert_btn.pack(side="left", padx=4)

    # -------------------------------------------------------------------------
    # Reversible Execution Engine (Native Win32 Integration)
    # -------------------------------------------------------------------------
    def execute_tweak_toggle(self, tweak, action="apply"):
        t_id = tweak["id"]
        t_name = tweak["name"]

        try:
            # 1. Classic Context Menu
            if t_id == "win11_classic_menu":
                clsid_path = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
                if action == "apply":
                    engine.win32_set_reg("HKCU", clsid_path, "", "REG_SZ", "")
                    self.applied_tweaks.add(t_id)
                else:
                    try:
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, clsid_path)
                        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}")
                    except OSError:
                        pass
                    self.applied_tweaks.discard(t_id)
                engine.win32_refresh_shell()

            # 2. Taskbar Alignment
            elif t_id in ("win11_taskbar_left", "win11_taskbar_center"):
                val = 0 if t_id == "win11_taskbar_left" and action == "apply" else 1
                engine.win32_set_reg("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarAl", "REG_DWORD", val)
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)

            # 3. Widgets
            elif t_id == "win11_disable_widgets":
                val = 0 if action == "apply" else 1
                engine.win32_set_reg("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarDa", "REG_DWORD", val)
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)

            # 4. Copilot
            elif t_id == "win11_disable_copilot":
                if action == "apply":
                    engine.win32_set_reg("HKCU", r"Software\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", "REG_DWORD", 1)
                    self.applied_tweaks.add(t_id)
                else:
                    engine.win32_delete_reg("HKCU", r"Software\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot")
                    self.applied_tweaks.discard(t_id)

            # 5. Bing Search in Start
            elif t_id == "win11_disable_bing":
                if action == "apply":
                    engine.win32_set_reg("HKCU", r"Software\Policies\Microsoft\Windows\Explorer", "DisableSearchBoxSuggestions", "REG_DWORD", 1)
                    engine.win32_set_reg("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", "REG_DWORD", 0)
                    self.applied_tweaks.add(t_id)
                else:
                    engine.win32_delete_reg("HKCU", r"Software\Policies\Microsoft\Windows\Explorer", "DisableSearchBoxSuggestions")
                    engine.win32_set_reg("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Search", "BingSearchEnabled", "REG_DWORD", 1)
                    self.applied_tweaks.discard(t_id)

            # 6. Hidden Files
            elif t_id == "win11_show_hidden":
                val = 1 if action == "apply" else 2
                engine.win32_set_reg("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "Hidden", "REG_DWORD", val)
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)
                engine.win32_refresh_shell()

            # 7. Known File Extensions
            elif t_id == "win11_show_extensions":
                val = 0 if action == "apply" else 1
                engine.win32_set_reg("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "HideFileExt", "REG_DWORD", val)
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)
                engine.win32_refresh_shell()

            # 8. Sticky Keys
            elif t_id == "win11_disable_sticky":
                flags = "506" if action == "apply" else "510"
                engine.win32_set_reg("HKCU", r"Control Panel\Accessibility\StickyKeys", "Flags", "REG_SZ", flags)
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)

            # 9. Ultimate Power Plan
            elif t_id == "game_ultimate_power":
                if action == "apply":
                    subprocess.run(["powercfg.exe", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"], shell=False, creationflags=CREATE_NO_WINDOW)
                    subprocess.run(["powercfg.exe", "/setactive", "e9a42b02-d5df-448d-aa00-03f14749eb61"], shell=False, creationflags=CREATE_NO_WINDOW)
                    self.applied_tweaks.add(t_id)
                else:
                    subprocess.run(["powercfg.exe", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], shell=False, creationflags=CREATE_NO_WINDOW)
                    self.applied_tweaks.discard(t_id)

            # 10. GameDVR
            elif t_id == "game_disable_dvr":
                val = 0 if action == "apply" else 1
                engine.win32_set_reg("HKCU", r"System\GameConfigStore", "GameDVR_Enabled", "REG_DWORD", val)
                engine.win32_set_reg("HKLM", r"SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", "REG_DWORD", val)
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)

            # 11. DiagTrack Telemetry Service
            elif t_id == "priv_diagtrack":
                if action == "apply":
                    engine.win32_stop_service("DiagTrack")
                    engine.win32_set_reg("HKLM", r"SYSTEM\CurrentControlSet\Services\DiagTrack", "Start", "REG_DWORD", 4)
                    self.applied_tweaks.add(t_id)
                else:
                    engine.win32_set_reg("HKLM", r"SYSTEM\CurrentControlSet\Services\DiagTrack", "Start", "REG_DWORD", 2)
                    self.applied_tweaks.discard(t_id)

            # 12. Explorer Shell Refresh
            elif t_id == "diag_restart_explorer":
                engine.win32_refresh_shell()
                messagebox.showinfo("Success", "Windows Explorer notification cache refreshed.")
                return

            # 13. Flush DNS
            elif t_id == "diag_flush_dns":
                try:
                    ctypes.windll.dnsapi.DnsFlushResolverCache()
                except Exception:
                    subprocess.run(["ipconfig.exe", "/flushdns"], shell=False, creationflags=CREATE_NO_WINDOW)
                messagebox.showinfo("Success", "DNS resolver cache flushed.")
                return

            # 14. Purge Temp
            elif t_id == "junk_clean_temp":
                temp = os.environ.get("TEMP", "")
                c = 0
                for r, dirs, files in os.walk(temp, topdown=False):
                    for f in files:
                        try:
                            os.remove(os.path.join(r, f))
                            c += 1
                        except OSError:
                            pass
                messagebox.showinfo("Success", f"Purged {c} temporary files.")
                return

            # 15. Recycle Bin
            elif t_id == "junk_empty_recycle":
                ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
                messagebox.showinfo("Success", "Recycle bins emptied.")
                return

            else:
                if action == "apply": self.applied_tweaks.add(t_id)
                else: self.applied_tweaks.discard(t_id)

            self.save_state()
            self.render_tweaks_batch()
            verb = "Applied" if action == "apply" else "Reverted"
            messagebox.showinfo("Success", f"{verb} tweak: {t_name}")

        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed modifying {t_name}:\n{e}")

    # -------------------------------------------------------------------------
    # VIEW 3: Universal File & Locker Shield
    # -------------------------------------------------------------------------
    def show_file_shield(self):
        self.set_active_nav("files")
        self.clear_viewport()

        head = ctk.CTkFrame(self.main_container, fg_color="transparent")
        head.pack(fill="x", pady=(0, 14))

        title = ctk.CTkLabel(head, text="Universal File & Locker Shield", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=T_TEXT)
        title.pack(anchor="w")

        sub = ctk.CTkLabel(head, text="Lock folders, break 'file in use' locks, take administrative ownership, or shred files.", font=ctk.CTkFont(size=13), text_color=T_TEXT_MUTED)
        sub.pack(anchor="w")

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        card = ctk.CTkFrame(scroll, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=10)
        card.pack(fill="x", pady=(0, 14), ipady=14, ipadx=14)

        lbl = ctk.CTkLabel(card, text="TARGET DIRECTORY OR FILE PATH", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=T_TEXT_MUTED)
        lbl.pack(anchor="w", padx=16, pady=(6, 4))

        self.custom_path_entry = ctk.CTkEntry(card, placeholder_text="Select or enter full absolute path...", height=40, fg_color=T_SURFACE_ALT, border_color=T_BORDER, text_color=T_TEXT)
        self.custom_path_entry.pack(fill="x", padx=16, pady=(0, 10))

        p_grid = ctk.CTkFrame(card, fg_color="transparent")
        p_grid.pack(fill="x", padx=16)
        p_grid.grid_columnconfigure((0, 1), weight=1)

        b_folder = ctk.CTkButton(p_grid, text="📂 Choose Folder", fg_color=T_SURFACE_ALT, text_color=T_TEXT, hover_color=T_ROW_HOVER, command=self.browse_custom_folder)
        b_folder.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        b_file = ctk.CTkButton(p_grid, text="📄 Choose File", fg_color=T_SURFACE_ALT, text_color=T_TEXT, hover_color=T_ROW_HOVER, command=self.browse_custom_file)
        b_file.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.create_action_card(scroll, "🔒 Apply System Cloak (+s +h)", "Makes path invisible to File Explorer, even with hidden items enabled.", "Cloak Path", self.apply_path_stealth, T_DANGER, T_DANGER_HOV)
        self.create_action_card(scroll, "🔓 Remove System Cloak (-s -h)", "Restores standard folder visibility in File Explorer.", "Restore Path", self.remove_path_stealth, T_SUCCESS, T_SUCCESS_HOV)
        self.create_action_card(scroll, "💥 Break Active File Locks", "Refreshes system handles to resolve 'File in use by another program' errors.", "Unlock Handle", self.break_file_lock, T_ACCENT, T_ACCENT_HOV)
        self.create_action_card(scroll, "🔑 Take Full Administrative Ownership", "Executes takeown & icacls to grant full access over protected system folders.", "Take Ownership", self.take_folder_ownership, T_ACCENT, T_ACCENT_HOV)
        self.create_action_card(scroll, "🔥 Secure Zero-Byte Shredder", "Overwrites file buffers with zeroes before removal to block recovery.", "Shred File", self.shred_selected_file, T_DANGER, T_DANGER_HOV)

    def create_action_card(self, parent, title, desc, btn_text, cmd, color, hover_color):
        card = ctk.CTkFrame(parent, fg_color=T_SURFACE, border_color=T_BORDER, border_width=1, corner_radius=10)
        card.pack(fill="x", pady=5, ipady=8, ipadx=12)

        box = ctk.CTkFrame(card, fg_color="transparent")
        box.pack(side="left", fill="both", expand=True, padx=12)

        t_lbl = ctk.CTkLabel(box, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=T_TEXT)
        t_lbl.pack(anchor="w")

        d_lbl = ctk.CTkLabel(box, text=desc, font=ctk.CTkFont(size=12), text_color=T_TEXT_MUTED)
        d_lbl.pack(anchor="w", pady=(2, 0))

        act_btn = ctk.CTkButton(card, text=btn_text, width=120, height=36, fg_color=color, hover_color=hover_color, text_color="#ffffff", font=ctk.CTkFont(size=12, weight="bold"), command=cmd)
        act_btn.pack(side="right", padx=12)

    # -------------------------------------------------------------------------
    # App Cloaker Operations
    # -------------------------------------------------------------------------
    def execute_hide_app(self):
        if not self.selected_app_name or self.selected_app_name not in self.filtered_apps:
            return
        meta = self.filtered_apps[self.selected_app_name]
        try:
            write_key = winreg.OpenKey(meta["root"], meta["route"], 0, winreg.KEY_ALL_ACCESS)
            try:
                cur_name, _ = winreg.QueryValueEx(write_key, "DisplayName")
                winreg.SetValueEx(write_key, "QuietDisplayName", 0, winreg.REG_SZ, cur_name)
                winreg.DeleteValue(write_key, "DisplayName")
            except FileNotFoundError:
                pass
            winreg.SetValueEx(write_key, "SystemComponent", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(write_key)

            if meta["directory"] and os.path.exists(meta["directory"]):
                engine.win32_set_stealth(meta["directory"], True)

            engine.win32_refresh_shell()
            meta["is_cloaked"] = True
            messagebox.showinfo("Success", f"Masked records & cloaked directory for:\n{self.selected_app_name}")
            self.render_app_list()
        except PermissionError:
            messagebox.showerror("Privilege Error", "Registry access denied. Run as Administrator.")

    def execute_restore_app(self):
        if not self.selected_app_name or self.selected_app_name not in self.filtered_apps:
            return
        meta = self.filtered_apps[self.selected_app_name]
        try:
            write_key = winreg.OpenKey(meta["root"], meta["route"], 0, winreg.KEY_ALL_ACCESS)
            try:
                q_name, _ = winreg.QueryValueEx(write_key, "QuietDisplayName")
                winreg.SetValueEx(write_key, "DisplayName", 0, winreg.REG_SZ, q_name)
                winreg.DeleteValue(write_key, "QuietDisplayName")
            except FileNotFoundError:
                pass
            try:
                winreg.DeleteValue(write_key, "SystemComponent")
            except FileNotFoundError:
                pass
            winreg.CloseKey(write_key)

            if meta["directory"] and os.path.exists(meta["directory"]):
                engine.win32_set_stealth(meta["directory"], False)

            engine.win32_refresh_shell()
            meta["is_cloaked"] = False
            messagebox.showinfo("Success", f"Restored standard visibility for:\n{self.selected_app_name}")
            self.render_app_list()
        except PermissionError:
            messagebox.showerror("Privilege Error", "Registry access denied. Run as Administrator.")

    def open_selected_folder(self):
        if not self.selected_app_name: return
        meta = self.filtered_apps[self.selected_app_name]
        if meta["directory"] and os.path.exists(meta["directory"]):
            os.startfile(meta["directory"])
        else:
            messagebox.showwarning("Not Found", "No registered directory found for this application.")

    def export_registry_key(self):
        if not self.selected_app_name: return
        meta = self.filtered_apps[self.selected_app_name]
        save_path = filedialog.asksaveasfilename(defaultextension=".reg", filetypes=[("Registry Script", "*.reg")], initialfile=f"{self.selected_app_name}_backup.reg")
        if save_path:
            root_str = "HKLM" if meta["root"] == winreg.HKEY_LOCAL_MACHINE else "HKCU"
            res = subprocess.run(["reg.exe", "export", f"{root_str}\\{meta['route']}", save_path, "/y"], shell=False, creationflags=CREATE_NO_WINDOW)
            if res.returncode == 0:
                messagebox.showinfo("Export Complete", f"Backup created:\n{save_path}")

    def direct_launch_app(self):
        if not self.selected_app_name: return
        meta = self.filtered_apps[self.selected_app_name]
        if meta["directory"] and os.path.exists(meta["directory"]):
            for file in os.listdir(meta["directory"]):
                if file.lower().endswith(".exe") and not any(x in file.lower() for x in ["unins", "crash", "helper"]):
                    os.startfile(os.path.join(meta["directory"], file))
                    return
        messagebox.showwarning("Notice", "Could not locate primary binary executable automatically.")

    def toggle_startup_state(self):
        if not self.selected_app_name:
            return
        run_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        ]
        found = False
        for root, p in run_paths:
            try:
                k = winreg.OpenKey(root, p, 0, winreg.KEY_ALL_ACCESS)
                for i in range(winreg.QueryInfoKey(k)[1]):
                    val_name, _, _ = winreg.EnumValue(k, i)
                    if self.selected_app_name.lower() in val_name.lower():
                        winreg.DeleteValue(k, val_name)
                        found = True
                        break
                winreg.CloseKey(k)
            except Exception:
                pass
        if found:
            messagebox.showinfo("Startup Cloaked", f"Removed '{self.selected_app_name}' from Windows Startup.")
        else:
            messagebox.showinfo("Clean", f"No active startup entry was matched for '{self.selected_app_name}'.")

    def camouflage_shortcut(self):
        p = filedialog.askopenfilename(filetypes=[("Shortcuts", "*.lnk")])
        if p and p.endswith(".lnk"):
            dir_name = os.path.dirname(p)
            new_path = os.path.join(dir_name, "Quarterly_Summary_Notes.docx.lnk")
            try:
                os.rename(p, new_path)
                messagebox.showinfo("Camouflaged", f"Shortcut disguised as document:\n{new_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed renaming shortcut:\n{e}")

    # -------------------------------------------------------------------------
    # File Shield Functions (Win32 Native Engine)
    # -------------------------------------------------------------------------
    def browse_custom_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.custom_path_entry.delete(0, tk.END)
            self.custom_path_entry.insert(0, os.path.normpath(p))

    def browse_custom_file(self):
        p = filedialog.askopenfilename()
        if p:
            self.custom_path_entry.delete(0, tk.END)
            self.custom_path_entry.insert(0, os.path.normpath(p))

    def apply_path_stealth(self):
        p = self.custom_path_entry.get().strip()
        if p and os.path.exists(p):
            if engine.win32_set_stealth(p, stealth=True):
                messagebox.showinfo("Protected", f"Native stealth attributes applied to:\n{p}")
            else:
                messagebox.showerror("Error", "Failed applying attributes to target path.")
        else:
            messagebox.showwarning("Invalid", "Please provide a valid file or folder path.")

    def remove_path_stealth(self):
        p = self.custom_path_entry.get().strip()
        if p and os.path.exists(p):
            if engine.win32_set_stealth(p, stealth=False):
                messagebox.showinfo("Restored", f"Attributes removed and visibility restored for:\n{p}")
            else:
                messagebox.showerror("Error", "Failed restoring attributes on target path.")
        else:
            messagebox.showwarning("Invalid", "Please provide a valid file or folder path.")

    def break_file_lock(self):
        p = self.custom_path_entry.get().strip()
        if not p or not os.path.exists(p):
            messagebox.showwarning("Invalid", "Target path does not exist.")
            return
        base_name = os.path.basename(p)
        if base_name.lower().endswith(".exe"):
            subprocess.run(["taskkill.exe", "/F", "/IM", base_name], shell=False, creationflags=CREATE_NO_WINDOW)
            messagebox.showinfo("Lock Terminated", f"Sent terminate signal to {base_name}.")
        else:
            engine.win32_refresh_shell()
            messagebox.showinfo("Shell Refreshed", "Shell notification broadcasted to clear open directory handles.")

    def take_folder_ownership(self):
        p = self.custom_path_entry.get().strip()
        if not p or not os.path.exists(p):
            messagebox.showwarning("Invalid", "Target path does not exist.")
            return
        # Run process arguments directly without shell invocation
        subprocess.run(["takeown.exe", "/F", p, "/R", "/D", "Y"], shell=False, creationflags=CREATE_NO_WINDOW)
        subprocess.run(["icacls.exe", p, "/grant", "administrators:F", "/T"], shell=False, creationflags=CREATE_NO_WINDOW)
        messagebox.showinfo("Ownership Granted", f"Administrative permissions assigned to:\n{p}")

    def shred_selected_file(self):
        p = self.custom_path_entry.get().strip()
        if not p or not os.path.isfile(p):
            messagebox.showwarning("Invalid", "Please select a specific individual file to shred.")
            return
        if messagebox.askyesno("Confirm Shred", f"Permanently overwrite and destroy:\n{p}?"):
            if engine.win32_shred_file(p):
                messagebox.showinfo("Shredded", "File safely zero-buffered and removed from disk.")
            else:
                messagebox.showerror("Error", "Failed shredding target file.")


# -----------------------------------------------------------------------------
# Runtime Entry with Auto-Elevation
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = PhantomDesk()
        app.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)