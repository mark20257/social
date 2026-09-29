"""
Carosello Makhymo 03 · CHECKLIST: 7 segnali che la tua postazione di lavoro sta riducendo
la produttivita'

Stile 'ritaglio' (mky_sticker.py), come il carosello sul codice a barre. In ogni slide le
caselle sotto il logo si spuntano una alla volta: la checklist avanza con il lettore.

Foto: oggetti generati con AI (Higgsfield, GPT Image 2.5) su fondo verde e scontornati con
make_stickers.py (assets/photos/postazione/). Nessuna persona riconoscibile.

Regole citate (verificate il 29/09/2026):
  - D.Lgs. 81/2008, Allegato XXXIV (videoterminali, requisiti minimi):
      schermo con il bordo superiore poco sotto l'orizzontale degli occhi, a circa 50-70 cm;
      piano di lavoro profondo quanto basta per la distanza visiva, ampio per schermo, tastiera
      e documenti, alto 70-80 cm; niente riflessi e abbagliamenti, postazione disposta in base
      alle fonti di luce, finestre con copertura regolabile; sedile regolabile in altezza
      indipendentemente dallo schienale; poggiapiedi a chi lo desidera; per l'uso prolungato
      del portatile tastiera e mouse esterni e un supporto per lo schermo.
  - D.Lgs. 81/2008, art. 173 (videoterminalista: almeno 20 ore settimanali) e art. 175
    (15 minuti di pausa ogni 120 minuti di applicazione continuativa).
Nessuna statistica sulla produttivita': il carosello resta sulle regole.
"""

from functools import partial

import mky_sticker
from mky_sticker import *  # noqa: F401,F403
from mky_svg import deliver

SLUG = "ChecklistPostazione"
PH = "photos/postazione/cut"
N = 7
ALL34 = "Fonte: D.Lgs. 81/2008, Allegato XXXIV"

# caselle e testi scendono: piu' respiro sotto il logo
story = partial(mky_sticker.story, photo_dir=PH, progress_y=182, head_top=254)
slides = []

# 00 · COVER --------------------------------------------------------------------
slides.append(story(
    "slide-01", "navy", "CHECKLIST",
    ["==7 SEGNALI==", "CHE LA TUA", "POSTAZIONE", "DI LAVORO STA", "RIDUCENDO LA", "PRODUTTIVITÀ."],
    "Spunta quelli che riconosci: dietro ognuno c’è una regola.",
    "00_checklist.png", "Checklist · postazione al videoterminale",
    ring=(900, 330), tape_at=(0.78, 0.16), tape_rot=8, photo_w=560, progress=(0, N),
    head_max=84))

# 01 · SCHERMO -------------------------------------------------------------------
slides.append(story(
    "slide-02", "red", "SCHERMO",
    ["A FINE GIORNATA", "HAI IL COLLO", "==DI LEGNO.=="],
    "Lo schermo è troppo basso o troppo alto. Il bordo superiore va tenuto poco sotto "
    "l’altezza degli occhi, a 50–70 cm da te.",
    "01_monitor_libri.png", ALL34, ring=(170, 380), tape_at=(0.80, 0.62), tape_rot=-8,
    progress=(1, N)))

# 02 · DISTANZA ------------------------------------------------------------------
slides.append(story(
    "slide-03", "navy", "DISTANZA",
    ["TI SPORGI", "IN AVANTI", "==PER LEGGERE.=="],
    "Schermo troppo lontano o caratteri troppo piccoli. La scrivania deve essere profonda "
    "abbastanza da tenere lo schermo alla distanza giusta.",
    "02_metro.png", ALL34, ring=(900, 360), tape_at=(0.30, 0.10), tape_rot=-9, photo_w=900,
    progress=(2, N)))

# 03 · LUCE ----------------------------------------------------------------------
slides.append(story(
    "slide-04", "red", "LUCE",
    ["CHIUDI LE TENDE", "==PER VEDERE==", "LO SCHERMO."],
    "Riflessi e abbagliamenti affaticano la vista. La postazione va orientata rispetto a "
    "finestre e lampade, e le finestre devono avere tende regolabili.",
    "03_lampada.png", ALL34, ring=(180, 400), tape_at=(0.30, 0.55), tape_rot=8,
    progress=(3, N)))

# 04 · SEDIA ---------------------------------------------------------------------
slides.append(story(
    "slide-05", "navy", "SEDIA",
    ["I PIEDI", "==NON TOCCANO==", "TERRA."],
    "La seduta deve regolarsi in altezza, indipendente dallo schienale. Se non basta, "
    "a chi lo chiede spetta un poggiapiedi.",
    "04_sedia.png", ALL34, ring=(880, 380), tape_at=(0.22, 0.30), tape_rot=-8,
    progress=(4, N)))

# 05 · PORTATILE -----------------------------------------------------------------
slides.append(story(
    "slide-06", "red", "PORTATILE",
    ["IL PORTATILE", "È ==TUTTA LA TUA==", "POSTAZIONE."],
    "Per un uso prolungato servono tastiera e mouse esterni e un supporto che alzi lo schermo. "
    "Altrimenti si lavora curvi.",
    "05_portatile.png", ALL34, ring=(170, 380), tape_at=(0.76, 0.12), tape_rot=8, photo_w=780,
    progress=(5, N)))

# 06 · SCRIVANIA -----------------------------------------------------------------
slides.append(story(
    "slide-07", "navy", "SCRIVANIA",
    ["NON C’È POSTO", "==PER UN FOGLIO==", "ACCANTO AL PC."],
    "Il piano deve bastare per schermo, tastiera e documenti, ed essere alto tra 70 e 80 cm. "
    "Se tutto si sovrappone, si perde tempo a spostare cose.",
    "06_pila_documenti.png", ALL34, ring=(900, 380), tape_at=(0.78, 0.30), tape_rot=-8,
    progress=(6, N)))

# 07 · PAUSE ---------------------------------------------------------------------
slides.append(story(
    "slide-08", "red", "PAUSE",
    ["LAVORI", "==DUE ORE DI FILA==", "SENZA STACCARE."],
    "Chi usa il videoterminale almeno 20 ore a settimana ha diritto a 15 minuti di pausa "
    "ogni 120 di lavoro continuativo.",
    "07_sveglia.png", "Fonte: D.Lgs. 81/2008, artt. 173 e 175", ring=(180, 380),
    tape_at=(0.80, 0.16), tape_rot=9, progress=(7, N)))

# 08 · CTA -----------------------------------------------------------------------
slides.append(story(
    "slide-09", "navy", "PARLIAMONE",
    ["QUANTE CASELLE", "HAI ==SPUNTATO?=="],
    ["Anche una sola basta per rivedere la postazione.",
     "Vieni nel nostro showroom di Asti, in Strada Valmanera 19:",
     "la rivediamo insieme, metro alla mano."],
    "08_spunta.png", ring=(880, 360), tape_at=(0.70, 0.66), tape_rot=-8, photo_w=720,
    progress=(7, N), cta=True))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, pdf=True)
    print(svg_path)
    print(prev)
