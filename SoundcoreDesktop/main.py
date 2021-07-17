__Copyright__ = """
    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) 2021 DamienS

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter
import socket

# Code Class `A3951DeviceManager`

window = tkinter.Tk()
window.geometry("340x500")

deviceAddress = ""

#Headphone
def SoundCoreConnection(action, address):
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    def searchPort(Macaddress):
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        for x in range(1000):
            try:
                s.connect((Macaddress, x))
                s.close()
                return x
            except OSError:
                pass
        return None

    port = searchPort(address)
    print((address, port))
    
    try:
        s.connect((address, 12))
        data = bytearray.fromhex(action)
        s.send(data)
        data = s.recv(4000)
        print(data.hex())
        s.close()
    except OSError as e:
        if "host" in str(e).split():
            print("Please fully close Soundcore app on your mobile device, and try again.")
        else:
            print(e)

def HeadPhoneControl(action):
    base = "08ee00000006810e000"
    if action == "Transparency":
        return base+"10101008e"
    elif action == "Normal":
        return base+"20101008f"
    elif action == "ANC":
        return base+"00101008d"
    elif action == "ANCTransport":
        return base+"00001008c"
    elif action == "ANCIndoor":
        return base+"00201008e"
    elif action == "ANCOutdoor":
        return base+"00101008d"
    else:
        print("Invaild choice")

def forgetANCWegets():
    global TransportButton, IndoorButton, OutdoorButton, ANCModetxt
    try:
        TransportButton.destroy()
        IndoorButton.destroy()
        OutdoorButton.destroy()
        ANCModetxt.destroy()
    except NameError:
        pass

def Normal():
    global image,Modeinfo
    forgetANCWegets()
    image = tkinter.PhotoImage(file="Images//Ambient Sound//a3029_img_normal.png")
    image = image.subsample(3,3)
    label.configure(image=image)
    Modeinfo.configure(text="Turn off noise cancellation and transparency")
    window.update()
    SoundCoreConnection(HeadPhoneControl("Normal"),deviceAddress)

def Transparency():
    global image,Modeinfo
    forgetANCWegets()
    image = tkinter.PhotoImage(file="Images//Ambient Sound//a3029_img_trans.png")
    image = image.subsample(3,3)
    label.configure(image=image)
    Modeinfo.configure(text="Stay aware of your sourrounding by allowing\n ambient sound in.")
    window.update()
    SoundCoreConnection(HeadPhoneControl("Transparency"),deviceAddress)

def ANC():
    global image, Modeinfo
    global TransportButton, IndoorButton, OutdoorButton, ANCModetxt
    var = tkinter.IntVar()
    var.set(1)
    def getAction(data=None):
        global image
        data = data if data != None else var.get()
        if data == 1:
            image = tkinter.PhotoImage(file="Images//ANC//a3951_img_transport.png")
            image = image.subsample(3,3)
            label.configure(image=image)
            SoundCoreConnection(HeadPhoneControl("ANCTransport"),deviceAddress)
        elif data == 2:
            image = tkinter.PhotoImage(file="Images//ANC//a3951_img_indoor.png")
            image = image.subsample(3,3)
            label.configure(image=image)
            SoundCoreConnection(HeadPhoneControl("ANCIndoor"),deviceAddress)
        elif data == 3:
            image = tkinter.PhotoImage(file="Images//ANC//a3951_img_outdoor.png")
            image = image.subsample(3,3)
            label.configure(image=image)
            SoundCoreConnection(HeadPhoneControl("ANCOutdoor"),deviceAddress)
    getAction(var.get())
    buttons = [
        ("Transport", 1, 30),
        ("Indoor", 2, 120),
        ("Outdoor", 3, 210)
        ]
    Modeinfo.configure(text="")
    ANCModetxt = tkinter.Label(window, text="Modes")
    ANCModetxt.configure(font=("Arial", 12, "bold"))
    ANCModetxt.place(x=30, y=166)

    TransportButton = tkinter.Radiobutton(window, text=buttons[0][0], variable=var, command=getAction, value=buttons[0][1], indicatoron = 0, width=10, height=2)
    TransportButton.place(x=buttons[0][2], y=200)

    IndoorButton = tkinter.Radiobutton(window, text=buttons[1][0], variable=var, command=getAction, value=buttons[1][1], indicatoron = 0, width=10, height=2)
    IndoorButton.place(x=buttons[1][2], y=200)

    OutdoorButton = tkinter.Radiobutton(window, text=buttons[2][0], variable=var, command=getAction, value=buttons[2][1], indicatoron = 0, width=10, height=2)
    OutdoorButton.place(x=buttons[2][2], y=200)
    #TransportButton = tkinter.Button(window, text="Transport", width=10, height=2, bg="white")
    #TransportButton.place(x=30, y=200)

    #IndoorButton = tkinter.Button(window, text="Indoor", width=10, height=2, bg="white")
    #IndoorButton.place(x=120, y=200)

    #OutdoorButton = tkinter.Button(window, text="Outdoor", width=10, height=2, bg="white")
    #OutdoorButton.place(x=210, y=200)
    print(deviceAddress)

def settings():
    global deviceAddress
    def submit():
        with open("settings.txt", "w") as setting:
            setting.write(Macaddress.get())
            deviceAddress = Macaddress.get()
        settingWindow.destroy()
    settingWindow = tkinter.Toplevel(window)
    settingWindow.geometry("200x75")
    Macaddress = tkinter.Entry(settingWindow)
    Macaddress.pack()
    submitButton = tkinter.Button(settingWindow, command=submit, text="Submit")
    submitButton.pack()

with open("settings.txt", "rb") as setting:
    deviceAddress = setting.read().decode("utf-8")

transImage = tkinter.PhotoImage(file="Images//Ambient Sound//a3029_img_trans.png")
transImage = transImage.subsample(3,3)
label = tkinter.Label(window, image=transImage)
label.place(x=0, y=180)

Modeinfo = tkinter.Label(window, text="Stay aware of your sourrounding by allowing\n ambient sound in.")
Modeinfo.configure(font=("Arial", 10))
Modeinfo.place(x=45, y=180)

ANCImg = tkinter.PhotoImage(file = "Images//Modes//a3029_ambient_icon_anc.png")
ANCImg = ANCImg.subsample(2,2)
page1btn = tkinter.Button(window, text="Noise Cancellation", image=ANCImg, compound = "top", background = "#714fb0", command=ANC, height=96, width=96, fg = "white", relief="groove")

TransparcyImg = tkinter.PhotoImage(file = "Images//Modes//a3029_ambient_icon_trans.png")
TransparcyImg = TransparcyImg.subsample(2,2)
page2btn = tkinter.Button(window, text="Transparency", image=TransparcyImg, compound = "top", background = "#4f75b0", command=Transparency, height=96, width=96, fg = "white", relief="groove")

NormalImg = tkinter.PhotoImage(file = "Images//Modes//a3029_ambient_icon_off.png")
NormalImg = NormalImg.subsample(2,2)
page3btn = tkinter.Button(window, text="Normal", image=NormalImg, compound = "top", background = "#525a6b", command=Normal, height=96, width=96, fg = "white", relief="groove")

settingsImage = tkinter.PhotoImage(file = "Images//Nav//a3909_eq_custom_setting.png")
settingsImage = settingsImage.subsample(3,3)
settingsButton = tkinter.Button(window, image=settingsImage, border=0, command=settings)
settingsButton.place(x=300, y=8)

NavLabel = tkinter.Label(text="Ambient Sound")
NavLabel.configure(font=("Arial", 20, "bold"))
NavLabel.place(x=8, y=10)

page1btn.place(x=10, y=50)
page2btn.place(x=23+96, y=50)
page3btn.place(x=35+(96*2), y=50)

#page2btn.pack()

window.mainloop()
