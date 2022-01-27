# Code by Camden

import os, sys, socket, signal, threading
from utilities import *

try:
    from colorama import Fore, Style
    color = True
except: color = False

def client():
    global color
    old = ""
    address = (g.IP, 12000)
    print("Client started...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    while g.on:
        try:
            encode = str.encode(g.read)
            sock.sendto(encode, address)
            data = sock.recv(1024)
            g.write = bytes.decode(data)
            if g.write != old:
                if color: print(f"{Fore.RED}RED{Style.RESET_ALL}: {g.write}")
                else: print(f"RED: {g.write}")
                old = g.write
        except: pass
    sock.close()

if __name__== "__main__":
    get()
    g.on = True
    g.p8 = sub()
    g.write = "blue"
    data = g.p8.stdout.read(1)
    data = int.from_bytes(data, "big")
    if data == 1:
        print("An experiment by Camden!")
        reading_thread = threading.Thread(target = from_pico8)
        writing_thread = threading.Thread(target = to_pico8)
        clients_thread = threading.Thread(target = client)
        reading_thread.start()
        writing_thread.start()
        clients_thread.start()
        try:
            while g.p8.poll() is None: pass
        except: pass
        try: os.kill(g.p8.pid, signal.SIGTERM)
        except: pass
        g.on = False
        reading_thread.join()
        writing_thread.join()
        clients_thread.join()
        print("Finished!")
    else:
        print("Failed to start!")
        sys.exit(1)
