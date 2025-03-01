# Create executable from a Python file

import PyInstaller.__main__
import shutil
import os

filename = "executable.py" # Enter your filename
exename = "benign.exe" # Enter your filename
icon = "Firefox.ico" # Choose an icon
pwd = os.getcwd()
usbdir = os.path.join(pwd,"USB")

if os.path.isfile(exename):
	os.remove(exename)

print("Creating EXE")

# Create executable from Python script
PyInstaller.__main__.run([
	"executable.py",
	"--onefile",
	"--clean",
	"--log-level=ERROR",
	"--name="+exename,
	"--icon="+icon
])

# Clean up after PyInstaller
shutil.move(os.path.join(pwd,"dist",exename),pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__", ignore_errors=True)
os.remove(exename+".spec")
