import os
import struct
import zlib

PAGE_W = 1024
PAGE_H = 1024

PAPER = (246, 239, 221)
RULE = (198, 188, 164)
RED = (163, 32, 26)
RED_LT = (200, 90, 60)

BASE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE, "assets")
TARGET = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(BASE, "out")),
    "entry.png",
)

PICTURES = [
    ("illo_cop31.png", 258, 174),
    ("illo_mexico.png", 24, 156),
    ("illo_peru.png", 24, 302),
    ("illo_estonia.png", 778, 156),
    ("illo_brazil.png", 778, 302),
    ("illo_airniugini.png", 24, 512),
    ("illo_eulevy.png", 270, 512),
    ("illo_italy.png", 516, 512),
    ("illo_modi.png", 762, 512),
    ("illo_brent.png", 24, 668),
    ("illo_cricket.png", 270, 668),
    ("illo_vance.png", 516, 668),
    ("illo_chips.png", 762, 668),
]

WORDS = [
    ("t_meta.png", 24, 11),
    ("t_ear_l.png", 24, 30),
    ("t_ear_r.png", 850, 30),
    ("t_masthead.png", 226, 54),
    ("t_tag.png", 213, 129),
    ("t_lead.png", 257, 158),
    ("t_side0.png", 23, 220),
    ("t_side1.png", 23, 366),
    ("t_side2.png", 777, 220),
    ("t_side3.png", 777, 366),
    ("t_band0_0.png", 23, 578),
    ("t_band0_1.png", 269, 578),
    ("t_band0_2.png", 515, 578),
    ("t_band0_3.png", 761, 578),
    ("t_band1_0.png", 23, 734),
    ("t_band1_1.png", 269, 734),
    ("t_band1_2.png", 515, 734),
    ("t_band1_3.png", 762, 734),
    ("t_numband.png", 24, 454),
    ("t_crypto.png", 24, 824),
    ("t_datecheck.png", 24, 914),
    ("t_alsotoday.png", 608, 914),
    ("t_foot.png", 24, 991),
]

H_RULES = [
    (24, 1000, 26, 1, RULE),
    (24, 1000, 148, 1, RED_LT),
    (24, 1000, 149, 2, RED),
    (24, 1000, 450, 1, RULE),
    (24, 1000, 507, 1, RULE),
    (24, 1000, 663, 1, RULE),
    (24, 1000, 818, 1, RULE),
    (24, 1000, 982, 2, RULE),
]

V_RULES = [
    (252, 156, 440, RULE),
    (772, 156, 440, RULE),
    (266, 512, 658, RULE),
    (512, 512, 658, RULE),
    (758, 512, 658, RULE),
    (266, 668, 814, RULE),
    (512, 668, 814, RULE),
    (758, 668, 814, RULE),
]


def _predict(left, up, up_left):
    score = left + up - up_left
    dl = abs(score - left)
    du = abs(score - up)
    dc = abs(score - up_left)
    if dl <= du and dl <= dc:
        return left
    if du <= dc:
        return up
    return up_left


def read_png(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG: " + path)
    pos = 8
    width = height = None
    bit_depth = colour = interlace = None
    payload = bytearray()
    while pos < len(data):
        size = struct.unpack_from(">I", data, pos)[0]
        tag = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + size]
        if tag == b"IHDR":
            width, height, bit_depth, colour, _a, _b, interlace = (
                struct.unpack(">IIBBBBB", chunk))
        elif tag == b"IDAT":
            payload += chunk
        elif tag == b"IEND":
            break
        pos += 12 + size
    if bit_depth != 8 or interlace != 0 or colour not in (0, 2, 6):
        raise ValueError("unsupported PNG: " + path)
    channels = {0: 1, 2: 3, 6: 4}[colour]
    stream = zlib.decompress(bytes(payload))
    step = width * channels
    if channels == 1:
        pixels = bytearray(width * height * 3)
    else:
        pixels = bytearray(width * height * channels)
    above = bytearray(step)
    cursor = 0
    for row in range(height):
        mode = stream[cursor]
        cursor += 1
        line = bytearray(stream[cursor:cursor + step])
        cursor += step
        if mode == 1:
            for i in range(channels, step):
                line[i] = (line[i] + line[i - channels]) & 255
        elif mode == 2:
            for i in range(step):
                line[i] = (line[i] + above[i]) & 255
        elif mode == 3:
            for i in range(step):
                west = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((west + above[i]) >> 1)) & 255
        elif mode == 4:
            for i in range(step):
                west = line[i - channels] if i >= channels else 0
                north = above[i]
                nw = above[i - channels] if i >= channels else 0
                line[i] = (line[i] + _predict(west, north, nw)) & 255
        elif mode != 0:
            raise ValueError("bad PNG filter %d in %s" % (mode, path))
        above = line
        if channels == 1:
            dest = row * width * 3
            for x in range(width):
                pixels[dest + x * 3] = line[x]
                pixels[dest + x * 3 + 1] = line[x]
                pixels[dest + x * 3 + 2] = line[x]
        else:
            dest = row * step
            pixels[dest:dest + step] = line
    return width, height, bytes(pixels), channels == 4


def _block(tag, body):
    return (
        struct.pack(">I", len(body))
        + tag
        + body
        + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF)
    )


def _scanlines(rgb, w, h, mode):
    step = w * 3
    out = bytearray()
    prior = bytes(step)
    for y in range(h):
        current = rgb[y * step:(y + 1) * step]
        out.append(mode)
        if mode == 0:
            out += current
        else:
            out += bytes((a - b) & 255 for a, b in zip(current, prior))
        prior = current
    return bytes(out)


def write_png(path, w, h, rgb):
    header = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    plain = zlib.compress(_scanlines(rgb, w, h, 0), 9)
    upped = zlib.compress(_scanlines(rgb, w, h, 2), 9)
    body = plain if len(plain) <= len(upped) else upped
    blob = (
        b"\x89PNG\r\n\x1a\n"
        + _block(b"IHDR", header)
        + _block(b"IDAT", body)
        + _block(b"IEND", b"")
    )
    with open(path, "wb") as handle:
        handle.write(blob)


def stamp(canvas, img, iw, ih, ox, oy, has_alpha):
    if not has_alpha:
        for y in range(ih):
            dst = ((oy + y) * PAGE_W + ox) * 3
            src = y * iw * 3
            canvas[dst:dst + iw * 3] = img[src:src + iw * 3]
        return
    for y in range(ih):
        prow = (oy + y) * PAGE_W * 3
        irow = y * iw * 4
        for x in range(iw):
            s = irow + x * 4
            a = img[s + 3]
            if a == 0:
                continue
            d = prow + (ox + x) * 3
            if a == 255:
                canvas[d:d + 3] = img[s:s + 3]
            else:
                rest = 255 - a
                for k in range(3):
                    canvas[d + k] = (
                        img[s + k] * a + canvas[d + k] * rest + 127
                    ) // 255


def fill(canvas, x0, y0, x1, y1, rgb):
    r, g, b = rgb
    for y in range(y0, y1 + 1):
        base = y * PAGE_W * 3
        for x in range(x0, x1 + 1):
            o = base + x * 3
            canvas[o] = r
            canvas[o + 1] = g
            canvas[o + 2] = b


def place(canvas, name, x, y):
    iw, ih, pix, alpha = read_png(os.path.join(ASSET_DIR, name))
    stamp(canvas, pix, iw, ih, x, y, alpha)


def render():
    canvas = bytearray(bytes(PAPER) * (PAGE_W * PAGE_H))
    gw, gh, grain, gal = read_png(os.path.join(ASSET_DIR, "grain_256.png"))
    for ty in range(0, PAGE_H, gh):
        for tx in range(0, PAGE_W, gw):
            stamp(canvas, grain, gw, gh, tx, ty, gal)
    for name, x, y in PICTURES:
        place(canvas, name, x, y)
    for x0, x1, y, th, col in H_RULES:
        top = y - (th - 1) // 2
        fill(canvas, x0, top, x1, top + th - 1, col)
    for x, y0, y1, col in V_RULES:
        fill(canvas, x, y0, x, y1, col)
    for name, x, y in WORDS:
        place(canvas, name, x, y)
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    write_png(TARGET, PAGE_W, PAGE_H, bytes(canvas))
    print("wrote", TARGET)


if __name__ == "__main__":
    render()
