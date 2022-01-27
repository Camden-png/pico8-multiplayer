# Code by Camden

import os, re, sys, time, platform, subprocess as sp

class g:
    directory_application = None
    directory_carts = None
    IP = "localhost"
    pause = None
    scale = None
    on = False
    p8 = None
    write = ""
    read = ""

def sub():
    g.scale = str(g.scale * 128)
    return sp.Popen([fr"{g.directory_application}", "-width", g.scale, "-height", g.scale, "-run", fr"{g.directory_carts}"], stdin = sp.PIPE, stdout = sp.PIPE)

def string_to_bytes(string):
    length = 16 - len(string)
    bytes = bytearray(string, "utf-8")
    bytes.extend(bytearray(length))
    return bytes

def to_pico8():
    old = None
    while g.on:
        try:
            bytes = bytearray(16)
            if g.write != old: bytes = string_to_bytes(g.write)
            g.p8.stdin.write(bytes)
            g.p8.stdin.flush()
            old = g.write
        except: pass
        time.sleep(g.pause)

def from_pico8():
    old = None
    string = ""
    while g.on:
        try:
            data = g.p8.stdout.read(1).decode("utf-8")
            if data != "$": string += data
            else:
                if string != old:
                    g.read = string
                    old = string
                string = ""
        except: pass

def clear():
    if platform.system() == "Windows": os.system("cls")
    else: os.system("clear")

def error(message, bool = True):
    global flag
    print(f"Error: {message} not found!")
    if bool: flag = True
    else: sys.exit(1)

def get():
    global flag
    clear()
    name = "settings.txt"
    try: file = open(name, "r")
    except: error(name, False)
    lines = file.read().splitlines()
    file.close()
    for line in lines:
        string = None
        groups = re.search(r"(?<=\:)([^\#]*)", line)
        if groups: string = groups.group().strip()
        if not string or string == "none": continue
        if line.startswith("Directory to application:"): g.directory_application = string
        elif line.startswith("Directory to cart:"): g.directory_carts = string
        elif line.startswith("Default IP:"): g.IP = string
        elif line.startswith("Pause:"):
            try: g.pause = abs(float(string))
            except: pass
        elif line.startswith("Scale:"):
            string = string.lower().replace("x", "")
            try:
                value = int(string)
                if value < 1: value = 1
                elif value > 11: value = 5
                g.scale = value
            except: pass
    flag = False
    if not g.directory_application: error("Pico-8 app")
    if not g.directory_carts: error("Pico-8 carts folder")
    if not g.IP: error("IP")
    if g.pause is None: error("waiting pause")
    if g.scale is None: error("window scale")
    if flag: sys.exit(1)
