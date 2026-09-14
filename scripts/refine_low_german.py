#!/usr/bin/env python3
"""Refine Low German (`nds_de`) using direct English -> Low German OPUS (`>>nds<<`)."""
from pathlib import Path
import json,re,torch
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
import bootstrap_low_german as base
ROOT=base.ROOT;ASSETS=base.ASSETS;MODEL_ID="Helsinki-NLP/opus-mt-en-mul";TARGET_TOKEN=">>nds<<"
PROTECT_RE=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b")
SUSPICIOUS_RE=re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]",re.MULTILINE)
def rj(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def wj(p,d):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def ps(t):return PROTECT_RE.findall(t)
def sanitize(s,v):
 if not base.placeholder_signature(s):v=base.PLACEHOLDER_RE.sub("",v)
 if "§" not in s:v=v.replace("§","")
 return re.sub(r"[ \t]{2,}"," ",v).strip()
def sources():
 a=rj(ROOT/"build/nds-discovery-mc-1.21.1/nds_de_missing_en.json");b=rj(ROOT/"build/nds-discovery-mc-26.1/nds_de_missing_en.json");c=rj(ROOT/"build/nds-discovery-mc-26.2/nds_de_missing_en.json");common={k:v for k,v in a.items() if b.get(k)==v and c.get(k)==v};d1={k:v for k,v in a.items() if k not in common};d2={k:v for k,v in b.items() if k not in common};d3={k:v for k,v in c.items() if k not in common}
 folders={"medievalorigins":"medievalorigins-upstream-audit","ibarnorigins":"ibarnorigins-upstream-audit","origins_fantasy":"origins-fantasy-upstream-audit","origins_backgrounds":"origins-backgrounds-upstream-audit","origins_backgrounds_two":"origins-more-backgrounds-upstream-audit","origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit","origins_furries":"origins-furries-upstream-audit","origins_classes_ex":"origins-classes-extended-upstream-audit","origins_classes_iss":"origins-classes-iss-upstream-audit","originsmodernui":"origin-architect-upstream-audit"};addons={n:rj(ROOT/f"build/{f}/upstream_en_us.json") for n,f in folders.items()};shared=set(addons["origins_backgrounds"]);addons["origins_backgrounds_two"]={k:v for k,v in addons["origins_backgrounds_two"].items() if k not in shared};addons["origins_backgrounds_iss"]={k:v for k,v in addons["origins_backgrounds_iss"].items() if k not in shared};return common,d1,d2,d3,addons
class MT:
 def __init__(self):self.t=AutoTokenizer.from_pretrained(MODEL_ID);self.m=AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID);self.m.eval();print(f"Low German direct target: {TARGET_TOKEN}",flush=True)
 def batch(self,x):
  if not x:return []
  e=self.t([f"{TARGET_TOKEN} {s}" for s in x],return_tensors="pt",padding=True,truncation=True,max_length=512)
  with torch.inference_mode():g=self.m.generate(**e,num_beams=2,max_new_tokens=512,early_stopping=True)
  return [v.strip() for v in self.t.batch_decode(g,skip_special_tokens=True)]
 def structural(self,s):
  pieces=PROTECT_RE.split(s);tokens=PROTECT_RE.findall(s);out=list(pieces);idx=[];cores=[];aff={}
  for i,p in enumerate(pieces):
   a=[j for j,c in enumerate(p) if c.isalpha()]
   if a:pre,core,suf=p[:a[0]],p[a[0]:a[-1]+1],p[a[-1]+1:];idx.append(i);cores.append(core);aff[i]=(pre,suf)
  vals=self.batch(cores)
  for i,core,v in zip(idx,cores,vals):pre,suf=aff[i];out[i]=pre+sanitize(core,v)+suf
  r=[]
  for i,p in enumerate(out):r.append(p);r.append(tokens[i]) if i<len(tokens) else None
  return "".join(r)
def main():
 before_files=sorted(ASSETS.glob("**/lang/nds_de.json"));
 if len(before_files)!=29:raise SystemExit(f"Expected 29 Low German files, found {len(before_files)}")
 before={p:rj(p) for p in before_files};common,d1,d2,d3,addons=sources();payloads=[common,d1,d2,d3,*addons.values()];unique=sorted({str(v) for p in payloads for v in p.values()});exact=base.build_corpus_map();tr={};direct=[]
 for s in unique:
  if s in base.MANUAL_VALUES:tr[s]=base.MANUAL_VALUES[s]
  elif s in exact:tr[s]=exact[s]
  else:direct.append(s)
 print(f"Low German pool: {len(unique)} unique; {len(unique)-len(direct)} corpus/manual; {len(direct)} direct OPUS",flush=True);mt=MT()
 for start in range(0,len(direct),24):
  batch=direct[start:start+24];vals=mt.batch(batch)
  for s,v in zip(batch,vals):
   v=sanitize(s,v);ok=bool(v) and base.placeholder_signature(s)==base.placeholder_signature(v) and ps(s)==ps(v)
   if not ok:v=sanitize(s,mt.structural(s))
   if not v or base.placeholder_signature(s)!=base.placeholder_signature(v) or ps(s)!=ps(v) or SUSPICIOUS_RE.search(v):raise SystemExit(f"Unsafe Low German translation: {s!r}->{v!r}")
   tr[s]=v
  done=min(start+len(batch),len(direct));
  if done%240==0 or done==len(direct):print(f"Direct Low German progress: {done}/{len(direct)}",flush=True)
 def pl(x):return {k:tr[str(v)] for k,v in x.items()}
 items=list(pl(common).items());[p.unlink() for p in ASSETS.glob("neoorigins_nds_common_*/lang/nds_de.json")]
 for i in range((len(items)+149)//150):wj(ASSETS/f"neoorigins_nds_common_{i+1:02d}/lang/nds_de.json",dict(items[i*150:(i+1)*150]))
 wj(ASSETS/"neoorigins_nds_121/lang/nds_de.json",pl(d1));wj(ASSETS/"neoorigins_26_1/lang/nds_de.json",pl(d2));wj(ASSETS/"neoorigins_26_2/lang/nds_de.json",pl(d3));[wj(ASSETS/n/"lang/nds_de.json",pl(x)) for n,x in addons.items()]
 after={p:rj(p) for p in sorted(ASSETS.glob("**/lang/nds_de.json"))};seen={};changed=total=0
 for p,d in after.items():
  if set(before[p])!=set(d):raise SystemExit(f"Low German key set changed: {p}")
  for k,v in d.items():total+=1;seen[k]=str(v);changed+=before[p][k]!=v
 changed_src=sum(1 for p in payloads for v in p.values() if tr[str(v)]!=str(v));text="\n".join(str(v) for d in after.values() for v in d.values())
 if TARGET_TOKEN in text or changed_src<2500 or seen.get("key.categories.originsmodernui")!="Origin Architect":raise SystemExit("Low German final gate failed")
 red=exact.get("Red");random=seen.get("button.neoorigins.random")
 if red and random and red.casefold()==random.casefold():raise SystemExit("Random translated as Red")
 if seen.get("neoorigins.night_vision.on")==seen.get("neoorigins.night_vision.off"):raise SystemExit("Night vision labels identical")
 print(f"Low German refinement passed: {total} values; {changed} bootstrap changes; {changed_src} sources changed",flush=True)
if __name__=="__main__":main()
