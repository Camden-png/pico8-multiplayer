# Code by Camden

import os, sys, socket, signal, threading
from utilities import *

try:
    from colorama import Fore, Style
    color = True
except: color = False

def server():
    global color
    old = ""
    address = ("0.0.0.0", 12000)
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    print(f"Server started with IP: {IP}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.bind(address)
    while g.on:
        try:
            data, address = sock.recvfrom(1024)
            g.write = bytes.decode(data)
            if g.write != old:
                if color: print(f"{Fore.BLUE}BLUE{Style.RESET_ALL}: {g.write}")
                else: print(f"BLUE: {g.write}")
                old = g.write
            encode = str.encode(g.read)
            sock.sendto(encode, address)
        except: pass
    sock.close()

if __name__== "__main__":
    get()
    g.on = True
    g.p8 = sub()
    g.write = "red"
    data = g.p8.stdout.read(1)
    data = int.from_bytes(data, "big")
    if data == 1:
        print("An experiment by Camden!")
        reading_thread = threading.Thread(target = from_pico8)
        writing_thread = threading.Thread(target = to_pico8)
        servers_thread = threading.Thread(target = server)
        reading_thread.start()
        writing_thread.start()
        servers_thread.start()
        try:
            while g.p8.poll() is None: pass
        except: pass
        try: os.kill(g.p8.pid, signal.SIGTERM)
        except: pass
        g.on = False
        reading_thread.join()
        writing_thread.join()
        servers_thread.join()
        print("Finished!")
    else:
        print("Failed to start!")
        sys.exit(1)
