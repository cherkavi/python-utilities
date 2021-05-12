import psutil

PROCNAME = "python.exe"

for proc in psutil.process_iter():
    # kill process
    if proc.name() == PROCNAME:
        proc.kill()
