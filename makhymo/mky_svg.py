"""
Libreria caroselli Makhymo (Makhymo S.r.l., Asti) in SVG per Illustrator.

Stile ricavato dai caroselli pubblicati:
  - fondo navy #122549 a carta stropicciata (assets/bg_navy.jpg)
  - testo bianco Lexend Deca, parole chiave in box rosso #C6183D
  - frecce bianche disegnate a mano, foto con angoli arrotondati
  - copertina e CTA con carta kraft strappata

Regole di costruzione:
  - ogni paragrafo e' UN solo <text>, una <tspan x y> per riga (righe spezzate a mano)
  - i box rossi di evidenziazione sono <rect> separati, sotto il testo
  - ogni slide e' un gruppo <g id="slide-NN"> con sottogruppi nominati
  - illustrazioni e icone sono tracciati vettoriali; le scritte a mano
    delle illustrazioni sono gia' convertite in tracciati (nessun font da installare)

Consegna: Makhymo_<Nome>_ALL_SLIDES.svg (tutte le tavole affiancate) + PNG di controllo.
"""

import base64
import math
import os
import re
from xml.sax.saxutils import escape

from PIL import ImageFont

# --------------------------------------------------------------------------
# Costanti
# --------------------------------------------------------------------------

W, H = 1080, 1350
M = 90                       # margine laterale
CW = W - 2 * M               # 900: larghezza utile
CONTENT_BOTTOM = 1190        # nessun contenuto sotto questa quota (tranne fonte e contatti)

NAVY = "#122549"
RED = "#C6183D"
RED_DARK = "#9A1030"
WHITE = "#FFFFFF"
CARD_DARK = "#0A1428"
CARD_LIGHT = "#1E2E4E"
MICRO = "#8A93A6"
SOFT = "#D5DCE8"
STEEL = "#AEB6C4"
KRAFT_INK = "#122549"

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONT_DIR = os.path.join(ASSETS, "fonts")

# ruolo -> (nome PostScript per Illustrator, famiglia per il render, file)
FONTS = {
    "reg": ("LexendDeca-Regular", "Lexend Deca", "LexendDeca-Regular.ttf"),
    "med": ("LexendDeca-Medium", "Lexend Deca Medium", "LexendDeca-Medium.ttf"),
    "semi": ("LexendDeca-SemiBold", "Lexend Deca SemiBold", "LexendDeca-SemiBold.ttf"),
    "bold": ("LexendDeca-Bold", "Lexend Deca", "LexendDeca-Bold.ttf"),
}
FONT_WEIGHT = {"reg": 400, "med": 500, "semi": 600, "bold": 700}

_pil = {}


def _font(role, size):
    key = (role, size)
    if key not in _pil:
        _pil[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[role][2]), size)
    return _pil[key]


def text_width(text, size, role="med"):
    return _font(role, size).getlength(text)


def _font_attrs(role):
    ps, fam, _ = FONTS[role]
    return f'font-family="{ps}, \'Lexend Deca\'" font-weight="{FONT_WEIGHT[role]}"'


# --------------------------------------------------------------------------
# Primitive
# --------------------------------------------------------------------------

def rect(x, y, w, h, fill, rx=0, extra=""):
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} fill="{fill}"{extra}/>'


def circle(cx, cy, r, fill, extra=""):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{extra}/>'


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}"{extra}/>'


def group(content, gid=None, transform=None, extra=""):
    a = f' id="{gid}"' if gid else ""
    t = f' transform="{transform}"' if transform else ""
    return f"<g{a}{t}{extra}>{content}</g>"


def place(content, x, y, scale=1.0, rotate=0, gid=None):
    """Posiziona un disegno fatto in coordinate locali."""
    t = f"translate({x:.1f} {y:.1f})"
    if rotate:
        t += f" rotate({rotate})"
    if scale != 1:
        t += f" scale({scale:.4f})"
    return group(content, gid=gid, transform=t)


def stroke(color, w, extra=""):
    return (f' stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}')


# --------------------------------------------------------------------------
# Testo: righe spezzate a mano, ==testo== = box rosso sotto le parole
# --------------------------------------------------------------------------

HL_TOP = 0.97        # il box sale fin sopra gli accenti delle maiuscole
HL_BOTTOM = 0.33     # e scende sotto le discendenti
HL_PAD = 0.19        # rientro orizzontale del box, in frazione del corpo


def _segments(line):
    """'ignori ==da mesi.==' -> [('ignori ', False), ('da mesi.', True)]"""
    out = []
    on = False
    for part in line.split("=="):
        if part:
            out.append((part, on))
        on = not on
    return out


def paragraph(sid, name, x, top, lines, size, role="semi", lh=1.2, fill=WHITE,
              hl_fill=RED, anchor="start", max_width=CW):
    """
    Un paragrafo = un <text>. `top` e' il bordo superiore del box della prima riga.
    Ritorna (svg, bottom) dove bottom e' il bordo inferiore dell'ultima riga (box compreso).
    """
    step = size * lh
    base0 = top + HL_TOP * size
    boxes = []
    tspans = []
    for i, line in enumerate(lines):
        segs = _segments(line)
        plain = "".join(s for s, _ in segs)
        lw = text_width(plain, size, role)
        assert lw <= max_width + 0.5, f"riga troppo lunga ({lw:.0f} > {max_width}): {plain!r}"
        lx = x - lw / 2 if anchor == "middle" else x
        by = base0 + i * step
        cx = lx
        for s, hl in segs:
            sw = text_width(s, size, role)
            if hl:
                core = s.strip()
                lead = text_width(s[: len(s) - len(s.lstrip())], size, role)
                cw = text_width(core, size, role)
                pad = HL_PAD * size
                boxes.append(rect(cx + lead - pad, by - HL_TOP * size, cw + 2 * pad,
                                  (HL_TOP + HL_BOTTOM) * size, hl_fill))
            cx += sw
        tspans.append(f'<tspan x="{lx:.1f}" y="{by:.1f}">{escape(plain)}</tspan>')
    txt = (f'<text id="{sid}-{name}" font-size="{size}" {_font_attrs(role)} fill="{fill}">'
           + "".join(tspans) + "</text>")
    hl = group("".join(boxes), gid=f"{sid}-{name}-evidenziazioni") if boxes else ""
    bottom = base0 + (len(lines) - 1) * step + HL_BOTTOM * size
    return hl + txt, bottom


def label(x, y, text, size, role="med", fill=WHITE, anchor="start", spacing=0, tid=None):
    """Riga singola (etichette, contatti)."""
    idattr = f' id="{tid}"' if tid else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text{idattr} x="{x:.1f}" y="{y:.1f}" font-size="{size}" {_font_attrs(role)} '
            f'fill="{fill}" text-anchor="{anchor}"{ls}>{escape(text)}</text>')


# --------------------------------------------------------------------------
# Scrittura a mano (Caveat) convertita in tracciati
# --------------------------------------------------------------------------

_hand = {}


def hand_path(text, x, y, size, fill=NAVY, anchor="start", extra=""):
    """Testo scritto a mano come <path>: y = linea di base. Ritorna (svg, larghezza)."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    if "f" not in _hand:
        f = TTFont(os.path.join(FONT_DIR, "Caveat-Bold.ttf"))
        _hand["f"] = f
        _hand["gs"] = f.getGlyphSet()
        _hand["cmap"] = f.getBestCmap()
        _hand["upm"] = f["head"].unitsPerEm
    gs, cmap, upm = _hand["gs"], _hand["cmap"], _hand["upm"]
    s = size / upm
    width = sum(gs[cmap[ord(c)]].width for c in text) * s
    if anchor == "middle":
        x -= width / 2
    pen = SVGPathPen(gs)
    cx = x
    for c in text:
        g = gs[cmap[ord(c)]]
        g.draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += g.width * s
    return f'<path d="{pen.getCommands()}" fill="{fill}"{extra}/>', width


# --------------------------------------------------------------------------
# Sfondi raster e logo
# --------------------------------------------------------------------------

_img = {}


def _data_uri(name):
    if name not in _img:
        with open(os.path.join(ASSETS, name), "rb") as f:
            _img[name] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    return _img[name]


def photo_background(sid, rel_path, max_side=1800, quality=88):
    """
    Foto a tutta pagina (4:5), ritagliata al centro e incorporata come JPEG.
    rel_path e' relativo ad assets/. Gruppo '<sid>-foto': in Illustrator si sostituisce con Collega/Incorpora.
    """
    import io
    from PIL import Image
    im = Image.open(os.path.join(ASSETS, rel_path)).convert("RGB")
    r = max(W / im.width, H / im.height)
    cw, ch = W / r, H / r
    left, top = (im.width - cw) / 2, (im.height - ch) / 2
    im = im.crop((round(left), round(top), round(left + cw), round(top + ch)))
    if max(im.size) > max_side:
        k = max_side / max(im.size)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    data = base64.b64encode(buf.getvalue()).decode()
    return group(rect(0, 0, W, H, NAVY)
                 + f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" '
                   f'xlink:href="data:image/jpeg;base64,{data}"/>',
                 gid=f"{sid}-foto")


def background(sid, name="bg_navy.jpg"):
    return group(rect(0, 0, W, H, NAVY)
                 + f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none" '
                   f'xlink:href="{_data_uri(name)}"/>',
                 gid=f"{sid}-sfondo")


_logo = {}


def _load_logo():
    if not _logo:
        src = open(os.path.join(ASSETS, "logo_makhymo_white.svg"), encoding="utf-8").read()
        vx, vy, vw, vh = map(float, re.search(r'viewBox="([^"]+)"', src).group(1).split())
        d = re.search(r' d="([^"]+)"', src).group(1)
        _logo.update(vx=vx, vy=vy, vw=vw, vh=vh, d=d)
    return _logo


def logo(sid, cx, top, width=460, fill=WHITE):
    """Logo Makhymo centrato su cx, largo `width`."""
    lg = _load_logo()
    s = width / lg["vw"]
    x = cx - width / 2
    return group(f'<path fill="{fill}" fill-rule="evenodd" d="{lg["d"]}"/>', gid=f"{sid}-logo",
                 transform=f'translate({x - lg["vx"] * s:.2f} {top - lg["vy"] * s:.2f}) scale({s:.5f})')


def logo_height(width=460):
    lg = _load_logo()
    return width * lg["vh"] / lg["vw"]


# --------------------------------------------------------------------------
# Elementi grafici ricorrenti
# --------------------------------------------------------------------------

def red_flag(h=100, pole=WHITE, pole_shade=STEEL, cloth=RED, cloth_shade=RED_DARK, outline=None):
    """
    La bandierina rossa (l'emoji 🚩 ridisegnata): asta con pomolo e drappo a punta.
    Disegnata in un box 100x100 con l'asta a x=10; scalata ad altezza h.
    outline=colore -> solo contorno del drappo (bandierine 'non ancora arrivate').
    """
    s = h / 100
    drape = "M13,9 C33,2 52,21 92,29 C62,35 42,57 13,55 Z"
    if outline:
        cloth_svg = path(drape, "none", stroke(outline, 3.2 / s ** 0.2))
        fold = ""
    else:
        cloth_svg = path(drape, cloth)
        fold = (path("M13,9 C21,6.5 28,7.5 35,10.8 L35,50.5 C27,53.5 20,55.2 13,55 Z",
                     cloth_shade, ' opacity="0.45"')
                + path("M52,17.5 C60,22 70,25.5 80,27.3 C68,30.5 60,34 52,39 Z", "#FFFFFF",
                       ' opacity="0.13"'))
    body = (rect(7, 6, 6.5, 94, pole, rx=3.2)
            + rect(10.6, 6, 2.9, 94, pole_shade, rx=1.4, extra=' opacity="0.8"')
            + circle(10.2, 6, 5.2, pole)
            + cloth_svg + fold)
    return group(body, transform=f"scale({s:.4f})")


def flag_progress(sid, idx, total=5, x=M, top=128, h=46, gap=40):
    """Paginazione a bandierine: quelle gia' viste rosse, le successive solo contorno."""
    out = ""
    for i in range(1, total + 1):
        fx = x + (i - 1) * gap - 7 * h / 100
        if i <= idx:
            f = red_flag(h)
        else:
            f = group(red_flag(h, pole="#FFFFFF", pole_shade="#FFFFFF", outline="#FFFFFF"),
                      extra=' opacity="0.35"')
        out += place(f, fx, top)
    return group(out, gid=f"{sid}-paginazione")


def hand_arrow(sid, p0, c1, c2, p1, width=4.2, head=30, color=WHITE, name="freccia"):
    """Freccia disegnata a mano: curva di Bezier + punta aperta, come nei caroselli pubblicati."""
    d = (f"M{p0[0]:.1f},{p0[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} "
         f"{c2[0]:.1f},{c2[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}")
    ang = math.atan2(p1[1] - c2[1], p1[0] - c2[0])
    wings = ""
    for da, k in ((math.radians(150), 1.0), (math.radians(-148), 0.86)):
        a = ang + da
        wx, wy = p1[0] + head * k * math.cos(a), p1[1] + head * k * math.sin(a)
        # leggera curvatura dell'ala
        mx = (p1[0] + wx) / 2 + 3 * math.cos(a + math.pi / 2)
        my = (p1[1] + wy) / 2 + 3 * math.sin(a + math.pi / 2)
        wings += f" M{wx:.1f},{wy:.1f} Q{mx:.1f},{my:.1f} {p1[0]:.1f},{p1[1]:.1f}"
    return group(path(d + wings, "none", stroke(color, width)), gid=f"{sid}-{name}")


def icon_camera(x, y, size, color=MICRO):
    s = size / 100
    body = (path("M12,32 h18 l8,-12 h24 l8,12 h18 a6,6 0 0 1 6,6 v44 a6,6 0 0 1 -6,6 h-76 "
                 "a6,6 0 0 1 -6,-6 v-44 a6,6 0 0 1 6,-6 Z", "none", stroke(color, 6))
            + circle(50, 58, 16, "none", stroke(color, 6)))
    return group(body, transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})")


def photo_slot(sid, x, y, w, h, label_txt, rx=40, rotate=0, name="foto"):
    """
    Segnaposto foto: cornice rossa, campitura scura, etichetta.
    In Illustrator: inserire la foto e usare il rettangolo 'maschera' come tracciato di ritaglio.
    """
    cx, cy = x + w / 2, y + h / 2
    inner = (rect(x, y, w, h, CARD_DARK, rx=rx, extra=f' id="{sid}-{name}-maschera"')
             + rect(x, y, w, h, "none", rx=rx, extra=f' stroke="{RED}" stroke-width="4"')
             + icon_camera(cx - 34, cy - 70, 68)
             + label(cx, cy + 40, label_txt, 26, "med", MICRO, "middle"))
    t = f"rotate({rotate} {cx:.1f} {cy:.1f})" if rotate else None
    return group(inner, gid=f"{sid}-{name}", transform=t)


def icon_phone(x, y, size, color):
    s = size / 100
    d = ("M30,12 C24,12 14,20 14,28 C14,58 42,86 72,86 C80,86 88,76 88,70 L88,64 "
         "C88,61 86,59 83,58 L68,53 C65,52 62,53 60,55 L54,62 C42,56 44,58 38,46 "
         "L45,40 C47,38 48,35 47,32 L42,17 C41,14 39,12 36,12 Z")
    return group(path(d, color), transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})")


def icon_mail(x, y, size, color):
    s = size / 100
    body = (rect(8, 22, 84, 58, "none", rx=8, extra=stroke(color, 8))
            + path("M12,28 L50,56 L88,28", "none", stroke(color, 8)))
    return group(body, transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})")


def icon_globe(x, y, size, color):
    s = size / 100
    body = (circle(50, 50, 38, "none", stroke(color, 7))
            + path("M12,50 H88 M50,12 C30,30 30,70 50,88 M50,12 C70,30 70,70 50,88",
                   "none", stroke(color, 6)))
    return group(body, transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})")


def contacts(sid, y=1252, color=KRAFT_INK, size=27):
    """Riga contatti centrata: solo sulla CTA finale."""
    items = [(icon_phone, "+39 0141 353902"), (icon_mail, "info@makhymo.it"),
             (icon_globe, "makhymo.it")]
    isz, igap, gap = 34, 12, 46
    widths = [isz + igap + text_width(t, size, "med") for _, t in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = W / 2 - total / 2
    out = ""
    for (ico, t), w in zip(items, widths):
        out += ico(x, y - isz * 0.86, isz, color)
        out += label(x + isz + igap, y, t, size, "med", color)
        x += w + gap
    return group(out, gid=f"{sid}-contatti")


# --------------------------------------------------------------------------
# Stile 'a scena': oggetto sul tavolo, macchia ondulata dietro, fumetto bianco
# --------------------------------------------------------------------------

DESK_TOP = 885        # bordo posteriore del piano
DESK_FRONT = 1180     # spigolo anteriore del piano
DESK_FACE = 1250      # fondo del bordo frontale
DESK_CORNER = 70      # x dello spigolo anteriore sinistro del tavolo


def rich_text(sid, name, x, baseline, lines, size, lh=1.35, role="reg", fill=NAVY,
              em_role="semi", em_fill=RED, max_width=CW):
    """
    Paragrafo con enfasi: **testo** = em_role / em_fill. Un solo <text>, una <tspan> per riga.
    Ritorna (svg, baseline_ultima_riga).
    """
    step = size * lh
    tspans = []
    for i, line in enumerate(lines):
        runs = []
        on = False
        for part in line.split("**"):
            if part:
                runs.append((part, on))
            on = not on
        lw = sum(text_width(t, size, em_role if e else role) for t, e in runs)
        assert lw <= max_width + 0.5, f"riga troppo lunga ({lw:.0f} > {max_width:.0f}): {line!r}"
        inner = ""
        for t, e in runs:
            if e:
                inner += f'<tspan {_font_attrs(em_role)} fill="{em_fill}">{escape(t)}</tspan>'
            else:
                inner += escape(t)
        tspans.append(f'<tspan x="{x:.1f}" y="{baseline + i * step:.1f}">{inner}</tspan>')
    svg = (f'<text id="{sid}-{name}" font-size="{size}" {_font_attrs(role)} fill="{fill}">'
           + "".join(tspans) + "</text>")
    return svg, baseline + (len(lines) - 1) * step


def bubble_path(x, y, w, h, tip, side="bottom", at=None, r=30, half=28):
    """Fumetto: rettangolo arrotondato con la punta verso `tip`, sul lato basso o destro."""
    tx, ty = tip
    if side == "bottom":
        bx = at if at is not None else x + w * 0.7
        return (f"M{x + r},{y} H{x + w - r} A{r},{r} 0 0 1 {x + w},{y + r} V{y + h - r} "
                f"A{r},{r} 0 0 1 {x + w - r},{y + h} H{bx + half} L{tx},{ty} L{bx - half},{y + h} "
                f"H{x + r} A{r},{r} 0 0 1 {x},{y + h - r} V{y + r} A{r},{r} 0 0 1 {x + r},{y} Z")
    by = at if at is not None else y + h * 0.5
    return (f"M{x + r},{y} H{x + w - r} A{r},{r} 0 0 1 {x + w},{y + r} V{by - half} "
            f"L{tx},{ty} L{x + w},{by + half} V{y + h - r} A{r},{r} 0 0 1 {x + w - r},{y + h} "
            f"H{x + r} A{r},{r} 0 0 1 {x},{y + h - r} V{y + r} A{r},{r} 0 0 1 {x + r},{y} Z")


def speech_bubble(sid, x, y, w, title_lines, body_lines, tip, side="bottom", at=None,
                  title_size=56, body_size=42, pad=46, flag=True):
    """
    Fumetto bianco come nei post di riferimento: titolo in grassetto, testo sotto,
    parti chiave in rosso. flag=True mette la bandierina 🚩 davanti al titolo.
    Ritorna (svg, bottom).
    """
    inner_w = w - 2 * pad
    fx = x + pad
    title_x = fx + (title_size * 0.95 if flag else 0)
    b1 = y + pad + 0.74 * title_size
    t_svg, t_last = rich_text(sid, "titolo", title_x, b1, title_lines, title_size, lh=1.18,
                              role="semi", max_width=inner_w - (title_x - fx))
    body_svg = ""
    last = t_last
    if body_lines:
        bb = t_last + 0.42 * title_size + 0.95 * body_size
        body_svg, last = rich_text(sid, "testo", fx, bb, body_lines, body_size, lh=1.36,
                                   max_width=inner_w)
        bottom_pad = 0.30 * body_size
    else:
        bottom_pad = 0.26 * title_size
    h = last + bottom_pad + pad - y
    d = bubble_path(x, y, w, h, tip, side, at)
    icon = ""
    if flag:
        fh = title_size * 1.02
        icon = place(red_flag(fh, pole=STEEL, pole_shade="#8A93A6"), fx - 0.07 * fh,
                     b1 - 0.86 * title_size)
    svg = group(f'<path d="{d}" fill="#000000" opacity="0.18" transform="translate(0 10)"/>'
                f'<path id="{sid}-fumetto-forma" d="{d}" fill="{WHITE}"/>'
                + icon + t_svg + body_svg, gid=f"{sid}-fumetto")
    return svg, y + h


def blob(sid, cx, cy, rx, ry, fill=RED, waves=9, amp=0.055, seed=1, name="macchia"):
    """Macchia dal bordo ondulato dietro l'oggetto (come la forma lilla del riferimento)."""
    import random
    rnd = random.Random(seed)
    ph1, ph2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
    n = 96
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        k = 1 + amp * math.sin(waves * t + ph1) + 0.05 * math.sin(2 * t + ph2)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    # Catmull-Rom chiusa -> Bezier cubiche
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return group(path(d + " Z", fill), gid=f"{sid}-{name}")


def soft_shadow(sid, cx, cy, rx, ry, opacity=0.35, name="ombra"):
    """Ombra di contatto morbida (gradiente radiale, niente filtri)."""
    gid = f"{sid}-{name}-grad"
    return group(f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5">'
                 f'<stop offset="0" stop-color="#0A1428" stop-opacity="{opacity}"/>'
                 f'<stop offset="0.6" stop-color="#0A1428" stop-opacity="{opacity * 0.45:.3f}"/>'
                 f'<stop offset="1" stop-color="#0A1428" stop-opacity="0"/></radialGradient></defs>'
                 f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{gid})"/>',
                 gid=f"{sid}-{name}")


def desk(sid, corner=DESK_CORNER):
    """Tavolo bianco visto leggermente dall'alto, spigolo sinistro in vista, pavimento scuro sotto."""
    g = f"{sid}-tavolo"
    back_x = corner + 80
    defs = (f'<defs>'
            f'<linearGradient id="{g}-piano" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#DDE3EB"/><stop offset="0.35" stop-color="#EEF2F6"/>'
            f'<stop offset="1" stop-color="#FAFBFD"/></linearGradient>'
            f'<linearGradient id="{g}-bordo" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#D6DCE5"/><stop offset="1" stop-color="#B9C1CD"/></linearGradient>'
            f'<linearGradient id="{g}-sotto" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#050C1A"/><stop offset="1" stop-color="#0C1A36"/></linearGradient>'
            f'<linearGradient id="{g}-ao" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#050C1A" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#050C1A" stop-opacity="0.45"/></linearGradient>'
            f'</defs>')
    body = (rect(0, DESK_TOP - 26, W, 26, f"url(#{g}-ao)")                         # ombra sul muro
            + rect(0, DESK_FRONT - 10, W, H - DESK_FRONT + 10, f"url(#{g}-sotto)")  # pavimento
            + path(f"M{back_x},{DESK_TOP} H{W} V{DESK_FRONT} H{corner} Z", f"url(#{g}-piano)")
            + rect(corner, DESK_FRONT, W - corner, DESK_FACE - DESK_FRONT, f"url(#{g}-bordo)")
            + rect(corner, DESK_FRONT - 2, W - corner, 3, WHITE, extra=' opacity="0.9"')
            + path(f"M{corner},{DESK_FACE} H{W} V{DESK_FACE + 26} H{corner + 20} Z", "#000000",
                   ' opacity="0.35"'))
    return group(defs + body, gid=g)


# --------------------------------------------------------------------------
# Assemblaggio e consegna
# --------------------------------------------------------------------------

SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'version="1.1" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')


def slide(sid, content):
    return group(content, gid=sid)


def slide_svg(content):
    return SVG_HEAD.format(w=W, h=H) + content + "</svg>"


def slides_to_multi_svg(slides, gap=120):
    """Tutte le tavole affiancate in orizzontale, ognuna nel suo gruppo <g id="tavola-NN">."""
    n = len(slides)
    tw = n * W + (n - 1) * gap
    body = ""
    for i, s in enumerate(slides):
        body += f'<g id="tavola-{i + 1:02d}" transform="translate({i * (W + gap)} 0)">{s}</g>'
    return SVG_HEAD.format(w=tw, h=H) + body + "</svg>"


def _for_render(svg):
    """Copia per cairo: la famiglia deve essere quella di fontconfig (cairo legge il primo nome)."""
    for role, (ps, fam, _) in FONTS.items():
        w = 700 if role == "bold" else 400
        svg = svg.replace(f'font-family="{ps}, \'Lexend Deca\'" font-weight="{FONT_WEIGHT[role]}"',
                          f'font-family="{fam}" font-weight="{w}"')
    return svg


def deliver(slides, slug, out_dir=None, sheet=True):
    """
    Scrive Makhymo_<slug>_ALL_SLIDES.svg e, in Makhymo_<slug>_PNG/, una PNG 1080x1350
    per slide (Makhymo_<slug>_NN.png, pronte per Instagram) + contact_sheet.jpg.
    """
    import io
    import xml.etree.ElementTree as ET

    import cairosvg
    from PIL import Image

    out_dir = out_dir or os.path.join(HERE, "output")
    prev_dir = os.path.join(out_dir, f"Makhymo_{slug}_PNG")
    os.makedirs(prev_dir, exist_ok=True)
    for f in os.listdir(prev_dir):           # niente slide di versioni precedenti
        if f.endswith(".png"):
            os.remove(os.path.join(prev_dir, f))

    svg_path = os.path.join(out_dir, f"Makhymo_{slug}_ALL_SLIDES.svg")
    multi = slides_to_multi_svg(slides)
    ET.fromstring(multi)                      # SVG valido o eccezione
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(multi)

    pngs = []
    for i, s in enumerate(slides, 1):
        doc = slide_svg(s)
        n_text = doc.count("<text")
        p = os.path.join(prev_dir, f"Makhymo_{slug}_{i:02d}.png")
        cairosvg.svg2png(bytestring=_for_render(doc).encode(), write_to=p)
        pngs.append(p)
        print(f"slide {i:02d}: {n_text} blocchi <text>")

    if sheet:
        cols = 4
        rows = math.ceil(len(pngs) / cols)
        tw_, th_ = 432, 540
        cs = Image.new("RGB", (cols * tw_ + (cols + 1) * 16, rows * th_ + (rows + 1) * 16), "#DDDDDD")
        for i, p in enumerate(pngs):
            im = Image.open(p).convert("RGB").resize((tw_, th_), Image.LANCZOS)
            cs.paste(im, (16 + (i % cols) * (tw_ + 16), 16 + (i // cols) * (th_ + 16)))
        cs.save(os.path.join(prev_dir, "contact_sheet.jpg"), quality=88)
    return svg_path, prev_dir
