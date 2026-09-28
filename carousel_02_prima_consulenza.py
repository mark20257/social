"""
Carosello 02 · Come funziona la prima consulenza in agenzia

Ispirazione di struttura: post di un competitor (ci conosciamo, analisi,
strategia, ti seguo nel tempo, cosa non faccio, contatti), riscritto con
voce e dati Madonia.

Fonti:
  - Codice delle Assicurazioni Private (D.Lgs. 209/2005), art. 119-bis:
    individuare richieste ed esigenze del contraente e proporre contratti coerenti
  - Regolamento IVASS n. 40/2018 (distribuzione assicurativa)
  - Codice delle Assicurazioni Private, art. 119-ter e Reg. IVASS 40/2018 art. 59:
    raccomandazione personalizzata e motivata quando e' prestata consulenza
  - Regolamento IVASS n. 41/2018 e Reg. di esecuzione (UE) 2017/1469: DIP Danni
    e le sue domande standard
  - Codice delle Assicurazioni Private, art. 177: recesso dai contratti vita
    individuali entro 30 giorni dalla conclusione
  - COVIP, Relazione annuale (giugno 2026, dati di fine 2025): tasso di
    partecipazione alla previdenza complementare 39,9% delle forze di lavoro
"""

from build_carousel import *  # noqa: F401,F403

SLUG = "PrimaConsulenza"
CRUCIAL = "/Volumes/Crucial X6/Allianz Assicurazioni/2026/10 - OTTOBRE/production/project/"

# una slide = un concetto: testi brevi, titoli grandi, un elemento visivo
slides = []

# 01 · COVER --------------------------------------------------------------------
slides.append(build_cover_photo(
    "slide-01",
    "PRIMA CONSULENZA",
    "Cosa succede davvero alla prima consulenza in agenzia?",
    "Ti raccontiamo come lavoriamo, ==passo dopo passo.==",
    group(icon_family(300, 170, 480, AZURE_LIGHT, NAVY), gid="slide-01-illustrazione"),
    photo="Madonia_Cover_PrimaConsulenza.jpg",
))

# 02 · Hook -----------------------------------------------------------------------
slides.append(build_stack("slide-02", "PRIMA CONSULENZA", [
    blk_hero(icon_chat),
    blk_title("Al primo incontro parliamo poco di polizze.", 66),
    blk_text("Sembra strano. ==Ecco perché.==", 44, WHITE),
], glow=(300, 500)))

# 03 · Passo 1: chi sei --------------------------------------------------------------
slides.append(build_stack("slide-03", "PASSO 1 · CI CONOSCIAMO", [
    blk_title("Prima vogliamo capire chi sei."),
    blk_cards([(icon_work, "Lavoro e reddito"), (icon_family, "Famiglia e persone care"),
               (icon_house, "Casa e patrimonio"), (icon_project, "Progetti e obiettivi")]),
], glow=(900, 900)))

# 04 · Passo 1: la norma -------------------------------------------------------------
slides.append(build_stack("slide-04", "PASSO 1 · CI CONOSCIAMO", [
    blk_hero(icon_scale),
    blk_title("Non è solo un metodo."),
    blk_text("Per legge, prima di proporti un contratto vanno individuate **le tue esigenze.**"),
], source="Fonti: Codice delle Assicurazioni Private, art. 119-bis; Regolamento IVASS n. 40/2018.",
    glow=(250, 350)))

# 05 · Passo 2: l'analisi -------------------------------------------------------------
slides.append(build_stack("slide-05", "PASSO 2 · L’ANALISI", [
    blk_title("Sai davvero cosa ti copre già?"),
    blk_text("Mettiamo in fila le coperture che hai, anche quelle dimenticate."),
    blk_pills([(icon_shield, "Protezione"), (icon_house, "Casa"),
               (icon_pension, "Previdenza"), (icon_piggy, "Risparmio")]),
], glow=(880, 1000)))

# 06 · Passo 2: il punto debole ---------------------------------------------------------
slides.append(build_stack("slide-06", "PASSO 2 · L’ANALISI", [
    blk_title("Il punto debole? Spesso è la previdenza."),
    blk_pictogram("4 su 10", "lavoratori hanno una\npensione complementare", 4, 10),
], source="Fonte: COVIP, Relazione annuale 2026: iscritti alla previdenza complementare "
          "pari al 39,9% delle forze di lavoro a fine 2025.", glow=(860, 760)))

# 07 · Passo 3: la proposta --------------------------------------------------------------
slides.append(build_stack("slide-07", "PASSO 3 · LA PROPOSTA", [
    blk_title("Un piano su misura, con un perché per ogni scelta."),
    blk_rows([(icon_target, "Cosa conviene fare"), (icon_scale, "Perché proprio per te"),
              (icon_calendar, "Da dove partire")]),
], glow=(160, 1100)))

# 08 · Passo 4: il DIP ------------------------------------------------------------------
slides.append(build_stack("slide-08", "PASSO 4 · PRIMA DI FIRMARE", [
    blk_title("Hai mai letto il DIP della tua polizza?"),
    blk_text("Lo leggiamo insieme, domanda per domanda."),
    blk_doc("DIP DANNI", ["Che cosa è assicurato?", "Che cosa non è assicurato?",
                          "Ci sono limiti di copertura?", "Dove vale la copertura?",
                          "Che obblighi ho?", "Quando e come devo pagare?",
                          "Quando comincia e quando finisce?", "Come posso disdire la polizza?"]),
], source="Fonti: Regolamento IVASS n. 41/2018; Regolamento di esecuzione (UE) 2017/1469.",
    gap=[30, 44], glow=(200, 900)))

# 09 · Cosa non facciamo --------------------------------------------------------------------
slides.append(build_stack("slide-09", "COSA NON FACCIAMO", [
    blk_title("Tre cose che in agenzia non succedono."),
    blk_donts(["Proporti una polizza prima di conoscerti.",
               "Consigliare la stessa soluzione a tutti.",
               "Metterti fretta per firmare subito."]),
], glow=(880, 300)))

# 10 · Nessuna fretta: 30 giorni ------------------------------------------------------------
slides.append(build_stack("slide-10", "NESSUNA FRETTA", [
    blk_hero(icon_calendar),
    blk_bigstat("30 giorni", "per ripensarci: dai contratti vita puoi recedere entro 30 giorni dalla conclusione."),
], source="Fonte: Codice delle Assicurazioni Private, art. 177 (contratti vita individuali "
          "di durata superiore a sei mesi).", glow=(300, 450)))

# 11 · Passo 5: nel tempo ------------------------------------------------------------------
slides.append(build_stack("slide-11", "PASSO 5 · NEL TEMPO", [
    blk_title("E dopo la firma? Ci rivediamo quando la vita cambia."),
    blk_timeline([(icon_work, "Un nuovo lavoro"), (icon_heart, "Matrimonio o convivenza"),
                  (icon_family, "La nascita di un figlio"), (icon_house, "Una casa o un mutuo"),
                  (icon_pension, "Verso la pensione")]),
], glow=(180, 700)))

# 12 · CTA ------------------------------------------------------------------------------
slides.append(build_layout_cta(
    "slide-12",
    lead=None,
    headline="Partiamo dalla tua situazione, non da un prodotto.",
    body=None,
    question="Fissa il tuo\nprimo incontro\nin agenzia.",
    contacts=[(icon_phone, "0141 557260"),
              (icon_mail, "asti4@ageallianz.it"),
              (icon_pin, "Via Alcide De Gasperi 2, Asti"),
              (icon_web, "www.agenziamadonia.it")],
    illu_fn=lambda sid, x, y, w: illu_calendar_savings(sid, x, y, w, label="APPUNTAMENTO"),
))


if __name__ == "__main__":
    pdf, svg, prev = deliver(slides, SLUG, crucial_dir=CRUCIAL)
    print(pdf)
    print(svg)
    print(prev)
