"""
Carosello Makhymo 01 · Red flag in ufficio che ignori da mesi. 🚩

Testo del cliente, impaginato senza modifiche (una red flag per slide):
  🚩 La sedia che scricchiola «da un po'» (da marzo).
  🚩 Il post-it sulla stampante: «NON usare il cassetto 2».
  🚩 Il PC che ci mette dieci minuti ad accendersi, «ma poi va».
  🚩 La sala riunioni che si prenota su un foglio A4 appeso alla porta.
  🚩 Il cavo HDMI che funziona solo se lo tieni con la mano.
  Aggiungi la tua nei commenti. Quella più votata la risolviamo noi, sul serio. 👇

Le emoji sono ridisegnate come vettori: 🚩 = bandierina rossa, 👇 = freccia a mano.
Nessun dato statistico: nessuna fonte da citare.
"""

import math

from mky_svg import *  # noqa: F401,F403

SLUG = "RedFlag"
N_FLAGS = 5

INK = "#22376B"          # penna blu delle scritte a mano
POSTIT = "#F7D64A"
POSTIT_SHADE = "#E6BF2E"
PAPER = "#FBFAF6"
WOOD = "#C99A68"
WOOD_DARK = "#B3834F"
PLASTIC = "#F3F5F9"
PLASTIC_2 = "#E3E8EF"
LINE = "#C9D0DC"

slides = []


# ==========================================================================
# Illustrazioni
# ==========================================================================

def planted_flag(x, top, h):
    """Bandierina piantata nella carta kraft, con ombra alla base."""
    base = top + h
    shadow = f'<ellipse cx="{x + 10 * h / 100:.1f}" cy="{base - 2:.1f}" rx="{h * 0.13:.1f}" ' \
             f'ry="{h * 0.028:.1f}" fill="#6B4E30" opacity="0.30"/>'
    return shadow + place(red_flag(h), x, top)


def printer():
    """Multifunzione da ufficio, due cassetti. Box locale 640 x 600."""
    o = f'<ellipse cx="320" cy="592" rx="310" ry="16" fill="#000000" opacity="0.28"/>'
    # alimentatore originali con fogli
    o += rect(180, 2, 280, 22, WHITE, rx=3, extra=f' stroke="{LINE}" stroke-width="2"')
    o += rect(150, 16, 340, 36, "#DCE1E9", rx=10)
    o += path("M70,44 H570 L592,112 H48 Z", "#E9EDF3")
    # corpo
    o += rect(28, 100, 584, 474, PLASTIC, rx=26)
    o += path("M560,100 H586 A26,26 0 0 1 612,126 V548 A26,26 0 0 1 586,574 H560 Z", "#DEE3EB")
    # pannello comandi
    o += rect(388, 124, 196, 72, CARD_LIGHT, rx=12)
    o += rect(400, 136, 104, 48, "#3C64B4", rx=6)
    o += rect(412, 148, 64, 7, WHITE, rx=3, extra=' opacity="0.85"')
    o += rect(412, 163, 44, 7, WHITE, rx=3, extra=' opacity="0.55"')
    o += circle(530, 160, 11, RED) + circle(561, 160, 8, STEEL)
    # uscita fogli
    o += rect(66, 138, 296, 36, CARD_DARK, rx=10)
    o += rect(96, 156, 236, 46, WHITE, rx=2)
    for i, w in enumerate((170, 196, 120)):
        o += rect(116, 168 + i * 11, w, 4, "#C9D0DC", rx=2)
    o += rect(28, 232, 584, 4, SOFT)
    # cassetti
    for i, y in enumerate((258, 414)):
        o += rect(58, y, 524, 138, PLASTIC_2, rx=14, extra=f' stroke="{LINE}" stroke-width="3"')
        o += rect(250, y + 52, 140, 22, STEEL, rx=11)
        o += circle(112, y + 69, 24, SOFT)
        o += label(112, y + 79, str(i + 1), 28, "semi", "#6B7890", "middle")
    # piedini
    o += rect(70, 572, 64, 14, STEEL, rx=5) + rect(506, 572, 64, 14, STEEL, rx=5)
    return o


def postit(w=270, h=230, lines=("NON usare", "il cassetto 2")):
    """Post-it giallo scritto a mano. Box locale w x h, origine in alto a sinistra."""
    o = rect(7, 9, w, h, "#000000", rx=3, extra=' opacity="0.25"')
    o += path(f"M0,0 H{w} V{h - 46} L{w - 46},{h} H0 Z", POSTIT)
    o += rect(0, 0, w, 44, POSTIT_SHADE, extra=' opacity="0.45"')
    o += path(f"M{w},{h - 46} L{w - 46},{h} C{w - 40},{h - 18} {w - 30},{h - 36} {w},{h - 46} Z",
              "#D9AE22")
    size = 58
    y = 108
    for i, t in enumerate(lines):
        svg, tw_ = hand_path(t, w / 2 - 4, y + i * 66, size, INK, anchor="middle")
        assert tw_ < w - 24, f"scritta post-it troppo larga: {t}"
        o += svg
        if i == 0:
            # sottolineatura rossa sotto NON
            nw = hand_path("NON", 0, 0, size)[1]
            x0 = w / 2 - 4 - tw_ / 2
            o += path(f"M{x0 - 2:.1f},{y + 12:.1f} C{x0 + nw * 0.4:.1f},{y + 8:.1f} "
                      f"{x0 + nw * 0.7:.1f},{y + 17:.1f} {x0 + nw + 6:.1f},{y + 10:.1f}",
                      "none", stroke(RED, 5))
    return o


def monitor():
    """Monitor in avvio: spinner e barra di caricamento ferma. Box locale 620 x 460."""
    o = f'<ellipse cx="310" cy="452" rx="190" ry="12" fill="#000000" opacity="0.28"/>'
    o += rect(270, 380, 80, 58, STEEL)
    o += rect(178, 430, 264, 22, SOFT, rx=11)
    o += rect(0, 0, 620, 392, CARD_DARK, rx=22, extra=f' stroke="#2A3B5E" stroke-width="3"')
    o += rect(20, 20, 580, 330, CARD_LIGHT, rx=10)
    o += circle(310, 372, 5.5, RED)
    # spinner: 8 punti a opacita' decrescente
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        o += circle(310 + 46 * math.cos(a), 150 + 46 * math.sin(a), 11 - i * 0.7, WHITE,
                    f' opacity="{1 - i * 0.11:.2f}"')
    # barra di avanzamento al 12%
    o += rect(160, 250, 300, 18, CARD_DARK, rx=9)
    o += rect(160, 250, 36, 18, RED, rx=9)
    return o


def clock(r=145):
    """Orologio con i primi dieci minuti evidenziati in rosso. Centro in (0,0)."""
    o = circle(6, 8, r, "#000000", ' opacity="0.28"')
    o += circle(0, 0, r, WHITE, f' stroke="{NAVY}" stroke-width="12"')
    rw = r - 26
    a1 = math.radians(-90 + 60)
    o += path(f"M0,0 L0,{-rw} A{rw},{rw} 0 0 1 {rw * math.cos(a1):.1f},{rw * math.sin(a1):.1f} Z",
              RED, ' opacity="0.92"')
    for i in range(12):
        a = math.radians(i * 30 - 90)
        r0 = r - 30 if i % 3 == 0 else r - 22
        o += path(f"M{r0 * math.cos(a):.1f},{r0 * math.sin(a):.1f} "
                  f"L{(r - 12) * math.cos(a):.1f},{(r - 12) * math.sin(a):.1f}",
                  "none", stroke(NAVY, 6 if i % 3 == 0 else 3.5))
    am = math.radians(60 - 90)
    ah = math.radians(5 - 90)
    o += path(f"M0,0 L{(r - 42) * math.cos(am):.1f},{(r - 42) * math.sin(am):.1f}", "none",
              stroke(NAVY, 9))
    o += path(f"M0,0 L{(r - 72) * math.cos(ah):.1f},{(r - 72) * math.sin(ah):.1f}", "none",
              stroke(NAVY, 12))
    o += circle(0, 0, 12, NAVY) + circle(0, 0, 5, RED)
    return o


def meeting_icon():
    """Iconcina sala riunioni per la targhetta. Box 60 x 34."""
    o = rect(12, 18, 36, 8, WHITE, rx=4)
    for cx in (14, 30, 46):
        o += circle(cx, 8, 6, WHITE)
    return o


def a4_sheet(w=236):
    """Foglio A4 di prenotazione, con tabella e nomi scarabocchiati. Box w x w*1.414."""
    h = w * 1.414
    o = rect(5, 7, w, h, "#000000", extra=' opacity="0.22"')
    o += rect(0, 0, w, h, PAPER)
    title, tw_ = hand_path("SALA RIUNIONI", w / 2, 44, 34, INK, anchor="middle")
    o += title
    o += path(f"M{w / 2 - tw_ / 2:.1f},54 L{w / 2 + tw_ / 2:.1f},52", "none", stroke(INK, 2.5))
    top, rows, rh = 74, 6, 42
    for i in range(rows + 1):
        y = top + i * rh
        o += path(f"M16,{y} L{w - 16},{y}", "none", stroke("#9AA6BA", 1.6))
    o += path(f"M72,{top} L72,{top + rows * rh}", "none", stroke("#9AA6BA", 1.6))
    times = ("9:00", "10:00", "11:00", "14:00", "15:00", "16:00")
    for i, t in enumerate(times):
        o += hand_path(t, 22, top + i * rh + 29, 24, INK)[0]
    # nomi scarabocchiati (non leggibili), una prenotazione cancellata in rosso
    scrib = {0: (0.75, INK), 1: (0.55, INK), 2: (0.85, INK), 4: (0.6, INK), 5: (0.7, INK)}
    for i, (k, col) in scrib.items():
        y = top + i * rh + 22
        x0, x1 = 86, 86 + (w - 110) * k
        d = f"M{x0},{y}"
        n = int((x1 - x0) / 9)
        for j in range(1, n + 1):
            d += f" L{x0 + j * 9:.1f},{y + (-6 if j % 2 else 5):.1f}"
        o += path(d, "none", stroke(col, 2.4))
    y = top + 1 * rh + 21
    o += path(f"M82,{y + 6} L{w - 30},{y - 8}", "none", stroke(RED, 3.2))
    y = top + 3 * rh + 22
    o += path(f"M88,{y} C120,{y - 14} 150,{y + 12} {w - 26},{y - 4}", "none", stroke(RED, 3.2))
    return o, h


def door():
    """Porta della sala riunioni con targhetta e foglio A4. Box locale 330 x 960."""
    o = rect(0, 0, 330, 960, "#E6EAF0", rx=6)
    o += rect(18, 18, 294, 942, WOOD)
    for x in (58, 104, 150, 205, 262):
        o += path(f"M{x},30 C{x + 6},300 {x - 5},620 {x + 3},950", "none",
                  stroke(WOOD_DARK, 2, ' opacity="0.35"'))
    o += rect(18, 18, 20, 942, "#000000", extra=' opacity="0.10"')
    o += rect(18, 884, 294, 58, SOFT, extra=' opacity="0.85"')           # battiscopa metallico
    # maniglia
    o += circle(60, 650, 17, SOFT) + rect(52, 640, 92, 18, "#EEF1F5", rx=9)
    o += rect(52, 650, 92, 8, STEEL, rx=4)
    # targhetta
    o += rect(105, 36, 120, 44, CARD_DARK, rx=8) + place(meeting_icon(), 135, 41)
    # foglio A4 con nastro adesivo
    sheet, sh = a4_sheet(236)
    o += place(sheet, 47, 270, rotate=-2.5)
    o += place(rect(-34, -11, 68, 22, "#F3EBD2", extra=' opacity="0.8"'), 58, 270, rotate=-32)
    o += place(rect(-34, -11, 68, 22, "#F3EBD2", extra=' opacity="0.8"'), 272, 260, rotate=28)
    return o


def hdmi_plug():
    """Spina HDMI con cavo e segni di 'contatto che va e viene'. Box locale ~ 360 x 130."""
    o = path("M150,62 C220,60 270,80 360,70", "none", stroke(CARD_DARK, 26))
    o += rect(70, 28, 110, 70, CARD_DARK, rx=12) + rect(78, 36, 94, 10, "#2A3B5E", rx=5)
    o += path("M8,38 H74 V90 H26 L8,74 Z", "#C9D0DC")
    o += path("M18,48 H64 V78 H30 L18,68 Z", "#6B7890")
    for i, (a, l) in enumerate(((-150, 24), (180, 28), (150, 24))):
        r = math.radians(a)
        x0, y0 = 2 + 16 * math.cos(r), 64 + 26 * math.sin(r)
        o += path(f"M{x0:.1f},{y0:.1f} L{x0 + l * math.cos(r):.1f},{y0 + l * math.sin(r):.1f}",
                  "none", stroke(WHITE, 5))
    return o


def comment_bar():
    """Campo commento finto: avatar, bandierina 'digitata', cursore, invio. Box 900 x 120."""
    o = rect(4, 8, 900, 120, "#000000", rx=60, extra=' opacity="0.25"')
    o += rect(0, 0, 900, 120, WHITE, rx=60)
    o += circle(66, 60, 38, SOFT)
    o += circle(66, 50, 13, NAVY) + path("M44,86 C46,66 86,66 88,86 Z", NAVY)
    o += place(red_flag(70), 122, 25)
    o += rect(200, 32, 5, 56, RED, rx=2.5)
    # invio (aeroplanino)
    o += path("M800,40 L860,60 L800,80 L810,60 Z", NAVY)
    o += path("M810,60 L842,60", "none", stroke(WHITE, 3))
    return o


# ==========================================================================
# Slide
# ==========================================================================

# 01 · COVER --------------------------------------------------------------------
sid = "slide-01"
out = background(sid, "bg_cover.jpg")
out += logo(sid, W / 2, 130, 460)
t, _ = paragraph(sid, "titolo", 108, 330,
                 ["==Red flag==", "in ufficio che", "ignori ==da mesi.=="], 112, "semi", lh=1.16)
out += group(t, gid=f"{sid}-testi")
flags = ""
for x, top, h in ((80, 970, 180), (240, 925, 290), (830, 1050, 150), (545, 810, 480), (420, 1120, 140)):
    flags += planted_flag(x, top, h)
out += group(flags, gid=f"{sid}-bandierine")
slides.append(slide(sid, out))

# 02 · LA SEDIA (testo + foto, freccia) --------------------------------------------
sid = "slide-02"
out = background(sid) + flag_progress(sid, 1)
t, bottom = paragraph(sid, "testo", M, 230,
                      ["La sedia che", "scricchiola «da un po’»", "==(da marzo).=="], 72, "semi")
out += group(t, gid=f"{sid}-testi")
out += hand_arrow(sid, (600, 440), (830, 390), (1010, 540), (885, 640))
out += photo_slot(sid, M, 570, 760, 600, "FOTO · la sedia che scricchiola")
slides.append(slide(sid, out))

# 03 · IL POST-IT (testo + illustrazione centrata) ------------------------------------
sid = "slide-03"
out = background(sid) + flag_progress(sid, 2)
t, bottom = paragraph(sid, "testo", M, 230,
                      ["Il post-it sulla", "stampante: ==«NON usare==", "==il cassetto 2».=="],
                      72, "semi")
out += group(t, gid=f"{sid}-testi")
ill = place(printer(), 220, 580, scale=0.96)
ill += place(postit(), 548, 930, rotate=-6)
out += group(ill, gid=f"{sid}-illustrazione")
slides.append(slide(sid, out))

# 04 · IL PC (card scura con barra rossa + monitor e orologio) ------------------------
sid = "slide-04"
out = background(sid) + flag_progress(sid, 3)
card_top = 230
t, bottom = paragraph(sid, "testo", M + 56, card_top + 50,
                      ["Il PC che ci mette dieci", "minuti ad accendersi,", "==«ma poi va».=="],
                      64, "semi", max_width=CW - 96)
card_h = bottom + 48 - card_top
card = rect(M, card_top, CW, card_h, CARD_DARK, rx=6) + rect(M, card_top, 12, card_h, RED)
out += group(card, gid=f"{sid}-card") + group(t, gid=f"{sid}-testi")
ill = place(monitor(), 120, 660)
ill += place(clock(145), 812, 1010)
out += group(ill, gid=f"{sid}-illustrazione")
slides.append(slide(sid, out))

# 05 · LA SALA RIUNIONI (testo a sinistra + porta a destra) ---------------------------
sid = "slide-05"
out = background(sid) + flag_progress(sid, 4)
t, bottom = paragraph(sid, "testo", M, 497,
                      ["La sala riunioni", "che si prenota su", "un ==foglio A4==", "==appeso alla porta.=="],
                      56, "semi", max_width=530)
out += group(t, gid=f"{sid}-testi")
out += hand_arrow(sid, (462, 668), (530, 680), (600, 668), (646, 648), head=22)
out += group(place(door(), 660, 230), gid=f"{sid}-illustrazione")
slides.append(slide(sid, out))

# 06 · IL CAVO HDMI (fascia rossa + foto ruotata) --------------------------------------
sid = "slide-06"
out = background(sid) + flag_progress(sid, 5)
band_top = 230
t, bottom = paragraph(sid, "testo", M, band_top + 56,
                      ["Il cavo HDMI che", "funziona solo se lo", "tieni con la mano."], 70, "semi")
band_h = bottom + 52 - band_top
out += group(rect(0, band_top, W, band_h, RED), gid=f"{sid}-fascia") + group(t, gid=f"{sid}-testi")
ph_top = band_top + band_h + 70
out += photo_slot(sid, 120, ph_top, 840, 1165 - ph_top - 20, "FOTO · la mano che tiene fermo il cavo HDMI",
                  rotate=-3)
out += group(place(hdmi_plug(), 754, ph_top - 69, scale=1.35, rotate=-25), gid=f"{sid}-spina")
slides.append(slide(sid, out))

# 07 · CTA ------------------------------------------------------------------------
sid = "slide-07"
out = background(sid, "bg_contatti.jpg")
out += logo(sid, W / 2, 130, 400)
t1, b1 = paragraph(sid, "invito", M, 300, ["Aggiungi la tua", "nei commenti."], 96, "semi", lh=1.16)
t2, b2 = paragraph(sid, "promessa", M, b1 + 60,
                   ["==Quella più votata la==", "==risolviamo noi, sul serio.=="], 60, "med", lh=1.22)
out += group(t1 + t2, gid=f"{sid}-testi")
bar_top = 930
out += hand_arrow(sid, (850, b2 - 150), (1010, b2 - 60), (905, b2 + 60), (880, bar_top - 26),
                  name="freccia-giu")
out += group(place(comment_bar(), M, bar_top), gid=f"{sid}-commento")
out += contacts(sid)
slides.append(slide(sid, out))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG)
    print(svg_path)
    print(prev)
