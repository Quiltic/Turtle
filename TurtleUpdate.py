import os, subprocess, time

time.sleep(10)
#get home and where to clone to
cwd = "/home/pi/Turtle"#os.getcwd()
#mainfile = cwd[:cwd.rfind('\\')]
print(cwd)


#Clone to location
os.system(("cd " + cwd))
os.system("git pull https://github.com/Quiltic/Turtle.git")
print("cloned")

#give it a moment or 12 then go home
time.sleep(3)
os.system(("cd "+ cwd))

#reopen turtle
time.sleep(10)
callfreind = "python3 " + cwd + "/Turtle.py"
os.system("ls")
print(callfreind)
subprocess.Popen(callfreind)
print("Updated!")

print("Turning off")
