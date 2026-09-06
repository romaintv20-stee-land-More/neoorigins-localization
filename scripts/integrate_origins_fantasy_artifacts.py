#!/usr/bin/env python3
import json
from pathlib import Path

LOCALES = ['fr_fr','de_de','es_es','pt_br','nl_nl','it_it','pl_pl','ru_ru','tr_tr','zh_cn']
ARTIFACTS = Path('build/origins-fantasy-artifacts')
TARGET = Path('src/main/resources/resourcepacks/fallback_localizations/assets/origins_fantasy/lang')
TARGET.mkdir(parents=True, exist_ok=True)

ORIGIN_NAMES = {
    'fr_fr': {'Deep Dwarf':'Nain des profondeurs','Fae':'Fae','Goblin':'Gobelin','Elf':'Elfe','Fiend':'Démon','Troll':'Troll','Lich':'Liche','Ogre':'Ogre','Orc':'Orc','Hag':'Sorcière'},
    'de_de': {'Deep Dwarf':'Tiefenzwerg','Fae':'Fee','Goblin':'Goblin','Elf':'Elf','Fiend':'Unhold','Troll':'Troll','Lich':'Lich','Ogre':'Oger','Orc':'Ork','Hag':'Hexe'},
    'es_es': {'Deep Dwarf':'Enano profundo','Fae':'Fae','Goblin':'Goblin','Elf':'Elfo','Fiend':'Demonio','Troll':'Troll','Lich':'Liche','Ogre':'Ogro','Orc':'Orco','Hag':'Bruja'},
    'pt_br': {'Deep Dwarf':'Anão das Profundezas','Fae':'Fae','Goblin':'Goblin','Elf':'Elfo','Fiend':'Demônio','Troll':'Troll','Lich':'Lich','Ogre':'Ogro','Orc':'Orc','Hag':'Bruxa'},
    'nl_nl': {'Deep Dwarf':'Dieptedwerg','Fae':'Fae','Goblin':'Goblin','Elf':'Elf','Fiend':'Duivel','Troll':'Troll','Lich':'Lich','Ogre':'Oger','Orc':'Ork','Hag':'Heks'},
    'it_it': {'Deep Dwarf':'Nano delle profondità','Fae':'Fae','Goblin':'Goblin','Elf':'Elfo','Fiend':'Demone','Troll':'Troll','Lich':'Lich','Ogre':'Ogre','Orc':'Orco','Hag':'Strega'},
    'pl_pl': {'Deep Dwarf':'Krasnolud z głębin','Fae':'Fae','Goblin':'Goblin','Elf':'Elf','Fiend':'Demon','Troll':'Troll','Lich':'Lich','Ogre':'Ogr','Orc':'Ork','Hag':'Wiedźma'},
    'ru_ru': {'Deep Dwarf':'Глубинный дворф','Fae':'Фэй','Goblin':'Гоблин','Elf':'Эльф','Fiend':'Демон','Troll':'Тролль','Lich':'Лич','Ogre':'Огр','Orc':'Орк','Hag':'Ведьма'},
    'tr_tr': {'Deep Dwarf':'Derin Cüce','Fae':'Fae','Goblin':'Goblin','Elf':'Elf','Fiend':'İblis','Troll':'Troll','Lich':'Lich','Ogre':'Ogre','Orc':'Ork','Hag':'Cadı'},
    'zh_cn': {'Deep Dwarf':'深地矮人','Fae':'仙灵','Goblin':'哥布林','Elf':'精灵','Fiend':'恶魔','Troll':'巨魔','Lich':'巫妖','Ogre':'食人魔','Orc':'兽人','Hag':'鬼婆'},
}

TECHNICAL_KEYS = [
    'power.origins_fantasy.aqua_spell_resist_iss.description',
    'power.origins_fantasy.blood_spell_power_iss.description',
    'power.origins_fantasy.deep_vision.description',
    'power.origins_fantasy.ice_spell_resist_iss.description',
    'power.origins_fantasy.spell_power_iss.description',
    'power.origins_fantasy.spell_resist_iss.description',
    'power.origins_fantasy.spell_ward.description',
    'power.origins_fantasy.tnt.description',
    'power.origins_fantasy.dwarf_in_the_depths.description',
]
TECHNICAL = {
    'fr_fr': ["Vous subissez beaucoup plus de dégâts provenant des sorts d'eau. (Nécessite Somake Spells)", "Votre magie de sang est 10 % plus puissante. (Nécessite Iron's Spells n Spellbooks)", "Vous bénéficiez de la vision nocturne sous y=50.", "Votre résistance aux sorts de glace est réduite de 50 %. (Nécessite Iron's Spells n Spellbooks)", "Vos sorts sont 10 % plus puissants. (Nécessite Iron's Spells n Spellbooks)", "Votre résistance aux sorts est augmentée de 25 %. (Nécessite Iron's Spells n Spellbooks)", "Votre résistance aux sorts est augmentée de 10 %. (Nécessite Iron's Spells n Spellbooks)", "Vous savez fabriquer de la TNT avec du gravier.", "Vous minez 10 % plus vite sous y=0."],
    'de_de': ["Du erleidest deutlich mehr Schaden durch Wasserzauber. (Benötigt Somake Spells)", "Deine Blutmagie ist 10 % stärker. (Benötigt Iron's Spells n Spellbooks)", "Unter y=50 erhältst du Nachtsicht.", "Deine Resistenz gegen Eiszauber ist um 50 % verringert. (Benötigt Iron's Spells n Spellbooks)", "Deine Zauber sind 10 % stärker. (Benötigt Iron's Spells n Spellbooks)", "Deine Zauberresistenz ist um 25 % erhöht. (Benötigt Iron's Spells n Spellbooks)", "Deine Zauberresistenz ist um 10 % erhöht. (Benötigt Iron's Spells n Spellbooks)", "Du weißt, wie man TNT mit Kies herstellt.", "Unter y=0 baust du weitere 10 % schneller ab."],
    'es_es': ["Recibes mucho más daño de los hechizos de agua. (Requiere Somake Spells)", "Tu magia de sangre es un 10 % más poderosa. (Requiere Iron's Spells n Spellbooks)", "Obtienes visión nocturna por debajo de y=50.", "Tu resistencia a los hechizos de hielo se reduce un 50 %. (Requiere Iron's Spells n Spellbooks)", "Tus hechizos son un 10 % más poderosos. (Requiere Iron's Spells n Spellbooks)", "Tu resistencia a los hechizos aumenta un 25 %. (Requiere Iron's Spells n Spellbooks)", "Tu resistencia a los hechizos aumenta un 10 %. (Requiere Iron's Spells n Spellbooks)", "Sabes fabricar TNT con grava.", "Minas un 10 % más rápido por debajo de y=0."],
    'pt_br': ["Você recebe muito mais dano de feitiços de água. (Requer Somake Spells)", "Sua magia de sangue é 10 % mais poderosa. (Requer Iron's Spells n Spellbooks)", "Você recebe visão noturna abaixo de y=50.", "Sua resistência a feitiços de gelo é reduzida em 50 %. (Requer Iron's Spells n Spellbooks)", "Seus feitiços são 10 % mais poderosos. (Requer Iron's Spells n Spellbooks)", "Sua resistência a feitiços é 25 % maior. (Requer Iron's Spells n Spellbooks)", "Sua resistência a feitiços é 10 % maior. (Requer Iron's Spells n Spellbooks)", "Você sabe fabricar TNT com cascalho.", "Você minera 10 % mais rápido abaixo de y=0."],
    'nl_nl': ["Je loopt aanzienlijk meer schade op door waterspreuken. (Vereist Somake Spells)", "Je bloedmagie is 10 % krachtiger. (Vereist Iron's Spells n Spellbooks)", "Onder y=50 krijg je nachtzicht.", "Je weerstand tegen ijsspreuken is 50 % lager. (Vereist Iron's Spells n Spellbooks)", "Je spreuken zijn 10 % krachtiger. (Vereist Iron's Spells n Spellbooks)", "Je spreukenweerstand is 25 % hoger. (Vereist Iron's Spells n Spellbooks)", "Je spreukenweerstand is 10 % hoger. (Vereist Iron's Spells n Spellbooks)", "Je weet hoe je TNT met grind maakt.", "Onder y=0 mijn je nog eens 10 % sneller."],
    'it_it': ["Subisci molti più danni dagli incantesimi d'acqua. (Richiede Somake Spells)", "La tua magia del sangue è il 10 % più potente. (Richiede Iron's Spells n Spellbooks)", "Sotto y=50 ottieni la visione notturna.", "La tua resistenza agli incantesimi di ghiaccio è ridotta del 50 %. (Richiede Iron's Spells n Spellbooks)", "I tuoi incantesimi sono il 10 % più potenti. (Richiede Iron's Spells n Spellbooks)", "La tua resistenza agli incantesimi è aumentata del 25 %. (Richiede Iron's Spells n Spellbooks)", "La tua resistenza agli incantesimi è aumentata del 10 %. (Richiede Iron's Spells n Spellbooks)", "Sai come fabbricare TNT con la ghiaia.", "Sotto y=0 scavi un ulteriore 10 % più velocemente."],
    'pl_pl': ["Otrzymujesz znacznie więcej obrażeń od zaklęć wodnych. (Wymaga Somake Spells)", "Twoja magia krwi jest o 10 % silniejsza. (Wymaga Iron's Spells n Spellbooks)", "Poniżej y=50 zyskujesz widzenie w ciemności.", "Twoja odporność na zaklęcia lodowe jest mniejsza o 50 %. (Wymaga Iron's Spells n Spellbooks)", "Twoje zaklęcia są o 10 % potężniejsze. (Wymaga Iron's Spells n Spellbooks)", "Twoja odporność na zaklęcia jest większa o 25 %. (Wymaga Iron's Spells n Spellbooks)", "Twoja odporność na zaklęcia jest większa o 10 %. (Wymaga Iron's Spells n Spellbooks)", "Wiesz, jak wytwarzać TNT ze żwiru.", "Poniżej y=0 kopiesz o kolejne 10 % szybciej."],
    'ru_ru': ["Вы получаете значительно больше урона от водных заклинаний. (Требуется Somake Spells)", "Ваша магия крови на 10 % сильнее. (Требуется Iron's Spells n Spellbooks)", "Ниже y=50 вы получаете ночное зрение.", "Ваша устойчивость к ледяным заклинаниям снижена на 50 %. (Требуется Iron's Spells n Spellbooks)", "Ваши заклинания на 10 % сильнее. (Требуется Iron's Spells n Spellbooks)", "Ваша устойчивость к заклинаниям повышена на 25 %. (Требуется Iron's Spells n Spellbooks)", "Ваша устойчивость к заклинаниям повышена на 10 %. (Требуется Iron's Spells n Spellbooks)", "Вы умеете изготавливать TNT из гравия.", "Ниже y=0 вы добываете блоки ещё на 10 % быстрее."],
    'tr_tr': ["Su büyülerinden önemli ölçüde daha fazla hasar alırsın. (Somake Spells gerektirir)", "Kan büyün %10 daha güçlüdür. (Iron's Spells n Spellbooks gerektirir)", "y=50 seviyesinin altında gece görüşü kazanırsın.", "Buz büyülerine karşı direncin %50 azalır. (Iron's Spells n Spellbooks gerektirir)", "Büyülerin %10 daha güçlüdür. (Iron's Spells n Spellbooks gerektirir)", "Büyü direncin %25 artar. (Iron's Spells n Spellbooks gerektirir)", "Büyü direncin %10 artar. (Iron's Spells n Spellbooks gerektirir)", "Çakılla TNT yapmayı bilirsin.", "y=0 seviyesinin altında %10 daha hızlı maden kazarsın."],
    'zh_cn': ["你受到的水系法术伤害显著增加。（需要 Somake Spells）", "你的血魔法威力提高 10%。（需要 Iron's Spells n Spellbooks）", "在 y=50 以下时，你获得夜视效果。", "你的冰系法术抗性降低 50%。（需要 Iron's Spells n Spellbooks）", "你的法术威力提高 10%。（需要 Iron's Spells n Spellbooks）", "你的法术抗性提高 25%。（需要 Iron's Spells n Spellbooks）", "你的法术抗性提高 10%。（需要 Iron's Spells n Spellbooks）", "你知道如何用砂砾制作 TNT。", "在 y=0 以下时，你的挖掘速度额外提高 10%。"],
}

NAME_FIXES = {
    'fr_fr': {'power.origins_fantasy.tough.name':'Robuste','power.origins_fantasy.goblin_sneaky.name':'Furtif'},
    'de_de': {'power.origins_fantasy.huge.name':'Riesig','power.origins_fantasy.tnt.name':'Bumm!'},
    'es_es': {'power.origins_fantasy.slow.name':'Lento'},
    'pt_br': {'power.origins_fantasy.basher.name':'Golpeador','power.origins_fantasy.beefy.name':'Robusto','power.origins_fantasy.lucky.name':'Sortudo','power.origins_fantasy.rage_top.name':'Fúria Máxima','power.origins_fantasy.sluggish.name':'Lento','power.origins_fantasy.tnt.name':'Boom!','power.origins_fantasy.tough.name':'Resistente','power.origins_fantasy.goblin_sneaky.name':'Furtivo'},
    'nl_nl': {'power.origins_fantasy.basher.name':'Slagkrachtig','power.origins_fantasy.beefy.name':'Robuust','power.origins_fantasy.sluggish.name':'Traag','power.origins_fantasy.tnt.name':'Boem!','power.origins_fantasy.tough.name':'Taai'},
    'it_it': {'power.origins_fantasy.beefy.name':'Robusto','power.origins_fantasy.huge.name':'Enorme','power.origins_fantasy.lucky.name':'Fortunato','power.origins_fantasy.sluggish.name':'Lento','power.origins_fantasy.speedy.name':'Veloce','power.origins_fantasy.tnt.name':'Boom!','power.origins_fantasy.tough.name':'Resistente'},
    'pl_pl': {'power.origins_fantasy.tnt.name':'Bum!'},
    'ru_ru': {'power.origins_fantasy.lucky.name':'Удачливый'},
    'tr_tr': {'power.origins_fantasy.lucky.name':'Şanslı','power.origins_fantasy.sluggish.name':'Hantal','power.origins_fantasy.tnt.name':'Boom!','power.origins_fantasy.goblin_sneaky.name':'Sinsi'},
    'zh_cn': {'power.origins_fantasy.basher.name':'猛击者','power.origins_fantasy.ignore_water.name':'无视水流','power.origins_fantasy.lich_bone_meal.name':'骨粉','power.origins_fantasy.ogre_immunity.name':'摆脱','power.origins_fantasy.plodding.name':'步履沉重','power.origins_fantasy.sluggish.name':'迟缓','power.origins_fantasy.tall.name':'高大','power.origins_fantasy.goblin_sneaky.name':'潜行'},
}

# English source is bundled by the older inspection artifact if present; otherwise use pinned JAR.
en_candidates = list(Path('build').rglob('en_us.json'))
if en_candidates:
    english = json.loads(en_candidates[0].read_text(encoding='utf-8'))
else:
    import io, urllib.request, zipfile
    url = 'https://edge.forgecdn.net/files/8816/068/Origins-Fantasy-1.21.1-NeoOrigins-1.1.3.jar'
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        english = json.loads(z.read('assets/origins_fantasy/lang/en_us.json').decode('utf-8'))

for locale in LOCALES:
    matches = [p for p in ARTIFACTS.rglob(f'{locale}.json') if p.name == f'{locale}.json']
    if len(matches) != 1:
        raise SystemExit(f'Expected exactly one artifact for {locale}, found {matches}')
    data = json.loads(matches[0].read_text(encoding='utf-8'))
    if set(data) != set(english):
        raise SystemExit(f'Key mismatch for {locale}: {len(data)} vs {len(english)}')

    for key, source in english.items():
        if key.startswith('origins.origins_fantasy.') and key.endswith('.name'):
            data[key] = ORIGIN_NAMES[locale].get(source, source)
    for key, value in zip(TECHNICAL_KEYS, TECHNICAL[locale]):
        data[key] = value
    data.update(NAME_FIXES.get(locale, {}))

    if any(not str(v).strip() for v in data.values()):
        raise SystemExit(f'Empty translation in {locale}')
    protected = ('YLEVEL','TNTTOKEN','IRONSSPELLSBOOKS','SOMAKESPELLS')
    if any(any(token in str(v) for token in protected) for v in data.values()):
        raise SystemExit(f'Protected token leak in {locale}')

    (TARGET / f'{locale}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(locale, len(data))
