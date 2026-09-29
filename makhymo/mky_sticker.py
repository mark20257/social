"""
Stile 'ritaglio' per i caroselli Makhymo (dal riferimento a sticker, nei colori Makhymo).

  - fondo pieno a carta stropicciata, navy e rosso alternati
  - cerchi concentrici chiari sullo sfondo (il codice a barre 'a bersaglio' del 1952)
  - titolone in maiuscolo Lexend Deca Black, parole chiave in kraft
  - foto in bianco e nero scontornata con bordo bianco da adesivo
  - nastro adesivo con la data, striscia di carta strappata in basso con la didascalia/fonte

Tutti i testi restano testo vivo (un <text> per paragrafo); foto, carta e striscia sono raster.
"""

import base64
import math
import os
from xml.sax.saxutils import escape

from mky_svg import (ASSETS, FONT_WEIGHT, H, M, NAVY, RED, W, WHITE, _font_attrs, circle, contacts,
                     group, logo, path, rect, slide, stroke, text_width)

ACCENT = "#F2CF9B"        # kraft chiaro: le parole chiave nei titoli
TAPE = "#E6E0D3"
CAPTION = "#3A4660"
BG = {"navy": ("bg_navy_sticker.jpg", NAVY), "red": ("bg_red_sticker.jpg", RED)}

_cache = {}


def _data(rel, mime):
    if rel not in _cache:
        with open(os.path.join(ASSETS, rel), "rb") as f:
            _cache[rel] = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    return _cache[rel]


def paper(sid, tone):
    name, col = BG[tone]
    return group(rect(0, 0, W, H, col)
                 + f'<image x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none" '
                   f'xlink:href="{_data(name, "image/jpeg")}"/>', gid=f"{sid}-sfondo")


def rings(sid, cx, cy, r0=260, step=86, n=4, width=34, opacity=0.07):
    """Cerchi concentrici sullo sfondo, come il codice 'a bersaglio' di Woodland e Silver."""
    out = "".join(circle(cx, cy, r0 + i * step, "none",
                         f' stroke="{WHITE}" stroke-width="{width}" opacity="{opacity}"')
                  for i in range(n))
    return group(out, gid=f"{sid}-cerchi")


def _spaced_width(t, size, role, ls):
    return text_width(t, size, role) + ls * max(len(t) - 1, 0)


def fit_size(lines, role="black", max_w=900, max_size=104, ls_em=-0.02):
    plain = [l.replace("==", "") for l in lines]
    size = max_size
    while size > 40 and any(_spaced_width(p, size, role, ls_em * size) > max_w for p in plain):
        size -= 1
    return size


def headline(sid, lines, top, size=None, role="black", lh=0.98, fill=WHITE, accent=ACCENT,
             cx=W / 2, ls_em=-0.02, max_w=900):
    """
    Titolone centrato, un solo <text>. ==parola== = colore accento.
    Ritorna (svg, bottom, size). top = cima delle maiuscole della prima riga.
    """
    size = size or fit_size(lines, role, max_w, ls_em=ls_em)
    ls = ls_em * size
    cap = 0.71 * size
    tspans = []
    for i, line in enumerate(lines):
        runs, on = [], False
        for part in line.split("=="):
            if part:
                runs.append((part, on))
            on = not on
        plain = "".join(t for t, _ in runs)
        lw = _spaced_width(plain, size, role, ls)
        assert lw <= max_w + 0.5, f"titolo troppo largo ({lw:.0f}): {plain}"
        x = cx - lw / 2
        y = top + cap + i * size * lh
        inner = "".join(f'<tspan fill="{accent}">{escape(t)}</tspan>' if a else escape(t) for t, a in runs)
        tspans.append(f'<tspan x="{x:.1f}" y="{y:.1f}">{inner}</tspan>')
    svg = (f'<text id="{sid}-titolo" font-size="{size}" {_font_attrs(role)} fill="{fill}" '
           f'letter-spacing="{ls:.2f}">' + "".join(tspans) + "</text>")
    bottom = top + cap + (len(lines) - 1) * size * lh
    return svg, bottom, size


def subline(sid, lines, top, size=31, role="med", fill=WHITE, opacity=0.92, lh=1.36, cx=W / 2,
            max_w=900):
    """Testo breve centrato sotto il titolo, un solo <text>. Ritorna (svg, bottom)."""
    tspans = []
    for i, line in enumerate(lines):
        lw = text_width(line, size, role)
        assert lw <= max_w + 0.5, f"riga troppo lunga ({lw:.0f}): {line}"
        y = top + 0.72 * size + i * size * lh
        tspans.append(f'<tspan x="{cx:.1f}" y="{y:.1f}">{escape(line)}</tspan>')
    svg = (f'<text id="{sid}-testo" font-size="{size}" {_font_attrs(role)} fill="{fill}" '
           f'opacity="{opacity}" text-anchor="middle">' + "".join(tspans) + "</text>")
    return svg, top + 0.72 * size + (len(lines) - 1) * size * lh


def sticker(sid, rel, cx, bottom, max_w, max_h, name="foto"):
    """Foto scontornata (PNG con bordo bianco) appoggiata con il fondo su `bottom`."""
    from PIL import Image
    im = Image.open(os.path.join(ASSETS, rel))
    k = min(max_w / im.width, max_h / im.height)
    w, h = im.width * k, im.height * k
    x, y = cx - w / 2, bottom - h
    img = (f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
           f'xlink:href="{_data(rel, "image/png")}"/>')
    return group(img, gid=f"{sid}-{name}"), (x, y, w, h)


def torn_strip(sid, top=H - 190):
    return group(f'<image x="0" y="{top}" width="{W}" height="190" '
                 f'xlink:href="{_data("strip_torn.png", "image/png")}"/>', gid=f"{sid}-striscia")


def caption(sid, text, y=1296, size=23):
    return (f'<text id="{sid}-didascalia" x="{W / 2:.1f}" y="{y}" font-size="{size}" '
            f'{_font_attrs("reg")} fill="{CAPTION}" text-anchor="middle">~ {escape(text)} ~</text>')


def tape(sid, cx, cy, label, color, rotate=-8, size=34, pad=38, h=66):
    """Nastro di carta con la scritta, bordi corti sfrangiati."""
    tw = text_width(label, size, "black") + 1.5 * (len(label) - 1)
    w = tw + 2 * pad
    x0, y0, x1, y1 = -w / 2, -h / 2, w / 2, h / 2
    right = " ".join(f"L{x1 - (7 if i % 2 else 0):.1f},{y0 + h * i / 8:.1f}" for i in range(9))
    left = " ".join(f"L{x0 + (7 if i % 2 else 0):.1f},{y1 - h * i / 8:.1f}" for i in range(9))
    d = f"M{x0:.1f},{y0:.1f} {right} {left} Z"
    body = (path(d, "#000000", ' opacity="0.22" transform="translate(4 6)"')
            + path(d, TAPE, ' opacity="0.96"')
            + f'<text x="0" y="{0.36 * size:.1f}" font-size="{size}" {_font_attrs("black")} '
              f'fill="{color}" text-anchor="middle" letter-spacing="1.5">{escape(label)}</text>')
    return group(body, gid=f"{sid}-nastro", transform=f"translate({cx:.1f} {cy:.1f}) rotate({rotate})")


def bullseye(sid, cx, cy, r, rings_n=5, name="bersaglio"):
    """Il codice 'a bersaglio' del brevetto: anelli neri concentrici su disco bianco, a sticker."""
    out = circle(cx + 10, cy + 14, r + 22, "#000000", ' opacity="0.28"')
    out += circle(cx, cy, r + 22, WHITE)
    out += circle(cx, cy, r, "#F4F4F1")
    widths = [0.06, 0.12, 0.05, 0.09, 0.05, 0.1, 0.04]
    rr = r * 0.94
    for i in range(rings_n * 2):
        wdt = widths[i % len(widths)] * r
        if i % 2 == 0:
            out += circle(cx, cy, rr - wdt / 2, "none", f' stroke="#141414" stroke-width="{wdt:.1f}"')
        rr -= wdt
        if rr < r * 0.12:
            break
    out += circle(cx, cy, r * 0.1, "#141414")
    return group(out, gid=f"{sid}-{name}")


def barcode_label(sid, x, y, w, h, rotate=0, seed=3, name="etichetta"):
    """Etichetta adesiva con codice a barre (decorativa), bianca con bordo e ombra."""
    import random
    rnd = random.Random(seed)
    bars = ""
    bx, x_end = 0.1 * w, 0.9 * w
    while bx < x_end:
        bw = rnd.choice((0.008, 0.008, 0.016, 0.024)) * w
        if bx + bw > x_end:
            break
        bars += rect(bx, 0.16 * h, bw, 0.62 * h, "#141414")
        bx += bw + rnd.choice((0.008, 0.012, 0.02)) * w
    body = (rect(8, 12, w, h, "#000000", rx=10, extra=' opacity="0.25"')
            + rect(0, 0, w, h, WHITE, rx=10) + bars)
    return group(body, gid=f"{sid}-{name}",
                 transform=f"translate({x:.1f} {y:.1f}) rotate({rotate} {w / 2:.1f} {h / 2:.1f})")


def checkboxes(sid, n, total, y=122, size=28, gap=14):
    """Caselle di spunta centrate: le prime n spuntate (kraft con segno navy), le altre vuote."""
    tot_w = total * size + (total - 1) * gap
    x = W / 2 - tot_w / 2
    out = ""
    for i in range(total):
        bx = x + i * (size + gap)
        if i < n:
            out += rect(bx, y, size, size, ACCENT, rx=6)
            out += path(f"M{bx + size * 0.24:.1f},{y + size * 0.52:.1f} L{bx + size * 0.43:.1f},"
                        f"{y + size * 0.72:.1f} L{bx + size * 0.78:.1f},{y + size * 0.3:.1f}",
                        "none", stroke(NAVY, 4))
        else:
            out += rect(bx + 1.5, y + 1.5, size - 3, size - 3, "none", rx=6,
                        extra=f' stroke="{WHITE}" stroke-width="3" opacity="0.55"')
    return group(out, gid=f"{sid}-caselle")


def wrap(text, size, role="med", max_w=860):
    """A capo automatico con regola anti-orfano."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and text_width(t, size, role) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    if len(lines) > 1 and " " not in lines[-1]:
        prev = lines[-2].rsplit(" ", 1)
        if len(prev) == 2 and text_width(prev[1] + " " + lines[-1], size, role) <= max_w:
            lines[-2], lines[-1] = prev[0], prev[1] + " " + lines[-1]
    return lines


def lib(series, name):
    """Ritaglio gia' pronto di un'altra serie, da riusare senza generare nulla:
    story(..., lib("postazione", "04_sedia"), ...). Catalogo: assets/photos/libreria.jpg."""
    rel = f"photos/{series}/cut/{name}.png"
    if not os.path.exists(os.path.join(ASSETS, rel)):
        raise FileNotFoundError(rel)
    return rel


def story(sid, tone, tape_txt, head, sub, photo=None, cap="", ring=(860, 300), tape_at=(0.70, 0.22),
          tape_rot=-8, photo_w=800, show_logo=True, extra=None, cta=False, photo_dir="",
          progress=None, head_top=168, head_max=104, progress_y=122, sub_size=31):
    """
    Slide completa in stile ritaglio: carta, cerchi, logo, titolone, testo, foto a sticker,
    striscia strappata con fonte (o contatti se cta), nastro sulla foto.
    progress=(n, totale) aggiunge le caselle di spunta sotto il logo.
    """
    tone_col = NAVY if tone == "navy" else RED
    out = paper(sid, tone) + rings(sid, *ring)
    if show_logo:
        out += logo(sid, W / 2, 62, 250)
    if progress:
        out += checkboxes(sid, *progress, y=progress_y)
    t, hb, _ = headline(sid, head, head_top, size=fit_size(head, max_size=head_max))
    lines = wrap(sub, sub_size) if isinstance(sub, str) else sub  # lista = righe spezzate a mano
    s_svg, sb = subline(sid, lines, hb + 44, size=sub_size) if sub else ("", hb)
    out += group(t + s_svg, gid=f"{sid}-testi")
    box = None
    if photo:
        top = sb + 56
        # "photos/..." = ritaglio preso dalla libreria di un'altra serie (vedi lib())
        rel = f"{photo_dir}/{photo}" if photo_dir and not photo.startswith("photos/") else photo
        st, box = sticker(sid, rel, W / 2, 1262, photo_w, 1262 - top)
        out += st
    if extra:
        out += extra(sb)
    out += torn_strip(sid)
    out += contacts(sid, y=1298, color=CAPTION, size=24) if cta else caption(sid, cap)
    if box and tape_txt:
        x, y, w, h = box
        tx = min(max(x + w * tape_at[0], 250), W - 250)
        ty = y + h * tape_at[1]
        out += tape(sid, tx, ty, tape_txt, tone_col, rotate=tape_rot)
    return slide(sid, out)
