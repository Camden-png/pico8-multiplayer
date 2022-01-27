import os, platform, multiprocessing, subprocess as sp
from multiprocessing import Process
from utilities import clear

def process(command, name):
    try: sp.run(f"{command} {name}.py", stdout = sp.DEVNULL, stderr = sp.DEVNULL)
    except: pass

if __name__ == "__main__":
    clear()
    command = "python"
    print("Terminal output is hidden in testing mode...")
    if platform.system() != "Windows": command += "3"
    try:
        server = Process(target = process, args = (command, "server"))
        client = Process(target = process, args = (command, "client"))
        server.start()
        client.start()
        server.join()
        client.join()
    except: pass
    print("Finished!")
