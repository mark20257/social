"""
Carosello Makhymo 02 · 7 ottobre 1952: il codice a barre (ricorrenza, dedicato LinkedIn)

Stile 'ritaglio' (mky_sticker.py): fondi pieni navy/rosso a carta stropicciata, titolone
Lexend Deca Black, foto scontornate in bianco e nero con bordo da adesivo, nastro con la data,
striscia strappata con la fonte.

Foto: oggetti generati con AI (Higgsfield, GPT Image 2.5) su fondo verde e scontornati con
make_stickers.py. Nessuna persona reale e' raffigurata.

Fatti e fonti (verificati il 29/09/2026):
  - 1948: Bernard Silver, studente del Drexel Institute (Filadelfia), sente un dirigente di
    supermercati chiedere al preside di ingegneria un modo per leggere i prodotti alla cassa.
    Fonte: Drexel University.
  - Inverno 1948-49, Miami Beach: Norman J. Woodland, pensando al Morse, affonda quattro dita
    nella sabbia e le tira verso di se': righe larghe e strette. Fonte: Smithsonian Magazine,
    «The History of the Bar Code»; GS1 UK.
  - Brevetto USA n. 2.612.994 «Classifying Apparatus and Method», depositato il 20/10/1949,
    concesso il 7/10/1952; descrive la versione lineare e quella a cerchi concentrici,
    leggibile da ogni direzione. Fonte: il brevetto.
  - 26/06/1974, ore 8:01, supermercato Marsh di Troy (Ohio): primo prodotto scansionato,
    un pacchetto di gomme da masticare, 67 centesimi. Fonte: History.com.
  - Oltre 10 miliardi di scansioni al giorno. Fonte: GS1.
  Non usato: l'anno di vendita del brevetto a Philco (le fonti non concordano).
"""

from mky_sticker import *  # noqa: F401,F403
from mky_svg import CW, contacts, logo, slide, deliver, text_width

SLUG = "CodiceABarre"
PH = "photos/barcode/cut"

slides = []


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


def story(sid, tone, tape_txt, head, sub, photo=None, cap="", ring=(860, 300), tape_at=(0.70, 0.22),
          tape_rot=-8, photo_w=800, show_logo=True, extra=None, cta=False):
    tone_col = NAVY if tone == "navy" else RED
    out = paper(sid, tone) + rings(sid, *ring)
    if show_logo:
        out += logo(sid, W / 2, 62, 250)
    t, hb, _ = headline(sid, head, 168)
    s_svg, sb = subline(sid, wrap(sub, 31), hb + 44) if sub else ("", hb)
    out += group(t + s_svg, gid=f"{sid}-testi")
    box = None
    if photo:
        top = sb + 56
        st, box = sticker(sid, f"{PH}/{photo}", W / 2, 1262, photo_w, 1262 - top)
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


# 01 · COVER --------------------------------------------------------------------
slides.append(story(
    "slide-01", "navy", "7 OTTOBRE 1952",
    ["==UNA RIGA==", "==DI INCHIOSTRO==", "CHE HA CAMBIATO", "COME SI MUOVONO", "LE COSE."],
    "", "01_mano_etichetta.png", "Brevetto USA n. 2.612.994 · Woodland e Silver",
    ring=(900, 330), tape_at=(0.95, 0.32), tape_rot=-7,
    extra=lambda sb: barcode_label("slide-01", -60, 1010, 250, 110, rotate=14, seed=5)))

# 02 · LA DOMANDA ------------------------------------------------------------------
slides.append(story(
    "slide-02", "red", "1948",
    ["TUTTO PARTE", "==DA UNA DOMANDA==", "IN CORRIDOIO."],
    "Un dirigente di supermercati chiede al Drexel Institute di Filadelfia come leggere "
    "i prodotti alla cassa, in automatico. Lo studente Bernard Silver sente tutto.",
    "02_registratore_cassa.png", "Fonte: Drexel University", ring=(160, 360),
    tape_at=(0.78, 0.18), tape_rot=8))

# 03 · LA SABBIA -------------------------------------------------------------------
slides.append(story(
    "slide-03", "navy", "MIAMI BEACH",
    ["L’IDEA ARRIVA", "CON ==QUATTRO DITA==", "NELLA SABBIA."],
    "Norman Woodland pensa all’alfabeto Morse. Affonda le dita nella sabbia e le tira "
    "verso di sé: punti e linee diventano righe, sottili e spesse.",
    "03_tasto_morse.png", "Fonte: Smithsonian Magazine, «The History of the Bar Code»",
    ring=(900, 380), tape_at=(0.32, 0.36), tape_rot=-9))

# 04 · IL BERSAGLIO ----------------------------------------------------------------
slides.append(story(
    "slide-04", "red", "US 2.612.994",
    ["IL PRIMO", "CODICE A BARRE", "ERA ==ROTONDO.=="],
    "Il brevetto, depositato nel 1949 e concesso il 7 ottobre 1952, lo disegna anche a "
    "cerchi concentrici: si legge da qualunque lato.",
    None, "Fonte: brevetto USA n. 2.612.994, «Classifying Apparatus and Method»",
    ring=(540, 930),
    extra=lambda sb: bullseye("slide-04", W / 2, 935, 230)
    + tape("slide-04", 760, 740, "US 2.612.994", RED, rotate=9)))

# 05 · LA PRIMA CASSA --------------------------------------------------------------
slides.append(story(
    "slide-05", "navy", "26 GIUGNO 1974",
    ["PER VEDERLO", "IN CASSA SERVONO", "==22 ANNI.=="],
    "Troy, Ohio, ore 8:01: un pacchetto di gomme da masticare passa sotto uno scanner laser. "
    "Sul registratore compare il prezzo: 67 centesimi.",
    "05_gomme.png", "Fonte: History.com, «June 26, 1974»", ring=(180, 420),
    tape_at=(0.36, 0.40), tape_rot=-14, photo_w=900))

# 06 · OGGI ----------------------------------------------------------------------
slides.append(story(
    "slide-06", "red", "OGGI",
    ["OLTRE", "==10 MILIARDI==", "DI SCANSIONI", "AL GIORNO."],
    "Pacchi, farmaci, biglietti, spesa: quella riga di inchiostro accompagna le cose "
    "ovunque vadano.",
    "06_pacco.png", "Fonte: GS1", ring=(880, 360), tape_at=(0.22, 0.12), tape_rot=-10,
    photo_w=640))

# 07 · IN UFFICIO ----------------------------------------------------------------
slides.append(story(
    "slide-07", "navy", "IN UFFICIO",
    ["ANCHE I DOCUMENTI", "POSSONO DIRE", "==CHI SONO.=="],
    "Un’etichetta con il codice ritrova un faldone in archivio. Un codice stampato sul "
    "foglio dice al software dove salvarlo, senza rinominare file a mano.",
    "07_stampante_etichette.png", "Stampa · etichette · gestione documentale",
    ring=(170, 380), tape_at=(0.80, 0.10), tape_rot=7, photo_w=680))

# 08 · CTA -----------------------------------------------------------------------
slides.append(story(
    "slide-08", "red", "PARLIAMONE",
    ["74 ANNI DOPO,", "LE RIGHE", "==LAVORANO ANCORA.=="],
    "Se in ufficio si perde tempo a cercare documenti, scrivici: partiamo da come "
    "archiviate oggi.",
    "08_lettore.png", ring=(880, 360), tape_at=(0.18, 0.30), tape_rot=-9, photo_w=700,
    cta=True))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, pdf=True)
    print(svg_path)
    print(prev)
