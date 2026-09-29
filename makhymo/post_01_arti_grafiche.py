"""
Post singolo Makhymo · Arti grafiche in azienda: quando produrre internamente e quando
affidarsi a un partner

Stile 'ritaglio' (mky_sticker.py) come i caroselli 02-04, in un'immagine sola: domanda,
regola pratica, due colonne a confronto (in ufficio / con un partner), contatti sulla striscia.

Foto: una sola generazione AI (Higgsfield, GPT Image 2.5) con quattro oggetti su fondo verde,
divisa da make_stickers.py (assets/photos/artigrafiche/). Qui servono multifunzione e stampati;
roll-up e risma restano in libreria.
Nessun dato numerico: il post resta sulla scelta pratica, quindi nessuna fonte da citare.
"""

from mky_sticker import *  # noqa: F401,F403
from mky_sticker import _font_attrs
from mky_svg import contacts, deliver, logo, path, slide, stroke, text_width

SLUG = "Post_ArtiGrafiche"
PH = "photos/artigrafiche/cut"
SID = "post"

COLS = [  # centro colonna, nastro, foto, casi tipici
    (305, "IN UFFICIO", "00_multifunzione.png",
     ["Documenti interni e bozze", "Poche copie, subito", "Correzioni fino all’ultimo"]),
    (775, "CON UN PARTNER", "01_stampati.png",
     ["Cataloghi, brochure, biglietti", "Tirature alte, grande formato", "Carte speciali e finiture"]),
]


def check(x, y, s=22):
    """Spunta kraft davanti a ogni caso."""
    return path(f"M{x:.1f},{y + s * 0.55:.1f} L{x + s * 0.38:.1f},{y + s * 0.92:.1f} "
                f"L{x + s:.1f},{y + s * 0.12:.1f}", "none", stroke(ACCENT, 5))


def column(i, cx, label, photo, items, photo_bottom=902, list_top=954, size=27, lh=48):
    sid = f"{SID}-colonna{i + 1}"
    st, (x, y, w, h) = sticker(sid, f"{PH}/{photo}", cx, photo_bottom, 410, 300)
    tp = tape(sid, cx, photo_bottom - 6, label, NAVY if i == 0 else RED, rotate=-4 if i == 0 else 4,
              size=30, h=60)
    # elenco allineato a sinistra ma centrato come blocco sotto la foto
    mark, gap = 22, 16
    block = mark + gap + max(text_width(t, size, "med") for t in items)
    x0 = cx - block / 2
    tx = x0 + mark + gap
    tspans = "".join(f'<tspan x="{tx:.1f}" y="{list_top + 0.72 * size + k * lh:.1f}">{escape(t)}</tspan>'
                     for k, t in enumerate(items))
    txt = (f'<text id="{sid}-casi" font-size="{size}" {_font_attrs("med")} fill="{WHITE}">'
           f'{tspans}</text>')
    marks = "".join(check(x0, list_top + k * lh - 1) for k in range(len(items)))
    return group(st + tp + marks + txt, gid=sid)


out = paper(SID, "navy") + rings(SID, 900, 330)
out += logo(SID, W / 2, 62, 250)
out += tape(SID, W / 2, 172, "ARTI GRAFICHE", RED, rotate=-3)
t, hb, _ = headline(SID, ["IN UFFICIO", "O ==DA UN PARTNER?=="], 240, size=fit_size(
    ["IN UFFICIO", "O ==DA UN PARTNER?=="], max_size=100))
s_svg, sb = subline(SID, ["Se serve subito e in poche copie, stampalo in ufficio.",
                          "Se deve durare e parlare per l’azienda,",
                          "affidalo a chi lo fa di mestiere."], hb + 40, size=30)
out += group(t + s_svg, gid=f"{SID}-testi")
assert sb + 50 < 902 - 300, f"testo troppo basso: {sb:.0f}"
# divisore tratteggiato tra le due colonne
out += group(path(f"M{W / 2},{sb + 70:.0f} L{W / 2},1120", "none",
                  f' stroke="{WHITE}" stroke-width="3" stroke-dasharray="4 14" '
                  f'stroke-linecap="round" opacity="0.35"'), gid=f"{SID}-divisore")
for i, c in enumerate(COLS):
    out += column(i, *c)
out += torn_strip(SID)
out += contacts(SID, y=1298, color=CAPTION, size=24)

slides = [slide("post-01", out)]

if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, sheet=False)
    print(svg_path)
    print(prev)
