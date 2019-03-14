"""
Author: Andrej Avbelj

All icons were downloaded from https://www.flaticon.com
Authors of icons:
https://www.flaticon.com/authors/hanan
https://www.flaticon.com/authors/dave-gandy
https://www.freepik.com/
https://www.flaticon.com/authors/situ-herrera
"""

from tkinter import *
from PIL import ImageTk, Image
from cv2 import *
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from time import sleep
import numpy as np

root = Tk()
root.title('Paint2')
root.state('zoomed')

bottomframe = Label(root)
bottomframe.pack( side = BOTTOM )

filename = "neki.png"
drawing = False
point1 = ()
point2 = ()
color = (0, 0, 0, 255)
colorForImage = "#000000"
zanka = None
photo = 0
vid = cv2.VideoCapture(0)
width = 0
height = 0
layer1 = None
res = 0
cng = 0
cvImg = 0
aliVideoAliSlika = 0
izbira = 1
text = ""


def tocka2(x, y):
    global point2
    point2 = (x, y)


def posodobiSLiko():
    global layer1, res, cvImg, bottomframe, photo, cng, aliVideoAliSlika, height, width

    cvImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

    height = np.size(cvImg, 0)
    width = np.size(cvImg, 1)

    if height > 800 or width > 1600:
        cvImg = cv2.resize(img, (int(width / 10), int(height / 10)))
        height = np.size(cvImg, 0)
        width = np.size(cvImg, 1)
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGBA)

    res = cvImg[:]
    cnd = layer1[:, :, 3] > 0
    res[cnd] = layer1[cnd]

    photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(res))
    bottomframe.photo = photo
    bottomframe.configure(image=photo)


def draw(event):
    global drawing
    global point1

    drawing = True
    point1 = (event.x, event.y)

    if izbira == 4:
        point1 = (event.x - 30, event.y)
        point2 = (event.x + 30, event.y)
        cv2.line(layer1, point1, point2, color, 5)

        point1 = (event.x, event.y - 30)
        point2 = (event.x, event.y + 30)
        cv2.line(layer1, point1, point2, color, 5)

    elif izbira == 5:
        print(izbira)
        cv2.putText(layer1, text, (event.x, event.y), 2, 2, color, 2, cv2.LINE_AA)
        point1 = (event.x, event.y)

    if aliVideoAliSlika == 0:
        posodobiSLiko()


def mouseDown(event):
    global drawing, color, layer1, point1, res, cvImg, aliVideoAliSlika


    if drawing == True:

        if izbira == 0:
            cv2.line(layer1, point1, (event.x,event.y), (0, 0, 0, 0), 20)
            point1 = (event.x, event.y)
        elif izbira == 1:
            cv2.line(layer1, point1, (event.x, event.y), color, 5)
            point1 = (event.x, event.y)
        elif izbira == 2:
            tocka2(event.x, event.y)

        if aliVideoAliSlika == 0:
            posodobiSLiko()


def buttonUp(event):
    global drawing, layer1, color, point1, point2

    drawing = False

    if izbira == 0:
        cv2.line(layer1, point1, (event.x, event.y), (0, 0, 0, 0), 5)
        point1 = (event.x, event.y)
    elif izbira == 1:
        cv2.line(layer1, point1, (event.x, event.y), color, 5)
        point1 = (event.x, event.y)
    elif izbira == 2:
        cv2.rectangle(layer1, point1, point2, color, 3)
    elif izbira == 3:

        radius = 0

        if(abs(point1[0]-event.x) > abs(point1[1]-event.y)):
            radius = abs(point1[0]-event.x)
        else:
            radius = abs(point1[1]-event.y)

        cv2.circle(layer1, point1, radius, color, 5)
        point1 = (event.x, event.y)

    if aliVideoAliSlika == 0:
        posodobiSLiko()


def cancel():
    global bottomframe, zanka, aliVideoAliSlika
    aliVideoAliSlika = 0

    if zanka is not None:
        bottomframe.after_cancel(zanka)
        zanka = None


def odprisliko():
    global filename, layer1, bottomframe, height, width, photo, img

    cancel()

    filename = askopenfilename()
    img = cv2.imread(filename)

    cvImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

    height = np.size(cvImg, 0)
    width = np.size(cvImg, 1)

    if height > 800 or width > 1600:
        cvImg = cv2.resize(img, (int(width / 10), int(height / 10)))
        height = np.size(cvImg, 0)
        width = np.size(cvImg, 1)
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGBA)

    layer1 = np.zeros((height, width, 4))

    print(layer1.size)
    print(cvImg.size)

    res = cvImg[:]
    cnd = layer1[:, :, 3] > 0
    res[cnd] = layer1[cnd]

    photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(res))
    bottomframe.photo = photo
    bottomframe.configure(image=photo)


def update():
    global vid, zanka, bottomframe, layer1

    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    res = img[:]
    cnd = layer1[:, :, 3] > 0
    res[cnd] = layer1[cnd]

    photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(res))
    bottomframe.photo = photo
    bottomframe.configure(image=photo)

    zanka = bottomframe.after(10, update)


def odprivideo():
    global vid, aliVideoAliSlika, height, width, layer1

    aliVideoAliSlika = 1

    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    layer1 = np.zeros((height, width, 4))

    if not vid.isOpened() or zanka == None:
        update()


def usePencil():
    global color, sizeOfBrush, izbira
    izbira = 1
    sizeOfBrush = 5
    color = (0, 0, 0, 255)


def zbrisi():
        global  izbira
        izbira = 0


def colorPick():
    global color, colorForImage
    pomozna = askcolor()

    color= pomozna[0]
    colorForImage = pomozna[1]
    c = list(color)
    c.append(255)
    color = tuple(c)
    print(color)


def vstaviText():
    global izbira, text
    if ent.get() == "":
        print("Nic ni notr")
    else:
        text = ent.get()
        izbira = 5


def useRectangle():
    global izbira
    izbira = 2


def useCircle():
    global izbira
    izbira = 3


def useCross():
    global izbira
    izbira = 4


pencil = PhotoImage(file="images/pencil.png")
rubber = PhotoImage(file="images/rubber.png")
colorPickerImg = PhotoImage(file="images/color.png")

rectImg = PhotoImage(file="images/rectangle.png")
circleImg = PhotoImage(file="images/circle.png")
crossImg = PhotoImage(file="images/add.png")

open = Button(root, text ="Open image", width=10, height=2, command=lambda: odprisliko())
open.pack(side=LEFT, anchor=W, expand=NO)

video = Button(root, text ="Video", width=10, height=2, command=lambda: odprivideo())
video.pack(side=LEFT, anchor=W, expand=NO)

brisi = Button(root, image=rubber, width=32, height=32, command=lambda: zbrisi())
brisi.pack(side=LEFT, anchor=W, expand=NO)

colorBtn = Button(root, image =colorPickerImg, width=32, height=32, command=lambda: colorPick())
colorBtn.pack(side=LEFT, anchor=W, expand=NO)

prostorocno = Button(root, image=pencil, width=32, height=32, command=lambda: usePencil())
prostorocno.pack(side=LEFT, anchor=W, expand=NO)

rectangle = Button(root, image=rectImg, width=32, height=32, command=lambda: useRectangle())
rectangle.pack(side=LEFT, anchor=W, expand=NO)

circle = Button(root, image=circleImg, width=32, height=32, command=lambda: useCircle())
circle.pack(side=LEFT, anchor=W, expand=NO)

cross = Button(root, image=crossImg, width=32, height=32, command=lambda: useCross())
cross.pack(side=LEFT, anchor=W, expand=NO)

Label(root, text="Text: ").pack(side=LEFT, anchor=W, expand=NO)

ent = Entry(root)
ent.pack(side=LEFT, anchor=W, expand=NO)

insertText = Button(root, text ="Vstavi", width=10, height=2, command=lambda: vstaviText())
insertText.pack(side=LEFT, anchor=W, expand=NO)

bottomframe.bind('<ButtonPress-1>', draw)
bottomframe.bind('<B1-Motion>', mouseDown)
bottomframe.bind('<ButtonRelease-1>', buttonUp)

root.mainloop()
