#!/usr/bin/env python3
"""Bootstrap Mohawk (`moh_ca`) fallbacks from English.
Exact Minecraft whole-string matches first; unmatched English stays for direct
OPUS `en -> moh`. No pivot and no isolated-word projection.
"""
from collections import Counter,defaultdict
from pathlib import Path
import json,re,urllib.request
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
PLACEHOLDER_RE=re.compile(r"%(?:\d+\$)?[sdif]");REF="83af272f5a618b287781ee9ce2a48cfc8f47dd61";BASE=f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{REF}/java";MANUAL_VALUES={"Origin Architect":"Origin Architect"}
def read_json(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def write_json(p,d):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def fetch(name):
 req=urllib.request.Request(f"{BASE}/{name}.json",headers={"User-Agent":"NeoOrigins-Mohawk-Bootstrap"});
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
def placeholder_signature(t):return sorted(PLACEHOLDER_RE.findall(t))
def build_corpus_map():
 en,moh=fetch("en_us"),fetch("moh_ca");votes=defaultdict(Counter);rejected=unchanged=0;shared=sorted(set(en)&set(moh))
 for k in shared:
  s,t=str(en[k]),str(moh[k])
  if s.casefold()==t.casefold():unchanged+=1;continue
  if not s.strip() or not t.strip() or placeholder_signature(s)!=placeholder_signature(t):rejected+=1;continue
  votes[s][t]+=1
 exact={};ambiguous=0
 for s,c in votes.items():
  t,n=c.most_common(1)[0];total=sum(c.values())
  if n/total>=.80:exact[s]=t
  else:ambiguous+=1
 print(f"Minecraft Mohawk corpus: {len(shared)} aligned; {rejected} rejected; {unchanged} unchanged; {len(exact)} exact; {ambiguous} ambiguous")
 return exact
def translate_payload(src,exact):
 out={}
 for k,raw in src.items():
  s=str(raw);t=MANUAL_VALUES.get(s,exact.get(s,s))
  if placeholder_signature(s)!=placeholder_signature(t):raise RuntimeError(f"Mohawk placeholder mismatch: {s!r}->{t!r}")
  out[k]=t
 return out
def main():
 n121=read_json(ROOT/"build/moh-discovery-mc-1.21.1/moh_ca_missing_en.json");n261=read_json(ROOT/"build/moh-discovery-mc-26.1/moh_ca_missing_en.json");n262=read_json(ROOT/"build/moh-discovery-mc-26.2/moh_ca_missing_en.json")
 common={k:v for k,v in n121.items() if n261.get(k)==v and n262.get(k)==v};d121={k:v for k,v in n121.items() if k not in common};d261={k:v for k,v in n261.items() if k not in common};d262={k:v for k,v in n262.items() if k not in common}
 folders={"medievalorigins":"medievalorigins-upstream-audit","ibarnorigins":"ibarnorigins-upstream-audit","origins_fantasy":"origins-fantasy-upstream-audit","origins_backgrounds":"origins-backgrounds-upstream-audit","origins_backgrounds_two":"origins-more-backgrounds-upstream-audit","origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit","origins_furries":"origins-furries-upstream-audit","origins_classes_ex":"origins-classes-extended-upstream-audit","origins_classes_iss":"origins-classes-iss-upstream-audit","originsmodernui":"origin-architect-upstream-audit"}
 addons={ns:read_json(ROOT/f"build/{folder}/upstream_en_us.json") for ns,folder in folders.items()};shared=set(addons["origins_backgrounds"]);addons["origins_backgrounds_two"]={k:v for k,v in addons["origins_backgrounds_two"].items() if k not in shared};addons["origins_backgrounds_iss"]={k:v for k,v in addons["origins_backgrounds_iss"].items() if k not in shared}
 exact=build_corpus_map();items=list(translate_payload(common,exact).items())
 for p in ASSETS.glob("neoorigins_moh_common_*/lang/moh_ca.json"):p.unlink()
 for i in range((len(items)+149)//150):write_json(ASSETS/f"neoorigins_moh_common_{i+1:02d}/lang/moh_ca.json",dict(items[i*150:(i+1)*150]))
 write_json(ASSETS/"neoorigins_moh_121/lang/moh_ca.json",translate_payload(d121,exact));write_json(ASSETS/"neoorigins_26_1/lang/moh_ca.json",translate_payload(d261,exact));write_json(ASSETS/"neoorigins_26_2/lang/moh_ca.json",translate_payload(d262,exact))
 for ns,src in addons.items():write_json(ASSETS/ns/"lang/moh_ca.json",translate_payload(src,exact))
 files=sorted(ASSETS.glob("**/lang/moh_ca.json"));sources=[common,d121,d261,d262,*addons.values()];total=sum(len(x) for x in sources);hits=sum(1 for x in sources for v in x.values() if str(v) in exact or str(v) in MANUAL_VALUES)
 if len(files)!=29:raise RuntimeError(f"Expected 29 Mohawk files, found {len(files)}")
 print(f"Mohawk bootstrap: 29 files; exact/manual {hits}/{total}; {total-hits} remain for direct OPUS")
if __name__=="__main__":main()
