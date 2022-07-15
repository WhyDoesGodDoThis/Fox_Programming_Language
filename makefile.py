#use this to turn main.foxbin into a print(text) program
text = b"hello world!"
with open("main.foxbin", "wb") as f:
    bytes = bytearray([int(i) for i in bytearray(text)])
    f.write(bytearray(b"\x08\x53\xff\x02\x61\xff\x04\x61\xff\x03")+bytes+bytearray(b"\xe2\xff\x06\x70\x00\xff\x01\xff\xfe"))