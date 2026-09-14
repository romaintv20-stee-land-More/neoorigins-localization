#!/usr/bin/env python3
"""Refine Mohawk (`moh_ca`) fallbacks with a direct English -> Mohawk NLLB fine-tune."""
from pathlib import Path
import json,re,torch
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
import bootstrap_mohawk as base

ROOT=base.ROOT;ASSETS=base.ASSETS
MODEL_ID="spikes12/nllb-600m-distilled-english-mohawk"
PROTECT_RE=re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b",re.IGNORECASE)
SUSPICIOUS_RE=re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]",re.MULTILINE)
TECHNICAL_CASEFOLD={"neoorigins","origin architect","hud","json","xp","hp","neoforge","minecraft","curseforge"}

def read_json(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def write_json(p,d):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def protected_signature(t):return [x.casefold() if x.casefold() in TECHNICAL_CASEFOLD else x for x in PROTECT_RE.findall(t)]
def sanitize(s,v):
 if not base.placeholder_signature(s):v=base.PLACEHOLDER_RE.sub("",v)
 if "§" not in s:v=v.replace("§","")
 return re.sub(r"[ \t]{2,}"," ",v).strip()
def sources():
 a=read_json(ROOT/"build/moh-discovery-mc-1.21.1/moh_ca_missing_en.json");b=read_json(ROOT/"build/moh-discovery-mc-26.1/moh_ca_missing_en.json");c=read_json(ROOT/"build/moh-discovery-mc-26.2/moh_ca_missing_en.json");common={k:v for k,v in a.items() if b.get(k)==v and c.get(k)==v};d1={k:v for k,v in a.items() if k not in common};d2={k:v for k,v in b.items() if k not in common};d3={k:v for k,v in c.items() if k not in common}
 folders={"medievalorigins":"medievalorigins-upstream-audit","ibarnorigins":"ibarnorigins-upstream-audit","origins_fantasy":"origins-fantasy-upstream-audit","origins_backgrounds":"origins-backgrounds-upstream-audit","origins_backgrounds_two":"origins-more-backgrounds-upstream-audit","origins_backgrounds_iss":"origins-backgrounds-iss-upstream-audit","origins_furries":"origins-furries-upstream-audit","origins_classes_ex":"origins-classes-extended-upstream-audit","origins_classes_iss":"origins-classes-iss-upstream-audit","originsmodernui":"origin-architect-upstream-audit"};addons={n:read_json(ROOT/f"build/{f}/upstream_en_us.json") for n,f in folders.items()};shared=set(addons["origins_backgrounds"]);addons["origins_backgrounds_two"]={k:v for k,v in addons["origins_backgrounds_two"].items() if k not in shared};addons["origins_backgrounds_iss"]={k:v for k,v in addons["origins_backgrounds_iss"].items() if k not in shared};return common,d1,d2,d3,addons

class MT:
 def __init__(self):
  print(f"Loading Mohawk-specific NLLB model: {MODEL_ID}",flush=True)
  self.t=AutoTokenizer.from_pretrained(MODEL_ID)
  self.m=AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID);self.m.eval()
  if hasattr(self.t,"src_lang"):self.t.src_lang="eng_Latn"
  vocab=self.t.get_vocab();unk=getattr(self.t,"unk_token_id",None)
  self.target_id=None;self.target_token=None
  for cand in ("moh_Latn","moh","moh_CA","moh_latn"):
   if cand in vocab:
    tid=self.t.convert_tokens_to_ids(cand)
    if tid is not None and tid!=unk:self.target_id=tid;self.target_token=cand;break
  if self.target_id is None:
   forced=getattr(self.m.generation_config,"forced_bos_token_id",None)
   if forced is not None:
    tok=self.t.convert_ids_to_tokens(forced)
    if tok and tok not in {"eng_Latn","<unk>"}:self.target_id=forced;self.target_token=tok
  print(f"Mohawk NLLB target token: {self.target_token!r} id={self.target_id}",flush=True)
  if self.target_id is None:
   candidates=[x for x in vocab if "moh" in x.lower()]
   raise SystemExit(f"Mohawk-specific model exposes no safe Mohawk target token; candidates={candidates[:20]}")
  smoke=self.batch(["Hello.","Choose your origin.","Night vision off."])
  print(f"Mohawk NLLB smoke: {smoke!r}",flush=True)
  if any(not x.strip() for x in smoke) or all(x.casefold() in {"hello.","choose your origin.","night vision off."} for x in smoke):
   raise SystemExit("Mohawk-specific model failed translation smoke test")
 def batch(self,x):
  if not x:return []
  e=self.t(x,return_tensors="pt",padding=True,truncation=True,max_length=512)
  with torch.inference_mode():g=self.m.generate(**e,forced_bos_token_id=self.target_id,num_beams=4,max_new_tokens=512,early_stopping=True)
  return [v.strip() for v in self.t.batch_decode(g,skip_special_tokens=True)]
 def structural(self,s):
  pieces=PROTECT_RE.split(s);tokens=PROTECT_RE.findall(s);out=list(pieces);idx=[];cores=[];aff={}
  for i,p in enumerate(pieces):
   a=[j for j,c in enumerate(p) if c.isalpha()]
   if a:pre,core,suf=p[:a[0]],p[a[0]:a[-1]+1],p[a[-1]+1:];idx.append(i);cores.append(core);aff[i]=(pre,suf)
  vals=self.batch(cores)
  if len(vals)!=len(idx):raise RuntimeError("Mohawk structural span mismatch")
  for i,core,v in zip(idx,cores,vals):pre,suf=aff[i];out[i]=pre+sanitize(core,v)+suf
  r=[]
  for i,p in enumerate(out):r.append(p);r.append(tokens[i]) if i<len(tokens) else None
  return "".join(r)

def main():
 before_files=sorted(ASSETS.glob("**/lang/moh_ca.json"));
 if len(before_files)!=29:raise SystemExit(f"Expected 29 Mohawk files, found {len(before_files)}")
 before={p:read_json(p) for p in before_files};common,d1,d2,d3,addons=sources();payloads=[common,d1,d2,d3,*addons.values()];unique=sorted({str(v) for p in payloads for v in p.values()});exact=base.build_corpus_map();tr={};direct=[]
 for s in unique:
  if s in base.MANUAL_VALUES:tr[s]=base.MANUAL_VALUES[s]
  elif s in exact:tr[s]=exact[s]
  else:direct.append(s)
 print(f"Mohawk pool: {len(unique)} unique; {len(unique)-len(direct)} corpus/manual; {len(direct)} direct NLLB",flush=True);mt=MT()
 for start in range(0,len(direct),16):
  batch=direct[start:start+16];vals=mt.batch(batch)
  if len(vals)!=len(batch):raise SystemExit("Mohawk NLLB batch size mismatch")
  for s,v in zip(batch,vals):
   v=sanitize(s,v);ok=bool(v) and base.placeholder_signature(s)==base.placeholder_signature(v) and protected_signature(s)==protected_signature(v)
   if not ok:v=sanitize(s,mt.structural(s))
   if not v or base.placeholder_signature(s)!=base.placeholder_signature(v) or protected_signature(s)!=protected_signature(v) or SUSPICIOUS_RE.search(v):raise SystemExit(f"Unsafe Mohawk translation: {s!r}->{v!r}")
   tr[s]=v
  done=min(start+len(batch),len(direct));
  if done%160==0 or done==len(direct):print(f"Direct Mohawk progress: {done}/{len(direct)}",flush=True)
 def pl(x):return {k:tr[str(v)] for k,v in x.items()}
 items=list(pl(common).items());[p.unlink() for p in ASSETS.glob("neoorigins_moh_common_*/lang/moh_ca.json")]
 for i in range((len(items)+149)//150):write_json(ASSETS/f"neoorigins_moh_common_{i+1:02d}/lang/moh_ca.json",dict(items[i*150:(i+1)*150]))
 write_json(ASSETS/"neoorigins_moh_121/lang/moh_ca.json",pl(d1));write_json(ASSETS/"neoorigins_26_1/lang/moh_ca.json",pl(d2));write_json(ASSETS/"neoorigins_26_2/lang/moh_ca.json",pl(d3));[write_json(ASSETS/n/"lang/moh_ca.json",pl(x)) for n,x in addons.items()]
 after={p:read_json(p) for p in sorted(ASSETS.glob("**/lang/moh_ca.json"))};seen={};changed=total=0
 for p,d in after.items():
  if set(before[p])!=set(d):raise SystemExit(f"Mohawk key set changed: {p}")
  for k,v in d.items():total+=1;seen[k]=str(v);changed+=before[p][k]!=v
 source_changed=sum(1 for p in payloads for v in p.values() if tr[str(v)]!=str(v));text="\n".join(str(v) for d in after.values() for v in d.values())
 if source_changed<2500 or seen.get("key.categories.originsmodernui")!="Origin Architect":raise SystemExit("Mohawk final semantic/coverage gate failed")
 red=exact.get("Red");random=seen.get("button.neoorigins.random")
 if red and random and red.casefold()==random.casefold():raise SystemExit("Random translated as Red")
 if seen.get("neoorigins.night_vision.on")==seen.get("neoorigins.night_vision.off"):raise SystemExit("Night vision labels identical")
 print(f"Mohawk refinement passed: {total} values; {changed} bootstrap changes; {source_changed} sources changed",flush=True)
if __name__=="__main__":main()
