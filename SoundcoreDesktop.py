import tkinter
from tkinter import ttk
import os
import json
from tkinter.constants import END, X
from SoundcoreAPI import Soundcore
import bluetooth

def passFunc():
    pass

isConnected = False
Headphone = None
parsedata = None

def ANCState(ANC):
    if ANC == b"\x02\x00\x01":
        return "Normal"
    elif ANC == b"\x01\x00\x01":
        return "Transparency"
    elif ANC == b"\x00\x00\x01":
        return "ANC Trans"
    elif ANC == b"\x00\x02\x01":
        return "ANC Indoor"
    elif ANC == b"\x00\x01\x01":
        return "ANC Outdoor"
    else:
        return None

window = tkinter.Tk()
window.title("Anker Soundcore Desktop")
window.geometry("340x500")

checkMark = tkinter.Label(window, text="✓", font=("Arial", 13, "bold"))
def onHeadphoneEvent(data):
    deviceInfo = Headphone.parseInfo()
    #ANCValue = ANCState(deviceInfo['ANC'])
    print(deviceInfo)
    # checkMarkPos = {
    #     "ANC": (10+5, 90+5, "#714fb0"),
    #     "Trans": (119+5, 90+5, "#4f75b0"),
    #     "Normal": (227+5, 90+5, "#525a6b")
    # }
    # print(ANCValue)
    # if "ANC" in ANCValue:
    #     print("ANC mode")
    #     checkMark.configure(background=checkMarkPos["ANC"][2])
    # elif "Normal" == ANCValue:
    #     print("Normal mode")
    #     checkMark.configure(background=checkMarkPos["Normal"][2])
    # elif "Transparency" == ANCValue:
    #     print("Trans mode")
    #     checkMark.configure(background=checkMarkPos["Trans"][2])
    # window.update()

if not os.path.exists(os.path.join(os.getcwd(), "lastConnect.json")):
    listBT = bluetooth.discover_devices(lookup_names=True)
    print(listBT)
    for device in listBT:
        if "Soundcore" in device[1]:
            macaddress = device[0]
    Headphone = Soundcore(macaddress, onHeadphoneEvent)
    with open(os.path.join(os.getcwd(), "lastConnect.json"), "w") as lastConnect:
        lastConnect.write(json.dumps({"macAddress": macaddress}))
else:
    with open(os.path.join(os.getcwd(), "lastConnect.json"), "r") as lastConnect:
        lastConnect = json.loads(lastConnect.readlines()[0])
    Headphone = Soundcore(lastConnect["macAddress"], onHeadphoneEvent)

Headphone.connect()
parsedata = Headphone.parseInfo()
if parsedata:
    isConnected = True

EQChoices = ["SoundCore Signature", "Acoustic", "Bass Booster", "Bass Reducer", "Classical", "Podcast",
        "Dance", "Deep", "Electronic", "Flat", "Hip-Hop", "Jazz", "Latin", "Lounge", "Piano", "Pop", "R&B", "Rock",
        "Small Speaker(s)", "Spoken Word", "Treble Booster", "Treble Reducer"]

EQlabel = tkinter.Label(text="EQ")
EQlabel.configure(font=("Arial", 13, "bold"))
EQlabel.place(x=2, y=5)

menu = tkinter.StringVar()
if parsedata != None:
    menu.set(Headphone.findCurrentEQ())

def onChangeEQ(*arg):
    if Headphone and menu.get() != "Change EQ":
        Headphone.preEQ(menu.get())

menu.trace("w", onChangeEQ)

drop= tkinter.OptionMenu(window, menu, *EQChoices)
drop.place(x=34, y=3)

inputtxt = tkinter.Entry(window, width=16)
if Headphone != None:
    inputtxt.delete(0, END)
    inputtxt.insert(0, Headphone.macaddress)
inputtxt.place(x=190 , y=9)

def tryConnect():
    global Headphone
    Headphone = Soundcore(inputtxt.get())
    Headphone.connect()
    data = Headphone.parseInfo()
    if data:
        with open(os.path.join(os.getcwd(), "lastConnect.json"), "w") as lastConnect:
            lastConnect.write(json.dumps({"macAddress": inputtxt.get()}))

connectButton = tkinter.Button(window, width=6, height=0, text="connect", command=tryConnect)
connectButton.place(x=290 , y=4)

ttk.Separator(window, orient='horizontal').place(y=40, relwidth=1, relheight=1)


transImage = tkinter.PhotoImage(file="Images//Ambient Sound//a3029_img_trans.png")
transImage = transImage.subsample(3,3)
label = tkinter.Label(window, image=transImage)
label.place(x=0, y=210)

Modeinfo = tkinter.Label(window, text="Stay aware of your sourrounding by allowing\n ambient sound in.")
Modeinfo.configure(font=("Arial", 10))
Modeinfo.place(x=45, y=200)

def removeImg():
    global label
    label.destroy()

text = {
    "ANC Outdoor": "Reduce ambient sound on-the-go for quieter city spaces",
    "ANC Trans": "Targets low-end frequencies like engine and road noise for serene journeys and commutes.",
    "ANC INDOOR": "Eliminate voices and mid-frequency noise from coffee shops and other inside spaces."
}

def forgetANCWegets():
    global TransportButton, IndoorButton, OutdoorButton, ANCModetxt, window
    try:
        TransportButton.destroy()
        IndoorButton.destroy()
        OutdoorButton.destroy()
        ANCModetxt.destroy()
        window.update()
    except NameError:
        print("error")

def ANC():
    global Modeinfo, label, window
    global TransportButton, IndoorButton, OutdoorButton, ANCModetxt
    var = tkinter.IntVar()
    var.set(1)

    ANCModetxt = tkinter.Label(window, text="Modes")
    ANCModetxt.configure(font=("Arial", 12, "bold"))
    ANCModetxt.place(x=30, y=196)

    buttons = [
        ("Transport", 1, 30),
        ("Indoor", 2, 120),
        ("Outdoor", 3, 210)
    ]

    def getAction(data=None):
        global image
        data = data if data != None else var.get()
        if data == 1:
            Modeinfo.configure(text="Targets low-end frequencies like engine and road\n noise for serene journeys and commutes.")
            image = tkinter.PhotoImage(file="Images//ANC//a3951_img_transport.png")
            image = image.subsample(3,3)
            label.configure(image=image)
            Headphone.ANC("ANC Transport")
        elif data == 2:
            Modeinfo.configure(text="Eliminate voices and mid-frequency noise from\n coffee shops and other inside spaces.")
            image = tkinter.PhotoImage(file="Images//ANC//a3951_img_indoor.png")
            image = image.subsample(3,3)
            label.configure(image=image)
            Headphone.ANC("ANC Indoor")
        elif data == 3:
            Modeinfo.configure(text="Reduce ambient sound on-the-go for quieter city\n spaces")
            image = tkinter.PhotoImage(file="Images//ANC//a3951_img_outdoor.png")
            image = image.subsample(3,3)
            label.configure(image=image)
            Headphone.ANC("ANC Outdoor")
        Modeinfo.place(x=25, y=450)
    
    getAction()

    TransportButton = tkinter.Radiobutton(window, text=buttons[0][0], variable=var, command=getAction, value=buttons[0][1], indicatoron = 0, width=10, height=2)
    TransportButton.place(x=buttons[0][2], y=230)

    IndoorButton = tkinter.Radiobutton(window, text=buttons[1][0], variable=var, command=getAction, value=buttons[1][1], indicatoron = 0, width=10, height=2)
    IndoorButton.place(x=buttons[1][2], y=230)

    OutdoorButton = tkinter.Radiobutton(window, text=buttons[2][0], variable=var, command=getAction, value=buttons[2][1], indicatoron = 0, width=10, height=2)
    OutdoorButton.place(x=buttons[2][2], y=230)

def trans():
    global Modeinfo, label, window
    forgetANCWegets()
    Modeinfo.configure(text="Stay aware of your sourrounding by allowing\n ambient sound in.")
    Modeinfo.place(x=45, y=200)
    #Modeinfo.configure(x=45, y=200)
    image = tkinter.PhotoImage(file="Images//Ambient Sound//a3029_img_trans.png")
    image = image.subsample(3,3)
    label.configure(image=image)
    label.image = image
    Headphone.ANC("Transparency")
    text = "Reduce ambient sound on-the-go for quieter city spaces"

def normal():
    global Modeinfo, label, window
    forgetANCWegets()
    Modeinfo.configure(text="Turn off noise cancellation and transparency")
    Modeinfo.place(x=45, y=200)
    image = tkinter.PhotoImage(file="Images//Ambient Sound//a3029_img_normal.png")
    image = image.subsample(3,3)
    label.configure(image=image)
    label.image = image
    Headphone.ANC("Normal")

ANCImg = tkinter.PhotoImage(file = "Images//Modes//a3029_ambient_icon_anc.png")
ANCImg = ANCImg.subsample(2,2)
page1btn = tkinter.Button(window, text="Noise Cancellation", image=ANCImg, compound = "top", background = "#714fb0", command=ANC, height=96, width=96, fg = "white", relief="groove")
# page1btn.bind("<Button-1>", lambda _: "break", add=True)

TransparcyImg = tkinter.PhotoImage(file = "Images//Modes//a3029_ambient_icon_trans.png")
TransparcyImg = TransparcyImg.subsample(2,2)
page2btn = tkinter.Button(window, text="Transparency", image=TransparcyImg, compound = "top", background = "#4f75b0", command=trans, height=96, width=96, fg = "white", relief="groove")
# page2btn.bind("<Button-1>", lambda _: "break", add=True)

NormalImg = tkinter.PhotoImage(file = "Images//Modes//a3029_ambient_icon_off.png")
NormalImg = NormalImg.subsample(2,2)
page3btn = tkinter.Button(window, text="Normal", image=NormalImg, compound = "top", background = "#525a6b", command=normal, height=96, width=96, fg = "white", relief="groove")
# page3btn.bind("<Button-1>", lambda _: "break", add=True)


NavLabel = tkinter.Label(text="Ambient Sound")
NavLabel.configure(font=("Arial", 20, "bold"))
NavLabel.place(x=8, y=45)

page1btn.place(x=5, y=90)
page2btn.place(x=23+96, y=90)
page3btn.place(x=232, y=90)

window.resizable(0,0)

def on_closing():
    if Headphone != None:
        Headphone.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()