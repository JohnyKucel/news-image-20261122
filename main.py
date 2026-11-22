import os
import struct
import zlib

W = 1024
H = 1024

BG = (246, 239, 221)
DIVIDER = (198, 188, 164)
ACCENT = (163, 32, 26)
ACCENT_SOFT = (200, 90, 60)

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(ROOT, "out")),
    "entry.png",
)

TEXT = [
    {"file": "t_meta.png", "x": 24, "y": 11},
    {"file": "t_ear_l.png", "x": 24, "y": 30},
    {"file": "t_ear_r.png", "x": 850, "y": 30},
    {"file": "t_masthead.png", "x": 226, "y": 54},
    {"file": "t_tag.png", "x": 213, "y": 129},
    {"file": "t_lead.png", "x": 257, "y": 158},
    {"file": "t_side0.png", "x": 23, "y": 220},
    {"file": "t_side1.png", "x": 23, "y": 366},
    {"file": "t_side2.png", "x": 777, "y": 220},
    {"file": "t_side3.png", "x": 777, "y": 366},
    {"file": "t_band0_0.png", "x": 23, "y": 578},
    {"file": "t_band0_1.png", "x": 269, "y": 578},
    {"file": "t_band0_2.png", "x": 515, "y": 578},
    {"file": "t_band0_3.png", "x": 761, "y": 578},
    {"file": "t_band1_0.png", "x": 23, "y": 734},
    {"file": "t_band1_1.png", "x": 269, "y": 734},
    {"file": "t_band1_2.png", "x": 515, "y": 734},
    {"file": "t_band1_3.png", "x": 762, "y": 734},
    {"file": "t_numband.png", "x": 24, "y": 454},
    {"file": "t_crypto.png", "x": 24, "y": 824},
    {"file": "t_datecheck.png", "x": 24, "y": 914},
    {"file": "t_alsotoday.png", "x": 608, "y": 914},
    {"file": "t_foot.png", "x": 24, "y": 991},
]

ART = [
    {"file": "illo_cop31.png", "x": 258, "y": 174},
    {"file": "illo_mexico.png", "x": 24, "y": 156},
    {"file": "illo_peru.png", "x": 24, "y": 302},
    {"file": "illo_estonia.png", "x": 778, "y": 156},
    {"file": "illo_brazil.png", "x": 778, "y": 302},
    {"file": "illo_airniugini.png", "x": 24, "y": 512},
    {"file": "illo_eulevy.png", "x": 270, "y": 512},
    {"file": "illo_italy.png", "x": 516, "y": 512},
    {"file": "illo_modi.png", "x": 762, "y": 512},
    {"file": "illo_brent.png", "x": 24, "y": 668},
    {"file": "illo_cricket.png", "x": 270, "y": 668},
    {"file": "illo_vance.png", "x": 516, "y": 668},
    {"file": "illo_chips.png", "x": 762, "y": 668},
]

BARS_H = [
    {"x0": 24, "x1": 1000, "y": 26, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 148, "t": 1, "c": ACCENT_SOFT},
    {"x0": 24, "x1": 1000, "y": 149, "t": 2, "c": ACCENT},
    {"x0": 24, "x1": 1000, "y": 450, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 507, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 663, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 818, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 982, "t": 2, "c": DIVIDER},
]

BARS_V = [
    {"x": 252, "y0": 156, "y1": 440, "c": DIVIDER},
    {"x": 772, "y0": 156, "y1": 440, "c": DIVIDER},
    {"x": 266, "y0": 512, "y1": 658, "c": DIVIDER},
    {"x": 512, "y0": 512, "y1": 658, "c": DIVIDER},
    {"x": 758, "y0": 512, "y1": 658, "c": DIVIDER},
    {"x": 266, "y0": 668, "y1": 814, "c": DIVIDER},
    {"x": 512, "y0": 668, "y1": 814, "c": DIVIDER},
    {"x": 758, "y0": 668, "y1": 814, "c": DIVIDER},
]


def _paeth(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _unfilter(kind, raw, prev, nch):
    row = bytearray(raw)
    if kind == 0:
        return row
    if kind == 1:
        for i in range(nch, len(row)):
            row[i] = (row[i] + row[i - nch]) & 255
        return row
    if kind == 2:
        for i in range(len(row)):
            row[i] = (row[i] + prev[i]) & 255
        return row
    if kind == 3:
        for i in range(len(row)):
            left = row[i - nch] if i >= nch else 0
            row[i] = (row[i] + ((left + prev[i]) >> 1)) & 255
        return row
    if kind == 4:
        for i in range(len(row)):
            left = row[i - nch] if i >= nch else 0
            up = prev[i]
            upleft = prev[i - nch] if i >= nch else 0
            row[i] = (row[i] + _paeth(left, up, upleft)) & 255
        return row
    raise ValueError("unknown filter %d" % kind)


def load_image(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad signature: " + path)
    off = 8
    w = h = None
    depth = kind = lace = None
    raw = bytearray()
    while off < len(data):
        size = struct.unpack_from(">I", data, off)[0]
        tag = data[off + 4:off + 8]
        body = data[off + 8:off + 8 + size]
        if tag == b"IHDR":
            w, h, depth, kind, _c, _m, lace = struct.unpack(">IIBBBBB", body)
        elif tag == b"IDAT":
            raw += body
        elif tag == b"IEND":
            break
        off += 12 + size
    if depth != 8 or lace != 0 or kind not in (0, 2, 6):
        raise ValueError("unsupported image: " + path)
    nch = {0: 1, 2: 3, 6: 4}[kind]
    stream = zlib.decompress(bytes(raw))
    step = w * nch
    if nch == 1:
        out = bytearray(w * h * 3)
    else:
        out = bytearray(w * h * nch)
    prev = bytearray(step)
    pos = 0
    for row in range(h):
        ftype = stream[pos]
        pos += 1
        line = _unfilter(ftype, stream[pos:pos + step], prev, nch)
        pos += step
        prev = line
        if nch == 1:
            base = row * w * 3
            for x in range(w):
                v = line[x]
                out[base + x * 3] = v
                out[base + x * 3 + 1] = v
                out[base + x * 3 + 2] = v
        else:
            base = row * step
            out[base:base + step] = line
    return w, h, bytes(out), kind == 6


def _chunk(kind, payload):
    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    )


def _rows(rgb, w, h, use_up):
    step = w * 3
    buf = bytearray()
    prev = bytes(step)
    for y in range(h):
        cur = rgb[y * step:(y + 1) * step]
        buf.append(2 if use_up else 0)
        if use_up:
            buf += bytes((a - b) & 255 for a, b in zip(cur, prev))
        else:
            buf += cur
        prev = cur
    return bytes(buf)


def save_png(path, w, h, rgb):
    head = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    plain = zlib.compress(_rows(rgb, w, h, False), 9)
    upped = zlib.compress(_rows(rgb, w, h, True), 9)
    pick = plain if len(plain) <= len(upped) else upped
    blob = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", head)
        + _chunk(b"IDAT", pick)
        + _chunk(b"IEND", b"")
    )
    with open(path, "wb") as fh:
        fh.write(blob)


def _paste(sheet, pic, pw, ph, ox, oy, alpha):
    if not alpha:
        for y in range(ph):
            d0 = ((oy + y) * W + ox) * 3
            s0 = y * pw * 3
            sheet[d0:d0 + pw * 3] = pic[s0:s0 + pw * 3]
        return
    for y in range(ph):
        drow = (oy + y) * W * 3
        srow = y * pw * 4
        for x in range(pw):
            s = srow + x * 4
            a = pic[s + 3]
            if a == 0:
                continue
            d = drow + (ox + x) * 3
            if a == 255:
                sheet[d:d + 3] = pic[s:s + 3]
            else:
                inv = 255 - a
                for k in range(3):
                    sheet[d + k] = (pic[s + k] * a + sheet[d + k] * inv + 127) // 255


def _rect(sheet, x0, y0, x1, y1, rgb):
    r, g, b = rgb
    seg = bytes((r, g, b)) * (x1 - x0 + 1)
    for y in range(y0, y1 + 1):
        base = y * W * 3 + x0 * 3
        sheet[base:base + len(seg)] = seg


def _draw(sheet, name, x, y):
    w, h, pix, alpha = load_image(os.path.join(ASSETS, name))
    _paste(sheet, pix, w, h, x, y, alpha)


def build():
    sheet = bytearray(bytes(BG) * (W * H))
    gw, gh, grain, galpha = load_image(os.path.join(ASSETS, "grain_256.png"))
    for ty in range(0, H, gh):
        for tx in range(0, W, gw):
            _paste(sheet, grain, gw, gh, tx, ty, galpha)
    for item in ART:
        _draw(sheet, item["file"], item["x"], item["y"])
    for bar in BARS_H:
        top = bar["y"] - (bar["t"] - 1) // 2
        _rect(sheet, bar["x0"], top, bar["x1"], top + bar["t"] - 1, bar["c"])
    for bar in BARS_V:
        _rect(sheet, bar["x"], bar["y0"], bar["x"], bar["y1"], bar["c"])
    for item in TEXT:
        _draw(sheet, item["file"], item["x"], item["y"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    save_png(OUT, W, H, bytes(sheet))
    print("wrote", OUT)


if __name__ == "__main__":
    build()
