"""
Carosello Makhymo 01 · Red flag in ufficio che ignori da mesi. 🚩

Versione con foto (v3): ogni slide e' una foto a tutta pagina con un fumetto bianco
che indica il soggetto, come i post prodotto di riferimento. I colori Makhymo stanno
nella foto (parete navy #122549, bandierina rossa) e nel fumetto (testo navy, parti
chiave in rosso #C6183D, 🚩 davanti al titolo).

Foto: immagini fotorealistiche generate con AI (Higgsfield, GPT Image 2.5, 1792x2240),
progetto Higgsfield «Makhymo · Red flag in ufficio». Sono in assets/photos/redflag/.
Non sono scatti reali di un ufficio Makhymo.

Testo del cliente, impaginato senza modifiche (una red flag per slide):
  🚩 La sedia che scricchiola «da un po'» (da marzo).
  🚩 Il post-it sulla stampante: «NON usare il cassetto 2».
  🚩 Il PC che ci mette dieci minuti ad accendersi, «ma poi va».
  🚩 La sala riunioni che si prenota su un foglio A4 appeso alla porta.
  🚩 Il cavo HDMI che funziona solo se lo tieni con la mano.
  CTA (riscritta su richiesta, sostituisce «Aggiungi la tua nei commenti. Quella più
  votata la risolviamo noi, sul serio. 👇»):
  Qual è la red flag nel tuo ufficio? Scrivila nei commenti

Nel fumetto il soggetto fa da titolo e il resto della frase da testo: la frase resta identica.
La 🚩 e' ridisegnata come vettore (bandierina davanti al titolo).
Nessun dato statistico: nessuna fonte da citare.
"""

from mky_svg import *  # noqa: F401,F403

SLUG = "RedFlag"
PHOTOS = "photos/redflag"

slides = []


def shade_top(sid, h=260, opacity=0.45):
    """Leggera sfumatura navy in alto: logo e bandierine restano leggibili su qualsiasi foto."""
    g = f"{sid}-sfumatura"
    return group(f'<defs><linearGradient id="{g}-grad" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="#0A1428" stop-opacity="{opacity}"/>'
                 f'<stop offset="1" stop-color="#0A1428" stop-opacity="0"/></linearGradient></defs>'
                 + rect(0, 0, W, h, f"url(#{g}-grad)"), gid=g)


def photo_slide(sid, photo, idx=None):
    out = photo_background(sid, f"{PHOTOS}/{photo}") + shade_top(sid)
    if idx:
        out += flag_progress(sid, idx)
    return out


# 01 · COVER --------------------------------------------------------------------
sid = "slide-01"
out = photo_slide(sid, "01_bandierina.jpg") + logo(sid, W / 2, 130, 460)
bub, _ = speech_bubble(sid, M, 270, CW, ["**Red flag** in ufficio", "che ignori da mesi."], [],
                       tip=(398, 650), at=440, title_size=84, flag=False)
out += bub
slides.append(slide(sid, out))

# 02 · LA SEDIA ------------------------------------------------------------------
sid = "slide-02"
out = photo_slide(sid, "02_sedia.jpg", 1)
bub, _ = speech_bubble(sid, M, 215, 640, ["La sedia"],
                       ["che scricchiola «da un po’»", "**(da marzo).**"], tip=(520, 612), at=450)
out += bub
slides.append(slide(sid, out))

# 03 · IL POST-IT ------------------------------------------------------------------
sid = "slide-03"
out = photo_slide(sid, "03_stampante.jpg", 2)
bub, _ = speech_bubble(sid, M, 200, 650, ["Il post-it sulla", "stampante:"],
                       ["**«NON usare il cassetto 2».**"], tip=(612, 530), at=540, title_size=52)
out += bub
slides.append(slide(sid, out))

# 04 · IL PC ---------------------------------------------------------------------
sid = "slide-04"
out = photo_slide(sid, "04_pc.jpg", 3)
bub, _ = speech_bubble(sid, M, 215, 660, ["Il PC"],
                       ["che ci mette dieci minuti ad", "accendersi, **«ma poi va».**"],
                       tip=(560, 650), at=500)
out += bub
slides.append(slide(sid, out))

# 05 · LA SALA RIUNIONI ----------------------------------------------------------------
sid = "slide-05"
out = photo_slide(sid, "05_sala_riunioni.jpg", 4)
bub, _ = speech_bubble(sid, M, 390, 530, ["La sala riunioni"],
                       ["che si prenota su un", "**foglio A4 appeso**", "**alla porta.**"],
                       tip=(722, 520), side="right", at=500, title_size=48, pad=40)
out += bub
slides.append(slide(sid, out))

# 06 · IL CAVO HDMI -------------------------------------------------------------------
sid = "slide-06"
out = photo_slide(sid, "06_hdmi.jpg", 5)
bub, _ = speech_bubble(sid, M, 215, 670, ["Il cavo HDMI"],
                       ["che funziona **solo se lo tieni**", "**con la mano.**"], tip=(600, 660), at=520)
out += bub
slides.append(slide(sid, out))

# 07 · CTA ------------------------------------------------------------------------
sid = "slide-07"
out = photo_slide(sid, "07_cta.jpg") + logo(sid, W / 2, 130, 380)
bub, _ = speech_bubble(sid, M, 240, 680, ["Qual è la red flag", "nel tuo ufficio?"],
                       ["**Scrivila nei commenti**"],
                       tip=(600, 640), at=560, title_size=66, body_size=44, flag=False)
out += bub
out += contacts(sid, y=1290, size=26)
slides.append(slide(sid, out))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG)
    print(svg_path)
    print(prev)
