from Crypto.Util.number import long_to_bytes
f = open("body.enc.ppm", "rb")
h1 = f.readline()
h2 = f.readline()
h3 = f.readline()

xs = []
while True:
    data = int.from_bytes(f.read(16), "big")
    if data == 0:
        break
    xs.append(data)
ys = []
for i in range(1, len(xs)):
    y = xs[i] - xs[i - 1]
    if y < 0:
        y += int(pow(256, 16))
    y = long_to_bytes(y)
    # while len(y) % 16 != 0:
    #     y = b"\0" + y
    ys.append(y)
with open("flag.ppm", "wb") as f2:
    f2.write(h1)
    f2.write(h2)
    f2.write(h3)
    f2.write(b"".join(ys))
