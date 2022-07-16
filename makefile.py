#use this to turn main.foxbin into a print(text) program
text = 10.3
with open("main.foxbin", "wb") as f:
    if text is float:
        bytes = bytearray(bytes(text+b'\xe3'))
    elif text is int:
        bytes = bytearray(bytes(text)+b'\xe1')
    else:
        bytes = bytearray([int(i) for i in bytearray(text)]+[b'\xe2'])
    f.write(bytearray(b"\x08\x53\xff\x02\x61\xff\x04\x61\xff\x03")+bytes+bytearray(b"\xff\x06\x70\x00\xff\x01\xff\xfe"))