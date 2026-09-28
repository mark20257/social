"""
Libreria caroselli Madonia (Cav. Madonia Maurizio Assicurazioni, Asti).

Genera slide 1080x1350 in SVG pensate per Illustrator:
  - ogni paragrafo e' un solo <text> con una <tspan x y> per riga
  - ogni slide e' un gruppo <g id="slide-NN"> con sottogruppi nominati
  - illustrazioni e infografiche sono tracciati vettoriali, niente raster

Consegna: PDF multipagina (una pagina = una tavola) + SVG multi-tavola.
"""

import math
import os
import random
import re
import shutil
from xml.sax.saxutils import escape

from PIL import ImageFont

# --------------------------------------------------------------------------
# Costanti
# --------------------------------------------------------------------------

W, H = 1080, 1350
M = 90                      # margine laterale
CW = W - 2 * M              # larghezza utile

NAVY = "#0F2659"
NAVY_DEEP = "#081A40"
NAVY_MID = "#1A3775"        # tinta di servizio per card e illustrazioni
NAVY_LINE = "#2B4C92"
AZURE = "#3B7FE8"
AZURE_LIGHT = "#6FA3F2"
AZURE_DARK = "#2A63C4"
WHITE = "#FFFFFF"
SOFT = "#D6E0F0"
DIM = "#C3CDE1"
DOT = "#AAC8FF"

BODY = 35                   # corpo testo principale
MIN_SIZE = 30               # nessun testo sotto questa misura

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONT_DIRS = [os.path.join(ASSETS, "fonts"), os.path.expanduser("~/.fonts")]

# nomi PostScript letti da Illustrator in apertura dell'SVG
PS_NAMES = {
    (400, "normal"): "Raleway-Regular",
    (700, "normal"): "Raleway-Bold",
    (400, "italic"): "Raleway-Italic",
    (700, "italic"): "Raleway-BoldItalic",
}
FONT_FILES = {
    (400, "normal"): "Raleway-400-normal.ttf",
    (700, "normal"): "Raleway-700-normal.ttf",
    (400, "italic"): "Raleway-400-italic.ttf",
    (700, "italic"): "Raleway-700-italic.ttf",
}

_font_cache = {}


def _font(weight, style, size):
    key = (weight, style, size)
    if key not in _font_cache:
        fname = FONT_FILES[(weight, style)]
        for d in FONT_DIRS:
            p = os.path.join(d, fname)
            if os.path.exists(p):
                _font_cache[key] = ImageFont.truetype(p, size)
                break
        else:
            raise FileNotFoundError(f"Font Raleway mancante: {fname}")
    return _font_cache[key]


def text_width(text, size, weight=400, style="normal", spacing=0):
    w = _font(weight, style, size).getlength(text)
    return w + spacing * max(len(text) - 1, 0)


def fmt(n, dec=0):
    """Numero in formato italiano: 1.234,5"""
    s = f"{n:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


# --------------------------------------------------------------------------
# Testo ricco: **grassetto**  ==azzurro==  (combinabili: **==x==**)
# --------------------------------------------------------------------------

def _tokens(text, base_weight, base_fill, accent_col=AZURE):
    """Divide il testo in parole con stile (peso, colore)."""
    out = []
    bold = False
    accent = False
    for part in re.split(r"(\*\*|==)", text):
        if part == "**":
            bold = not bold
            continue
        if part == "==":
            accent = not accent
            continue
        style = (700 if bold else base_weight, accent_col if accent else base_fill)
        for i, word in enumerate(part.split(" ")):
            if word == "":
                if i > 0 and out:
                    out[-1]["space_after"] = True
                continue
            if i > 0 and out:
                out[-1]["space_after"] = True
            out.append({"w": word, "style": style, "space_after": False})
    # spazio dopo l'ultima parola di un run se il run successivo inizia dopo spazio
    return out


def _line_width(line, size, italic):
    st = "italic" if italic else "normal"
    tot = 0
    for i, t in enumerate(line):
        tot += text_width(t["w"], size, t["style"][0], st)
        if i < len(line) - 1 and t["space_after"]:
            tot += text_width(" ", size, t["style"][0], st)
    return tot


def wrap(text, size, max_width, weight=400, fill=WHITE, italic=False, accent=AZURE):
    """Word-wrap con regola anti-orfano. Supporta '\n' come a capo forzato."""
    lines = []
    for para in text.split("\n"):
        toks = _tokens(para, weight, fill, accent)
        cur = []
        para_lines = []
        for t in toks:
            trial = cur + [t]
            if cur and _line_width(trial, size, italic) > max_width:
                para_lines.append(cur)
                cur = [t]
            else:
                cur = trial
        if cur:
            para_lines.append(cur)
        # anti-orfano: l'ultima riga non resta mai con una sola parola
        if len(para_lines) >= 2 and len(para_lines[-1]) == 1 and len(para_lines[-2]) >= 2:
            trial = [para_lines[-2][-1]] + para_lines[-1]
            if _line_width(trial, size, italic) <= max_width:
                para_lines[-2].pop()
                para_lines[-1] = trial
        lines.extend(para_lines)
    return lines


def _font_attrs(weight, italic):
    st = "italic" if italic else "normal"
    ps = PS_NAMES[(weight, st)]
    a = f'font-family="{ps}, Raleway" font-weight="{weight}"'
    if italic:
        a += ' font-style="italic"'
    return a


def text_block(x, y, text, size=BODY, weight=400, fill=WHITE, max_width=CW,
               lh=1.4, anchor="start", italic=False, tid=None, spacing=0, accent=AZURE):
    """
    Paragrafo come UN solo <text>. y = linea di base della prima riga.
    Ritorna (svg, altezza_occupata, n_righe). L'altezza va dalla cima
    del maiuscolo della prima riga alla base dell'ultima.
    """
    assert size >= MIN_SIZE, f"testo sotto {MIN_SIZE}px: {text[:30]}"
    lines = wrap(text, size, max_width, weight, fill, italic, accent)
    step = size * lh
    idattr = f' id="{tid}"' if tid else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    parts = [f'<text{idattr} x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
             f'{_font_attrs(weight, italic)} fill="{fill}" text-anchor="{anchor}"{ls}>']
    for i, line in enumerate(lines):
        ly = y + i * step
        runs = []
        for j, t in enumerate(line):
            sp = " " if (j < len(line) - 1 and t["space_after"]) else ""
            if runs and runs[-1]["style"] == t["style"]:
                runs[-1]["txt"] += t["w"] + sp
            else:
                runs.append({"style": t["style"], "txt": t["w"] + sp})
        inner = ""
        for r in runs:
            w_, f_ = r["style"]
            txt = escape(r["txt"])
            if (w_, f_) == (weight, fill):
                inner += txt
            else:
                attrs = ""
                if w_ != weight:
                    attrs += f' {_font_attrs(w_, italic)}'
                if f_ != fill:
                    attrs += f' fill="{f_}"'
                inner += f"<tspan{attrs}>{txt}</tspan>"
        if anchor == "middle" and len(runs) > 1:
            # righe centrate con stili misti: posizione calcolata, allineamento a sinistra
            lx = x - _line_width(line, size, italic) / 2
            parts.append(f'<tspan x="{lx:.1f}" y="{ly:.1f}" text-anchor="start">{inner}</tspan>')
        else:
            parts.append(f'<tspan x="{x:.1f}" y="{ly:.1f}">{inner}</tspan>')
    parts.append("</text>")
    cap = size * 0.72
    height = cap + (len(lines) - 1) * step
    return "".join(parts), height, len(lines)


def block_height(text, size=BODY, weight=400, max_width=CW, lh=1.4, italic=False):
    n = len(wrap(text, size, max_width, weight, WHITE, italic))
    return size * 0.72 + (n - 1) * size * lh


# --------------------------------------------------------------------------
# Primitive SVG
# --------------------------------------------------------------------------

def rect(x, y, w, h, fill, rx=0, extra=""):
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} fill="{fill}"{extra}/>'


def circle(cx, cy, r, fill, extra=""):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{extra}/>'


def group(content, gid=None, transform=None, extra=""):
    a = f' id="{gid}"' if gid else ""
    t = f' transform="{transform}"' if transform else ""
    return f"<g{a}{t}{extra}>{content}</g>"


def svg_diamond(cx, cy, s, fill=AZURE):
    return (f'<rect x="{cx - s / 2:.1f}" y="{cy - s / 2:.1f}" width="{s}" height="{s}" '
            f'fill="{fill}" transform="rotate(45 {cx:.1f} {cy:.1f})"/>')


def svg_text(x, y, text, size, weight=400, fill=WHITE, anchor="start",
             italic=False, spacing=0, tid=None):
    """Riga singola (etichette, numeri)."""
    assert size >= MIN_SIZE, f"testo sotto {MIN_SIZE}px: {text}"
    idattr = f' id="{tid}"' if tid else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text{idattr} x="{x:.1f}" y="{y:.1f}" font-size="{size}" {_font_attrs(weight, italic)} '
            f'fill="{fill}" text-anchor="{anchor}"{ls}>{escape(text)}</text>')


# --------------------------------------------------------------------------
# Sfondo, logo, elementi ricorrenti
# --------------------------------------------------------------------------

def background(sid, glow=(880, 160)):
    gx, gy = glow
    return group(
        f'<defs>'
        f'<pattern id="{sid}-dots" width="30" height="30" patternUnits="userSpaceOnUse">'
        f'<circle cx="15" cy="15" r="1.7" fill="{DOT}"/></pattern>'
        f'<radialGradient id="{sid}-glow" cx="{gx}" cy="{gy}" r="620" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{AZURE}" stop-opacity="0.30"/>'
        f'<stop offset="1" stop-color="{AZURE}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="{sid}-deep" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0.45" stop-color="{NAVY_DEEP}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{NAVY_DEEP}" stop-opacity="0.85"/></linearGradient>'
        f'</defs>'
        + rect(0, 0, W, H, NAVY)
        + rect(0, 0, W, H, f"url(#{sid}-deep)")
        + rect(0, 0, W, H, f"url(#{sid}-glow)")
        + rect(0, 0, W, H, f"url(#{sid}-dots)", extra=' opacity="0.13"'),
        gid=f"{sid}-sfondo")


_logo_cache = {}


def _load_logo():
    """Logo 'Tavola disegno 2' vettoriale (assets/logo_tavola2.svg)."""
    if "logo" in _logo_cache:
        return _logo_cache["logo"]
    p = os.path.join(ASSETS, "logo_tavola2.svg")
    if not os.path.exists(p):
        _logo_cache["logo"] = None
        return None
    src = open(p, encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1).split()
    vx, vy, vw, vh = map(float, vb)
    inner = re.sub(r"^.*?<svg[^>]*>", "", src, flags=re.S)
    inner = re.sub(r"</svg>\s*$", "", inner.strip(), flags=re.S)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    _logo_cache["logo"] = (vx, vy, vw, vh, inner)
    return _logo_cache["logo"]


def logo_ratio():
    lg = _load_logo()
    return (lg[2] / lg[3]) if lg else 2408.65 / 1371


def svg_logo(x, y, height, sid, anchor="start"):
    """Logo alto `height` px. anchor: start | middle | end rispetto a x."""
    lg = _load_logo()
    ratio = logo_ratio()
    w = height * ratio
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    if lg is None:
        # segnaposto: sostituire con Tavola disegno 2 in Illustrator
        return group(rect(x, y, w, height, "none",
                          extra=f' stroke="{WHITE}" stroke-width="2" stroke-dasharray="8 6"')
                     + svg_text(x + w / 2, y + height / 2 + 11, "LOGO", 30, 700, WHITE, "middle"),
                     gid=f"{sid}-logo")
    vx, vy, vw, vh, inner = lg
    # id univoci per slide
    inner = re.sub(r'id="([^"]+)"', lambda m_: f'id="{sid}-lg-{m_.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m_: f'url(#{sid}-lg-{m_.group(1)})', inner)
    inner = re.sub(r'href="#([^"]+)"', lambda m_: f'href="#{sid}-lg-{m_.group(1)}"', inner)
    s = height / vh
    return group(inner, gid=f"{sid}-logo",
                 transform=f"translate({x - vx * s:.2f} {y - vy * s:.2f}) scale({s:.5f})")


def svg_logo_topright(sid, height=120):
    return svg_logo(W - M + 20, 56, height, sid, anchor="end")


def svg_logo_center(sid, y, height):
    return svg_logo(W / 2, y, height, sid, anchor="middle")


def eyebrow(sid, text, x=M, y=112):
    return group(rect(x, y - 30, 8, 36, AZURE)
                 + svg_text(x + 24, y, text, 30, 700, AZURE, spacing=3),
                 gid=f"{sid}-occhiello")


def source_block(sid, text, bottom=1292):
    """Fonte ancorata in basso. Ritorna (svg, y_top) per ancorare i blocchi sopra."""
    size = 30
    lh = 1.3
    n = len(wrap(text, size, CW, 400, DIM, True))
    y0 = bottom - (n - 1) * size * lh
    svg, h, _ = text_block(M, y0, text, size, 400, DIM, CW, lh, italic=True, tid=f"{sid}-fonte")
    top = y0 - size * 0.72
    return group(svg, gid=f"{sid}-fonte-g"), top


def counter(sid, i, n):
    return svg_text(W - M, 1292, f"{i:02d}/{n:02d}", 30, 700, AZURE, "end", tid=f"{sid}-num")


# --------------------------------------------------------------------------
# Icone vettoriali (disegnate su un quadrato 100x100, poi scalate)
# --------------------------------------------------------------------------

def _icon(content, x, y, size, gid=None):
    s = size / 100
    return group(content, gid=gid, transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})")


def icon_bank(x, y, size, c=WHITE, gid=None):
    return _icon(
        f'<path d="M50 6 L94 30 L94 38 L6 38 L6 30 Z" fill="{c}"/>'
        + "".join(rect(14 + i * 20, 44, 12, 34, c) for i in range(4))
        + rect(6, 82, 88, 10, c, 2), x, y, size, gid)


def icon_cart(x, y, size, c=WHITE, gid=None):
    return _icon(
        f'<path d="M4 14 L20 14 L32 66 L82 66" fill="none" stroke="{c}" stroke-width="8" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M24 26 L94 26 L86 54 L30 54 Z" fill="{c}"/>'
        + circle(38, 84, 8, c) + circle(76, 84, 8, c), x, y, size, gid)


def icon_target(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        circle(46, 54, 40, c) + circle(46, 54, 29, bg) + circle(46, 54, 19, c) + circle(46, 54, 9, bg)
        + f'<path d="M46 54 L86 14" stroke="{c}" stroke-width="6" stroke-linecap="round"/>'
        + f'<path d="M78 6 L80 20 L94 22 L86 30 L72 28 L70 14 Z" fill="{c}"/>', x, y, size, gid)


def icon_calendar(x, y, size, c=WHITE, bg=NAVY, gid=None):
    cells = ""
    for r_ in range(3):
        for c_ in range(4):
            cells += rect(18 + c_ * 18, 46 + r_ * 14, 10, 8, bg, 1)
    return _icon(
        rect(6, 14, 88, 80, c, 10) + rect(6, 14, 88, 22, c, 10)
        + rect(14, 6, 10, 20, c, 4) + rect(76, 6, 10, 20, c, 4)
        + rect(6, 34, 88, 4, bg) + cells, x, y, size, gid)


def icon_gauge(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        f'<path d="M8 72 A42 42 0 0 1 92 72" fill="none" stroke="{c}" stroke-width="14"/>'
        f'<path d="M50 72 L74 40" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
        + circle(50, 72, 9, c)
        + rect(8, 84, 84, 8, c, 4), x, y, size, gid)


def icon_house(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        f'<path d="M50 8 L94 46 L84 46 L84 92 L16 92 L16 46 L6 46 Z" fill="{c}"/>'
        + rect(40, 60, 20, 32, bg, 2) + rect(66, 14, 12, 22, c), x, y, size, gid)


def icon_pension(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Clessidra: il tempo della pensione."""
    return _icon(
        rect(18, 6, 64, 10, c, 4) + rect(18, 84, 64, 10, c, 4)
        + f'<path d="M26 16 L74 16 L74 24 Q74 40 54 50 Q74 60 74 76 L74 84 L26 84 L26 76 '
          f'Q26 60 46 50 Q26 40 26 24 Z" fill="{c}"/>'
        + f'<path d="M34 24 L66 24 Q64 36 50 44 Q36 36 34 24 Z" fill="{bg}"/>'
        + f'<path d="M50 60 Q64 66 66 78 L34 78 Q36 66 50 60 Z" fill="{bg}" opacity="0.55"/>',
        x, y, size, gid)


def icon_project(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Lampadina: un progetto futuro."""
    return _icon(
        circle(50, 40, 32, c)
        + f'<path d="M34 58 L66 58 L62 74 L38 74 Z" fill="{c}"/>'
        + rect(38, 78, 24, 6, c, 3) + rect(42, 88, 16, 6, c, 3)
        + f'<path d="M40 44 L46 36 L50 46 L54 36 L60 44" fill="none" stroke="{bg}" '
          f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>', x, y, size, gid)


def icon_shield(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        f'<path d="M50 6 L88 20 L88 48 Q88 78 50 94 Q12 78 12 48 L12 20 Z" fill="{c}"/>'
        f'<path d="M32 50 L46 64 L70 38" fill="none" stroke="{bg}" stroke-width="9" '
        f'stroke-linecap="round" stroke-linejoin="round"/>', x, y, size, gid)


def icon_phone(x, y, size, c=WHITE, gid=None):
    return _icon(
        f'<path d="M22 8 L38 8 L46 30 L36 38 Q44 56 62 64 L70 54 L92 62 L92 78 Q90 92 76 92 '
        f'Q40 90 18 64 Q6 46 8 22 Q10 8 22 8 Z" fill="{c}"/>', x, y, size, gid)


def icon_mail(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        rect(6, 20, 88, 62, c, 8)
        + f'<path d="M12 28 L50 56 L88 28" fill="none" stroke="{bg}" stroke-width="7" '
          f'stroke-linecap="round" stroke-linejoin="round"/>', x, y, size, gid)


def icon_pin(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        f'<path d="M50 96 Q16 58 16 38 A34 34 0 0 1 84 38 Q84 58 50 96 Z" fill="{c}"/>'
        + circle(50, 38, 13, bg), x, y, size, gid)


def icon_web(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Globo stilizzato: sito web."""
    return _icon(
        circle(50, 50, 44, c) + circle(50, 50, 36, bg)
        + f'<ellipse cx="50" cy="50" rx="15" ry="36" fill="none" stroke="{c}" stroke-width="7"/>'
        + rect(14, 46, 72, 8, c) + rect(46, 14, 8, 72, c), x, y, size, gid)


def icon_work(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Valigetta: lavoro e reddito."""
    return _icon(
        f'<path d="M36 22 L36 14 Q36 8 42 8 L58 8 Q64 8 64 14 L64 22" fill="none" stroke="{c}" stroke-width="7"/>'
        + rect(6, 22, 88, 66, c, 10) + rect(6, 46, 88, 6, bg) + rect(42, 40, 16, 18, c, 3)
        + rect(45, 43, 10, 12, bg, 2), x, y, size, gid)


def icon_family(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Due adulti e un bambino: famiglia."""
    return _icon(
        circle(28, 22, 12, c) + f'<path d="M8 90 L8 56 Q8 40 28 40 Q48 40 48 56 L48 90 Z" fill="{c}"/>'
        + circle(72, 22, 12, c) + f'<path d="M52 90 L52 56 Q52 40 72 40 Q92 40 92 56 L92 90 Z" fill="{c}"/>'
        + circle(50, 54, 12, bg) + circle(50, 54, 9, c)
        + f'<path d="M34 94 L34 80 Q34 68 50 68 Q66 68 66 80 L66 94 Z" fill="{c}" stroke="{bg}" stroke-width="4"/>',
        x, y, size, gid)


def icon_person(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(circle(50, 22, 18, c)
                 + f'<path d="M18 98 L18 62 Q18 44 50 44 Q82 44 82 62 L82 98 Z" fill="{c}"/>', x, y, size, gid)


def icon_scale(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Bilancia: la norma."""
    return _icon(
        rect(46, 12, 8, 72, c, 3) + rect(26, 84, 48, 10, c, 4) + rect(12, 20, 76, 7, c, 3)
        + circle(50, 14, 7, c)
        + f'<path d="M20 26 L8 56 L32 56 Z M80 26 L68 56 L92 56 Z" fill="none" stroke="{c}" stroke-width="4" stroke-linejoin="round"/>'
        + f'<path d="M4 56 L36 56 Q34 70 20 70 Q6 70 4 56 Z M64 56 L96 56 Q94 70 80 70 Q66 70 64 56 Z" fill="{c}"/>',
        x, y, size, gid)


def icon_heart(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        f'<path d="M50 90 Q10 62 8 36 Q8 12 30 12 Q44 12 50 26 Q56 12 70 12 Q92 12 92 36 Q90 62 50 90 Z" fill="{c}"/>',
        x, y, size, gid)


def icon_piggy(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Salvadanaio: risparmio."""
    return _icon(
        f'<ellipse cx="50" cy="54" rx="38" ry="30" fill="{c}"/>'
        + f'<path d="M24 32 L28 14 L42 28 Z" fill="{c}"/>'
        + rect(22, 74, 12, 20, c, 4) + rect(62, 74, 12, 20, c, 4)
        + f'<ellipse cx="10" cy="54" rx="8" ry="10" fill="{c}"/>'
        + rect(40, 30, 22, 6, bg, 3) + circle(28, 46, 4, bg), x, y, size, gid)


def icon_x(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(circle(50, 50, 46, c)
                 + f'<path d="M32 32 L68 68 M68 32 L32 68" stroke="{bg}" stroke-width="10" stroke-linecap="round"/>',
                 x, y, size, gid)


def icon_question(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(circle(50, 50, 46, c)
                 + f'<path d="M36 38 Q36 22 50 22 Q64 22 64 36 Q64 46 52 50 L50 60" fill="none" stroke="{bg}" '
                   f'stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
                 + circle(50, 76, 6, bg), x, y, size, gid)


def icon_chat(x, y, size, c=WHITE, bg=NAVY, gid=None):
    """Due fumetti: dialogo."""
    return _icon(
        f'<path d="M6 14 Q6 6 14 6 L62 6 Q70 6 70 14 L70 44 Q70 52 62 52 L30 52 L16 64 L18 52 L14 52 Q6 52 6 44 Z" fill="{c}"/>'
        + f'<path d="M38 60 L38 58 Q38 56 40 56 L86 56 Q94 56 94 64 L94 84 Q94 92 86 92 L82 92 L84 100 L72 92 L46 92 '
          f'Q38 92 38 84 Z" fill="{c}" stroke="{bg}" stroke-width="5"/>'
        + circle(24, 29, 5, bg) + circle(38, 29, 5, bg) + circle(52, 29, 5, bg), x, y, size, gid)


def icon_eye_off(x, y, size, c=WHITE, bg=NAVY, gid=None):
    return _icon(
        f'<path d="M6 50 Q50 6 94 50 Q50 94 6 50 Z" fill="{c}"/>'
        + circle(50, 50, 18, bg) + circle(50, 50, 8, c)
        + f'<path d="M14 88 L86 12" stroke="{bg}" stroke-width="14" stroke-linecap="round"/>'
        + f'<path d="M14 88 L86 12" stroke="{c}" stroke-width="7" stroke-linecap="round"/>',
        x, y, size, gid)


def icon_euro_coin(cx, cy, r, face=SOFT, edge=AZURE_LIGHT, sym=NAVY, gid=None):
    """Moneta vista di fronte con simbolo euro."""
    s = r / 50
    return group(
        circle(0, 0, 50, edge) + circle(0, 0, 42, face)
        + f'<path d="M16 -20 Q8 -30 -2 -30 Q-24 -30 -24 0 Q-24 30 -2 30 Q8 30 16 20" fill="none" '
          f'stroke="{sym}" stroke-width="8" stroke-linecap="round"/>'
        + rect(-34, -10, 36, 6, sym, 3) + rect(-34, 4, 32, 6, sym, 3),
        gid=gid, transform=f"translate({cx:.1f} {cy:.1f}) scale({s:.4f})")


# --------------------------------------------------------------------------
# Illustrazioni
# --------------------------------------------------------------------------

def illu_piggy_dissolve(sid, x, y, scale=1.0, seed=7):
    """
    Salvadanaio che si sgretola in pixel sul retro: il capitale resta,
    il potere d'acquisto se ne va senza farsi vedere.
    Coordinate locali 0..700 x 0..460.
    """
    rnd = random.Random(seed)
    cut = 318                                   # oltre questa x il corpo si dissolve
    body = (
        f'<ellipse cx="290" cy="235" rx="215" ry="165" fill="url(#{sid}-pig)"/>'
        f'<path d="M150 118 L178 46 L232 104 Z" fill="{AZURE_DARK}"/>'           # orecchio
        + rect(140, 330, 44, 88, AZURE_DARK, 14) + rect(208, 340, 44, 80, AZURE, 14)
        + rect(330, 336, 44, 84, AZURE, 14) + rect(398, 326, 44, 92, AZURE_DARK, 14)
        + f'<ellipse cx="86" cy="240" rx="44" ry="56" fill="{AZURE_DARK}"/>'    # grugno
        + f'<ellipse cx="76" cy="222" rx="8" ry="12" fill="{NAVY_DEEP}"/>'
        + f'<ellipse cx="76" cy="258" rx="8" ry="12" fill="{NAVY_DEEP}"/>'
        + circle(168, 190, 12, NAVY_DEEP) + circle(172, 186, 4, WHITE)
        + rect(240, 74, 110, 16, NAVY_DEEP, 8)                                  # fessura
        + f'<ellipse cx="250" cy="170" rx="90" ry="46" fill="{WHITE}" opacity="0.12"/>'
    )
    clip = (f'<clipPath id="{sid}-pigclip"><path d="M0 0 L{cut} 0 L{cut + 14} 90 L{cut - 6} 170 '
            f'L{cut + 12} 250 L{cut - 4} 330 L{cut + 8} 460 L0 460 Z"/></clipPath>')

    def inside(px, py):
        e = ((px - 290) / 215) ** 2 + ((py - 235) / 165) ** 2 <= 1
        legs = (330 <= px <= 374 and 336 <= py <= 420) or (398 <= px <= 442 and 326 <= py <= 418)
        return e or legs

    cells = []
    step = 20
    for gx in range(cut - 20, 520, step):
        for gy in range(60, 430, step):
            cx_, cy_ = gx + step / 2, gy + step / 2
            if not inside(cx_, cy_):
                continue
            p = max(0.0, 1 - (gx - (cut - 20)) / 230)
            if rnd.random() < p:
                col = rnd.choice([AZURE, AZURE, AZURE_DARK, AZURE_LIGHT])
                cells.append(rect(gx + 1, gy + 1, step - 3, step - 3, col, 2))
    # particelle che volano via, sempre piu' piccole e trasparenti
    for _ in range(46):
        px = rnd.uniform(440, 690)
        t = (px - 440) / 250
        py = rnd.uniform(40, 360) - t * 60
        s = 14 * (1 - t) + 4
        op = 0.85 * (1 - t) + 0.12
        col = rnd.choice([AZURE, AZURE_LIGHT, DOT])
        cells.append(rect(px, py, s, s, col, 2, extra=f' opacity="{op:.2f}"'))
    coin = icon_euro_coin(296, 20, 34, gid=f"{sid}-moneta")
    defs = (f'<defs>{clip}<linearGradient id="{sid}-pig" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{AZURE_LIGHT}"/><stop offset="1" stop-color="{AZURE}"/>'
            f'</linearGradient></defs>')
    shadow = f'<ellipse cx="300" cy="432" rx="230" ry="18" fill="{NAVY_DEEP}" opacity="0.55"/>'
    return group(defs + shadow + group(body, extra=f' clip-path="url(#{sid}-pigclip)"')
                 + group("".join(cells), gid=f"{sid}-pixel") + coin,
                 gid=f"{sid}-illustrazione", transform=f"translate({x} {y}) scale({scale})")


def illu_globe(sid, cx, cy, r):
    """Globo con meridiani, paralleli e segnaposto."""
    rnd = random.Random(3)
    lines = ""
    for k in (-0.6, -0.2, 0.2, 0.6):
        ry = r * math.sqrt(1 - k * k)
        lines += (f'<ellipse cx="{cx}" cy="{cy + k * r:.1f}" rx="{ry:.1f}" ry="{ry * 0.16:.1f}" '
                  f'fill="none" stroke="{AZURE_LIGHT}" stroke-width="3" opacity="0.55"/>')
    for k in (0.25, 0.55, 0.85):
        lines += (f'<ellipse cx="{cx}" cy="{cy}" rx="{r * k:.1f}" ry="{r:.1f}" fill="none" '
                  f'stroke="{AZURE_LIGHT}" stroke-width="3" opacity="0.55"/>')
    lines += f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="{AZURE_LIGHT}" stroke-width="3" opacity="0.55"/>'
    dots = ""
    for _ in range(90):
        a = rnd.uniform(0, 2 * math.pi)
        d = r * math.sqrt(rnd.uniform(0, 0.92))
        dots += circle(cx + d * math.cos(a), cy + d * math.sin(a), 3.2, DOT, extra=' opacity="0.5"')
    pins = ""
    for (px, py, s) in [(-0.45, -0.35, 1.0), (0.3, -0.5, 0.8), (0.5, 0.15, 0.9),
                        (-0.2, 0.3, 0.75), (0.05, -0.05, 1.15)]:
        size = 64 * s
        pins += icon_pin(cx + px * r - size / 2, cy + py * r - size, size, WHITE, AZURE)
    return group(
        f'<defs><radialGradient id="{sid}-globe" cx="{cx - r * 0.3}" cy="{cy - r * 0.35}" r="{r * 1.3}" '
        f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{AZURE}"/>'
        f'<stop offset="1" stop-color="{NAVY_MID}"/></radialGradient></defs>'
        + circle(cx, cy, r + 18, AZURE, extra=' opacity="0.12"')
        + circle(cx, cy, r, f"url(#{sid}-globe)") + lines + dots + pins,
        gid=f"{sid}-illustrazione")


def illu_calendar_savings(sid, x, y, w, label="OTTOBRE"):
    """Pagina di calendario con una data cerchiata e un salvadanaio di monete."""
    s = w / 400
    days = ""
    n = 1
    for r_ in range(5):
        for c_ in range(7):
            if n > 31:
                break
            dx, dy = 34 + c_ * 52, 150 + r_ * 44
            days += rect(dx, dy, 34, 26, NAVY_LINE, 5)
            n += 1
    ring = (f'<ellipse cx="{34 + 4 * 52 + 17}" cy="{150 + 2 * 44 + 13}" rx="36" ry="28" fill="none" '
            f'stroke="{AZURE}" stroke-width="7"/>'
            + rect(34 + 4 * 52, 150 + 2 * 44, 34, 26, AZURE, 5))
    coins = "".join(
        f'<ellipse cx="330" cy="{378 - i * 16}" rx="52" ry="14" fill="{AZURE_LIGHT if i % 2 else SOFT}" '
        f'stroke="{NAVY}" stroke-width="3"/>' for i in range(6))
    return group(
        rect(0, 20, 400, 380, SOFT, 26) + rect(0, 20, 400, 96, NAVY, 26) + rect(0, 80, 400, 36, NAVY)
        + svg_text(200, 92, label, 40, 700, WHITE, "middle", spacing=4)
        + rect(70, 0, 18, 56, NAVY_DEEP, 9) + rect(312, 0, 18, 56, NAVY_DEEP, 9)
        + f'<g transform="translate(0 0)">{days}</g>' + ring + coins,
        gid=f"{sid}-illustrazione", transform=f"translate({x} {y}) scale({s:.4f})")


def infog_value_bars(sid, top, bottom, rows):
    """
    Barre-banconota orizzontali a confronto.
    rows: lista di (etichetta, valore, valore_massimo, colore_barra, colore_testo)
    La parte mancante rispetto al massimo e' tratteggiata con la differenza in euro.
    """
    bar_h = 84
    lab_gap = 16
    row_h = 30 * 0.72 + lab_gap + bar_h
    gap = 40
    tot = len(rows) * row_h + (len(rows) - 1) * gap
    y = top + (bottom - top - tot) / 2
    out = ""
    for i, (lab, v, vmax, col, tcol) in enumerate(rows):
        out += svg_text(M, y + 30 * 0.72, lab, 30, 700, AZURE_LIGHT, spacing=2, tid=f"{sid}-barra-{i + 1}-etichetta")
        by = y + 30 * 0.72 + lab_gap
        bw = CW * v / vmax
        if v < vmax:
            out += rect(M + bw - 20, by + 2, CW - bw + 18, bar_h - 4, "none",
                        extra=f' stroke="{DIM}" stroke-width="3" stroke-dasharray="10 8" rx="16" opacity="0.8"')
            out += svg_text(M + bw + (CW - bw) / 2, by + bar_h / 2 + 11, "-" + fmt(vmax - v) + " €",
                            30, 700, DIM, "middle")
        # banconota stilizzata
        out += rect(M, by, bw, bar_h, col, 16)
        out += rect(M + 10, by + 10, bw - 20, bar_h - 20, "none",
                    extra=f' stroke="{NAVY}" stroke-width="2" opacity="0.25" rx="10"')
        out += f'<ellipse cx="{M + bw * 0.62:.1f}" cy="{by + bar_h / 2:.1f}" rx="{bar_h * 0.55:.1f}" ry="{bar_h * 0.3:.1f}" fill="{NAVY}" opacity="0.10"/>'
        out += icon_euro_coin(M + 52, by + bar_h / 2, 28, face=WHITE, edge=AZURE_LIGHT if col != AZURE else SOFT)
        out += svg_text(M + bw - 30, by + bar_h / 2 + 15, fmt(v) + " €", 42, 700, tcol, "end",
                        tid=f"{sid}-barra-{i + 1}-valore")
        y += row_h + gap
    return group(out, gid=f"{sid}-infografica")


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

def _slide(sid, content):
    return group(content, gid=sid)


def _cover_photo_path(photo):
    """Percorso della foto di copertina (assets/covers/) se esiste."""
    if not photo:
        return None
    p = photo if os.path.isabs(photo) else os.path.join(ASSETS, "covers", photo)
    return p if os.path.exists(p) else None


def _photo_image(sid, path):
    """Foto a piena pagina, ritagliata 1080x1350 e incorporata (JPEG base64)."""
    import base64
    import io
    from PIL import Image
    im = Image.open(path).convert("RGB")
    # ritaglio centrato al formato 4:5 e ridimensionamento a 2x per la stampa del PDF
    tw, th = W * 2, H * 2
    r = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88, optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    return group(f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" '
                 f'xlink:href="data:image/jpeg;base64,{data}"/>', gid=f"{sid}-foto")


def build_cover_photo(sid, eyebrow_txt, title, subtitle, illustration_svg, photo=None):
    """Cover: illustrazione piena pagina, gradiente dal basso, testi in basso a sinistra, logo centrato."""
    logo_h = 170
    logo_y = H - 56 - logo_h
    # testo impilato dal basso verso l'alto sopra il logo
    sub_size, title_size = 38, 64
    sub_h = block_height(subtitle, sub_size, 400, CW, 1.3)
    tit_h = block_height(title, title_size, 700, CW, 1.12)
    sub_y = logo_y - 70 - sub_h + sub_size * 0.72
    tit_y = sub_y - sub_size * 0.72 - 36 - tit_h + title_size * 0.72
    eb_y = tit_y - title_size * 0.72 - 44

    photo_path = _cover_photo_path(photo)
    if photo_path:
        photo_layer = _photo_image(sid, photo_path)
        # sul fotografico serve un gradiente piu' pieno per la leggibilita'
        stops = ((0, 0.35), (0.22, 0), (0.42, 0.10), (0.60, 0.82), (0.74, 0.96), (1, 1))
    else:
        photo_layer = illustration_svg
        stops = ((0, 0), (0.40, 0), (0.66, 0.88), (1, 1))
    grad = (f'<defs><linearGradient id="{sid}-cover" x1="0" y1="0" x2="0" y2="1">'
            + "".join(f'<stop offset="{o}" stop-color="{NAVY_DEEP}" stop-opacity="{a}"/>' for o, a in stops)
            + '</linearGradient></defs>'
            + rect(0, 0, W, H, f"url(#{sid}-cover)"))
    t_svg, _, _ = text_block(M, tit_y, title, title_size, 700, WHITE, CW, 1.12, tid=f"{sid}-titolo")
    s_svg, _, _ = text_block(M, sub_y, subtitle, sub_size, 400, SOFT, CW, 1.3, tid=f"{sid}-sottotitolo")
    return _slide(sid, background(sid, glow=(560, 420)) + photo_layer + group(grad, gid=f"{sid}-gradiente")
                  + eyebrow(sid, eyebrow_txt, M, eb_y)
                  + group(t_svg + s_svg, gid=f"{sid}-testi")
                  + svg_logo_center(sid, logo_y, logo_h))


def build_layout_versus(sid, n_tot, idx, eyebrow_txt, quote, answer, body, left, right, source):
    """Due colonne a confronto sotto un blocco di testo."""
    out = background(sid) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    q, qh, _ = text_block(M, y, quote, 46, 700, WHITE, CW, 1.18, tid=f"{sid}-citazione")
    y += qh + 40 + 40 * 0.72
    a, ah, _ = text_block(M, y, answer, 40, 700, AZURE, CW, 1.2, tid=f"{sid}-risposta")
    y += ah + 34 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    out += group(q + a + b, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    # colonne ancorate sopra la fonte
    col_h = 410
    col_y = src_top - 40 - col_h
    col_w = (CW - 30) / 2
    cols = ""
    for i, c in enumerate((left, right)):
        cx = M + i * (col_w + 30)
        fill = NAVY_MID if i == 0 else AZURE
        cols += rect(cx, col_y, col_w, col_h, fill, 26)
        cols += c["icon"](cx + 36, col_y + 34, 84)
        cols += svg_text(cx + 36, col_y + 180, c["label"], 30, 700, WHITE if i else AZURE_LIGHT, spacing=2)
        cols += svg_text(cx + 32, col_y + 276, c["value"], 84, 700, WHITE)
        cap, _, _ = text_block(cx + 36, col_y + 330, c["caption"], 30, 400, WHITE if i else SOFT,
                               col_w - 60, 1.25)
        cols += cap
    vs = circle(W / 2, col_y + 60, 34, NAVY_DEEP) + svg_text(W / 2, col_y + 71, "vs", 30, 700, WHITE, "middle")
    out += group(cols + vs, gid=f"{sid}-infografica") + src
    return _slide(sid, out)


def build_layout_callout(sid, n_tot, idx, eyebrow_txt, title, question, body, infographic_fn,
                         punchline, source):
    """Testo in alto, infografica al centro, box azzurro pieno in basso."""
    out = background(sid, glow=(180, 200)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    t, th, _ = text_block(M, y, title, 46, 700, WHITE, CW, 1.18, tid=f"{sid}-titolo")
    y += th + 34 + 40 * 0.72
    q, qh, _ = text_block(M, y, question, 40, 700, AZURE, CW, 1.2, tid=f"{sid}-domanda")
    y += qh + 32 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    y += bh
    out += group(t + q + b, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    box_h = 150
    box_y = src_top - 36 - box_h
    p, ph, pn = text_block(W / 2, 0, punchline, 38, 700, WHITE, CW - 80, 1.25, anchor="middle")
    p_y = box_y + box_h / 2 - ph / 2 + 38 * 0.72
    p, _, _ = text_block(W / 2, p_y, punchline, 38, 700, WHITE, CW - 80, 1.25, anchor="middle",
                         tid=f"{sid}-punchline", accent=NAVY_DEEP)
    out += group(rect(M, box_y, CW, box_h, AZURE, 24) + p, gid=f"{sid}-callout")
    out += infographic_fn(sid, y + 40, box_y - 40)
    out += src
    return _slide(sid, out)


def build_layout_statement(sid, n_tot, idx, eyebrow_txt, big, big_sub, body, chips, source, illu_fn):
    """Numero enorme in alto che inquadra il tema, illustrazione a destra, testo sotto."""
    out = background(sid, glow=(820, 420)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    out += illu_fn(sid)
    out += group(svg_text(M - 6, 380, big, 150, 700, WHITE, tid=f"{sid}-numero")
                 + svg_text(M, 446, big_sub, 44, 700, AZURE, tid=f"{sid}-numero-sub"),
                 gid=f"{sid}-statement")
    y = 560 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    out += group(b, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    chip_h = 270
    chip_y = src_top - 40 - chip_h
    n = len(chips)
    gap = 20
    cw = (CW - gap * (n - 1)) / n
    ch = ""
    for i, (num, lab) in enumerate(chips):
        cx = M + i * (cw + gap)
        ch += rect(cx, chip_y, cw, chip_h, NAVY_MID, 22) + rect(cx, chip_y, cw, 8, AZURE, 4)
        ch += svg_text(cx + 28, chip_y + 92, num, 58, 700, WHITE)
        lb, _, _ = text_block(cx + 28, chip_y + 146, lab, 30, 400, SOFT, cw - 50, 1.22)
        ch += lb
    out += group(ch, gid=f"{sid}-dati") + src
    return _slide(sid, out)


def build_layout_chart(sid, n_tot, idx, eyebrow_txt, blocks, bars, legend, source):
    """Grafico a barre verticali (monete impilate stilizzate) sotto una sequenza di testi.
    blocks: lista di (testo, size, peso, colore)."""
    out = background(sid, glow=(900, 900)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    parts = ""
    for i, (txt, size, wgt, col) in enumerate(blocks):
        if i:
            y += 26 + size * 0.72
        tb, th, _ = text_block(M, y, txt, size, wgt, col, CW, 1.18 if size > 40 else 1.4,
                               tid=f"{sid}-testo-{i + 1}")
        parts += tb
        y += th
    out += group(parts, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    base_y = src_top - 100
    leg_y = y + 70 + 30 * 0.72
    loss_y = leg_y + 70
    top_y = loss_y + 26
    full_h = base_y - top_y
    n = len(bars)
    bw = 170
    gap = (CW - n * bw) / (n - 1)
    vmax = max(v for _, v in bars)
    ch = svg_text(M, leg_y, legend, 30, 400, SOFT, italic=True, tid=f"{sid}-legenda")
    ch += (f'<defs><linearGradient id="{sid}-bar" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{AZURE_LIGHT}"/><stop offset="1" stop-color="{AZURE}"/>'
           f'</linearGradient></defs>')
    for i, (lab, v) in enumerate(bars):
        bx = M + i * (bw + gap)
        h = full_h * v / vmax
        by = base_y - h
        if v < vmax:
            ch += rect(bx + 2, top_y + 2, bw - 4, full_h - h + 10, "none",
                       extra=f' stroke="{DIM}" stroke-width="3" stroke-dasharray="10 8" opacity="0.75" rx="14"')
            ch += svg_text(bx + bw / 2, loss_y, "-" + fmt(vmax - v) + " €", 32, 700, DIM, "middle")
        fill = SOFT if i == 0 else f"url(#{sid}-bar)"
        ch += rect(bx, by, bw, h, fill, 14)
        k = by + 84
        while k < base_y - 12:
            ch += (f'<line x1="{bx + 16}" y1="{k:.1f}" x2="{bx + bw - 16}" y2="{k:.1f}" '
                   f'stroke="{NAVY}" stroke-width="2" opacity="0.16"/>')
            k += 26
        ch += svg_text(bx + bw / 2, by + 52, fmt(v) + " €", 36, 700, NAVY_DEEP if i == 0 else WHITE, "middle")
        ch += svg_text(bx + bw / 2, base_y + 52, lab, 32, 700, SOFT if i == 0 else AZURE_LIGHT, "middle")
    ch += f'<line x1="{M}" y1="{base_y}" x2="{W - M}" y2="{base_y}" stroke="{DIM}" stroke-width="3" opacity="0.6"/>'
    out += group(ch, gid=f"{sid}-grafico") + src
    return _slide(sid, out)


def build_layout_scenarios(sid, n_tot, idx, eyebrow_txt, quote, answer, body, lead, items, closing):
    """Elenco con icone in cerchio + frase di chiusura in fondo."""
    out = background(sid, glow=(160, 1100)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    q, qh, _ = text_block(M, y, quote, 52, 700, WHITE, CW, 1.15, tid=f"{sid}-citazione")
    y += qh + 34 + 40 * 0.72
    a, ah, _ = text_block(M, y, answer, 40, 700, AZURE, CW, 1.2, tid=f"{sid}-risposta")
    y += ah + 30 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    y += bh + 50 + BODY * 0.72
    l, lh_, _ = text_block(M, y, lead, BODY, 700, WHITE, CW, 1.42, tid=f"{sid}-lead")
    y += lh_ + 36
    out += group(q + a + b + l, gid=f"{sid}-testi")
    # chiusura in fondo, ancorata
    cl_size = 34
    cl_h = block_height(closing, cl_size, 400, CW - 60, 1.35, italic=True)
    cl_box_h = cl_h + 70
    cl_y = 1300 - cl_box_h
    c_svg, _, _ = text_block(M + 36, cl_y + 35 + cl_size * 0.72, closing, cl_size, 400, WHITE, CW - 60, 1.35,
                             italic=True, tid=f"{sid}-chiusura")
    out += group(rect(M, cl_y, 8, cl_box_h, AZURE) + c_svg, gid=f"{sid}-chiusura-g")
    # elementi distribuiti tra y e cl_y, collegati da una linea (percorso in 3 passi)
    avail = cl_y - 40 - y
    row_h = avail / len(items)
    rows = (f'<line x1="{M + 70}" y1="{y + row_h / 2:.1f}" x2="{M + 70}" y2="{y + avail - row_h / 2:.1f}" '
            f'stroke="{AZURE}" stroke-width="6" stroke-dasharray="4 12" stroke-linecap="round"/>')
    for i, (icon_fn, num, txt) in enumerate(items):
        ry = y + i * row_h
        cy = ry + row_h / 2
        rows += rect(M + 70, ry + 10, CW - 70, row_h - 20, NAVY_MID, 22)
        rows += circle(M + 70, cy, 60, NAVY)
        rows += circle(M + 70, cy, 50, AZURE)
        rows += icon_fn(M + 70 - 29, cy - 29, 58, WHITE, AZURE)
        tx = M + 160
        tw_ = CW - 190
        t_, th_, tn = text_block(tx, 0, txt, BODY, 700, WHITE, tw_, 1.22)
        blk = 30 * 0.72 + 16 + th_
        top = cy - blk / 2
        rows += svg_text(tx, top + 30 * 0.72, num, 30, 700, AZURE_LIGHT, spacing=2)
        t_, _, _ = text_block(tx, top + 30 * 0.72 + 16 + BODY * 0.72, txt, BODY, 700, WHITE, tw_, 1.22,
                              tid=f"{sid}-voce-{i + 1}")
        rows += t_
    out += group(rows, gid=f"{sid}-elenco")
    return _slide(sid, out)


def build_layout_grid(sid, n_tot, idx, eyebrow_txt, lead, question, cards, closing, stat, stat_txt, source):
    """Griglia 2x2 di card con icona, domanda sopra, dato in fondo."""
    out = background(sid, glow=(900, 700)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    l, lh_, _ = text_block(M, y, lead, BODY, 400, SOFT, CW, 1.4, tid=f"{sid}-lead")
    y += lh_ + 30 + 46 * 0.72
    q, qh, _ = text_block(M, y, question, 46, 700, WHITE, CW, 1.18, tid=f"{sid}-domanda")
    y += qh + 44
    out += group(l + q, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    # dato in fondo
    st_h = 170 if not callable(stat) else max(170, block_height(stat_txt, 32, 700, CW - 204, 1.25) + 70)
    st_y = src_top - 36 - st_h
    st = rect(M, st_y, CW, st_h, AZURE, 24)
    if callable(stat):
        st += circle(M + 40 + 50, st_y + st_h / 2, 50, WHITE)
        st += stat(M + 40 + 22, st_y + st_h / 2 - 28, 56, AZURE, WHITE)
        sw = 40 + 100 + 34
    else:
        st += svg_text(M + 40, st_y + st_h / 2 + 34, stat, 96, 700, WHITE)
        sw = text_width(stat, 96, 700) + 40 + 34
    s_t, s_h, _ = text_block(M + sw, 0, stat_txt, 32, 700, WHITE, CW - sw - 30, 1.25)
    s_t, _, _ = text_block(M + sw, st_y + st_h / 2 - s_h / 2 + 32 * 0.72, stat_txt, 32, 700, WHITE,
                           CW - sw - 30, 1.25, tid=f"{sid}-dato-testo")
    out += group(st + s_t, gid=f"{sid}-dato")
    # chiusura sopra il dato
    cl_h = block_height(closing, BODY, 400, CW, 1.4)
    cl_y = st_y - 40 - cl_h + BODY * 0.72
    c_svg, _, _ = text_block(M, cl_y, closing, BODY, 400, SOFT, CW, 1.4, tid=f"{sid}-chiusura")
    out += group(c_svg, gid=f"{sid}-chiusura-g")
    # griglia
    g_top = y
    g_bot = cl_y - BODY * 0.72 - 44
    gap = 22
    cw = (CW - gap) / 2
    chh = (g_bot - g_top - gap) / 2
    g = ""
    for i, (icon_fn, lab) in enumerate(cards):
        cx = M + (i % 2) * (cw + gap)
        cy = g_top + (i // 2) * (chh + gap)
        g += rect(cx, cy, cw, chh, NAVY_MID, 22)
        isz = min(66, chh - 70)
        tx = cx + 28 + isz + 22
        tw_ = cw - (tx - cx) - 18
        g += icon_fn(cx + 28, cy + (chh - isz) / 2, isz, AZURE_LIGHT, NAVY_MID)
        tb, th_, _ = text_block(tx, 0, lab, BODY, 700, WHITE, tw_, 1.2)
        tb, _, _ = text_block(tx, cy + chh / 2 - th_ / 2 + BODY * 0.72, lab, BODY, 700,
                              WHITE, tw_, 1.2, tid=f"{sid}-card-{i + 1}")
        g += tb
    out += group(g, gid=f"{sid}-griglia") + src
    return _slide(sid, out)


def build_layout_cta(sid, lead, headline, body, question, contacts, illu_fn, logo_h=175):
    """CTA: logo grande in alto, headline, corpo, domanda con illustrazione, contatti."""
    out = background(sid, glow=(540, 260))
    out += svg_logo_center(sid, 64, logo_h)
    y = 64 + logo_h + 62
    parts = ""
    if lead:
        y += BODY * 0.72
        l, lh_, _ = text_block(W / 2, y, lead, BODY, 400, SOFT, CW, 1.4, anchor="middle", tid=f"{sid}-lead")
        parts += l
        y += lh_ + 26
    hs = 46 if (lead or body) else 54
    y += hs * 0.72
    h, hh, _ = text_block(W / 2, y, headline, hs, 700, WHITE, CW, 1.16, anchor="middle", tid=f"{sid}-headline")
    parts += h
    y += hh
    if body:
        y += 28 + BODY * 0.72
        b, bh, _ = text_block(W / 2, y, body, BODY, 400, SOFT, CW, 1.4, anchor="middle", tid=f"{sid}-corpo")
        parts += b
        y += bh
    y += 56
    out += group(parts, gid=f"{sid}-testi")
    # contatti ancorati in basso
    c_rows = len(contacts)
    row = 62
    c_y0 = 1300 - c_rows * row
    cs = ""
    for i, (icon_fn, txt) in enumerate(contacts):
        ry = c_y0 + i * row
        cs += circle(M + 24, ry + 22, 24, AZURE)
        cs += icon_fn(M + 24 - 14, ry + 22 - 14, 28, WHITE)
        cs += svg_text(M + 70, ry + 34, txt, 34, 700 if i == 0 else 400, WHITE)
    out += group(cs, gid=f"{sid}-contatti")
    # box domanda con illustrazione tra testo e contatti
    box_y = y
    box_h = c_y0 - 40 - box_y
    ill_w = min(300, box_h - 60)
    q_w = CW - ill_w - 110
    qs = 42 if (lead or body) else 50
    qb, qh, _ = text_block(0, 0, question, qs, 700, WHITE, q_w, 1.18)
    qb, _, _ = text_block(M + 44, box_y + box_h / 2 - qh / 2 + qs * 0.72, question, qs, 700, WHITE, q_w, 1.18,
                          tid=f"{sid}-domanda")
    out += group(rect(M, box_y, CW, box_h, AZURE, 26) + qb
                 + illu_fn(sid, W - M - ill_w - 36, box_y + (box_h - ill_w) / 2, ill_w),
                 gid=f"{sid}-box-domanda")
    return _slide(sid, out)


def build_layout_people(sid, n_tot, idx, eyebrow_txt, title, body, big, big_sub, filled, total, areas, source):
    """Pittogramma a persone (es. 4 su 10) + testo + aree analizzate."""
    out = background(sid, glow=(860, 760)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    t, th, _ = text_block(M, y, title, 50, 700, WHITE, CW, 1.15, tid=f"{sid}-titolo")
    y += th + 34 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    y += bh
    out += group(t + b, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    # aree in basso
    pill_h = 84
    gap = 16
    cols = 2
    rows_ = math.ceil(len(areas) / cols)
    pill_y = src_top - 40 - rows_ * pill_h - (rows_ - 1) * gap
    pw = (CW - gap * (cols - 1)) / cols
    ar = ""
    for i, (icon_fn, lab) in enumerate(areas):
        px = M + (i % cols) * (pw + gap)
        py = pill_y + (i // cols) * (pill_h + gap)
        ar += rect(px, py, pw, pill_h, NAVY_MID, 20)
        ar += icon_fn(px + 26, py + (pill_h - 46) / 2, 46, AZURE_LIGHT, NAVY_MID)
        ar += svg_text(px + 94, py + pill_h / 2 + 12, lab, BODY, 700, WHITE, tid=f"{sid}-area-{i + 1}")
    out += group(ar, gid=f"{sid}-aree")
    # pannello dato: numero grande + pittogramma
    p_top = y + 50
    p_bot = pill_y - 36
    ph = p_bot - p_top
    pan = rect(M, p_top, CW, ph, NAVY_MID, 26)
    pan += svg_text(M + 44, p_top + ph / 2 + 8, big, 110, 700, WHITE, tid=f"{sid}-numero")
    # 10 figure su due righe, a destra
    cols = 5
    rows = math.ceil(total / cols)
    fig = min(60, (ph - 60) / rows - 12)
    fx0 = W - M - 36 - cols * fig - (cols - 1) * 12
    sub, sh, _ = text_block(M + 48, p_top + ph / 2 + 66, big_sub, 32, 700, AZURE_LIGHT,
                            fx0 - 36 - (M + 48), 1.2, tid=f"{sid}-numero-sub")
    pan += sub
    fy0 = p_top + (ph - rows * fig - (rows - 1) * 14) / 2
    for k in range(total):
        cx = fx0 + (k % cols) * (fig + 12)
        cy = fy0 + (k // cols) * (fig + 14)
        pan += icon_person(cx, cy, fig, AZURE if k < filled else NAVY_LINE)
    out += group(pan, gid=f"{sid}-infografica") + src
    return _slide(sid, out)


def build_layout_doc(sid, n_tot, idx, eyebrow_txt, title, body, doc_title, questions, source):
    """Documento stilizzato con l'elenco delle domande standard (es. DIP)."""
    out = background(sid, glow=(200, 900)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    t, th, _ = text_block(M, y, title, 50, 700, WHITE, CW, 1.15, tid=f"{sid}-titolo")
    y += th + 34 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    y += bh
    out += group(t + b, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    d_top = y + 48
    d_bot = src_top - 36
    dh = d_bot - d_top
    dx = M + 30
    dw = CW - 60
    doc = rect(dx + 14, d_top + 14, dw, dh, NAVY_DEEP, 20, extra=' opacity="0.6"')
    doc += rect(dx, d_top, dw, dh, SOFT, 20)
    doc += rect(dx, d_top, dw, 76, AZURE, 20) + rect(dx, d_top + 40, dw, 36, AZURE)
    doc += svg_text(dx + 30, d_top + 50, doc_title, 30, 700, WHITE, spacing=2)
    n = len(questions)
    cols = 2
    rows = math.ceil(n / cols)
    ry0 = d_top + 76 + 22
    rh = (dh - 76 - 44) / rows
    cw_ = (dw - 60 - 20) / cols
    for i, q in enumerate(questions):
        cx = dx + 30 + (i // rows) * (cw_ + 20)
        cy = ry0 + (i % rows) * rh
        doc += icon_question(cx, cy + (rh - 38) / 2, 38, AZURE, SOFT)
        qb, qh, _ = text_block(cx + 52, 0, q, 30, 700, NAVY_DEEP, cw_ - 56, 1.12)
        qb, _, _ = text_block(cx + 52, cy + rh / 2 - qh / 2 + 30 * 0.72, q, 30, 700, NAVY_DEEP, cw_ - 56, 1.12,
                              tid=f"{sid}-domanda-{i + 1}")
        doc += qb
    out += group(doc, gid=f"{sid}-documento") + src
    return _slide(sid, out)


def build_layout_donts(sid, n_tot, idx, eyebrow_txt, title, items, big, big_txt, source):
    """Elenco di cose che non facciamo + box con un dato di garanzia."""
    out = background(sid, glow=(880, 300)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    t, th, _ = text_block(M, y, title, 56, 700, WHITE, CW, 1.12, tid=f"{sid}-titolo")
    y += th + 56
    out += group(t, gid=f"{sid}-testi")
    src, src_top = source_block(sid, source)
    box_h = 250
    box_y = src_top - 36 - box_h
    bx = rect(M, box_y, CW, box_h, AZURE, 26)
    bx += svg_text(M + 44, box_y + 118, big, 96, 700, WHITE, tid=f"{sid}-numero")
    bt, bth, _ = text_block(M + 44, box_y + 176, big_txt, 32, 700, WHITE, CW - 88, 1.25, tid=f"{sid}-numero-testo")
    bx += bt
    out += group(bx, gid=f"{sid}-garanzia")
    avail = box_y - 40 - y
    row_h = avail / len(items)
    li = ""
    for i, txt in enumerate(items):
        ry = y + i * row_h
        cy = ry + row_h / 2
        li += icon_x(M, cy - 34, 68, AZURE, NAVY)
        tb, tbh, _ = text_block(M + 100, 0, txt, 38, 700, WHITE, CW - 110, 1.2)
        tb, _, _ = text_block(M + 100, cy - tbh / 2 + 38 * 0.72, txt, 38, 700, WHITE, CW - 110, 1.2,
                              tid=f"{sid}-voce-{i + 1}")
        li += tb
        if i < len(items) - 1:
            li += f'<line x1="{M + 100}" y1="{ry + row_h:.1f}" x2="{W - M}" y2="{ry + row_h:.1f}" stroke="{NAVY_LINE}" stroke-width="2"/>'
    out += group(li, gid=f"{sid}-elenco") + src
    return _slide(sid, out)


def build_layout_timeline(sid, n_tot, idx, eyebrow_txt, title, body, events, closing):
    """Linea del tempo verticale con eventi di vita + chiusura in box."""
    out = background(sid, glow=(180, 700)) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    y = 262
    t, th, _ = text_block(M, y, title, 56, 700, WHITE, CW, 1.12, tid=f"{sid}-titolo")
    y += th + 34 + BODY * 0.72
    b, bh, _ = text_block(M, y, body, BODY, 400, SOFT, CW, 1.42, tid=f"{sid}-corpo")
    y += bh + 44
    out += group(t + b, gid=f"{sid}-testi")
    cl_h = block_height(closing, 36, 700, CW - 80, 1.25)
    box_h = cl_h + 76
    box_y = 1300 - box_h
    c_svg, _, _ = text_block(W / 2, box_y + 38 + 36 * 0.72, closing, 36, 700, WHITE, CW - 80, 1.25,
                             anchor="middle", tid=f"{sid}-chiusura")
    out += group(rect(M, box_y, CW, box_h, AZURE, 24) + c_svg, gid=f"{sid}-chiusura-g")
    avail = box_y - 36 - y
    n = len(events)
    step = avail / n
    lx = M + 44
    tl = (f'<line x1="{lx}" y1="{y + step / 2:.1f}" x2="{lx}" y2="{y + avail - step / 2:.1f}" '
          f'stroke="{AZURE}" stroke-width="6" stroke-linecap="round"/>')
    for i, (icon_fn, lab) in enumerate(events):
        cy = y + i * step + step / 2
        r = min(40, step / 2 - 6)
        tl += circle(lx, cy, r + 8, NAVY) + circle(lx, cy, r, AZURE)
        tl += icon_fn(lx - r * 0.55, cy - r * 0.55, r * 1.1, WHITE, AZURE)
        tl += rect(lx + r + 30, cy - step / 2 + 8, W - M - (lx + r + 30), step - 16, NAVY_MID, 18)
        tl += svg_text(lx + r + 58, cy + 12, lab, BODY, 700, WHITE, tid=f"{sid}-evento-{i + 1}")
    out += group(tl, gid=f"{sid}-timeline")
    return _slide(sid, out)


# --------------------------------------------------------------------------
# Layout "leggeri": una slide = un concetto. Blocchi impilati e centrati
# in verticale, testi grandi, molta aria.
# --------------------------------------------------------------------------

def blk_title(text, size=64, color=WHITE, lh=1.12):
    h = block_height(text, size, 700, CW, lh)

    def draw(sid, i, y):
        svg, _, _ = text_block(M, y + size * 0.72, text, size, 700, color, CW, lh, tid=f"{sid}-titolo-{i}")
        return svg
    return h, draw


def blk_text(text, size=40, color=SOFT, weight=400, lh=1.36):
    h = block_height(text, size, weight, CW, lh)

    def draw(sid, i, y):
        svg, _, _ = text_block(M, y + size * 0.72, text, size, weight, color, CW, lh, tid=f"{sid}-testo-{i}")
        return svg
    return h, draw


def blk_hero(icon_fn, r=100):
    """Icona grande in un cerchio azzurro con alone."""
    h = 2 * r + 24

    def draw(sid, i, y):
        cx, cy = M + r + 12, y + r + 12
        return group(circle(cx, cy, r + 12, AZURE, extra=' opacity="0.25"') + circle(cx, cy, r, AZURE)
                     + icon_fn(cx - r * 0.56, cy - r * 0.56, r * 1.12, WHITE, AZURE), gid=f"{sid}-icona-{i}")
    return h, draw


def blk_cards(cards, card_h=180):
    """Griglia 2x2 di card con icona ed etichetta."""
    gap = 22
    rows = math.ceil(len(cards) / 2)
    h = rows * card_h + (rows - 1) * gap

    def draw(sid, i, y):
        cw = (CW - gap) / 2
        g = ""
        for k, (icon_fn, lab) in enumerate(cards):
            cx = M + (k % 2) * (cw + gap)
            cy = y + (k // 2) * (card_h + gap)
            g += rect(cx, cy, cw, card_h, NAVY_MID, 24)
            isz = 70
            g += icon_fn(cx + 30, cy + (card_h - isz) / 2, isz, AZURE_LIGHT, NAVY_MID)
            tx = cx + 30 + isz + 24
            tw_ = cw - (tx - cx) - 20
            tb, th_, _ = text_block(tx, 0, lab, 38, 700, WHITE, tw_, 1.18)
            tb, _, _ = text_block(tx, cy + card_h / 2 - th_ / 2 + 38 * 0.72, lab, 38, 700, WHITE, tw_, 1.18,
                                  tid=f"{sid}-card-{k + 1}")
            g += tb
        return group(g, gid=f"{sid}-griglia")
    return h, draw


def blk_rows(items, row_h=150):
    """Righe con icona in cerchio, collegate da una linea tratteggiata."""
    gap = 18
    h = len(items) * row_h + (len(items) - 1) * gap

    def draw(sid, i, y):
        r = 54
        cx = M + r + 8
        g = (f'<line x1="{cx}" y1="{y + row_h / 2:.1f}" x2="{cx}" y2="{y + h - row_h / 2:.1f}" '
             f'stroke="{AZURE}" stroke-width="6" stroke-dasharray="4 12" stroke-linecap="round"/>')
        for k, (icon_fn, lab) in enumerate(items):
            ry = y + k * (row_h + gap)
            cy = ry + row_h / 2
            g += rect(cx, ry, W - M - cx, row_h, NAVY_MID, 24)
            g += circle(cx, cy, r + 8, NAVY) + circle(cx, cy, r, AZURE)
            g += icon_fn(cx - r * 0.58, cy - r * 0.58, r * 1.16, WHITE, AZURE)
            tx = cx + r + 34
            tb, th_, _ = text_block(tx, 0, lab, 42, 700, WHITE, W - M - tx - 24, 1.18)
            tb, _, _ = text_block(tx, cy - th_ / 2 + 42 * 0.72, lab, 42, 700, WHITE, W - M - tx - 24, 1.18,
                                  tid=f"{sid}-voce-{k + 1}")
            g += tb
        return group(g, gid=f"{sid}-elenco")
    return h, draw


def blk_pills(areas, pill_h=124):
    gap = 18
    rows = math.ceil(len(areas) / 2)
    h = rows * pill_h + (rows - 1) * gap

    def draw(sid, i, y):
        pw = (CW - gap) / 2
        g = ""
        for k, (icon_fn, lab) in enumerate(areas):
            px = M + (k % 2) * (pw + gap)
            py = y + (k // 2) * (pill_h + gap)
            g += rect(px, py, pw, pill_h, NAVY_MID, 22)
            g += circle(px + 62, py + pill_h / 2, 38, AZURE)
            g += icon_fn(px + 62 - 23, py + pill_h / 2 - 23, 46, WHITE, AZURE)
            g += svg_text(px + 122, py + pill_h / 2 + 15, lab, 42, 700, WHITE, tid=f"{sid}-area-{k + 1}")
        return group(g, gid=f"{sid}-aree")
    return h, draw


def blk_pictogram(big, sub, filled, total, panel_h=400):
    def draw(sid, i, y):
        pan = rect(M, y, CW, panel_h, NAVY_MID, 28)
        pan += svg_text(M + 48, y + panel_h / 2 + 10, big, 124, 700, WHITE, tid=f"{sid}-numero")
        cols = 5
        rows = math.ceil(total / cols)
        fig = 58
        fx0 = W - M - 40 - cols * fig - (cols - 1) * 12
        fy0 = y + (panel_h - rows * fig - (rows - 1) * 16) / 2
        for k in range(total):
            pan += icon_person(fx0 + (k % cols) * (fig + 12), fy0 + (k // cols) * (fig + 16), fig,
                               AZURE if k < filled else NAVY_LINE)
        sb, _, _ = text_block(M + 52, y + panel_h / 2 + 70, sub, 32, 700, AZURE_LIGHT, fx0 - 40 - (M + 52), 1.2,
                              tid=f"{sid}-numero-sub")
        return group(pan + sb, gid=f"{sid}-infografica")
    return panel_h, draw


def blk_bigstat(big, text, size=170):
    th = block_height(text, 42, 700, CW, 1.25)
    desc = size * 0.26 + 30                      # spazio per le discendenti (la "g" di giorni)
    h = size * 0.74 + desc + th

    def draw(sid, i, y):
        svg = svg_text(M - 6, y + size * 0.74, big, size, 700, AZURE, tid=f"{sid}-numero")
        tb, _, _ = text_block(M, y + size * 0.74 + desc + 42 * 0.72, text, 42, 700, WHITE, CW, 1.25,
                              tid=f"{sid}-numero-testo")
        return group(svg + tb, gid=f"{sid}-dato")
    return h, draw


def blk_doc(title, questions, row_h=100):
    rows = math.ceil(len(questions) / 2)
    head = 80
    h = head + 26 + rows * row_h + 20

    def draw(sid, i, y):
        dx, dw = M, CW
        d = rect(dx + 14, y + 14, dw, h, NAVY_DEEP, 22, extra=' opacity="0.6"')
        d += rect(dx, y, dw, h, SOFT, 22) + rect(dx, y, dw, head, AZURE, 22) + rect(dx, y + head - 30, dw, 30, AZURE)
        d += svg_text(dx + 34, y + head / 2 + 11, title, 30, 700, WHITE, spacing=2)
        cw_ = (dw - 68 - 24) / 2
        for k, q in enumerate(questions):
            cx = dx + 34 + (k // rows) * (cw_ + 24)
            cy = y + head + 26 + (k % rows) * row_h
            d += icon_question(cx, cy + (row_h - 42) / 2, 42, AZURE, SOFT)
            qb, qh, _ = text_block(cx + 56, 0, q, 32, 700, NAVY_DEEP, cw_ - 60, 1.12)
            qb, _, _ = text_block(cx + 56, cy + row_h / 2 - qh / 2 + 32 * 0.72, q, 32, 700, NAVY_DEEP, cw_ - 60,
                                  1.12, tid=f"{sid}-domanda-{k + 1}")
            d += qb
        return group(d, gid=f"{sid}-documento")
    return h, draw


def blk_donts(items, row_h=176):
    h = len(items) * row_h

    def draw(sid, i, y):
        g = ""
        for k, txt in enumerate(items):
            ry = y + k * row_h
            cy = ry + row_h / 2
            g += icon_x(M, cy - 42, 84, AZURE, NAVY)
            tb, th_, _ = text_block(M + 118, 0, txt, 46, 700, WHITE, CW - 124, 1.18)
            tb, _, _ = text_block(M + 118, cy - th_ / 2 + 46 * 0.72, txt, 46, 700, WHITE, CW - 124, 1.18,
                                  tid=f"{sid}-voce-{k + 1}")
            g += tb
            if k < len(items) - 1:
                g += (f'<line x1="{M + 118}" y1="{ry + row_h:.1f}" x2="{W - M}" y2="{ry + row_h:.1f}" '
                      f'stroke="{NAVY_LINE}" stroke-width="2"/>')
        return group(g, gid=f"{sid}-elenco")
    return h, draw


def blk_timeline(events, step=120):
    h = len(events) * step

    def draw(sid, i, y):
        lx = M + 48
        r = 44
        g = (f'<line x1="{lx}" y1="{y + step / 2:.1f}" x2="{lx}" y2="{y + h - step / 2:.1f}" '
             f'stroke="{AZURE}" stroke-width="6" stroke-linecap="round"/>')
        for k, (icon_fn, lab) in enumerate(events):
            cy = y + k * step + step / 2
            g += circle(lx, cy, r + 8, NAVY) + circle(lx, cy, r, AZURE)
            g += icon_fn(lx - r * 0.56, cy - r * 0.56, r * 1.12, WHITE, AZURE)
            g += rect(lx + r + 26, cy - step / 2 + 9, W - M - (lx + r + 26), step - 18, NAVY_MID, 20)
            g += svg_text(lx + r + 56, cy + 14, lab, 40, 700, WHITE, tid=f"{sid}-evento-{k + 1}")
        return group(g, gid=f"{sid}-timeline")
    return h, draw


def build_stack(sid, eyebrow_txt, blocks, source=None, gap=52, glow=(880, 300), top=210, bias=0.42):
    """Slide leggera: blocchi impilati e centrati tra l'intestazione e la fonte."""
    out = background(sid, glow=glow) + eyebrow(sid, eyebrow_txt) + svg_logo_topright(sid)
    if source:
        src, src_top = source_block(sid, source)
        bottom = src_top - 44
    else:
        src, bottom = "", 1290
    gaps = gap if isinstance(gap, (list, tuple)) else [gap] * (len(blocks) - 1)
    total = sum(h for h, _ in blocks) + sum(gaps[:len(blocks) - 1])
    avail = bottom - top
    assert total <= avail + 1, f"{sid}: contenuto troppo alto ({total:.0f} > {avail:.0f})"
    y = top + (avail - total) * bias
    body = ""
    for i, (h, draw) in enumerate(blocks):
        body += draw(sid, i + 1, y)
        y += h + (gaps[i] if i < len(blocks) - 1 else 0)
    return _slide(sid, out + group(body, gid=f"{sid}-contenuto") + src)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'version="1.1" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')


def slide_svg(content):
    return SVG_HEAD.format(w=W, h=H) + content + "</svg>"


def slides_to_multi_svg(slides, gap=120):
    """Tutte le slide affiancate in orizzontale, una per gruppo <g id="slide-NN">."""
    n = len(slides)
    tw = n * W + (n - 1) * gap
    body = ""
    for i, s in enumerate(slides):
        body += f'<g id="tavola-{i + 1:02d}" transform="translate({i * (W + gap)} 0)">{s}</g>'
    return SVG_HEAD.format(w=tw, h=H) + body + "</svg>"


def _for_render(svg, pt=False):
    """Copia per cairo: family 'Raleway' (cairosvg legge solo il primo nome)."""
    svg = re.sub(r'font-family="Raleway-[A-Za-z]+, Raleway"', 'font-family="Raleway"', svg)
    if pt:
        svg = svg.replace(f'width="{W}" height="{H}"', f'width="{W}pt" height="{H}pt"', 1)
    return svg


def deliver(slides, slug, out_dir=None, crucial_dir=None, preview=True):
    """Genera PDF multipagina + SVG multi-tavola (+ PNG di controllo)."""
    import cairosvg
    from pypdf import PdfWriter, PdfReader
    import io

    out_dir = out_dir or os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f"Madonia_Carosello_{slug}.pdf")
    svg_path = os.path.join(out_dir, f"Madonia_Carosello_{slug}.svg")

    writer = PdfWriter()
    prev_dir = os.path.join(out_dir, f"preview_{slug}")
    if preview:
        os.makedirs(prev_dir, exist_ok=True)
    for i, s in enumerate(slides, 1):
        doc = slide_svg(s)
        buf = io.BytesIO()
        cairosvg.svg2pdf(bytestring=_for_render(doc, pt=True).encode(), write_to=buf)
        buf.seek(0)
        for p in PdfReader(buf).pages:
            writer.add_page(p)
        if preview:
            cairosvg.svg2png(bytestring=_for_render(doc).encode(),
                             write_to=os.path.join(prev_dir, f"slide_{i:02d}.png"))
    writer.add_metadata({"/Title": f"Madonia Carosello {slug}", "/Author": "Agenzia Cav. Madonia"})
    with open(pdf_path, "wb") as f:
        writer.write(f)

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(slides_to_multi_svg(slides))

    if crucial_dir and os.path.isdir(os.path.dirname(crucial_dir.rstrip("/"))):
        os.makedirs(crucial_dir, exist_ok=True)
        shutil.copy2(pdf_path, crucial_dir)
        shutil.copy2(svg_path, crucial_dir)
    return pdf_path, svg_path, prev_dir
