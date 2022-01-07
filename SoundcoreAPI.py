import socket
import threading
from bluetooth import lookup_name


class Soundcore():
    def __init__(self, macaddress: str, onEvent = None):
        self.macaddress = macaddress
        self.Port = self.getPort()
        self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.__thread = threading.Thread(target=self.__ParseReceiveData)
        self._running = True
        self.callback = onEvent 
        self.data = ""
        self.presetEQprofile = {
            "SoundCore Signature":    "08ee00000002811400000078787878787878784d",
            "Acoustic":               "08ee000000028114000100a0828c8ca0a0a08c34",
            "Bass Booster":           "08ee000000028114000200a0968278787878789f",
            "Bass Reducer":           "08ee000000028114000300505a6e787878787800",
            "Classical":              "08ee00000002811400040096966464788c96a0bf",
            "Podcast":                "08ee0000000281140005005a8ca0a0968c7864b6",
            "Dance":                  "08ee0000000281140006008c5a6e828c8c825a5d",
            "Deep":                   "08ee0000000281140007008c8296968c64504654",
            "Electronic":             "08ee000000028114000800968c648c828c9696e1",
            "Flat":                   "08ee00000002811400090064646e7878786464fc",
            "Hip-Hop":                "08ee000000028114000a008c966e6e8c6e8c96b1",
            "Jazz":                   "08ee000000028114000b008c8c6464788c96a0b2",
            "Latin":                  "08ee000000028114000c0078786464647896aa6d",
            "Lounge":                 "08ee000000028114000d006e8ca09678648c82b4",
            "Piano":                  "08ee000000028114000e007896968ca0aa96a04b",
            "Pop":                    "08ee000000028114000f006e829696826e645a66",
            "R&B":                    "08ee000000028114001000b48c64648c9696a0fd",
            "Rock":                   "08ee000000028114001100968c6e6e82969696e0",
            "Small Speaker(s)":       "08ee000000028114001200a0968278645a50502d",
            "Spoken Word":            "08ee0000000281140013005a64828c8c82785a4c",
            "Treble Booster":         "08ee0000000281140014006464646e828c8ca075",
            "Treble Reducer":         "08ee000000028114001500787878645a50503ca4"
        }

    def __recvData(self):
        if not (data := self.client.recv(1024)) == self.data:
            self.data = data
            if self.callback != None:
                threading.Thread(target = self.callback, args=(self.data,)).start()

    def __ParseReceiveData(self):
        try:
            if self._running:
                self.__recvData()
                self.__ParseReceiveData()
        except Exception as e:
            if 'timed out' or "[WinError 10054]" in list(str(e)):
                print(e)
                return
            else:
                pass
                #print(e)

    def getPort(self):
        """
        This function trys to look for Device ports range can be changed with `times` args

        Range port is Only 1-30
        https://people.csail.mit.edu/albert/bluez-intro/x148.html
        """
        print(self.macaddress)
        if "Soundcore" in str(lookup_name(self.macaddress)).split():
            for x in range(1,31):
                try:
                    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                    s.connect((self.macaddress, x))
                    s.close()
                    return x
                except OSError:
                    pass
        return None

    # def GetNearby_devices(self):
    #     #return bluetooth.discover_devices(lookup_names=True)
    #     return bluetooth.find_service(address=self.macaddress)
    
    def send(self, data):
        from time import sleep
        #print(data)
        self.client.send(bytearray.fromhex(data))
        sleep(0.1)


    def parseInfo(self):
        """
        This returns a dict with SN, battery status, Modes, etc...
        """
        def getData():
            self.send("08ee00000001010a0002")
            return {"EQ": self.data.hex()[22:42], "battery": self.data[9]*10, "ANC": self.data[44:47], "SN": self.data[53:68], "firmware": self.data[48:52]}
        return getData()

    def ANC(self, modes: str):
        '''
        "Transparency": Set your headphone to Transparency mode
        "Normal": Set your headphone to Normal mode
        "ANC Indoor": Set your headphone to ANC Indoor mode
        "ANC Outdoor": Set your headphone to ANC Outdoor mode
        "ANC Transport": Set your headphone to ANC Transport mode
        '''
        base = "08ee00000006810e000"
        if modes == "Transparency":
            self.send(base+"10101008e")
        elif modes == "Normal":
            self.send(base+"20101008f")
        elif modes == "ANC Indoor":
            self.send(base+"00201008e")
        elif modes == "ANC Outdoor":
            self.send(base+"00101008d")
        elif modes == "ANC Transport":
            self.send(base+"00001008c")

    def preEQ(self, premadeEQ: str):
        '''
        Custom EQ settings made by Soundcore
        Here is list of them all
        - SoundCore Signature
        - Acoustic
        - Bass Booster
        - Bass Reducer
        - Classical
        - Podcast
        - Dance
        - Deep
        - Electronic
        - Flat
        - Hip-Hop
        - Jazz
        - Latin
        - Lounge
        - Piano
        - Pop
        - R&B
        - Rock
        - Small Speaker(s)
        - Spoken Word
        - Treble Booster
        - Treble Reducer
        '''
        #print(premadeEQ in self.presetEQprofile.keys())
        if premadeEQ in list(self.presetEQprofile.keys()):
            self.send(self.presetEQprofile[premadeEQ])
        else:
            raise TypeError(premadeEQ+" is Invaild")

    def findCurrentEQ(self):
        currentEQ = self.parseInfo()["EQ"]
        for eqName, eqValue in self.presetEQprofile.items():
            if currentEQ in eqValue:
                return eqName
            

        return "Unkown"

    def EQGain(self, values: list):
        """
        Custom EQ
        values: list require 8 values (From Range 60-180)
        If you pass anything higher then 180 or lower then 60 it will count as 120 which is middle value of "0" in app

        This allows you to set/make your own custom EQ.
        It has range between 60-180 because you can go between +6 and +5 on the Mobile app

        If you would like to have range of -6 to +6 you can use this math Value*10+120
        """
        gainValues = bytearray.fromhex("08ee00000002811400fefe")
        if len(values) == 8:
            for value in values:
                if 180 >= value >= 60:
                    gainValues.append(value)
                else:
                    gainValues.append(120)
            def getCrc(packet):
                crc = 0
                for b in packet:
                    crc += b
                return (crc & 0xFF)
            gainValues.append(getCrc(gainValues))
            self.send(gainValues)
        

    def connect(self):
        """
        This sets up the connection.
        """
        if self.Port:
            self.client.connect((self.macaddress, self.Port))
            print(f"Connected to {self.macaddress} on port {self.Port}")
            self.__thread.start()
        else:
            raise ConnectionError(f"Cannot connect to {self.macaddress}")

    def close(self):
        """
        This stops the bluetooth connection with headphone, If you dont do this your Mobile app may not able to connect.
        """
        self._running = False
        self.client.close()
        self.__thread.join()
        print("Disconnected")