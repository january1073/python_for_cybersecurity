# Setup an autorun key in the Windows registry

import os, shutil, winreg

filedir = os.path.join(os.getcwd(),"Temp")
filename = "benign.exe"
filepath = os.path.join(filedir,filename)

if os.path.isfile(filepath):
	os.remove(filepath)

# Use buildexe.py to create an executable
os.system("python buildexe.py")

# Move the executable to the desired directory
shutil.move(filename,filedir)

# Windows default autorun keys:
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
# HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
# HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce

regkey = 1

if regkey < 2:
	reghive = winreg.HKEY_CURRENT_USER
else:
	reghive = winreg.HKEY_LOCAL_MACHINE
if (regkey % 2) == 0:
	regpath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
else:
	regpath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"

#Add registry autorun key
reg = winreg.ConnectRegistry(None,reghive)
key = winreg.OpenKey(reg, regpath,0,winreg.KEY_WRITE)
winreg.SetValueEx(key,"SecurityScan",0,winreg.REG_SZ,filepath)
