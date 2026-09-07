"""
PhantomDesk Native Win32 API Engine
Replaces subprocess calls with direct Kernel32, Shell32, Advapi32, and Winreg APIs.
"""

import os
import sys
import ctypes
from ctypes import wintypes
import winreg

# --- WIN32 CONSTANTS & APIS ---
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32
advapi32 = ctypes.windll.advapi32

FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
FILE_ATTRIBUTE_NORMAL = 0x80
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF

SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0000

SC_MANAGER_ALL_ACCESS = 0xF003F
SERVICE_STOP = 0x0020
SERVICE_START = 0x0010
SERVICE_CONTROL_STOP = 0x00000001


class SERVICE_STATUS(ctypes.Structure):
    _fields_ = [
        ("dwServiceType", wintypes.DWORD),
        ("dwCurrentState", wintypes.DWORD),
        ("dwControlsAccepted", wintypes.DWORD),
        ("dwWin32ExitCode", wintypes.DWORD),
        ("dwServiceSpecificExitCode", wintypes.DWORD),
        ("dwCheckPoint", wintypes.DWORD),
        ("dwWaitHint", wintypes.DWORD),
    ]


# --- 1. REGISTRY OPERATIONS (Bypasses 'reg.exe') ---
HIVE_MAP = {
    "HKLM": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKCU": winreg.HKEY_CURRENT_USER,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
}

TYPE_MAP = {
    "REG_DWORD": winreg.REG_DWORD,
    "REG_SZ": winreg.REG_SZ,
    "REG_EXPAND_SZ": winreg.REG_EXPAND_SZ,
    "REG_MULTI_SZ": winreg.REG_MULTI_SZ,
}


def win32_set_reg(hive_str: str, subkey: str, name: str, reg_type_str: str, value) -> bool:
    """Sets a registry key value directly via Winreg."""
    try:
        hive = HIVE_MAP.get(hive_str.upper())
        reg_type = TYPE_MAP.get(reg_type_str, winreg.REG_SZ)
        if hive is None:
            return False

        if reg_type == winreg.REG_DWORD:
            value = int(value)

        with winreg.CreateKeyEx(hive, subkey, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY) as key:
            winreg.SetValueEx(key, name, 0, reg_type, value)
        return True
    except Exception:
        return False


def win32_delete_reg(hive_str: str, subkey: str, name: str) -> bool:
    """Removes a registry value without touching the parent key."""
    try:
        hive = HIVE_MAP.get(hive_str.upper())
        if hive is None:
            return False

        with winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY) as key:
            winreg.DeleteValue(key, name)
        return True
    except FileNotFoundError:
        return True
    except Exception:
        return False


# --- 2. FILE VISIBILITY & LOCKER (Bypasses 'attrib.exe') ---
def win32_set_stealth(path: str, stealth: bool = True) -> bool:
    """Applies or strips Hidden (+h) and System (+s) flags natively."""
    try:
        current_attrs = kernel32.GetFileAttributesW(path)
        if current_attrs == INVALID_FILE_ATTRIBUTES:
            return False

        if stealth:
            new_attrs = current_attrs | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
        else:
            new_attrs = current_attrs & ~(FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)
            if new_attrs == 0:
                new_attrs = FILE_ATTRIBUTE_NORMAL

        return bool(kernel32.SetFileAttributesW(path, new_attrs))
    except Exception:
        return False


# --- 3. SHELL NOTIFICATION (Bypasses 'taskkill /f /im explorer.exe') ---
def win32_refresh_shell():
    """Forces Windows Explorer to refresh its icon, desktop, and menu cache silently."""
    shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)


# --- 4. SERVICE CONTROL (Bypasses 'sc.exe') ---
def win32_stop_service(service_name: str) -> bool:
    """Stops a Windows service through the Service Control Manager API."""
    scm = advapi32.OpenSCManagerW(None, None, SC_MANAGER_ALL_ACCESS)
    if not scm:
        return False

    try:
        svc = advapi32.OpenServiceW(scm, service_name, SERVICE_STOP)
        if not svc:
            return False

        try:
            status = SERVICE_STATUS()
            return bool(advapi32.ControlService(svc, SERVICE_CONTROL_STOP, ctypes.byref(status)))
        finally:
            advapi32.CloseServiceHandle(svc)
    finally:
        advapi32.CloseServiceHandle(scm)


# --- 5. CLEAN FILE SHREDDER (Bypasses Wiper Heuristics) ---
def win32_shred_file(path: str) -> bool:
    """Overwrites file data with zeros in fixed 64KB buffers and deletes the file handle."""
    try:
        if not os.path.exists(path):
            return False

        file_size = os.path.getsize(path)
        chunk_size = 65536
        zero_buffer = b"\x00" * chunk_size

        with open(path, "wb") as f:
            remaining = file_size
            while remaining > 0:
                write_len = min(remaining, chunk_size)
                f.write(zero_buffer[:write_len])
                remaining -= write_len
            f.flush()

        os.remove(path)
        return True
    except Exception:
        return False