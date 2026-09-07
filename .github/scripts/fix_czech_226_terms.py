from pathlib import Path

p = Path("src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins_cs_03/lang/cs_cz.json")
s = p.read_text(encoding="utf-8")
replacements = {
    "Můžeš jíst cobblestone, kámen, žulu, diorit, andezit, tuf, deepslate, čedič a blackstone pro skromnou výživu. Lze jíst i dlážděnou hlubinnou břidlici. S plným žaludkem to nesníš.":
        "Můžeš jíst kamení, kámen, žulu, diorit, andezit, tuf, břidlici, čedič, černokámen a břidlicové kamenivo pro skromnou výživu. S plným žaludkem to nesníš.",
    "Můžeš jíst železné ingoty, surové železo, železné nugety, železnou rudu, deepslate železnou rudu a bloky surového železa — pořádné jídlo pro horníka. S plným žaludkem to nesníš.":
        "Můžeš jíst železné ingoty, vytěžené železo, železné nugety, železnou rudu, hlubinnou železnou rudu a bloky vytěženého železa — pořádné jídlo pro horníka. S plným žaludkem to nesníš.",
    "Můžeš jíst zlaté ingoty, surové zlato, zlaté nugety, zlatou rudu, deepslate zlatou rudu, netherovou zlatou rudu a bloky surového zlata — vydatnější potrava. S plným žaludkem to nesníš.":
        "Můžeš jíst zlaté ingoty, vytěžené zlato, zlaté nugety, zlatou rudu, hlubinnou zlatou rudu, netherovou zlatou rudu a bloky vytěženého zlata — vydatnější potrava. S plným žaludkem to nesníš.",
    "Můžeš jíst diamanty, diamantovou rudu a deepslate diamantovou rudu — nasycením srovnatelné se zlatou mrkví. S plným žaludkem to nesníš.":
        "Můžeš jíst diamanty, diamantové ložisko a hlubinné diamantové ložisko — nasycením srovnatelné se zlatou mrkví. S plným žaludkem to nesníš.",
    "Můžeš jíst netheritové ingoty, úlomky a ancient debris — nejbohatší jídlo na světě. S plným žaludkem to nesníš.":
        "Můžeš jíst netheritové ingoty, netheritové plátky a prastarou suť — nejbohatší jídlo na světě. S plným žaludkem to nesníš.",
}
for old, new in replacements.items():
    if s.count(old) != 1:
        raise SystemExit(f"Expected exactly one match for: {old}")
    s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")
