import math
import csv
from tkinter import *
import re

frz_names = {}

with open("./frz_names.csv",'r') as data:
   for line in csv.reader(data):
       frz_names[line[0]] = line[1]

def ms_to_frames(ms): return round(ms*6/100) + 200
def get_column_index(x, keyCount): return math.floor(x * keyCount / 512)

def execute():
    id = id_ent.get()
    f = open(path_ent.get(), "r")
    whole = f.readlines()
    i = 0
    while (whole[i] != "[Difficulty]\n"): i += 1
    i += 2 #coloca no CS
    keyCount = int(re.search("[0-9]{1,2}$", whole[i]).group())

    speed_data = "|speed_data" + id + "="
    while (whole[i] != "[TimingPoints]\n"): i += 1
    i += 1
    while (whole[i] != "\n"):
        curr = whole[i].split(",")
        if (curr[6] == "0"):
            frame = ms_to_frames(round(float(curr[0])))
            speed = 100 / float(curr[1][1:])
            speed_data += str(frame) + "," + str(speed) + ","
        i += 1

    if speed_data[-1] == ',':
        speed_data = speed_data[:-1]

    while(whole[i] != "[HitObjects]\n"): i += 1
    i += 1 #coloca na primeira nota


    notes = [[] for _ in range(keyCount)]
    notes_frz = [[] for _ in range(keyCount)]

    try:
        while(whole[i] != ""):
            curr = whole[i].split(",")
            col = get_column_index(int(curr[0]), keyCount)
            frame = ms_to_frames(int(curr[2]))
            is_frz = int(curr[3]) >= 128
            if is_frz:
                frz_end = ms_to_frames(int(curr[5].split(":")[0]))
                notes_frz[col].append(frame)
                notes_frz[col].append(frz_end)
            else:
                notes[col].append(frame)

            i += 1
    except IndexError:
        print(":3")
    except:
        print("error")

    col_names = col_names_txt.get("1.0", "end - 1 chars").splitlines()

    result_ent.delete(0, END)
    s = ""

    for col in range(keyCount):
        s += "|" + col_names[col] + id + "_data="
        for n in notes[col]:
            s += str(n) + ","
        if s[-1] == ',':
            s = s[:-1]

    for col in range(keyCount):
        s += "|" + frz_names[col_names[col]] + id + "_data="
        for n in notes_frz[col]:
            s += str(n) + ","
        if s[-1] == ',':
            s = s[:-1]
    print("meow!")

    result_ent.insert(0, s + speed_data)






master = Tk()
Label(master, text='.osu path').grid(row=0, column=0)
path_ent = Entry(master, width=105)
path_ent.grid(row=0, column=1)
Label(master, text='id').grid(row=1, column=0)
id_ent = Entry(master, width=105)
id_ent.grid(row=1, column=1)
Label(master, text='col names').grid(row=2, column=0)
col_names_txt = Text(master)
col_names_txt.grid(row=2, column=1)
Label(master, text='result').grid(row=3, column=0)
result_ent = Entry(master, width=105)
result_ent.grid(row=3, column=1)
Button(master, text='execute', command=execute,width=50).grid(row=4, column=1)
mainloop()