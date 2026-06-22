import os
import shutil
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
# why did you decomplile this code lil bro
# as you here... hi

def kill_minecraft():
    """Silently terminates the Minecraft process if it is running to release file locks."""
    print("[-] Ensuring Minecraft process is closed to avoid file locks...")
    os.system("taskkill /f /im Minecraft.Windows.exe >nul 2>&1")

print("      MINECRAFT WINDOWS EDITION - DLSS  REPLACER      ")
def select_replacement_file() -> Path:
    """Opens a file dialog for the user to select the replacement DLL."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("[-] Opening file select menu...")
    selected_file = filedialog.askopenfilename(
        title="Select the replacement file: nvngx_dlss.dll",
        filetypes=[("DLL Files", "*.dll"), ("All Files", "*.*")],
    )

    if not selected_file:
        print("[-] No file selected. Exiting.")
        sys.exit(1)

    return Path(selected_file)


def perform_replacement():
    TARGET_PATH = Path(
        r"C:\XboxGames\Minecraft for Windows\Content\nvngx_dlss.dll"
    )
    BACKUP_PATH = TARGET_PATH.with_suffix(".dll.bak")

    # 1. Verify target directory and original file exist
    if not TARGET_PATH.is_file():
        print(f"[-] Target original file not found at: {TARGET_PATH}")
        print("[-] Verification failed. Exiting.")
        return

    # 2. Backup the original file first if a backup doesn't already exist
    if not BACKUP_PATH.exists():
        try:
            print(f"[-] Creating backup of original DLL at: {BACKUP_PATH}")
            shutil.copy2(TARGET_PATH, BACKUP_PATH)
            print("[-] Backup created successfully.")
        except Exception as e:
            print(f"[-] Failed to create backup: {e}")
            return
    else:
        print(f"[-] Existing backup found at: {BACKUP_PATH} (Skipping backup stage)")

    # 3. Get the replacement file via GUI prompt
    replacement_path = select_replacement_file()

    # 4. Kill the process if it spawned to unlock the file handle
    kill_minecraft()

    try:
        # 5. Overwrite the target
        print(f"[-] Overwriting {TARGET_PATH.name}...")
        shutil.copy2(replacement_path, TARGET_PATH)
        print(f" sent to: {TARGET_PATH.name}")

        print ("-patched successfully!")
    except PermissionError as e:
        print(f"[-] Permission Denied: {e}")
        print(
            "[-] If the process was killed, this directory likely requires elevated permissions or ACL modification."
        )
    except Exception as e:
        print(f"[-] An error occurred during replacement: {e}")


if __name__ == "__main__":
    perform_replacement()