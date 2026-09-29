"""
Carosello Makhymo 04 · L'importanza della reception

Stile 'ritaglio' (mky_sticker.py), come i caroselli sul codice a barre e sulla postazione.
Il filo: seguiamo un cliente dalla porta alla sala d'attesa. Prima l'impressione (ingresso,
bancone, ordine), poi le funzioni (accessibilita', registrazione ospiti, digital signage).

Foto: oggetti generati con AI (Higgsfield, GPT Image 2.5) su fondo verde e scontornati con
make_stickers.py (assets/photos/reception/). Nessuna persona raffigurata.

Regole citate (verificate il 29/09/2026):
  - D.M. 14 giugno 1989, n. 236 (barriere architettoniche), punto 4.1.5 «Arredi fissi»: nei
    luoghi aperti al pubblico banconi e piani d'appoggio devono essere utilizzabili, almeno in
    parte, da persona su sedia a ruote; punto 8.1.5: dove il contatto con il pubblico avviene con
    un bancone continuo, almeno una parte deve avere il piano a 0,90 m dal calpestio.
Nessuna statistica sulla «prima impressione»: i numeri che girano (secondi, percentuali) non
hanno una fonte solida, quindi il carosello non ne usa.
"""

from functools import partial

import mky_sticker
from mky_sticker import *  # noqa: F401,F403
from mky_svg import deliver

SLUG = "Reception"
PH = "photos/reception/cut"

# testi un po' piu' in basso: respiro sotto il logo, come chiesto per il carosello 03
story = partial(mky_sticker.story, photo_dir=PH, head_top=214)
slides = []

# 01 · COVER --------------------------------------------------------------------
slides.append(story(
    "slide-01", "navy", "RECEPTION",
    ["LA RECEPTION", "==PARLA DI TE==", "PRIMA DI TE."],
    "Segui un cliente dalla porta alla sala d’attesa: ecco cosa vede, e cosa gli serve.",
    "00_bancone.png", "Arredo · accoglienza · digital signage",
    ring=(900, 330), tape_at=(0.80, 0.14), tape_rot=8, photo_w=940))

# 02 · L'INGRESSO ----------------------------------------------------------------
slides.append(story(
    "slide-02", "red", "INGRESSO",
    ["LA PORTA SI APRE.", "==IL GIUDIZIO==", "==È GIÀ PARTITO.=="],
    "Nessuno ha ancora detto una parola, ma il cliente guarda: luce, ordine, arredo. "
    "Sono le prime cose che sa della tua azienda.",
    "01_maniglia.png", "Prima impressione · l’ingresso",
    ring=(170, 380), tape_at=(0.78, 0.20), tape_rot=-8))

# 03 · IL TOTEM ------------------------------------------------------------------
slides.append(story(
    "slide-03", "navy", "DIGITAL SIGNAGE",
    ["IL PRIMO SALUTO", "==PUÒ DARLO==", "==UNO SCHERMO.=="],
    "Un totem all’ingresso accoglie l’ospite per nome e indica piano e sala riunioni. "
    "Chi sta al bancone ha più tempo per le persone.",
    "02_totem.png", "Digital signage · benvenuto e indicazioni",
    ring=(900, 380), tape_at=(0.50, 0.80), tape_rot=-8))

# 04 · IL BANCONE ----------------------------------------------------------------
slides.append(story(
    "slide-04", "red", "ARREDO",
    ["IL BANCONE", "È IL ==BIGLIETTO==", "==DA VISITA.=="],
    "Materiali, colori e finiture raccontano l’azienda prima ancora del logo alla parete. "
    "Sceglili coerenti con quello che fai e con chi ricevi.",
    "03_campioni.png", "Arredo · materiali e finiture",
    ring=(180, 380), tape_at=(0.24, 0.20), tape_rot=-9, photo_w=900))

# 05 · L'ORDINE ------------------------------------------------------------------
slides.append(story(
    "slide-05", "navy", "ORDINE",
    ["DAL LATO", "DEL CLIENTE", "==SI VEDE TUTTO.=="],
    "Cavi, pacchi e post-it sul piano raccontano fretta. Passacavi, vani chiusi e un posto "
    "per posta e consegne tengono l’ordine anche nei giorni pieni.",
    "04_cavi.png", "Arredo · passacavi e contenitori",
    ring=(880, 380), tape_at=(0.22, 0.14), tape_rot=-8, photo_w=760))

# 06 · ACCESSIBILITA' --------------------------------------------------------------
slides.append(story(
    "slide-06", "red", "PER TUTTI",
    ["IL BANCONE", "==È ALLA PORTATA==", "DI TUTTI?"],
    "Nei luoghi aperti al pubblico, almeno una parte del bancone deve servire chi è "
    "in sedia a ruote, con il piano a 90 cm da terra.",
    "05_sedia_rotelle.png", "Fonte: D.M. 236/1989, punti 4.1.5 e 8.1.5",
    ring=(170, 400), tape_at=(0.80, 0.12), tape_rot=8, photo_w=700))

# 07 · GLI OSPITI ----------------------------------------------------------------
slides.append(story(
    "slide-07", "navy", "OSPITI",
    ["L’OSPITE ARRIVA.", "==CHI LO ASPETTA==", "==LO SA SUBITO.=="],
    "Un tablet sul bancone registra nome e azienda, stampa il badge e avvisa il collega. "
    "Nessuno resta in piedi mentre si cerca chi chiamare.",
    "06_tablet_badge.png", "Accoglienza · registrazione ospiti",
    ring=(900, 380), tape_at=(0.78, 0.18), tape_rot=8, photo_w=720))

# 08 · L'ATTESA ------------------------------------------------------------------
slides.append(story(
    "slide-08", "red", "SALA D’ATTESA",
    ["SE DEVE", "ASPETTARE,", "==CHE STIA COMODO.=="],
    "Poltroncine accoglienti, un tavolino, una presa per il telefono. Pochi minuti in uno "
    "spazio curato passano meglio.",
    "07_poltrona.png", "Arredo · sala d’attesa",
    ring=(170, 380), tape_at=(0.30, 0.10), tape_rot=-8, photo_w=820))

# 09 · LO SCHERMO IN ATTESA ------------------------------------------------------
slides.append(story(
    "slide-09", "navy", "DIGITAL SIGNAGE",
    ["MENTRE ASPETTA,", "==COSA GUARDA?=="],
    "Uno schermo in sala d’attesa racconta novità, progetti, prodotti. I contenuti si "
    "aggiornano dal computer, senza ristampare cartelli.",
    "08_schermo.png", "Digital signage · sala d’attesa",
    ring=(880, 360), tape_at=(0.70, 0.08), tape_rot=7, photo_w=900))

# 10 · CTA -----------------------------------------------------------------------
slides.append(story(
    "slide-10", "red", "PARLIAMONE",
    ["LA TUA RECEPTION", "==COSA DICE DI TE?=="],
    ["Arredo e digital signage, dal bancone allo schermo.",
     "Scrivici nei commenti per una consulenza gratuita."],
    "09_campanello.png", ring=(170, 360), tape_at=(0.78, 0.30), tape_rot=-8, photo_w=800,
    cta=True))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, pdf=True)
    print(svg_path)
    print(prev)
