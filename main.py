import tkMessageBox
from Tkinter import *
from math import sqrt
from tkSimpleDialog import askstring

root = Tk()

datadict = {}
group = 0
groupc = 0
cx = 0
cy = 1
label = True
k = ''
v = ''


class NewPreset:
    def __init__(self, data):
        self.data = data
        self.title = ''
        self.eq = ''
        self.comp = ''
        for item in data:
            if 'Title' in item:
                self.title = data[item]
            elif 'Comp' in item:
                self.comp = data[item]
            elif 'EQ' in item:
                self.eq = data[item]


class Preset:
    def __init__(self, data, count):
        self.data = data
        self.count = count
        self.title = ''
        self.eq = ''
        self.comp = ''
        for item in data:
            if str(count) in item:
                if 'Title' in item:
                    self.title = data[item][0:-1]
                elif 'Comp' in item:
                    self.comp = data[item]
                elif 'EQ' in item:
                    self.eq = data[item]


with open('data.api', 'r+') as datafile:
    rawlist = datafile.readlines()

    while cy < len(rawlist):
        if rawlist[cx] == 'Title\n':
            group += 1
        k = 'Group ' + str(group) + " " + rawlist[cx]
        v = rawlist[cy]
        datadict[k] = v
        cx += 2
        cy += 2

classlist = []
n = 1
while n < group + 1:
    newclass = Preset(datadict, n)
    classlist.append(newclass)
    n += 1


def load(unused):
    temp2 = ''
    eqdata = []
    compdata = []
    selection = loadvar.get()
    for item in classlist:
        if item.title == selection:
            # EQ PROCESSING
            temp = str(item.eq)[0:-1]
            for char in temp:
                if char != ' ':
                    temp2 += char
                    if len(temp) > 1:
                        temp = temp[1:]
                    else:
                        eqdata.append(temp2)
                        temp2 = ''
                elif char == ' ':
                    eqdata.append(temp2)
                    temp2 = ''
                    temp = temp[1:]
            # COMP PROCESSING
            temp = str(item.comp)[0:-1]
            temp2 = ''
            for char in temp:
                if char != ' ':
                    temp2 += char
                    if len(temp) > 1:
                        temp = temp[1:]
                    else:
                        compdata.append(temp2)
                        temp2 = ''
                elif char == ' ':
                    compdata.append(temp2)
                    temp2 = ''
                    temp = temp[1:]

            b1var.set(freqoptions1[freqoptions1.index(int(eqdata[0]))])
            b2var.set(freqoptions2[freqoptions2.index(int(eqdata[2]))])
            b3var.set(freqoptions3[freqoptions3.index(int(eqdata[4]))])
            b1gvar.set(gainoptions[gainoptions.index(eqdata[1])])
            b2gvar.set(gainoptions[gainoptions.index(eqdata[3])])
            b3gvar.set(gainoptions[gainoptions.index(eqdata[5])])

            thresholdvalue.set(compdata[0])
            ratiovalue.set(compdata[1])
            releasevalue.set(compdata[2])
            if compdata[3] == '1':
                prevar.set(True)
            else:
                prevar.set(False)
            if compdata[4] == '1':
                attackvar.set(True)
            else:
                attackvar.set(False)
            if compdata[5] == '1':
                kneevar.set(True)
            else:
                kneevar.set(False)
            if compdata[6] == '1':
                typevar.set(True)
            else:
                typevar.set(False)


def checktotext():
    checkboxes = ''
    if prevar.get() != '0':
        checkboxes += "1 "
    else:
        checkboxes += "0 "
    if attackvar.get() != '0':
        checkboxes += "1 "
    else:
        checkboxes += "0 "
    if kneevar.get() != '0':
        checkboxes += "1 "
    else:
        checkboxes += "0 "
    if typevar.get() != '0':
        checkboxes += "1"
    else:
        checkboxes += "0"
    return checkboxes


def createtextdata(title):
    checkboxes = checktotext()
    newtext = 'Title\n' + str(title.title) + '\n' + 'EQ\n' + str(b1var.get()) + ' ' + str(b1gvar.get()) + ' ' + str(
        b2var.get()) + ' ' + str(b2gvar.get()) + ' ' + str(b3var.get()) + ' ' + str(
        b3gvar.get()) + '\n' + 'Comp\n' + str(thresholdvalue.get())[0:-2] + ' ' + str(ratiovalue.get())[
                                                                                  0:-2] + ' ' + str(releasevalue.get())[
                                                                                                0:-4] + ' ' + checkboxes + '\n'
    return newtext


def createfinaltextdata(data):
    newtext = 'Title\n' + str(data.title) + '\n' + 'EQ\n' + data.eq + 'Comp\n' + data.comp + '\n'
    return newtext


newdictforsaving = {}


def writenewfile():
    savedata = ''
    for item in classlist:
        temp = createfinaltextdata(item)
        savedata += temp
    with open('data.api', 'r+') as file:
        file.write(savedata)


def createpreset(data):
    newpreset = NewPreset(data)
    classlist.append(newpreset)
    writenewfile(classlist)


def createdictfromcurrent(title):
    checkboxes = checktotext()
    newdictforsaving['Title'] = title
    newdictforsaving[
        'EQ'] = b1var.get() + ' ' + b1gvar.get() + ' ' + b2var.get() + ' ' + b2gvar.get() + ' ' + b3var.get() + ' ' + b3gvar.get() + '\n'
    newdictforsaving['Comp'] = thresholdvalue.get()[0:-2] + ' ' + ratiovalue.get()[0:-2] + ' ' + releasevalue.get()[
                                                                                                 0:-4] + ' ' + checkboxes + '\n'
    # newdictforsaving['Comp'] = str(thresholdvalue.get())[0:-2] + ' ' + str(ratiovalue.get())[0:-2] +' ' +  str(releasevalue.get())[0:-4] +' ' +  checkboxes + '\n'
    # this is not returning the .gets ^
    createpreset(newdictforsaving)


def save():
    neworupdate = tkMessageBox.askquestion('New or Update', 'Save as a new preset?')
    if neworupdate == "yes":
        newtitle = askstring('Name', 'What are these settings for?')  # returns plain string to variable
    else:
        newtitle = loadvar.get()
    for item in classlist:
        if item.title == newtitle:
            classlist.remove(item)
    createdictfromcurrent(newtitle)


menu = Frame(root, bg='black', height=100, borderwidth=5, relief='raised')
title = Label(menu, font=(None, 35), text="API 7600 SETTINGS", foreground='blue', background='black')
title.pack()
menu.pack(side=TOP, anchor='n', fill=X)

toolbar = Frame(menu, bg='black')
b = Button(toolbar, text="Save", width=6, command=save, fg='black')
b.pack(side=RIGHT, anchor='e', padx=20)
loadvar = StringVar(toolbar)
loadvar.set('Load')
savedsettings = []
for item in classlist:
    savedsettings.append(item.title)
# loaddd = apply(OptionMenu, (toolbar, loadvar) + tuple(savedsettings))
loaddd = OptionMenu(toolbar, loadvar, *savedsettings, command=load)
loaddd.pack(side=LEFT, anchor='w', padx=20)
toolbar.pack()

eqbox = Frame(width=2, height=2, bd=1, relief="sunken")
eqlabel = Label(eqbox, text="EQ Section")

eqlabel.pack(anchor='n')
b1box = Frame(eqbox)
b2box = Frame(eqbox)
b3box = Frame(eqbox)

freqoptions1 = [30, 40, 50, 100, 200, 300, 400]
freqoptions2 = [200, 400, 600, 800, 1500, 3000, 5000]
freqoptions3 = [2500, 5000, 7000, 10000, 12500, 15000, 20000]
gainoptions = ['-12', '-9', '-6', '-4', '-2', '0', '+2', '+4', '+6', '+9', '+12']

b1label = Label(b1box, text='Band 1', font=(None, 15))
b2label = Label(b2box, text='Band 2', font=(None, 15))
b3label = Label(b3box, text='Band 3', font=(None, 15))
b1flabel = Label(b1box, text='Frequency', font=(None, 12), pady=15)
b1var = StringVar(b1box)
b1var.set(freqoptions1[0])  # default value
b1dd = apply(OptionMenu, (b1box, b1var) + tuple(freqoptions1))

b2flabel = Label(b2box, text='Frequency', font=(None, 12), pady=15)
b2var = StringVar(b2box)
b2var.set(freqoptions2[0])  # default value
b2dd = apply(OptionMenu, (b2box, b2var) + tuple(freqoptions2))

b3flabel = Label(b3box, text='Frequency', font=(None, 12), pady=15)
b3var = StringVar(b3box)
b3var.set(freqoptions3[0])  # default value
b3dd = apply(OptionMenu, (b3box, b3var) + tuple(freqoptions3))

b1glabel = Label(b1box, text='Gain', font=(None, 12), pady=15)
b1gvar = StringVar(b1box)
b1gvar.set(gainoptions[5])  # default value
b1gaindd = apply(OptionMenu, (b1box, b1gvar) + tuple(gainoptions))
b2glabel = Label(b2box, text='Gain', font=(None, 12), pady=15)
b2gvar = StringVar(b2box)
b2gvar.set(gainoptions[5])  # default value
b2gaindd = apply(OptionMenu, (b2box, b2gvar) + tuple(gainoptions))
b3glabel = Label(b3box, text='Gain', font=(None, 12), pady=15)
b3gvar = StringVar(b3box)
b3gvar.set(gainoptions[5])  # default value
b3gaindd = apply(OptionMenu, (b3box, b3gvar) + tuple(gainoptions))
b1label.pack(pady=25)
b1flabel.pack()
b1dd.pack()
b1glabel.pack()
b1gaindd.pack()

b2label.pack(pady=25)
b2flabel.pack()
b2dd.pack()
b2glabel.pack()
b2gaindd.pack()

b3label.pack(pady=25)
b3flabel.pack()
b3dd.pack()
b3glabel.pack()
b3gaindd.pack()

b1box.pack(anchor='ne', side=LEFT, padx=30)
b2box.pack(anchor='n', side=LEFT, padx=30)
b3box.pack(anchor='nw', side=LEFT, padx=30)
eqbox.pack(side=LEFT, anchor='n', padx=80, pady=20, fill=BOTH)

compbox = Frame(width=2, height=2, bd=1, relief="sunken")

comptop = Frame(compbox)
threshbox = Frame(comptop, bd=1, relief="sunken")
ratiobox = Frame(comptop, bd=1, relief="sunken")
releasebox = Frame(comptop, bd=1, relief="sunken")
threshlabel = Label(threshbox, text="Threshold", font=(None, 15))
ratiolabel = Label(ratiobox, text="Ratio", font=(None, 15))
releaselabel = Label(releasebox, text="Release", font=(None, 15))
complabel = Label(comptop, text="Comp Section")
complabel.pack(anchor='n')
threshlabel.pack()
thresholdvalue = StringVar()
thresholdvalue.set('10db')

# THRESHKNOB STUFF
c = Canvas(threshbox, width=112, height=112)
c.pack(anchor='e')

xy = [(28, 28), (84, 28), (84, 84), (28, 84)]
c.create_oval(16, 16, 96, 96, width=1, fill='black')
polygon_item = c.create_polygon(xy, fill='')
center = 56, 56
line = c.create_line((84, 28), (56, 56), fill='white')


def getangle(event):
    dx = c.canvasx(event.x) - center[0]
    dy = c.canvasy(event.y) - center[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0  # cannot determine angle


def threshpress(event):
    global start
    start = getangle(event)


def threshmotion(event):
    global start
    angle = getangle(event) / start
    offset = complex(center[0], center[1])
    newxy = []

    for x, y in xy:
        v = angle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    if newxy[0] > 88:
        pass
    else:
        c.coords(polygon_item, *newxy)
        linenewxy = [newxy[2], newxy[0], 56, 56]
        c.coords(line, *linenewxy)

        if newxy[2] < 56:
            adjustedxy = (-1 * newxy[0])
        else:
            adjustedxy = newxy[0]
        actualthresh = round(30 * ((int(adjustedxy * 0.5 + 43.2)) * 0.0114942529), 1) - 10

        thresholdvalue.set(str(round(actualthresh, 2)) + 'db')


# noinspection PyUnusedLocal
def threshtakefocus(event):
    c.bind("<Button-1>", threshpress)
    c.bind("<B1-Motion>", threshmotion)


c.bind('<Motion>', threshtakefocus)

thresholdvalueentry = Entry(threshbox, textvariable=thresholdvalue)

thresholdvalueentry.pack()
ratiolabel.pack()

ratiovalue = StringVar()
ratiovalue.set('20:1')
# RATKNOB STUFF
ratc = Canvas(ratiobox, width=112, height=112)
ratc.pack()

xy = [(28, 28), (84, 28), (84, 84), (28, 84)]
ratc.create_oval(16, 16, 96, 96, width=1, fill='black')
ratpolygon_item = ratc.create_polygon(xy, fill='')
ratcenter = 56, 56
ratline = ratc.create_line((84, 28), (56, 56), fill='white')


def ratgetangle(event):
    dx = ratc.canvasx(event.x) - ratcenter[0]
    dy = ratc.canvasy(event.y) - ratcenter[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0  # cannot determine angle


def ratpress(event):
    global ratstart
    ratstart = ratgetangle(event)


def ratmotion(event):
    global ratstart
    angle = ratgetangle(event) / ratstart
    offset = complex(ratcenter[0], ratcenter[1])
    newxy = []

    for x, y in xy:
        v = angle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    if newxy[0] > 88:
        pass
    else:
        ratc.coords(ratpolygon_item, *newxy)
        linenewxy = [newxy[2], newxy[0], 56, 56]
        ratc.coords(ratline, *linenewxy)

        if newxy[2] < 56:
            adjustedxy = (-1 * newxy[0])
        else:
            adjustedxy = newxy[0]
        ratio = round(30 * ((int(adjustedxy * 0.5 + 43.2)) * 0.0114942529), 1)
        if ratio > 28:
            ratio = 'inf'
        if ratio <= 1:
            ratio = 1
        ratio = str(ratio) + ":1"
        ratiovalue.set(ratio)


# noinspection PyUnusedLocal
def rattakefocus(event):
    ratc.bind("<Button-1>", ratpress)
    ratc.bind("<B1-Motion>", ratmotion)


ratc.bind('<Motion>', rattakefocus)

ratioentry = Entry(ratiobox, textvariable=ratiovalue)
ratioentry.pack()
releaselabel.pack()
releasevalue = StringVar()
releasevalue.set('0.80 sec')

# RELKNOB STUFF
relc = Canvas(releasebox, width=112, height=112)
relc.pack()

xy = [(28, 28), (84, 28), (84, 84), (28, 84)]
relc.create_oval(16, 16, 96, 96, width=1, fill='black')
relpolygon_item = relc.create_polygon(xy, fill='')
relcenter = 56, 56
relline = relc.create_line((84, 28), (56, 56), fill='white')


def relgetangle(event):
    dx = relc.canvasx(event.x) - relcenter[0]
    dy = relc.canvasy(event.y) - relcenter[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0  # cannot determine angle


def relpress(event):
    global relstart
    relstart = relgetangle(event)


def relmotion(event):
    global relstart
    angle = relgetangle(event) / relstart
    offset = complex(relcenter[0], relcenter[1])
    newxy = []

    for x, y in xy:
        v = angle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)

    if newxy[0] > 88:
        pass
    else:
        relc.coords(relpolygon_item, *newxy)
        linenewxy = [newxy[2], newxy[0], 56, 56]
        relc.coords(relline, *linenewxy)

        if newxy[2] < 56:
            adjustedxy = (-1 * newxy[0])
        else:
            adjustedxy = newxy[0]
        data = round(100 * ((int(adjustedxy * 0.5 + 43.2)) * 0.0114942529), 1)
        # IT'S FUCKED UP IN THIS TRANSITION
        if data <= 15:
            release = data
        elif data <= 25:
            release = (2 * data) - 15
        elif data <= 75:
            # release = (data * 0.55) + 21.25
            release = sqrt(data + (50 * data)) * 1.3
        elif data <= 80:
            # release = (data * 0.55) + 21.25
            release = sqrt(data + (50 * data)) * 1.4
        elif data <= 90:
            # release = (data * 0.55) + 21.25
            release = sqrt(data + (50 * data)) * 1.6
        elif data <= 95:
            # release = (data * 0.55) + 21.25
            release = sqrt(data + (50 * data)) * 1.7
        else:
            release = sqrt(data + (50 * data)) * 1.8
        release = round(release, 2)
        releasefullsex = 0
        if release > 100:
            releasefullsex += 1
            release -= 100
        release = releasefullsex + (release * 0.01)
        releasevalue.set(str(round(release, 2)) + " sec")


# 0 to 15 is .01 to .15, ~X=Y
#  15 to 35 is .15 to .25, ~X=2Y
# 35 to 63 is .25 to .75, ~X=.57Y
# 63 to 85 is .75 to 1.5 ~X=.31Y

def reltakefocus(event):
    relc.bind("<Button-1>", relpress)
    relc.bind("<B1-Motion>", relmotion)


relc.bind('<Motion>', reltakefocus)

releaseentry = Entry(releasebox, textvariable=releasevalue)
releaseentry.pack()
threshbox.pack(anchor='ne', side=LEFT, padx=30)
ratiobox.pack(anchor='n', side=LEFT, padx=30)
releasebox.pack(anchor='nw', side=RIGHT, padx=30)

typevar = StringVar()
kneevar = StringVar()
attackvar = StringVar()
prevar = StringVar()
typevar.set(False)
kneevar.set(False)
attackvar.set(False)
prevar.set(False)
compbuttonsbox = Frame(compbox)

typebox = Frame(compbuttonsbox)
kneebox = Frame(compbuttonsbox)
attackbox = Frame(compbuttonsbox)
prebox = Frame(compbuttonsbox)

typecheck = Checkbutton(typebox, variable=typevar)
typelabel = Label(typebox, text='Type', font=(None, 15))
kneecheck = Checkbutton(kneebox, variable=kneevar)
kneelabel = Label(kneebox, text='Knee', font=(None, 15))
attackcheck = Checkbutton(attackbox, variable=attackvar)
attacklabel = Label(attackbox, text='Attack', font=(None, 15))
precheck = Checkbutton(prebox, variable=prevar)
prelabel = Label(prebox, text='Pre', font=(None, 15))

typecheck.pack()
typelabel.pack()
typebox.pack(side=RIGHT, padx=20)
kneecheck.pack()
kneelabel.pack()
kneebox.pack(side=RIGHT, padx=20)
attackcheck.pack()
attacklabel.pack()
attackbox.pack(side=RIGHT, padx=20)
precheck.pack()
prelabel.pack()
prebox.pack(side=RIGHT, padx=20)

compbuttonsbox.pack(side=BOTTOM, pady=30)
comptop.pack(side=TOP)
compbox.pack(side=RIGHT, anchor='n', padx=80, pady=20, fill=BOTH)

root.minsize(500, 500)
root.title('API Settings Manager')

mainloop()
