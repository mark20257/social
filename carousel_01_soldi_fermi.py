"""
Carosello 01 · World Investor Week (5-11 ottobre 2026)
"Lasciare i soldi fermi è davvero la scelta più prudente?"

Fonti dei dati:
  - ISTAT, Prezzi al consumo, agosto 2026 (NIC +3,3% su base annua)
  - ISTAT, NIC variazioni medie annue: 2021 +1,9% · 2022 +8,1% · 2023 +5,7% · 2024 +1,0% · 2025 +1,5%
    cumulato 2020-2025: +19,4% -> 10.000 € valgono come 8.378 €
  - ABI, Rapporto mensile settembre 2026: tasso medio conti correnti ad agosto 2026 0,32%
  - IOSCO, comunicato del 22 luglio 2026: 10ª edizione WIW, 5-11 ottobre, temi
    Investor Resilience, Digital Deception, Scam Alert; dal 2017, oltre 100 giurisdizioni
  - BCE: obiettivo di inflazione al 2% nel medio termine (simulazione 5/10/20 anni)
  - Consob, VIII Rapporto sulle scelte di investimento delle famiglie italiane:
    obiettivi 39% protezione capitale, 27% crescita, 18% reddito, 16% non sa indicarlo
"""

from build_carousel import *  # noqa: F401,F403

SLUG = "SoldiFermi_WorldInvestorWeek"
CRUCIAL = "/Volumes/Crucial X6/Allianz Assicurazioni/2026/10 - OTTOBRE/production/project/"
N = 8
EB = "WORLD INVESTOR WEEK"

# inflazione cumulata 2021-2025 (ISTAT, NIC medie annue)
RATES = [1.9, 8.1, 5.7, 1.0, 1.5]
cum = 1.0
for r_ in RATES:
    cum *= 1 + r_ / 100
REAL_2025 = round(10000 / cum)                 # 8.378
CUM_PCT = fmt((cum - 1) * 100, 1)             # 19,4

# potere d'acquisto con inflazione al 2% annuo (obiettivo BCE)
PROJ = [("Oggi", 10000)] + [(f"Tra {n} anni", round(10000 / 1.02 ** n)) for n in (5, 10, 20)]


slides = []

# 01 · COVER ----------------------------------------------------------------
slides.append(build_cover_photo(
    "slide-01",
    "WORLD INVESTOR WEEK · 5-11 OTTOBRE",
    "Lasciare i soldi fermi è davvero la scelta più prudente?",
    "Il rischio che non si vede: ==l’inflazione.==",
    illu_piggy_dissolve("slide-01", 118, 140, scale=1.22),
))

# 02 · VERSUS: quello che vedi e quello che non vedi -------------------------
slides.append(build_layout_versus(
    "slide-02", N, 2, EB,
    quote="“Se i soldi sono sul conto, non sto rischiando nulla.”",
    answer="Non necessariamente.",
    body="Il capitale può rimanere invariato sul conto, mentre nel tempo può diminuire "
         "il suo **potere d’acquisto**. Ed è un rischio che non compare sull’estratto conto.",
    left={"icon": icon_bank, "label": "SUL CONTO", "value": "0,32%",
          "caption": "interesse medio lordo annuo sui conti correnti"},
    right={"icon": icon_cart, "label": "NEI PREZZI", "value": "+3,3%",
           "caption": "aumento dei prezzi al consumo in un anno"},
    source="Fonti: ABI, Rapporto mensile di settembre 2026 (dato di agosto); "
           "ISTAT, Prezzi al consumo, agosto 2026.",
))

# 03 · CALLOUT: nominale vs reale ---------------------------------------------
slides.append(build_layout_callout(
    "slide-03", N, 3, EB,
    title="10.000 € oggi sono sempre 10.000 € tra 5 anni.",
    question="Ma potranno comprare le stesse cose?",
    body=f"Se nel frattempo i prezzi aumentano, la risposta è no. È già successo: "
         f"tra il 2020 e il 2025 i prezzi in Italia sono saliti del **{CUM_PCT}%**.",
    infographic_fn=lambda sid, top, bottom: infog_value_bars(sid, top, bottom, [
        ("SUL CONTO, NEL 2020", 10000, 10000, SOFT, NAVY_DEEP),
        ("QUANTO VALGONO NEL 2025", REAL_2025, 10000, AZURE, WHITE),
    ]),
    punchline="Il valore nominale resta uguale.\n==Il valore reale cambia.==",
    source="Fonte: elaborazione su dati ISTAT, indice NIC, variazioni medie annue 2021-2025 "
           "(+1,9%, +8,1%, +5,7%, +1,0%, +1,5%).",
))

# 04 · STATEMENT: la World Investor Week --------------------------------------
slides.append(build_layout_statement(
    "slide-04", N, 4, EB,
    big="5-11",
    big_sub="OTTOBRE 2026",
    body="È proprio su questi temi che si concentra la **World Investor Week**, l’iniziativa "
         "internazionale promossa da **IOSCO** e coordinata in Italia da **Consob**. L’obiettivo è "
         "aumentare la consapevolezza degli investitori e favorire scelte più informate.",
    chips=[("10ª", "edizione, la prima nel 2017"),
           ("100+", "giurisdizioni nel mondo"),
           ("3", "temi: truffe, inganni digitali e resilienza")],
    source="Fonte: IOSCO, comunicato stampa del 22 luglio 2026; worldinvestorweek.org.",
    illu_fn=lambda sid: illu_globe(sid, 790, 330, 160),
))

# 05 · CHART: quanto potrò acquistare -----------------------------------------
slides.append(build_layout_chart(
    "slide-05", N, 5, EB,
    blocks=[
        ("Perché quando parliamo di risparmi, la domanda non dovrebbe essere soltanto:", BODY, 400, SOFT),
        ("“Quanto ho sul conto?”", 44, 700, WHITE),
        ("Ma anche:", BODY, 400, SOFT),
        ("“Quanto potrò acquistare con questi soldi tra 5, 10 o 20 anni?”", 44, 700, AZURE),
    ],
    bars=PROJ,
    legend="Potere d’acquisto di 10.000 € se i prezzi crescono del 2% l’anno",
    source="Simulazione con inflazione costante al 2% annuo, l’obiettivo di medio termine "
           "della BCE. Valori in euro di oggi.",
))

# 06 · SCENARIOS: prima di investire, tre domande -------------------------------
slides.append(build_layout_scenarios(
    "slide-06", N, 6, EB,
    quote="“Quindi bisogna investire?”",
    answer="Non necessariamente.",
    body="Investire significa anche esporsi a determinati rischi. "
         "Non esiste una soluzione valida per tutti.",
    lead="Prima bisogna capire:",
    items=[
        (icon_target, "01 · OBIETTIVO", "A cosa servono quei soldi"),
        (icon_calendar, "02 · TEMPO", "Quando serviranno"),
        (icon_gauge, "03 · RISCHIO", "Quale livello di rischio è coerente con il proprio obiettivo"),
    ],
    closing="Solo dopo ha senso scegliere uno strumento.",
))

# 07 · GRID: per quale obiettivo ------------------------------------------------
slides.append(build_layout_grid(
    "slide-07", N, 7, EB,
    lead="Per questo, una buona pianificazione parte da una domanda diversa:",
    question="“Per quale obiettivo sto mettendo da parte questi soldi?”",
    cards=[(icon_house, "Una casa"), (icon_pension, "La pensione"),
           (icon_project, "Un progetto per il futuro"), (icon_shield, "La conservazione del patrimonio")],
    closing="La destinazione del capitale cambia il modo in cui può essere gestito.",
    stat="16%",
    stat_txt="degli investitori intervistati non sa indicare il proprio obiettivo",
    source="Fonte: Consob, VIII Rapporto sulle scelte di investimento delle famiglie italiane.",
))

# 08 · CTA ---------------------------------------------------------------------
slides.append(build_layout_cta(
    "slide-08",
    lead="La World Investor Week ci ricorda una cosa importante:",
    headline="non decidere come gestire i propri risparmi è comunque una decisione.",
    body="La domanda è: **è una decisione consapevole?**",
    question="Hai mai provato\na dare una data\nai tuoi risparmi?",
    contacts=[(icon_phone, "0141 557260"),
              (icon_mail, "asti4@ageallianz.it"),
              (icon_pin, "Via Alcide De Gasperi 2, Asti")],
    illu_fn=illu_calendar_savings,
))


if __name__ == "__main__":
    pdf, svg, prev = deliver(slides, SLUG, crucial_dir=CRUCIAL)
    print(pdf)
    print(svg)
    print(prev)
