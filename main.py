"""The World in One Day -- Sunday 22 November 2026 (v4).

Entry for make.fun news-image-20261122. A 34-story front page, drawn
in code: COP31 lead, four side stories, a numbered world map, a
CRYPTO NEWS strip, and a 24-cell numbered story grid. The artwork and
text were pre-rendered by the build script (Pillow, outside this
repository) into assets/*.png. This program is standard library only:
it tiles the paper grain, pastes the pre-rendered pieces at fixed
positions, draws the rules, and writes the poster, byte for byte, so
every run writes the same file.
"""

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
    {"file": "t_tag.png", "x": 213, "y": 127},
    {"file": "t_lead.png", "x": 257, "y": 150},
    {"file": "t_side0.png", "x": 23, "y": 212},
    {"file": "t_side1.png", "x": 23, "y": 350},
    {"file": "t_side2.png", "x": 777, "y": 212},
    {"file": "t_side3.png", "x": 777, "y": 350},
    {"file": "t_numband.png", "x": 24, "y": 436},
    {"file": "t_map.png", "x": 24, "y": 490},
    {"file": "t_crypto.png", "x": 24, "y": 552},
    {"file": "t_grid00.png", "x": 27, "y": 636},
    {"file": "t_grid01.png", "x": 191, "y": 636},
    {"file": "t_grid02.png", "x": 355, "y": 636},
    {"file": "t_grid03.png", "x": 519, "y": 636},
    {"file": "t_grid04.png", "x": 683, "y": 636},
    {"file": "t_grid05.png", "x": 847, "y": 636},
    {"file": "t_grid06.png", "x": 27, "y": 707},
    {"file": "t_grid07.png", "x": 191, "y": 707},
    {"file": "t_grid08.png", "x": 355, "y": 707},
    {"file": "t_grid09.png", "x": 519, "y": 707},
    {"file": "t_grid10.png", "x": 683, "y": 707},
    {"file": "t_grid11.png", "x": 847, "y": 707},
    {"file": "t_grid12.png", "x": 27, "y": 778},
    {"file": "t_grid13.png", "x": 191, "y": 778},
    {"file": "t_grid14.png", "x": 355, "y": 778},
    {"file": "t_grid15.png", "x": 519, "y": 778},
    {"file": "t_grid16.png", "x": 683, "y": 778},
    {"file": "t_grid17.png", "x": 847, "y": 778},
    {"file": "t_grid18.png", "x": 27, "y": 849},
    {"file": "t_grid19.png", "x": 191, "y": 849},
    {"file": "t_grid20.png", "x": 355, "y": 849},
    {"file": "t_grid21.png", "x": 519, "y": 849},
    {"file": "t_grid22.png", "x": 683, "y": 849},
    {"file": "t_grid23.png", "x": 847, "y": 849},
    {"file": "t_datecheck.png", "x": 24, "y": 928},
    {"file": "t_alsotoday.png", "x": 608, "y": 928},
    {"file": "t_foot.png", "x": 24, "y": 997},
]

ART = [
    {"file": "illo_cop31.png", "x": 258, "y": 168},
    {"file": "illo_mexico.png", "x": 24, "y": 150},
    {"file": "illo_peru.png", "x": 24, "y": 296},
    {"file": "illo_estonia.png", "x": 778, "y": 150},
    {"file": "illo_brazil.png", "x": 778, "y": 296},
    {"file": "illo_airniugini_s.png", "x": 27, "y": 636},
    {"file": "illo_eulevy_s.png", "x": 191, "y": 636},
    {"file": "illo_italy_s.png", "x": 355, "y": 636},
    {"file": "illo_modi_s.png", "x": 519, "y": 636},
    {"file": "illo_brent_s.png", "x": 683, "y": 636},
    {"file": "illo_cricket_s.png", "x": 847, "y": 636},
    {"file": "illo_vance_s.png", "x": 27, "y": 707},
    {"file": "illo_chips_s.png", "x": 191, "y": 707},
    {"file": "illo_aviation.png", "x": 355, "y": 707},
    {"file": "illo_russia.png", "x": 519, "y": 707},
    {"file": "illo_icj.png", "x": 683, "y": 707},
    {"file": "illo_shenzhen.png", "x": 847, "y": 707},
    {"file": "illo_akvan.png", "x": 27, "y": 778},
    {"file": "illo_wallst.png", "x": 191, "y": 778},
    {"file": "illo_iran.png", "x": 355, "y": 778},
    {"file": "illo_gta.png", "x": 519, "y": 778},
    {"file": "illo_denmark.png", "x": 683, "y": 778},
    {"file": "illo_footeng.png", "x": 847, "y": 778},
    {"file": "illo_footeur.png", "x": 27, "y": 849},
    {"file": "illo_nba.png", "x": 191, "y": 849},
    {"file": "illo_ronaldo.png", "x": 355, "y": 849},
    {"file": "illo_psm.png", "x": 519, "y": 849},
    {"file": "illo_soletf.png", "x": 683, "y": 849},
    {"file": "illo_roadmap.png", "x": 847, "y": 849},
]

BARS_H = [
    {"x0": 24, "x1": 1000, "y": 26, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 140, "t": 1, "c": ACCENT_SOFT},
    {"x0": 24, "x1": 1000, "y": 141, "t": 2, "c": ACCENT},
    {"x0": 24, "x1": 1000, "y": 430, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 486, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 548, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 632, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 924, "t": 1, "c": DIVIDER},
    {"x0": 24, "x1": 1000, "y": 988, "t": 2, "c": DIVIDER},
]

BARS_V = [
    {"x": 252, "y0": 150, "y1": 424, "c": DIVIDER},
    {"x": 772, "y0": 150, "y1": 424, "c": DIVIDER},
    {"x": 184, "y0": 636, "y1": 920, "c": DIVIDER},
    {"x": 348, "y0": 636, "y1": 920, "c": DIVIDER},
    {"x": 512, "y0": 636, "y1": 920, "c": DIVIDER},
    {"x": 676, "y0": 636, "y1": 920, "c": DIVIDER},
    {"x": 840, "y0": 636, "y1": 920, "c": DIVIDER},
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


def _tile_grain(sheet):
    gw, gh, grain, galpha = load_image(os.path.join(ASSETS, "grain_256.png"))
    for ty in range(0, H, gh):
        for tx in range(0, W, gw):
            _paste(sheet, grain, gw, gh, tx, ty, galpha)


def build():
    sheet = bytearray(bytes(BG) * (W * H))
    _tile_grain(sheet)
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
