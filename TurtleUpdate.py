import os, subprocess, time

#get home and where to clone to
cwd = os.getcwd()
mainfile = cwd[:cwd.rfind('\\')]
print(cwd)
print(mainfile)

#Clone to location
os.system(("cd " + cwd))
os.system("git pull https://github.com/Quiltic/Turtle.git")
print("cloned")

#give it a moment or 12 then go home
time.sleep(3)
os.system(("cd "+ cwd))

#reopen turtle
callfreind = "python " + cwd + "\\Turtle.py"
print(callfreind)
subprocess.Popen(callfreind)
print("Updated!")