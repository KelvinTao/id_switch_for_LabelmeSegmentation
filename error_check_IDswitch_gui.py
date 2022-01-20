#conda activate bcnet_bak_20211105
#E:
#cd E:\txm\rat\script\vps_script_20211227\segFormatConvert_here
#python #4_1_error_check_IDswitch_gui.py
#python

import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
import requests,glob,os,shutil
from PIL import Image,ImageTk
import numpy as np
import json

##
HEIGHT = 800
WIDTH = 900

def open_folder():
    global i,imgs
    path_=askdirectory()#.replace('/','\\')
    #path.set(path_)
    imgs=glob.glob(os.path.join(path_,'*.jpg'))
    index=np.argsort([int(os.path.split(os.path.splitext(j)[0])[1]) for j in imgs])
    imgs=[imgs[j] for j in index]
    i=0
    show_image()
    label0['text'] = str(len(imgs))+': '+imgs[i]


def switch():
    global i,imgs
    #label['text'] = 'switched!'
    ann=json.load(open(imgs[i].replace('.jpg','.json')))
    mid=ann['shapes'][0]['label']
    ann['shapes'][0]['label']=ann['shapes'][1]['label']
    ann['shapes'][1]['label']=mid
    coco_file = open(imgs[i].replace('.jpg','.json'), "w",encoding='utf-8') 
    json.dump(ann, coco_file, indent = 4)
    coco_file.close()
    show_image()

def delete():
    global i,imgs
    os.remove(imgs[i])
    os.remove(imgs[i].replace('.jpg','.json'))##remove json file
    imgs.pop(i)
    judge()
    show_image()


def move():
    global i,imgs
    errorPath=os.path.split(imgs[i])[0]+'/'+'error'
    imgName=os.path.split(imgs[i])[1]
    os.makedirs(errorPath,exist_ok=True)
    shutil.move(imgs[i].replace('.jpg','.json'),errorPath+'/'+imgName.replace('.jpg','.json'))##remove json file
    shutil.move(imgs[i],errorPath+'/'+imgName)##remove jpg file
    imgs.pop(i)
    judge()
    show_image()



def get_pre_img():
    global i,imgs
    i=i-1
    judge()
    show_image()


def judge():
    global i,imgs
    if i<0:
        i=0
    if i>=len(imgs):
        i=len(imgs)-1


def get_next_img():
    global i,imgs
    i=i+1
    judge()
    show_image()


def show_image():
    global i,imgs
    #转换成array
    #im_array = np.array(Image.open(imgs[i]))
    #array转换成image    #image = ImageTk.PhotoImage(Image.open(imgs[i]))
    ##adapt to tk
    #image = ImageTk.PhotoImage(Image.fromarray(np.uint8(im_array)))
    image=prepare_image()
    label.configure(image=image)
    label.image=image
    label0['text'] = str(len(imgs))+': '+imgs[i]


def prepare_image():
    global i,imgs
    ##get image
    im_array = np.array(Image.open(imgs[i]))##600x800x3
    ##get json
    ann=json.load(open(imgs[i].replace('.jpg','.json')))
    ##get annotation
    ##ratwhite0: red; ratwhite1:blue
    for l in range(len(ann['shapes'])):
        if ann['shapes'][l]['label']=='rat-white0':
            colorSlice=0
        elif ann['shapes'][l]['label']=='rat-white1':
            colorSlice=1
        else:
            colorSlice=2
        for cr in ann['shapes'][l]['points']:#800x600
            ro=int(cr[1])
            co=int(cr[0])
            im_array[ro-2:ro+2,co-2:co+2,colorSlice]=255
    #array转换成image
    ##adapt to tk
    #image = ImageTk.PhotoImage(Image.open(imgs[i]))
    image = ImageTk.PhotoImage(Image.fromarray(np.uint8(im_array)))
    label0['text'] = str(len(imgs))+': '+imgs[i]
    return image

def keyFunc(event):
    if event.char=='a':
        get_pre_img()
    if event.char=='d':
        get_next_img()
    if event.char=='s':
        switch()
    if event.char=='x':
        delete()
    if event.char=='o':
        open_folder()
    if event.char=='m':
        move()

        
##
'''
path0='E:/txm/rat/script/vps_script_20211227/GUI-master'
#path0='/Users/taoxianming/Documents/research/Rat/segment/vps_script_20211227/GUI-master'
folder='wwrat_1_15fps_0'
path=os.path.join(path0,folder)
##images sort by number
imgs=glob.glob(os.path.join(path,'*.jpg'))
index=np.argsort([int(os.path.split(os.path.splitext(j)[0])[1]) for j in imgs])
imgs=[imgs[j] for j in index]
'''


##path and file setup
i=0
imgs=[]
#path=StringVar()
#path.set(os.path.abspath('.'))

##gui setup
root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


##show image path region
frame0 = tk.Frame(root, bg='#80c1ff', bd=2)
frame0.place(relx=0.5, rely=0.01, relwidth=0.8, relheight=0.05, anchor='n')
label0 = tk.Label(frame0,font=30)
label0.place(relwidth=1, relheight=1)

##button regoin
frame = tk.Frame(root, bg='#80c1ff', bd=2)
frame.place(relx=0.5, rely=0.07, relwidth=0.6, relheight=0.06, anchor='n')
##
button_opendir = tk.Button(frame, text="opendir\no", font=30, command=lambda: open_folder())
button_opendir.place(relx=0.05, relheight=1, relwidth=0.15)

#entry = tk.Entry(frame, font=40)
#entry.place(relwidth=0.65, relheight=1)
button_pre = tk.Button(frame, text="pre\na", font=30, command=lambda: get_pre_img())
button_pre.place(relx=0.3, relheight=1, relwidth=0.12)
##
button_next = tk.Button(frame, text="next\nd", font=30, command=lambda: get_next_img())
button_next.place(relx=0.45, relheight=1, relwidth=0.12)
##
button = tk.Button(frame, text="switch\ns", font=40, command=lambda: switch())
button.place(relx=0.60, relheight=1, relwidth=0.12)

##
button_m = tk.Button(frame, text="move\nm", font=40, command=lambda: move())
button_m.place(relx=0.75, relheight=1, relwidth=0.12)

##
button_d = tk.Button(frame, text="del\nx", font=40, command=lambda: delete())
button_d.place(relx=0.9, relheight=1, relwidth=0.12)
#

##image show region
lower_frame = tk.Frame(root, bg='#80c1ff', bd=2)
lower_frame.place(relx=0.5, rely=0.2, relwidth=0.888888, relheight=0.75, anchor='n')

#image0=prepare_image()
#label = tk.Label(lower_frame,image=image0)
label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)
##binding keys
root.bind("<Key>",keyFunc)
##
root.mainloop()
