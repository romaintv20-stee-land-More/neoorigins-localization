#!/usr/bin/env python3
"""Bootstrap Low German (`nds_de`) fallbacks from English.
Exact Minecraft whole-string matches first; unmatched English stays for direct
OPUS `en -> nds`. Never pivot through Standard German.
"""
from collections import Counter,defaultdict
from pathlib import Path
import json,re,urllib.request
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/"src/main/resources/resourcepacks/fallback_localizations/assets"
PLACEHOLDER_RE=re.compile(r"%(?:\d+\$)?[sdif]");REF="83af272f5a618b287781ee9ce2a48cfc8f47dd61";BASE=f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{REF}/java";MANUAL_VALUES={"Origin Architect":"Origin Architect"}
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def wj(p,d):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def fetch(name):
 req=urllib.request.Request(f"{BASE}/{name}.json",headers={"User-Agent":"NeoOrigins-Low-German-Bootstrap"});
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
def placeholder_signature(t):return sorted(PLACEHOLDER_RE.findall(t))
def build_corpus_map():
 en,nds=fetch("en_us"),fetch("nds_de");votes=defaultdict(Counter);rej=unch=0;shared=sorted(set(en)&set(nds))
 for k in shared:
  s,t=str(en[k]),str(nds[k])
  if s.casefold()==t.casefold():unch+=1;continue
  if not s.strip() or not t.strip() or placeholder_signature(s)!=placeholder_signature(t):rej+=1;continue
  votes[s][t]+=1
 exact={};amb=0
 for s,c in votes.items():
  t,n=c.most_common(1)[0];total=sum(c.values())
  if n/total>=.80:exact[s]=t
  else:amb+=1
 print(f"Minecraft Low German corpus: {len(shared)} aligned; {rej} rejected; {unch} unchanged; {len(exact)} exact; {amb} ambiguous")
 return exact
def pl(src,exact):
 out={}
 for k,raw in src.items():
  s=str(raw);t=MANUAL_VALUES.get(s,exact.get(s,s))
  if placeholder_signature(s)!=placeholder_signature(t):raise RuntimeError(f"Low German placeholder mismatch: {s!r}->{t!r}")
  out[k]=t
 return out
def main():
 a=rj(ROOT/"build/nds-discovery-mc-1.21.1/nds_de_missing_en.json");b=rj(ROOT/"build/nds-discovery-mc-26.1/nds_de_missing_en.json");c=rj(ROOT/"build/nds-discovery-mc-26.2/nds_de_missing_en.json");common={k:v for k,v in a.items() if b.get(k)==v and c.get(k)==v};d1={k:v for k,v in a.items() if k not in common};d2={k:v for k,v in b.items() if k not in common};d3={k:v for k,v in c.items() if k not in common}
 folders={"medievalorigins":"medievalorigins-upstream-audit","ibarnorigins":"ibarnorigins-upstream-audit","origins_fantasy":"origins-fantasy-upstream-audit","origins_backgrounds":"origins-backgrounds-upstream-audit","origins_backgrounds_two":"origins-more-backgrounds-upstream-audit","origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit","origins_furries":"origins-furries-upstream-audit","origins_classes_ex":"origins-classes-extended-upstream-audit","origins_classes_iss":"origins-classes-iss-upstream-audit","originsmodernui":"origin-architect-upstream-audit"};addons={n:rj(ROOT/f"build/{f}/upstream_en_us.json") for n,f in folders.items()};shared=set(addons["origins_backgrounds"]);addons["origins_backgrounds_two"]={k:v for k,v in addons["origins_backgrounds_two"].items() if k not in shared};addons["origins_backgrounds_iss"]={k:v for k,v in addons["origins_backgrounds_iss"].items() if k not in shared}
 exact=build_corpus_map();items=list(pl(common,exact).items());[p.unlink() for p in ASSETS.glob("neoorigins_nds_common_*/lang/nds_de.json")]
 for i in range((len(items)+149)//150):wj(ASSETS/f"neoorigins_nds_common_{i+1:02d}/lang/nds_de.json",dict(items[i*150:(i+1)*150]))
 wj(ASSETS/"neoorigins_nds_121/lang/nds_de.json",pl(d1,exact));wj(ASSETS/"neoorigins_26_1/lang/nds_de.json",pl(d2,exact));wj(ASSETS/"neoorigins_26_2/lang/nds_de.json",pl(d3,exact));[wj(ASSETS/n/"lang/nds_de.json",pl(x,exact)) for n,x in addons.items()]
 files=sorted(ASSETS.glob("**/lang/nds_de.json"));sources=[common,d1,d2,d3,*addons.values()];total=sum(len(x) for x in sources);hits=sum(1 for x in sources for v in x.values() if str(v) in exact or str(v) in MANUAL_VALUES)
 if len(files)!=29:raise RuntimeError(f"Expected 29 Low German files, found {len(files)}")
 print(f"Low German bootstrap: 29 files; exact/manual {hits}/{total}; {total-hits} remain for direct OPUS")
if __name__=="__main__":main()
