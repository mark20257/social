"""
Carosello Makhymo 05 · Cosa succede quando una stampante arriva a fine vita

Stile 'ritaglio' (mky_sticker.py). Il filo segue la macchina tappa per tappa: prima si prova a
ripararla, poi si mettono al sicuro i dati, si separano i toner, si raccolgono le macchine e il
resto parte come RAEE; chiude il totale dei rifiuti gestiti e tre domande pratiche.

Foto:
  - scatti sul campo forniti dal cliente (assets/photos/finevita/foto/), trasformati in stampe
    in bianco e nero da make_prints.py; scritte e telefono del trasportatore sfocati o tagliati,
    nessuna persona riconoscibile;
  - oggetti generati con AI (Higgsfield, GPT Image 2.5) in una sola immagine da quattro, divisa da
    make_stickers.py; la multifunzione della CTA viene dalla libreria (artigrafiche).

Fatti e fonti (verificati il 29/09/2026):
  - Makhymo, Bilancio di Sostenibilita' 2025: 24.321 kg di rifiuti nel 2025, gestiti tramite
    trasportatori e impianti autorizzati; toner esausti 205 kg (CER 080318), batterie 46 kg;
    toner affidati a un operatore iscritto all'Albo Nazionale Gestori Ambientali;
    4.624 interventi tecnici nel 2025.
    NB: il PDF non era raggiungibile da questo ambiente; i dati vengono dagli estratti indicizzati
    del documento. Il dettaglio carta/cartone e RAEE non e' usato finche' non e' confermato.
  - Garante privacy, provvedimento 13 ottobre 2008 «RAEE e misure di sicurezza dei dati
    personali»: cancellazione sicura o distruzione dei supporti prima dello smaltimento.
  - Canon, manuale utente imageRUNNER: il disco conserva dati di copie, scansioni e stampe.
  - D.Lgs. 49/2014: gestione dei rifiuti di apparecchiature elettriche ed elettroniche (RAEE).
"""

from functools import partial

import mky_sticker
from mky_sticker import *  # noqa: F401,F403
from mky_svg import deliver

SLUG = "FineVita"
PH = "photos/finevita/cut"
PR = "photos/finevita/print"
BIL = "Fonte: Makhymo, Bilancio di Sostenibilità 2025"

story = partial(mky_sticker.story, photo_dir=PH, head_top=214)
slides = []

# 01 · COVER --------------------------------------------------------------------
slides.append(story(
    "slide-01", "navy", "FINE VITA",
    ["COSA SUCCEDE", "QUANDO UNA STAMPANTE", "==ARRIVA A FINE VITA?=="],
    "Prima di finire nel cassone passa da alcune tappe precise. Eccole in fila.",
    f"{PR}/22_pinza_aperta_pila.png", "Assistenza · dati · toner · RAEE",
    ring=(900, 330), tape_at=(0.80, 0.10), tape_rot=8, photo_w=640, head_max=84))

# 02 · SI PROVA A RIPARARLA ------------------------------------------------------
slides.append(story(
    "slide-02", "red", "ASSISTENZA",
    ["PRIMA DI TUTTO", "SI PROVA", "==A RIPARARLA.=="],
    "Se il guasto si ripara, la macchina torna a lavorare e il rifiuto non nasce. "
    "Nel 2025 i nostri tecnici hanno fatto 4.624 interventi.",
    "08_riparazione.png", BIL, ring=(170, 380), tape_at=(0.78, 0.14), tape_rot=-8,
    photo_w=820))

# 03 · I DATI --------------------------------------------------------------------
slides.append(story(
    "slide-03", "navy", "DATI",
    ["DENTRO C’È", "==UN ARCHIVIO==", "DI DOCUMENTI."],
    "Molte multifunzioni salvano sul disco quello che copiano e scansionano. Prima dello "
    "smaltimento i dati vanno cancellati in modo sicuro, o il disco distrutto.",
    "09_disco_rigido.png", "Fonti: Garante privacy, provvedimento 13/10/2008; Canon, manuale utente",
    ring=(900, 380), tape_at=(0.22, 0.14), tape_rot=-8, photo_w=760))

# 04 · I TONER -------------------------------------------------------------------
slides.append(story(
    "slide-04", "red", "TONER",
    ["==205 KG==", "DI TONER ESAUSTI", "NEL 2025."],
    "Tanto ne abbiamo gestito l’anno scorso. Il toner viaggia a parte: lo ritira un "
    "operatore iscritto all’Albo Nazionale Gestori Ambientali.",
    "10_toner_esausti.png", BIL, ring=(170, 380), tape_at=(0.80, 0.20), tape_rot=8,
    photo_w=640))

# 05 · LA RACCOLTA ---------------------------------------------------------------
slides.append(story(
    "slide-05", "navy", "RACCOLTA",
    ["RITIRATE,", "ASPETTANO", "==IL CAMION.=="],
    "Tolti toner e consumabili, le macchine a fine vita si raccolgono fino al giorno "
    "del carico.",
    f"{PR}/23_piazzale.png", "Ritiro · raccolta · carico",
    ring=(900, 360), tape_at=(0.78, 0.08), tape_rot=7, photo_w=820))

# 06 · IL CARICO -----------------------------------------------------------------
slides.append(story(
    "slide-06", "red", "RAEE",
    ["IL RESTO", "PARTE COME", "==RAEE.=="],
    "Rifiuti di apparecchiature elettriche ed elettroniche. Viaggiano con trasportatori "
    "autorizzati verso impianti che separano plastica, metalli e schede.",
    f"{PR}/16_gru_cassone.png", "Fonti: Makhymo, Bilancio di Sostenibilità 2025; D.Lgs. 49/2014",
    ring=(170, 380), tape_at=(0.20, 0.12), tape_rot=-8, photo_w=860))

# 07 · IL TOTALE -----------------------------------------------------------------
slides.append(story(
    "slide-07", "navy", "2025",
    ["==24.321 KG==", "DI RIFIUTI GESTITI", "IN UN ANNO."],
    "Imballaggi, apparecchiature, toner e batterie: tutto affidato a trasportatori e "
    "impianti autorizzati.",
    f"{PR}/12_pinza_stringe.png", BIL, ring=(900, 380), tape_at=(0.80, 0.12), tape_rot=8,
    photo_w=640))

# 08 · TRE DOMANDE ---------------------------------------------------------------
slides.append(story(
    "slide-08", "red", "PRIMA DI SALUTARLA",
    ["TRE DOMANDE", "==DA FARE SUBITO.=="],
    ["Si può ancora riparare?", "Chi cancella i dati dal disco?", "Chi ritira toner e macchina?"],
    f"{PR}/10_stampante_schiacciata.png", "Assistenza · dati · ritiro",
    ring=(170, 380), tape_at=(0.50, 0.06), tape_rot=-4, photo_w=720, sub_size=38))

# 09 · CTA -----------------------------------------------------------------------
slides.append(story(
    "slide-09", "navy", "PARLIAMONE",
    ["HAI UNA STAMPANTE", "==A FINE VITA?=="],
    ["Prima di buttarla, vediamo se si ripara.", "Scrivici nei commenti."],
    lib("artigrafiche", "00_multifunzione"), ring=(880, 360), tape_at=(0.78, 0.30), tape_rot=-8,
    photo_w=640, cta=True))


if __name__ == "__main__":
    svg_path, prev = deliver(slides, SLUG, pdf=True)
    print(svg_path)
    print(prev)
