"""
Carosello Makhymo 01 · Red flag in ufficio che ignori da mesi. 🚩

Stile 'a scena' (v2): come i post prodotto di riferimento, ogni slide mostra un
oggetto appoggiato su un tavolo bianco, con una macchia ondulata rossa dietro e un
fumetto bianco con titolo in grassetto e testo. Colori Makhymo: parete navy,
rosso #C6183D, bianco, kraft.

Testo del cliente, impaginato senza modifiche (una red flag per slide):
  🚩 La sedia che scricchiola «da un po'» (da marzo).
  🚩 Il post-it sulla stampante: «NON usare il cassetto 2».
  🚩 Il PC che ci mette dieci minuti ad accendersi, «ma poi va».
  🚩 La sala riunioni che si prenota su un foglio A4 appeso alla porta.
  🚩 Il cavo HDMI che funziona solo se lo tieni con la mano.
  Aggiungi la tua nei commenti. Quella più votata la risolviamo noi, sul serio. 👇

Nel fumetto il soggetto fa da titolo e il resto della frase da testo, come
«Colla in barattolo» + descrizione nel riferimento: la frase resta identica.
Le emoji sono ridisegnate come vettori (🚩 bandierina, 👇 freccia).
Nessun dato statistico: nessuna fonte da citare.
"""

import math

from mky_svg import *  # noqa: F401,F403

SLUG = "RedFlag"

INK = "#22376B"          # penna blu delle scritte a mano
POSTIT = "#F7D64A"
POSTIT_SHADE = "#E6BF2E"
PAPER = "#FBFAF6"
WOOD = "#C99A68"
WOOD_DARK = "#B3834F"
PLASTIC = "#F3F5F9"
PLASTIC_2 = "#E3E8EF"
LINE = "#C9D0DC"
SKIN = "#E9B48C"
SKIN_DARK = "#CF9468"
FABRIC = "#2F3A50"
FABRIC_LIGHT = "#3B4862"
FABRIC_DARK = "#1C2433"
KRAFT = "#E3C7A4"
TAPE = "#D9BC8F"
SURFACE_Y = 1105          # quota d'appoggio degli oggetti sul piano

slides = []


# ==========================================================================
# Illustrazioni
# ==========================================================================

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
    o += circle(60, 690, 17, SOFT) + rect(52, 680, 92, 18, "#EEF1F5", rx=9)
    o += rect(52, 690, 92, 8, STEEL, rx=4)
    # targhetta
    o += rect(105, 36, 120, 44, CARD_DARK, rx=8) + place(meeting_icon(), 135, 41)
    # foglio A4 con nastro adesivo
    sheet, sh = a4_sheet(236)
    o += place(sheet, 47, 270, rotate=-2.5)
    o += place(rect(-34, -11, 68, 22, "#F3EBD2", extra=' opacity="0.8"'), 58, 270, rotate=-32)
    o += place(rect(-34, -11, 68, 22, "#F3EBD2", extra=' opacity="0.8"'), 272, 260, rotate=28)
    return o


def desk_flag(h=440):
    """La 🚩 come bandierina da scrivania: base metallica, asta, drappo. Origine = centro base."""
    o = f'<ellipse cx="0" cy="0" rx="{h * 0.2:.1f}" ry="{h * 0.05:.1f}" fill="#8A93A6"/>'
    o += f'<ellipse cx="0" cy="{-h * 0.018:.1f}" rx="{h * 0.2:.1f}" ry="{h * 0.045:.1f}" fill="#D5DCE8"/>'
    o += f'<ellipse cx="0" cy="{-h * 0.024:.1f}" rx="{h * 0.07:.1f}" ry="{h * 0.017:.1f}" fill="#AEB6C4"/>'
    o += place(red_flag(h), -0.102 * h, -h * 1.0)
    return o


def office_chair():
    """Sedia da ufficio consumata: nastro kraft sullo schienale, imbottitura strappata. Box 420 x 640."""
    o = ""
    # base a cinque razze con ruote
    for (x2, y2) in ((34, 606), (386, 606), (104, 628), (316, 628)):
        o += path(f"M210,586 L{x2},{y2}", "none", stroke(FABRIC_DARK, 20))
    for (x2, y2) in ((34, 606), (386, 606), (104, 628), (316, 628)):
        o += circle(x2, y2 + 10, 16, "#0A1428") + circle(x2 - 4, y2 + 6, 5, "#3B4862")
    o += circle(210, 586, 20, FABRIC_DARK)
    # pistone
    o += rect(198, 452, 24, 140, "#AEB6C4") + rect(210, 452, 12, 140, "#8A93A6")
    o += rect(150, 432, 120, 30, FABRIC_DARK, rx=10)
    # braccioli
    for x in (40, 348):
        o += rect(x + 22, 330, 18, 104, FABRIC_DARK, rx=6)
        o += rect(x, 316, 72, 24, FABRIC_DARK, rx=12)
    # schienale e supporto
    o += rect(193, 330, 34, 80, FABRIC_DARK, rx=6)
    o += rect(88, 30, 244, 324, FABRIC, rx=64)
    o += rect(108, 50, 204, 284, FABRIC_LIGHT, rx=52)
    o += path("M126,190 C170,204 250,204 294,190", "none", stroke(FABRIC, 4, ' opacity="0.7"'))
    # nastro kraft a X sullo strappo
    o += place(rect(-66, -14, 132, 28, TAPE, extra=' opacity="0.95"'), 222, 128, rotate=-32)
    o += place(rect(-66, -14, 132, 28, TAPE, extra=' opacity="0.95"'), 222, 128, rotate=30)
    # seduta
    o += f'<ellipse cx="210" cy="428" rx="176" ry="34" fill="{FABRIC_DARK}"/>'
    o += f'<ellipse cx="210" cy="410" rx="176" ry="40" fill="{FABRIC_LIGHT}"/>'
    o += path("M126,404 L146,392 L160,408 L182,394 L196,410 L176,420 L150,416 Z", "#EFE3C8")
    return o


def squeak(x, y, side=1, color=WHITE):
    """Segni di scricchiolio: tre trattini a ventaglio (side=-1 verso sinistra)."""
    o = ""
    for a in (-32, 0, 32):
        r = math.radians(a)
        x0, y0 = x + side * 12 * math.cos(r), y + 12 * math.sin(r)
        x1, y1 = x + side * 44 * math.cos(r), y + 44 * math.sin(r)
        o += path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", "none", stroke(color, 7))
    return o


def laptop():
    """Portatile aperto con immagine che sfarfalla. Origine: angolo alto sinistro dello schermo."""
    o = rect(0, 0, 440, 286, CARD_DARK, rx=16) + rect(16, 16, 408, 246, CARD_LIGHT, rx=6)
    o += circle(220, 8, 3, "#3B4862")
    for (x, y, w, h, c, op) in ((16, 58, 408, 20, RED, .7), (70, 104, 354, 10, WHITE, .35),
                                (16, 140, 290, 28, "#3C64B4", .75), (140, 196, 284, 12, RED, .5),
                                (16, 224, 180, 8, WHITE, .3)):
        o += rect(x, y, w, h, c, extra=f' opacity="{op}"')
    o += path("M-40,286 H480 L512,312 H-72 Z", "#D5DCE8")
    o += path("M-72,312 H512 V320 Q512,326 506,326 H-66 Q-72,326 -72,320 Z", "#AEB6C4")
    o += rect(180, 314, 80, 5, "#8A93A6", rx=2.5)
    return o


def hand_with_plug():
    """
    Mano che tiene fermo lo spinotto HDMI nella porta. Origine: punta dello spinotto.
    Il braccio entra da sinistra.
    """
    o = path("M-120,16 C-180,16 -230,40 -300,44 C-360,48 -420,40 -520,46", "none",
             stroke(CARD_DARK, 12))                                                  # cavo
    o += rect(-30, -8, 30, 16, "#C9D0DC") + rect(-24, -3, 20, 6, "#6B7890", rx=1)    # punta metallica
    o += rect(-106, -16, 78, 32, CARD_DARK, rx=6)                                   # corpo spinotto
    # braccio e polsino
    o += path("M-560,-86 L-250,-66 L-250,26 L-560,50 Z", FABRIC_LIGHT)
    o += rect(-262, -70, 24, 98, WHITE, rx=6)
    # mano: dorso, dita chiuse sotto, pollice sopra lo spinotto
    o += path("M-240,-60 C-200,-78 -150,-74 -118,-52 C-104,-40 -100,-20 -102,-6 "
              "L-104,30 C-130,46 -196,48 -240,20 Z", SKIN)
    o += path("M-150,-2 C-132,-6 -110,0 -100,14 C-98,30 -110,42 -128,44 C-150,46 -160,30 -156,14 Z",
              SKIN_DARK, ' opacity="0.55"')
    for y in (8, 22, 36):
        o += path(f"M-178,{y} C-160,{y + 4} -140,{y + 4} -120,{y - 2}", "none", stroke(SKIN_DARK, 3))
    o += path("M-196,-58 C-160,-52 -110,-40 -80,-24 C-74,-18 -80,-10 -90,-10 "
              "C-120,-14 -160,-22 -200,-30 Z", SKIN)
    o += path("M-96,-22 C-88,-20 -84,-16 -86,-12", "none", stroke(SKIN_DARK, 3))
    return o


def phone():
    """Smartphone sul supporto con un commento in scrittura: 🚩 e cursore. Box 220 x 462."""
    o = path("M-6,432 H226 L212,462 H8 Z", "#AEB6C4")
    o += rect(0, 0, 220, 440, CARD_DARK, rx=30) + rect(9, 9, 202, 422, WHITE, rx=23)
    o += rect(84, 18, 52, 12, CARD_DARK, rx=6)
    # anteprima del post: la copertina del carosello
    o += rect(22, 42, 176, 176, NAVY, rx=10)
    o += rect(38, 64, 96, 18, RED, rx=2) + rect(38, 90, 120, 12, WHITE, rx=2, extra=' opacity="0.85"')
    o += rect(38, 108, 104, 12, WHITE, rx=2, extra=' opacity="0.85"')
    o += place(desk_flag(70), 126, 204)
    # icone azione
    o += path("M34,246 C28,238 36,230 42,236 C48,230 56,238 50,246 L42,254 Z", RED)
    o += circle(76, 244, 9, "none", stroke(NAVY, 3)) + path("M70,252 L66,258 L74,253", "none", stroke(NAVY, 3))
    # commenti
    for i, w in enumerate((120, 90)):
        y = 282 + i * 40
        o += circle(34, y, 11, SOFT) + rect(52, y - 10, w, 8, "#C9D0DC", rx=4)
        o += rect(52, y + 4, w - 36, 7, "#E1E6EE", rx=3.5)
    # campo commento
    o += rect(20, 372, 180, 44, "#F3F5F9", rx=22, extra=f' stroke="{SOFT}" stroke-width="2"')
    o += place(red_flag(30), 34, 380) + rect(72, 382, 3.5, 24, RED, rx=1.5)
    o += path("M168,386 L186,394 L168,402 L172,394 Z", NAVY)
    return o


def notebooks():
    """Due quaderni impilati con una penna. Origine: angolo basso sinistro sul piano."""
    o = rect(0, -28, 250, 28, NAVY, rx=4) + rect(8, -21, 234, 6, WHITE, rx=2, extra=' opacity="0.9"')
    o += rect(22, -52, 206, 24, RED, rx=4) + rect(30, -45, 190, 5, WHITE, rx=2, extra=' opacity="0.9"')
    o += rect(46, -62, 150, 10, CARD_DARK, rx=5) + path("M196,-62 L214,-57 L196,-52 Z", STEEL)
    return o


def mug():
    """Tazza bianca con fascia rossa e vapore. Origine: centro della base sul piano."""
    o = path("M34,-78 C66,-78 66,-30 34,-30", "none", stroke(WHITE, 12))
    o += rect(-42, -100, 84, 100, WHITE, rx=12) + rect(-42, -64, 84, 18, RED)
    o += rect(-42, -100, 84, 10, "#D5DCE8", rx=5)
    for x in (-14, 10):
        o += path(f"M{x},-116 C{x - 12},-132 {x + 12},-146 {x},-164", "none",
                  stroke(WHITE, 5, ' opacity="0.55"'))
    return o


def down_arrow_icon(x, y, size, color=RED):
    """👇 ridisegnata: freccia in giu' dentro un cerchio."""
    s = size / 100
    body = (circle(50, 50, 46, color)
            + path("M50,24 V74 M30,54 L50,74 L70,54", "none", stroke(WHITE, 11)))
    return group(body, transform=f"translate({x:.1f} {y:.1f}) scale({s:.4f})")


# ==========================================================================
# Slide
# ==========================================================================

def scene(sid, idx=None):
    """Parete navy sfocata + (eventuale) paginazione a bandierine."""
    out = background(sid, "bg_scene.jpg")
    if idx:
        out += flag_progress(sid, idx)
    return out


# 01 · COVER --------------------------------------------------------------------
sid = "slide-01"
out = scene(sid) + logo(sid, W / 2, 130, 460)
out += desk(sid)
out += blob(sid, 600, 900, 250, 235, KRAFT, seed=4)
out += soft_shadow(sid, 610, SURFACE_Y + 6, 150, 26)
out += group(place(desk_flag(440), 600, SURFACE_Y), gid=f"{sid}-bandierina")
bub, _ = speech_bubble(sid, M, 270, CW, ["**Red flag** in ufficio", "che ignori da mesi."], [],
                       tip=(610, 612), at=560, title_size=84, flag=False)
out += bub
slides.append(slide(sid, out))

# 02 · LA SEDIA ------------------------------------------------------------------
sid = "slide-02"
out = scene(sid, 1) + desk(sid)
out += blob(sid, 735, 1010, 300, 320, RED, seed=7)
out += soft_shadow(sid, 735, 1336, 230, 22, 0.5)
ch = place(office_chair(), 525, 690)
ch += place(squeak(0, 0, -1), 525 + 44, 690 + 440) + place(squeak(0, 0, 1), 525 + 376, 690 + 440)
out += group(ch, gid=f"{sid}-sedia")
bub, _ = speech_bubble(sid, M, 230, 640, ["La sedia"],
                       ["che scricchiola «da un po’»", "**(da marzo).**"], tip=(640, 588), at=580)
out += bub
slides.append(slide(sid, out))

# 03 · IL POST-IT ------------------------------------------------------------------
sid = "slide-03"
out = scene(sid, 2) + desk(sid)
out += blob(sid, 620, 905, 300, 230, RED, seed=11)
k = 0.72
px = 620 - 320 * k
py = SURFACE_Y + 8 - 586 * k
out += soft_shadow(sid, 620, SURFACE_Y + 8, 250, 24, 0.45)
ill = place(printer(), px, py, scale=k)
ill += place(postit(), px + 328 * k, py + 350 * k, scale=k, rotate=-6)
out += group(ill, gid=f"{sid}-stampante")
bub, _ = speech_bubble(sid, M, 230, 650, ["Il post-it sulla", "stampante:"],
                       ["**«NON usare il cassetto 2».**"], tip=(560, 600), at=500)
out += bub
slides.append(slide(sid, out))

# 04 · IL PC ---------------------------------------------------------------------
sid = "slide-04"
out = scene(sid, 3) + desk(sid)
out += place(clock(92), 886, 392)
out += blob(sid, 560, 905, 310, 230, RED, seed=5)
k = 0.8
out += soft_shadow(sid, 560, SURFACE_Y + 4, 230, 22, 0.45)
out += group(place(monitor(), 560 - 310 * k, SURFACE_Y + 4 - 452 * k, scale=k), gid=f"{sid}-monitor")
bub, _ = speech_bubble(sid, M, 230, 660, ["Il PC"],
                       ["che ci mette dieci minuti ad", "accendersi, **«ma poi va».**"],
                       tip=(520, 600), at=470)
out += bub
slides.append(slide(sid, out))

# 05 · LA SALA RIUNIONI ----------------------------------------------------------------
sid = "slide-05"
out = scene(sid, 4)
out += blob(sid, 872, 610, 230, 280, RED, seed=9)
out += group(place(door(), 716, 300, scale=0.92), gid=f"{sid}-porta")
out += desk(sid)
out += soft_shadow(sid, 318, SURFACE_Y + 8, 170, 16, 0.4, name="ombra-quaderni")
out += soft_shadow(sid, 560, SURFACE_Y + 8, 70, 12, 0.4, name="ombra-tazza")
out += group(place(notebooks(), 190, SURFACE_Y + 8) + place(mug(), 560, SURFACE_Y + 8),
             gid=f"{sid}-scrivania")
bub, _ = speech_bubble(sid, M, 470, 560, ["La sala riunioni"],
                       ["che si prenota su un", "**foglio A4 appeso**", "**alla porta.**"],
                       tip=(712, 610), side="right", at=580, title_size=52)
out += bub
slides.append(slide(sid, out))

# 06 · IL CAVO HDMI -------------------------------------------------------------------
sid = "slide-06"
out = scene(sid, 5) + desk(sid)
out += blob(sid, 610, 915, 330, 220, RED, seed=3)
lx, ly = 480, SURFACE_Y - 326
out += soft_shadow(sid, lx + 220, SURFACE_Y + 4, 300, 22, 0.45)
ill = place(laptop(), lx, ly)
ill += place(hand_with_plug(), lx - 72, ly + 306)
ill += place(squeak(0, 0, 1), lx - 88, ly + 306 - 30, rotate=-90)
out += group(ill, gid=f"{sid}-portatile")
bub, _ = speech_bubble(sid, M, 230, 670, ["Il cavo HDMI"],
                       ["che funziona **solo se lo tieni**", "**con la mano.**"], tip=(430, 600), at=390)
out += bub
slides.append(slide(sid, out))

# 07 · CTA ------------------------------------------------------------------------
sid = "slide-07"
out = scene(sid) + logo(sid, W / 2, 130, 380)
out += desk(sid)
out += blob(sid, 700, 890, 250, 240, RED, seed=2)
k = 0.9
out += soft_shadow(sid, 700, SURFACE_Y + 6, 150, 20, 0.45)
out += group(place(phone(), 700 - 110 * k, SURFACE_Y + 6 - 462 * k, scale=k), gid=f"{sid}-telefono")
bub, bb = speech_bubble(sid, M, 240, 760, ["Aggiungi la tua", "nei commenti."],
                        ["Quella più votata **la risolviamo**", "**noi, sul serio.**"],
                        tip=(640, 648), at=600, title_size=62, flag=False)
out += bub
# 👇 in coda al testo: seconda riga del corpo, dopo «noi, sul serio.»
tx = M + 46 + text_width("noi, sul serio.", 42, "semi") + 16
out += group(down_arrow_icon(tx, bb - 46 - 13 - 34, 40), gid=f"{sid}-emoji")
out += contacts(sid, y=1226, size=26)
slides.append(slide(sid, out))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG)
    print(svg_path)
    print(prev)
