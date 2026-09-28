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
N = 8

slides = []

# 01 · COVER --------------------------------------------------------------------
slides.append(build_cover_photo(
    "slide-01",
    "PRIMA CONSULENZA",
    "Cosa succede davvero alla prima consulenza in agenzia?",
    "Ti raccontiamo come lavoriamo, ==passo dopo passo.==",
    group(icon_family(300, 170, 480, AZURE_LIGHT, NAVY), gid="slide-01-illustrazione"),
    photo="Madonia_Cover_PrimaConsulenza.jpg",   # assets/covers/; se manca resta l'illustrazione
))

# 02 · GRID: ci conosciamo --------------------------------------------------------
slides.append(build_layout_grid(
    "slide-02", N, 2, "PASSO 1 · CI CONOSCIAMO",
    lead="Sembra strano, ma al primo incontro parliamo poco di polizze.",
    question="Prima vogliamo capire chi sei e cosa ti sta a cuore.",
    cards=[(icon_work, "Lavoro e reddito"), (icon_family, "Famiglia e persone care"),
           (icon_house, "Casa e patrimonio"), (icon_project, "Progetti e obiettivi")],
    closing="La polizza viene dopo: prima viene la tua situazione.",
    stat=icon_scale,
    stat_txt="Non è solo un metodo: per legge vanno individuate le tue esigenze prima di proporti un contratto.",
    source="Fonti: Codice delle Assicurazioni Private, art. 119-bis; Regolamento IVASS n. 40/2018.",
))

# 03 · PEOPLE: l'analisi ------------------------------------------------------------
slides.append(build_layout_people(
    "slide-03", N, 3, "PASSO 2 · L’ANALISI",
    title="Sai davvero cosa ti copre già?",
    body="Mettiamo in fila le coperture che hai, anche quelle dimenticate, e le confrontiamo con "
         "i rischi reali. Spesso il punto debole è quello che nessuno ha mai guardato. "
         "La previdenza, per esempio:",
    big="4 su 10",
    big_sub="lavoratori hanno una\npensione complementare",
    filled=4, total=10,
    areas=[(icon_shield, "Protezione"), (icon_house, "Casa"),
           (icon_pension, "Previdenza"), (icon_piggy, "Risparmio")],
    source="Fonte: COVIP, Relazione annuale 2026: iscritti alla previdenza complementare "
           "pari al 39,9% delle forze di lavoro a fine 2025.",
))

# 04 · SCENARIOS: la proposta --------------------------------------------------------
slides.append(build_layout_scenarios(
    "slide-04", N, 4, "PASSO 3 · LA PROPOSTA",
    quote="Dall’analisi nasce un piano su misura.",
    answer="Con un perché per ogni scelta.",
    body="Non una lista di prodotti, ma le priorità in ordine: così sai da dove partire, "
         "anche se non vuoi fare tutto subito.",
    lead="Per ogni punto ti spieghiamo:",
    items=[
        (icon_target, "01 · COSA", "Cosa conviene fare"),
        (icon_scale, "02 · PERCHÉ", "Perché è importante proprio per te"),
        (icon_calendar, "03 · QUANDO", "Da cosa partire e cosa può aspettare"),
    ],
    closing="Quando c’è consulenza, la raccomandazione è personalizzata e motivata: "
            "lo prevede l’art. 119-ter del Codice delle Assicurazioni Private.",
))

# 05 · DOC: il DIP --------------------------------------------------------------------
slides.append(build_layout_doc(
    "slide-05", N, 5, "PASSO 4 · PRIMA DI FIRMARE",
    title="Hai mai letto il DIP della tua polizza?",
    body="È il documento informativo precontrattuale: una scheda breve, con lo stesso schema "
         "per tutte le polizze danni, che ricevi prima di firmare. Lo leggiamo insieme, "
         "domanda per domanda.",
    doc_title="DIP DANNI",
    questions=["Che cosa è assicurato?", "Che cosa non è assicurato?",
               "Ci sono limiti di copertura?", "Dove vale la copertura?",
               "Che obblighi ho?", "Quando e come devo pagare?",
               "Quando comincia e quando finisce?", "Come posso disdire la polizza?"],
    source="Fonti: Regolamento IVASS n. 41/2018; Regolamento di esecuzione (UE) 2017/1469.",
))

# 06 · DONTS: cosa non facciamo ----------------------------------------------------------
slides.append(build_layout_donts(
    "slide-06", N, 6, "COSA NON FACCIAMO",
    title="Tre cose che in agenzia non succedono.",
    items=["Proporti una polizza prima di conoscerti.",
           "Consigliare la stessa soluzione a tutti.",
           "Metterti fretta per firmare subito."],
    big="30 giorni",
    big_txt="per ripensarci: dai contratti vita puoi recedere entro 30 giorni dalla conclusione.",
    source="Fonte: Codice delle Assicurazioni Private, art. 177 (contratti vita individuali "
           "di durata superiore a sei mesi).",
))

# 07 · TIMELINE: nel tempo ---------------------------------------------------------------
slides.append(build_layout_timeline(
    "slide-07", N, 7, "PASSO 5 · NEL TEMPO",
    title="E dopo la firma?",
    body="Le esigenze cambiano e il piano deve cambiare con loro. Per questo ci rivediamo con "
         "verifiche periodiche e ogni volta che arriva una svolta:",
    events=[(icon_work, "Un nuovo lavoro"), (icon_heart, "Matrimonio o convivenza"),
            (icon_family, "La nascita di un figlio"), (icon_house, "Una casa o un mutuo"),
            (icon_pension, "L’avvicinarsi della pensione")],
    closing="Una copertura giusta oggi può non esserlo tra cinque anni.",
))

# 08 · CTA -----------------------------------------------------------------------------
slides.append(build_layout_cta(
    "slide-08",
    lead="La prima consulenza è il punto di partenza.",
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
