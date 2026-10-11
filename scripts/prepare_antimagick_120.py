#!/usr/bin/env python3
"""Integrate Anti Magick: NeoOrigins 0.1.2 (MIT) with 93-locales coverage.

Only two labels exist upstream. Russian is supplied by the upstream mod and
must not be overwritten. Regional/dialect labels are community-review candidates.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMESPACE="antimagick_neoorigins"
BASE=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
CODES=sorted(p.stem for p in (BASE/"origins_furries/lang").glob("*.json"))
# Source English strings:
# category.antimagick_neoorigins.active_powers = NeoOrigins active powers
# category.antimagick_neoorigins.summons = NeoOrigins summons
# Values below preserve the proper name NeoOrigins.
ROWS="""
af_za|Aktiewe kragte van NeoOrigins|Oproepings van NeoOrigins
ar_sa|قدرات NeoOrigins النشطة|استدعاءات NeoOrigins
ast_es|Poderes activos de NeoOrigins|Invocaciones de NeoOrigins
az_az|NeoOrigins aktiv gücləri|NeoOrigins çağırışları
ba_ru|NeoOrigins әүҙем көстәре|NeoOrigins саҡырыуҙары
bar|Aktive Kräfte vo NeoOrigins|Beschwörungen vo NeoOrigins
be_by|Актыўныя здольнасці NeoOrigins|Заклікі NeoOrigins
bg_bg|Активни сили на NeoOrigins|Призовавания на NeoOrigins
br_fr|Galloudoù oberiant NeoOrigins|Galvadennoù NeoOrigins
brb|Actieve krachten van NeoOrigins|Oproepingen van NeoOrigins
bs_ba|Aktivne moći NeoOrigins|Prizivanja NeoOrigins
ca_es|Poders actius de NeoOrigins|Invocacions de NeoOrigins
cs_cz|Aktivní schopnosti NeoOrigins|Vyvolávání NeoOrigins
cv_cu|NeoOrigins активлă вăйĕсем|NeoOrigins чĕнӳсем
cy_gb|Pwerau gweithredol NeoOrigins|Gwysiadau NeoOrigins
da_dk|Aktive kræfter fra NeoOrigins|Påkaldelser fra NeoOrigins
de_de|Aktive Kräfte von NeoOrigins|Beschwörungen von NeoOrigins
el_gr|Ενεργές δυνάμεις του NeoOrigins|Επικλήσεις του NeoOrigins
eo_uy|Aktivaj povoj de NeoOrigins|Alvokoj de NeoOrigins
es_es|Poderes activos de NeoOrigins|Invocaciones de NeoOrigins
esan|Poderes activos de NeoOrigins|Invocacione de NeoOrigins
et_ee|NeoOriginsi aktiivsed võimed|NeoOriginsi väljakutsumised
eu_es|NeoOrigins-en botere aktiboak|NeoOrigins-en deialdiak
fa_ir|قدرت‌های فعال NeoOrigins|احضارهای NeoOrigins
fi_fi|NeoOriginsin aktiiviset voimat|NeoOriginsin kutsunnat
fil_ph|Mga aktibong kapangyarihan ng NeoOrigins|Mga pagpapatawag ng NeoOrigins
fo_fo|Virknir máttir hjá NeoOrigins|Útkallingar hjá NeoOrigins
fr_fr|Pouvoirs actifs de NeoOrigins|Invocations de NeoOrigins
fra_de|Aktive Kräft vo NeoOrigins|Beschwörungen vo NeoOrigins
fur_it|Podês atîfs di NeoOrigins|Invocazions di NeoOrigins
fy_nl|Aktive krêften fan NeoOrigins|Opropingen fan NeoOrigins
ga_ie|Cumhachtaí gníomhacha NeoOrigins|Toghairmeacha NeoOrigins
gd_gb|Cumhachdan gnìomhach NeoOrigins|Gairmean NeoOrigins
gl_es|Poderes activos de NeoOrigins|Invocacións de NeoOrigins
go_fr|Pouairrs actifs de NeoOrigins|Invocacions de NeoOrigins
gv_im|Pooaraghyn breeoil NeoOrigins|Eamaghyn NeoOrigins
haw_us|Nā mana hana o NeoOrigins|Nā kāhea a NeoOrigins
he_il|כוחות פעילים של NeoOrigins|זימונים של NeoOrigins
hi_in|NeoOrigins की सक्रिय शक्तियाँ|NeoOrigins के आह्वान
hr_hr|Aktivne moći NeoOriginsa|Prizivanja NeoOriginsa
hu_hu|A NeoOrigins aktív képességei|A NeoOrigins idézései
hy_am|NeoOrigins-ի ակտիվ ուժերը|NeoOrigins-ի կանչերը
id_id|Kekuatan aktif NeoOrigins|Pemanggilan NeoOrigins
ig_ng|Ike NeoOrigins na-arụ ọrụ|Oku NeoOrigins
io_en|Aktiva povori di NeoOrigins|Voki di NeoOrigins
is_is|Virkir kraftar NeoOrigins|Ákallanir NeoOrigins
isv|Aktivne moči NeoOrigins|Prizyvanja NeoOrigins
it_it|Poteri attivi di NeoOrigins|Evocazioni di NeoOrigins
ja_jp|NeoOriginsのアクティブ能力|NeoOriginsの召喚
ka_ge|NeoOrigins-ის აქტიური ძალები|NeoOrigins-ის გამოძახებები
kab_kab|Tizemmar tiruradin n NeoOrigins|Asiwel n NeoOrigins
kk_kz|NeoOrigins белсенді қабілеттері|NeoOrigins шақырулары
kn_in|NeoOrigins ಸಕ್ರಿಯ ಶಕ್ತಿಗಳು|NeoOrigins ಆವಾಹನೆಗಳು
ko_kr|NeoOrigins 활성 능력|NeoOrigins 소환
ksh|Aktive Krääfte vun NeoOrigins|Beschwörunge vun NeoOrigins
ky_kg|NeoOrigins активдүү күчтөрү|NeoOrigins чакыруусу
lb_lu|Aktiv Kräfte vun NeoOrigins|Beschwéierunge vun NeoOrigins
li_li|Actieve krach van NeoOrigins|Oproopinge van NeoOrigins
lo_la|ພະລັງທີ່ໃຊ້ງານຂອງ NeoOrigins|ການອັນເຊີນຂອງ NeoOrigins
lt_lt|Aktyvios „NeoOrigins“ galios|„NeoOrigins“ iškvietimai
lv_lv|NeoOrigins aktīvās spējas|NeoOrigins izsaukumi
mk_mk|Активни моќи на NeoOrigins|Повикувања на NeoOrigins
mn_mn|NeoOrigins идэвхтэй хүчнүүд|NeoOrigins дуудлагууд
mr_in|NeoOrigins च्या सक्रिय शक्ती|NeoOrigins चे आवाहन
ms_my|Kuasa aktif NeoOrigins|Seruan NeoOrigins
mt_mt|Setgħat attivi ta' NeoOrigins|Taħrikiet ta' NeoOrigins
nds_de|Aktive Kräften vun NeoOrigins|Beschwören vun NeoOrigins
nl_nl|Actieve krachten van NeoOrigins|Oproepingen van NeoOrigins
nn_no|Aktive krefter frå NeoOrigins|Tilkallingar frå NeoOrigins
no_no|Aktive krefter fra NeoOrigins|Tilkallinger fra NeoOrigins
oc_fr|Poders actius de NeoOrigins|Invocacions de NeoOrigins
pl_pl|Aktywne moce NeoOrigins|Przywołania NeoOrigins
pt_br|Poderes ativos de NeoOrigins|Invocações de NeoOrigins
ro_ro|Puteri active NeoOrigins|Invocări NeoOrigins
ru_ru|Активные способности NeoOrigins|Призывы NeoOrigins
se_no|NeoOrigins doaibmi fámut|NeoOrigins gohččumat
sk_sk|Aktívne schopnosti NeoOrigins|Vyvolávania NeoOrigins
sl_si|Aktivne moči NeoOrigins|Priklici NeoOrigins
so_so|Awoodaha firfircoon ee NeoOrigins|U yeerista NeoOrigins
sq_al|Fuqitë aktive të NeoOrigins|Thirrjet e NeoOrigins
sr_cs|Aktivne moći NeoOrigins|Prizivanja NeoOrigins
sr_sp|Активне моћи NeoOrigins|Призивања NeoOrigins
sv_se|Aktiva krafter från NeoOrigins|Åkallanden från NeoOrigins
ta_in|NeoOrigins செயலில் உள்ள சக்திகள்|NeoOrigins அழைப்புகள்
th_th|พลังที่ใช้งานของ NeoOrigins|การอัญเชิญของ NeoOrigins
tr_tr|NeoOrigins etkin güçleri|NeoOrigins çağırmaları
tt_ru|NeoOrigins актив көчләре|NeoOrigins чакырулары
uk_ua|Активні здібності NeoOrigins|Закликання NeoOrigins
uz_uz|NeoOrigins faol kuchlari|NeoOrigins chaqiruvlari
vi_vn|Sức mạnh chủ động của NeoOrigins|Triệu hồi của NeoOrigins
yo_ng|Àwọn agbára NeoOrigins tí ń ṣiṣẹ́|Àwọn ìpè NeoOrigins
zh_cn|NeoOrigins 主动能力|NeoOrigins 召唤
zh_tw|NeoOrigins 主動能力|NeoOrigins 召喚
"""
mapx={}
for raw in ROWS.strip().splitlines():
    code,a,b=raw.split("|")
    assert code not in mapx,(code,'duplicate')
    mapx[code]={
       "category.antimagick_neoorigins.active_powers":a,
       "category.antimagick_neoorigins.summons":b
    }
assert set(mapx)==set(CODES),(len(mapx),len(CODES),set(CODES)-set(mapx),set(mapx)-set(CODES))
en={
 "category.antimagick_neoorigins.active_powers":"NeoOrigins active powers",
 "category.antimagick_neoorigins.summons":"NeoOrigins summons"
}
# The mod itself includes Russian, which is more authoritative; never duplicate it.
lang=BASE/NAMESPACE/"lang"
lang.mkdir(parents=True,exist_ok=True)
for code,values in mapx.items():
    if code=="ru_ru":
        continue
    p=lang/(code+".json")
    assert not p.exists(),f'Existing file would be replaced: {p}'
    assert set(values)==set(en)
    assert all("NeoOrigins" in v for v in values.values()),code
    p.write_text(json.dumps(values,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
catalog=ROOT/"catalog.json"
data=json.loads(catalog.read_text(encoding="utf-8"))
assert "antimagick_neoorigins" not in [x['id'] for x in data['supported_projects']]
existing=data["supported_projects"][7]
languages={}
for code in CODES:
    old=existing["languages"][code]
    languages[code]={
      "name":old.get("name",code),
      "status":"official_upstream" if code=="ru_ru" else "supported",
      **({} if code=="ru_ru" else {"file":f"src/main/resources/resourcepacks/fallback_localizations/assets/{NAMESPACE}/lang/{code}.json"})
    }
data["supported_projects"].append({
 "id":NAMESPACE,"name":"Anti Magick: NeoOrigins","author":"Anti Magick contributors",
 "namespace":NAMESPACE,
 "modrinth":"https://modrinth.com/mod/anti-magick-neoorigins",
 "license":{"code_and_content":"MIT","attribution_required":True},
 "compatibility":{
   "method":"Optional integration between Anti Magick and NeoOrigins",
   "version":"0.1.2 / Minecraft 1.21.1",
   "minecraft":["1.21.1"],"loader":["neoforge"],
   "modrinth_project_id":"Ef2BIfFi","modrinth_version_id":"PkvY4hbS",
   "required_mods":["antimagick","neoorigins"],
   "in_game_validation":"pending",
   "integration_status":"supported",
   "note":"Two English strings: 92 low-priority fallback locales; Russian is provided upstream. Dialect translations are provisional and require community QA; no 26.x add-on compatibility."
 },
 "coverage":{"source_keys":2,"fallback_keys_per_locale":2,"upstream_locales":["en_us","ru_ru"]},
 "languages":languages
})
data["project"]["builds"]["1.21.1"]["included_projects"].append(NAMESPACE)
data["project"]["release_notes"]["addon_changes"][NAMESPACE]={
 "from":None,"to":"0.1.2","new_english_keys":2,
 "localized_fallback_locales":92,"official_upstream_locales":["ru_ru"]
}
catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
build=ROOT/"build.gradle"
s=build.read_text(encoding="utf-8")
anchor="        exclude 'resourcepacks/fallback_localizations/assets/pathfinder_origins/**'"
assert anchor in s
s=s.replace(anchor,anchor+"\n        exclude 'resourcepacks/fallback_localizations/assets/antimagick_neoorigins/**'")
build.write_text(s,encoding="utf-8")
print(f"Anti Magick: NeoOrigins 0.1.2: {len(mapx)-1} fallback files, {len(mapx)*2} strings available including upstream Russian")
