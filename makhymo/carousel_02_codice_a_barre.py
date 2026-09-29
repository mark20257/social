"""
Carosello Makhymo 02 · 7 ottobre 1952: il codice a barre (ricorrenza, dedicato LinkedIn)

Stile 'ritaglio' (mky_sticker.py): fondi pieni navy/rosso a carta stropicciata, titolone
Lexend Deca Black, foto scontornate in bianco e nero con bordo da adesivo, nastro con la data,
striscia strappata con la fonte.

Foto: oggetti generati con AI (Higgsfield, GPT Image 2.5) su fondo verde e scontornati con
make_stickers.py. Nessuna persona reale e' raffigurata.

Fatti e fonti (verificati il 29/09/2026):
  - 1948: al Drexel Institute (Filadelfia) un dirigente di supermercati chiede al preside di
    ingegneria come leggere i prodotti alla cassa; il preside rifiuta, lo studente Bernard Silver
    ne parla all'amico Norman J. Woodland. Fonti: Drexel University; IEEE Milestone
    «Birthplace of the Bar Code, 1948».
  - Inverno 1949, Miami Beach: Woodland, pensando al Morse, affonda quattro dita nella sabbia e
    le tira verso di se': righe larghe e strette. Fonte: Smithsonian Magazine, «The History of
    the Bar Code»; Drexel University.
  - Brevetto USA n. 2.612.994 «Classifying Apparatus and Method», depositato il 20/10/1949,
    concesso il 7/10/1952; versione lineare e a cerchi concentrici. Fonte: il brevetto.
  - Il prototipo di lettore: lampada a incandescenza da 500 watt, grande come una scrivania;
    mancavano una luce precisa e un computer piccolo, arrivati con laser e minicomputer.
    Fonti: Smithsonian Magazine; National Inventors Hall of Fame.
  - Bernard Silver muore il 28/08/1963 a 38 anni. Fonte: National Inventors Hall of Fame.
  - Woodland entra in IBM nel 1951; il 3/04/1973 l'industria alimentare USA adotta come standard
    l'UPC progettato in IBM (George Laurer), con il contributo di Woodland. Fonte: IBM.
  - 26/06/1974, ore 8:01, supermercato Marsh di Troy (Ohio): primo prodotto scansionato,
    un pacchetto di gomme da masticare, 67 Cent (0,67 dollari). Fonte: History.com.
  - Oltre 10 miliardi di scansioni al giorno. Fonte: GS1.
  Non usato: l'anno di vendita del brevetto a Philco (le fonti non concordano).
"""

from functools import partial

import mky_sticker
from mky_sticker import *  # noqa: F401,F403
from mky_svg import CW, _font_attrs, circle, contacts, logo, rect, slide, deliver, text_width

SLUG = "CodiceABarre"
PH = "photos/barcode/cut"

slides = []
story = partial(mky_sticker.story, photo_dir=PH)


# 01 · COVER --------------------------------------------------------------------
slides.append(story(
    "slide-01", "navy", "7 OTTOBRE 1952",
    ["==UNA RIGA==", "==DI INCHIOSTRO==", "CHE HA CAMBIATO", "COME SI MUOVONO", "LE COSE."],
    "", "01_mano_etichetta.png", "Brevetto USA n. 2.612.994 · Woodland e Silver",
    ring=(900, 330), tape_at=(0.95, 0.32), tape_rot=-7,
    extra=lambda sb: barcode_label("slide-01", -60, 1010, 250, 110, rotate=14, seed=5)))


def timeline(sid, top, rows, x_year=M, x_text=318, text_w=672, size=29, gap=44):
    """Linea del tempo: anno in kraft a sinistra, testo a destra, punti su una linea verticale."""
    line_x = 268
    out, y, dots = "", top, []
    for year, text in rows:
        lines = wrap(text, size, "med", text_w)
        yb = y + 0.72 * 46
        out += (f'<text id="{sid}-anno-{year}" x="{x_year}" y="{yb:.1f}" font-size="46" '
                f'{_font_attrs("black")} fill="{ACCENT}">{year}</text>')
        t, bottom = subline(sid + f"-{year}", lines, y + 4, size=size, cx=0, max_w=text_w)
        out += t.replace('text-anchor="middle"', "").replace(' x="0.0"', f' x="{x_text}"')
        dots.append(y + 17)
        y = max(bottom, yb) + gap + 14
    line = rect(line_x - 1.5, dots[0], 3, dots[-1] - dots[0], WHITE, extra=' opacity="0.35"')
    pts = "".join(circle(line_x, d, 10, ACCENT) + circle(line_x, d, 4, NAVY) for d in dots)
    return group(line + pts + out, gid=f"{sid}-linea-tempo")


# 02 · LA DOMANDA ------------------------------------------------------------------
slides.append(story(
    "slide-02", "red", "1948",
    ["TUTTO PARTE", "==DA UNA DOMANDA==", "IN CORRIDOIO."],
    "Un dirigente di supermercati chiede al Drexel Institute di Filadelfia come leggere i "
    "prodotti alla cassa. Il preside dice no. Lo studente Bernard Silver ne parla all’amico "
    "Norman Joseph Woodland.",
    "02_registratore_cassa.png", "Fonti: Drexel University; IEEE, «Birthplace of the Bar Code, 1948»",
    ring=(160, 360), tape_at=(0.78, 0.18), tape_rot=8))

# 03 · LA SABBIA -------------------------------------------------------------------
slides.append(story(
    "slide-03", "navy", "MIAMI BEACH",
    ["L’IDEA ARRIVA", "CON ==QUATTRO DITA==", "NELLA SABBIA."],
    "Woodland passa l’inverno a Miami con in testa la domanda di Silver. Sulla spiaggia ripensa "
    "al Morse, affonda le dita nella sabbia e le tira verso di sé: punti e linee diventano righe.",
    "03_tasto_morse.png", "Fonte: Smithsonian Magazine, «The History of the Bar Code»",
    ring=(900, 380), tape_at=(0.32, 0.36), tape_rot=-9))

# 04 · IL BERSAGLIO ----------------------------------------------------------------
slides.append(story(
    "slide-04", "red", "US 2.612.994",
    ["IL PRIMO", "CODICE A BARRE", "ERA ==ROTONDO.=="],
    "Woodland e Silver lo mettono nero su bianco: brevetto depositato nell’ottobre 1949, "
    "concesso il 7 ottobre 1952. Righe dritte o cerchi concentrici, leggibili da qualunque lato.",
    None, "Fonte: brevetto USA n. 2.612.994, «Classifying Apparatus and Method»",
    ring=(540, 950),
    extra=lambda sb: bullseye("slide-04", W / 2, 955, 220)
    + tape("slide-04", 760, 770, "US 2.612.994", RED, rotate=9)))

# 05 · DALLA SABBIA ALLA CASSA ----------------------------------------------------------
slides.append(story(
    "slide-05", "navy", None,
    ["DALLA SABBIA", "ALLA CASSA:", "==25 ANNI.=="],
    "", None, "Fonti: Smithsonian Magazine; National Inventors Hall of Fame; IBM",
    ring=(900, 300),
    extra=lambda sb: timeline("slide-05", sb + 70, [
        ("1949", "Woodland e Silver depositano il brevetto del codice a barre."),
        ("1952", "Brevetto concesso. Il lettore però usa una lampada da 500 watt ed è grande "
                 "come una scrivania."),
        ("1963", "Bernard Silver muore a 38 anni, senza vedere il suo codice in cassa."),
        ("1973", "Laser e computer più piccoli rendono possibile la lettura. I supermercati "
                 "americani adottano lo standard UPC, sviluppato in IBM con Woodland."),
        ("1974", "Il primo prodotto viene letto in cassa."),
    ])))

# 06 · IL PRIMO BIP ---------------------------------------------------------------
slides.append(story(
    "slide-06", "red", "TROY, OHIO",
    ["26 GIUGNO 1974:", "==IL PRIMO «BIP»==", "IN CASSA."],
    "Alle 8:01 un pacchetto di gomme da masticare passa sotto uno scanner laser. Sul "
    "registratore compare il prezzo: 67 Cent.",
    "05_gomme.png", "Fonte: History.com, «June 26, 1974»", ring=(180, 420),
    tape_at=(0.36, 0.40), tape_rot=-14, photo_w=900))

# 07 · OGGI ----------------------------------------------------------------------
slides.append(story(
    "slide-07", "navy", "OGGI",
    ["OLTRE", "==10 MILIARDI==", "DI SCANSIONI", "AL GIORNO."],
    "Dalle gomme di Troy ai pacchi, ai farmaci, ai biglietti: le righe di Woodland e Silver "
    "accompagnano le cose ovunque vadano.",
    "06_pacco.png", "Fonte: GS1", ring=(880, 360), tape_at=(0.22, 0.12), tape_rot=-10,
    photo_w=640))

# 08 · IN UFFICIO ----------------------------------------------------------------
slides.append(story(
    "slide-08", "red", "IN UFFICIO",
    ["ANCHE I DOCUMENTI", "POSSONO DIRE", "==CHI SONO.=="],
    "La stessa idea lavora sulla scrivania: un’etichetta con il codice ritrova un faldone in "
    "archivio, un codice sul foglio dice al software dove salvarlo.",
    "07_stampante_etichette.png", "Stampa · etichette · gestione documentale",
    ring=(170, 380), tape_at=(0.80, 0.10), tape_rot=7, photo_w=680))

# 09 · CTA -----------------------------------------------------------------------
slides.append(story(
    "slide-09", "navy", "PARLIAMONE",
    ["74 ANNI DOPO,", "LE RIGHE", "==LAVORANO ANCORA.=="],
    "Se in ufficio si perde tempo a cercare documenti, scrivici: partiamo da come "
    "archiviate oggi.",
    "08_lettore.png", ring=(880, 360), tape_at=(0.18, 0.30), tape_rot=-9, photo_w=700,
    cta=True))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, pdf=True)
    print(svg_path)
    print(prev)
