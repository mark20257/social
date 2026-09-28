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

# un racconto continuo: frasi complete e discorsive, poche per slide, un elemento visivo
slides = []

# 01 · COVER --------------------------------------------------------------------
slides.append(build_cover_photo(
    "slide-01",
    "PRIMA CONSULENZA",
    "Cosa succede davvero alla prima consulenza in agenzia?",
    "Te lo raccontiamo ==passo dopo passo.==",
    group(icon_family(300, 170, 480, AZURE_LIGHT, NAVY), gid="slide-01-illustrazione"),
    photo="Madonia_Cover_PrimaConsulenza.jpg",
    eyebrow_style="pill",
))

# 02 · La conversazione --------------------------------------------------------------
slides.append(build_stack("slide-02", "PRIMA CONSULENZA", [
    blk_title("Al primo incontro le domande le facciamo soprattutto noi.", 56),
    blk_chat([
        ("left", "TU", "Che polizza mi consigliate?"),
        ("right", "NOI", "Prima raccontaci un po’ di te."),
        ("right", "NOI", "Che lavoro fai? Chi vive con te? Cosa ti preoccupa di più?"),
    ], size=42, max_w=700, gap=34),
    blk_text("Può sembrare un giro lungo, ma è da qui che parte ogni consiglio sensato.", 38),
], gap=[62, 40], glow=(900, 700)))

# 03 · Passo 1: ci conosciamo ----------------------------------------------------------
slides.append(build_stack("slide-03", "PASSO 1 · CI CONOSCIAMO", [
    blk_title("Prima di parlare di polizze, parliamo di te.", 58),
    blk_text("Ci facciamo raccontare la tua situazione partendo da quattro aspetti della tua vita:", 38),
    blk_cards([(icon_work, "Lavoro e reddito"), (icon_family, "Famiglia e persone care"),
               (icon_house, "Casa e patrimonio"), (icon_project, "Progetti e obiettivi")]),
], gap=[44, 48], glow=(900, 900)))

# 04 · Perché le esigenze contano --------------------------------------------------------
slides.append(build_stack("slide-04", "PASSO 1 · CI CONOSCIAMO", [
    blk_title("Due persone con lo stesso stipendio possono avere bisogni opposti.", 52),
    blk_compare("STESSO STIPENDIO",
                {"icon": icon_family, "who": "Ha un mutuo e due figli piccoli",
                 "need": "Proteggere il reddito di famiglia"},
                {"icon": icon_person, "who": "Vive da solo e paga un affitto",
                 "need": "Pensare per tempo alla pensione"}),
    blk_text("Per questo conoscere le tue esigenze viene prima di tutto il resto.", 38),
], gap=[44, 44], glow=(540, 800)))

# 05 · Passo 2: cosa hai già ---------------------------------------------------------------
slides.append(build_stack("slide-05", "PASSO 2 · L’ANALISI", [
    blk_title("Poi guardiamo insieme cosa hai già.", 58),
    blk_text("Mettiamo sul tavolo tutte le coperture che hai, anche quelle che magari hai "
             "dimenticato, come la polizza abbinata al mutuo o quella offerta dal lavoro. "
             "Solo così si vede cosa manca davvero.", 38),
    blk_pills([(icon_shield, "Protezione"), (icon_house, "Casa"),
               (icon_pension, "Previdenza"), (icon_piggy, "Risparmio")]),
], gap=[44, 48], glow=(880, 1000)))

# 06 · Passo 2: la previdenza ------------------------------------------------------------------
slides.append(build_stack("slide-06", "PASSO 2 · L’ANALISI", [
    blk_title("Spesso il vuoto più grande riguarda la pensione.", 56),
    blk_text("Solo 4 lavoratori su 10 hanno una pensione complementare: tutti gli altri "
             "contano soltanto su quella pubblica. È uno dei primi punti che guardiamo insieme.", 38),
    blk_pictogram("4 su 10", "lavoratori hanno una\npensione complementare", 4, 10, panel_h=340),
], source="Fonte: COVIP, Relazione annuale 2026: iscritti alla previdenza complementare "
          "pari al 39,9% delle forze di lavoro a fine 2025.", gap=[44, 44], glow=(860, 760)))

# 07 · Passo 3: la proposta ----------------------------------------------------------------------
slides.append(build_stack("slide-07", "PASSO 3 · LA PROPOSTA", [
    blk_title("Alla fine non ti diamo un prodotto, ma un piano.", 56),
    blk_text("Ti spieghiamo cosa conviene fare e perché, partendo da quello che ci hai raccontato. "
             "E mettiamo le priorità in ordine: se non vuoi fare tutto subito, sai da dove cominciare.", 38),
    blk_plan("IL TUO PIANO", ["Cosa conviene fare", "Perché proprio per te", "Da dove partire"]),
], gap=[44, 48], glow=(160, 1100)))

# 08 · Passo 4: cos'è il DIP ------------------------------------------------------------------------
slides.append(build_stack("slide-08", "PASSO 4 · PRIMA DI FIRMARE", [
    blk_title("Prima di firmare ricevi il DIP. Ma cos’è?", 56),
    blk_text("È il Documento Informativo Precontrattuale: una scheda breve che riassume la polizza "
             "in parole semplici. Ha lo stesso schema per tutte le compagnie, così puoi capire "
             "e confrontare senza perderti tra le clausole.", 38),
    blk_docillu("DIP", 440),
], gap=[44, 40], glow=(540, 900)))

# 09 · Passo 4: le domande del DIP --------------------------------------------------------------------
slides.append(build_stack("slide-09", "PASSO 4 · PRIMA DI FIRMARE", [
    blk_title("Risponde sempre alle stesse domande.", 56),
    blk_text("Lo leggiamo insieme, una domanda alla volta, finché ogni punto è chiaro.", 38),
    blk_doc("LE DOMANDE DEL DIP DANNI", ["Che cosa è assicurato?", "Che cosa non è assicurato?",
                                        "Ci sono limiti di copertura?", "Dove vale la copertura?",
                                        "Che obblighi ho?", "Quando e come devo pagare?",
                                        "Quando comincia e quando finisce?", "Come posso disdire la polizza?"]),
], source="Fonti: Regolamento IVASS n. 41/2018; Regolamento di esecuzione (UE) 2017/1469.",
    gap=[42, 44], glow=(200, 900)))

# 10 · Cosa non facciamo ------------------------------------------------------------------------------
slides.append(build_stack("slide-10", "COSA NON FACCIAMO", [
    blk_title("Ci sono anche cose che non facciamo mai.", 58),
    blk_donts(["Proporti una polizza prima di averti conosciuto.",
               "Dare a tutti la stessa soluzione.",
               "Chiederti di firmare subito, senza tempo per pensarci."]),
], glow=(880, 300)))

# 11 · Il tempo per decidere ----------------------------------------------------------------------------
slides.append(build_stack("slide-11", "IL TEMPO PER DECIDERE", [
    blk_hero(icon_calendar),
    blk_bigstat("30 giorni", "Per le polizze vita, anche dopo aver firmato hai 30 giorni per "
                             "cambiare idea e recedere dal contratto."),
], source="Fonte: Codice delle Assicurazioni Private, art. 177 (contratti vita individuali "
          "di durata superiore a sei mesi).", glow=(300, 450)))

# 12 · Passo 5: nel tempo ---------------------------------------------------------------------------------
slides.append(build_stack("slide-12", "PASSO 5 · NEL TEMPO", [
    blk_title("Dopo la firma, restiamo in contatto.", 58),
    blk_text("La vita cambia e con lei le cose da proteggere. Per questo ci risentiamo "
             "periodicamente e ogni volta che arriva una svolta:", 38),
    blk_timeline([(icon_work, "Un nuovo lavoro"), (icon_family, "Una famiglia che cresce"),
                  (icon_house, "Una casa o un mutuo"), (icon_pension, "L’avvicinarsi della pensione")]),
], gap=[44, 44], glow=(180, 700)))

# 13 · CTA ------------------------------------------------------------------------------------------------
slides.append(build_layout_cta(
    "slide-13",
    lead=None,
    headline="Partiamo dalla tua situazione, non da un prodotto.",
    body="Se vuoi, porta le polizze che hai già: **cominciamo da lì.**",
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
