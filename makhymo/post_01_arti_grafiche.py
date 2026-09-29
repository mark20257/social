"""
Post singolo Makhymo · Arti grafiche in azienda: quando produrre internamente e quando
affidarsi a un partner

Post di supporto all'articolo del blog «Stampa digitale professionale ad Asti: Xerox Beyond
CMYK» (makhymo.it/blog/stampa-digitale-professionale-ad-asti-xerox-beyond-cmyk/). L'area Arti
grafiche fornisce sistemi Xerox di produzione a tipografie, centri stampa e reparti stampa
interni alle aziende: il post aiuta a capire quando portare la produzione in casa e quando
conviene ancora un partner esterno.

Stile 'ritaglio' (mky_sticker.py) in un'immagine sola: domanda, aggancio Beyond CMYK, due righe
sfalsate (in azienda / con un partner) con i casi in cui ciascuna conviene, contatti sulla
striscia.

Fatti (verificati il 29/09/2026):
  - Xerox Beyond CMYK: oro, argento, fluorescenti, strati di bianco e trasparente oltre alla
    quadricromia. Fonte: Xerox, «Beyond CMYK Color with Xerox CMYK Plus Solutions».
  - Makhymo: sistemi Xerox di produzione, supporti speciali e applicazioni Beyond CMYK per
    tipografie, centri stampa e reparti stampa interni. Fonte: makhymo.it, area Arti grafiche.

Foto: generazioni AI (Higgsfield, GPT Image 2.5) con quattro oggetti per immagine, divise da
make_stickers.py (assets/photos/artigrafiche/).
"""

from mky_sticker import *  # noqa: F401,F403
from mky_sticker import _font_attrs
from mky_svg import contacts, deliver, logo, path, slide, stroke, text_width

SLUG = "Post_ArtiGrafiche"
PH = "photos/artigrafiche/cut"
SID = "post"
SIZE, LH, MARK, GAP = 27, 46, 22, 16


def check(x, y, s=MARK):
    """Spunta kraft davanti a ogni caso."""
    return path(f"M{x:.1f},{y + s * 0.55:.1f} L{x + s * 0.38:.1f},{y + s * 0.92:.1f} "
                f"L{x + s:.1f},{y + s * 0.12:.1f}", "none", stroke(ACCENT, 5))


def cases(sid, x0, top, items):
    """«Conviene se:» in kraft + elenco con spunte, allineato a sinistra da x0. Ritorna svg."""
    head = (f'<text id="{sid}-conviene" x="{x0:.1f}" y="{top + 0.72 * 26:.1f}" font-size="26" '
            f'{_font_attrs("bold")} fill="{ACCENT}">Conviene se:</text>')
    tx = x0 + MARK + GAP
    top += 50
    for t in items:
        assert tx + text_width(t, SIZE, "med") <= 990.5, f"caso troppo lungo: {t}"
    tspans = "".join(f'<tspan x="{tx:.1f}" y="{top + 0.72 * SIZE + k * LH:.1f}">{escape(t)}</tspan>'
                     for k, t in enumerate(items))
    txt = f'<text id="{sid}-casi" font-size="{SIZE}" {_font_attrs("med")} fill="{WHITE}">{tspans}</text>'
    marks = "".join(check(x0, top + k * LH - 1) for k in range(len(items)))
    return head + marks + txt


def row(i, photo, cx, bottom, max_w, max_h, label, color, rot, x_text, items):
    sid = f"{SID}-riga{i + 1}"
    st, (x, y, w, h) = sticker(sid, f"{PH}/{photo}", cx, bottom, max_w, max_h)
    tp = tape(sid, cx, bottom - 8, label, color, rotate=rot, size=30, h=60)
    txt_top = y + h / 2 - (50 + 2 * LH + SIZE) / 2          # elenco centrato sulla foto
    return group(st + tp + cases(sid, x_text, txt_top, items), gid=sid)


out = paper(SID, "navy") + rings(SID, 900, 330)
out += logo(SID, W / 2, 62, 250)
out += tape(SID, W / 2, 172, "ARTI GRAFICHE", RED, rotate=-3)
head = ["IN AZIENDA", "O DA ==UN PARTNER?=="]
t, hb, _ = headline(SID, head, 240, size=fit_size(head, max_size=100))
s_svg, sb = subline(SID, ["Con Xerox Beyond CMYK anche oro, argento,",
                          "bianco, trasparente e fluo si stampano in azienda."], hb + 40, size=30)
out += group(t + s_svg, gid=f"{SID}-testi")

# riga 1: produzione interna, foto a sinistra e casi a destra
top1 = sb + 70
out += row(0, "04_macchina_produzione.png", 318, top1 + 262, 456, 262, "IN AZIENDA", NAVY, -4,
           580, ["Stampi spesso, tutto l’anno", "Ti servono tempi stretti",
                 "Serie brevi e personalizzate"])
# divisore tratteggiato tra le due righe
yd = top1 + 300
out += group(path(f"M{M},{yd:.0f} L{W - M},{yd:.0f}", "none",
                  f' stroke="{WHITE}" stroke-width="3" stroke-dasharray="4 14" '
                  f'stroke-linecap="round" opacity="0.35"'), gid=f"{SID}-divisore")
# riga 2: partner esterno, casi a sinistra e foto a destra
out += row(1, "05_pacchi_volantini.png", 790, 1126, 390, 1126 - yd - 40, "CON UN PARTNER", RED, 4,
           M, ["Stampi poco e di rado", "Tirature enormi, tutte uguali",
               "Non hai spazio né persone"])
out += torn_strip(SID)
out += contacts(SID, y=1298, color=CAPTION, size=24)

slides = [slide("post-01", out)]

if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, sheet=False)
    print(svg_path)
    print(prev)
