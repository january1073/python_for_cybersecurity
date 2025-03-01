# Read the path value and edit it

import os
import winreg

def readPathValue(reghive, regpath):
    try:
        with winreg.OpenKey(reghive, regpath, 0, winreg.KEY_READ) as key:
            index = 0
            while True:
                val = winreg.EnumValue(key, index)
                if val[0] == "Path":
                    return val[1]
                index += 1
    except OSError:
        return None

def editPathValue(reghive, regpath, targetdir):
    path = readPathValue(reghive, regpath)
    if path is None:
        print("Failed to read Path value.")
        return

    newpath = targetdir + ";" + path

    try:
        with winreg.OpenKey(reghive, regpath, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, newpath)
            print(f"Successfully updated Path with: {targetdir}")
    except OSError:
        print("Failed to update Path value. Try running as administrator.")

# Modify user path
reghive = winreg.HKEY_CURRENT_USER
regpath = "Environment"
targetdir = os.getcwd()

editPathValue(reghive, regpath, targetdir)

# Modify SYSTEM path (requires admin)
# reghive = winreg.HKEY_LOCAL_MACHINE
# regpath = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
# editPathValue(reghive, regpath, targetdir)
