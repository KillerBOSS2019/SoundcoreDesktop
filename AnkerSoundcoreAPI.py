import socket
import sys

LifeQ30 = {
    "SoundCore Signature":    "08ee00000002811400000078787878787878784d",
    "Acoustic":               "08ee000000028114000100a0828c8ca0a0a08c34",
    "Base Booster":           "08ee000000028114000200a0968278787878789f",
    "Base Reducer":           "08ee000000028114000300505a6e787878787800",
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

if len(sys.argv) > 3:
    if sys.argv[1] == "-EQPresets" and sys.argv[2] in list(LifeQ30.keys()):
        print('running -EQPresets')
        SoundCoreConnection(LifeQ30[sys.argv[2]], sys.argv[3])
    elif sys.argv[1] == "-AmbientSound":
        print('running -AmbientSound')
        SoundCoreConnection(HeadPhoneControl(sys.argv[2]), sys.argv[3])
else:
    print(\
        """
Commands: -EQPresets, -AmbientSound
-EQPresets                -AmbientSound has
SoundCore Signature       Transparency
Acoustic                  Normal
Base Booster              ANC
Base Reducer              Transport
Classical                 Indoor
Podcast                   Outdoor
Dance
Deep
Electronic
Flat
Hip-Hop
Jazz
Latin
Lounge
Piano
Pop
R&B
Rock
Small Speaker(s)
Spoken Word
Treble Booster
Treble Reducer


Usage:
   AnkerSoundcoreAPI.py -EQPresets "SoundCore Signature" 00:00:00:00:00:00

   AnkerSoundcoreAPI.py -AmbientSound "Transparency" 00:00:00:00:00:00
        """
        )
