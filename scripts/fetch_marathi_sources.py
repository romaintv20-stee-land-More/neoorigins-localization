#!/usr/bin/env python3
"""Fetch exact upstream English inventories for Minecraft and supported add-ons."""
from pathlib import Path
import concurrent.futures,hashlib,json,subprocess,sys,time,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build/marathi-sources"
OUT.mkdir(parents=True,exist_ok=True)
def req(url):
    r=urllib.request.Request(url,headers={"User-Agent":"NeoOrigins-Localization/1.1.1 (Marathi integration)"})
    return urllib.request.urlopen(r,timeout=75)
def minecraft():
    manifest=json.load(req("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"))
    versions={v["id"]:v["url"] for v in manifest["versions"]}
    for version in ("1.21.1","26.1.2","26.2"):
        dst=OUT/f"minecraft_{version}_en_us.json"
        if dst.exists():
            print("Cached Minecraft",version,len(json.loads(dst.read_text(encoding="utf-8"))),flush=True)
            continue
        if version not in versions:raise RuntimeError(f"No official Minecraft version {version} in manifest")
        metadata=json.load(req(versions[version]))
        jarurl=metadata["downloads"]["client"]["url"]
        jarpath=OUT/f"minecraft_{version}.jar"
        if not jarpath.exists():
            with req(jarurl) as src,jarpath.open("wb") as target:
                import shutil;shutil.copyfileobj(src,target)
        expected=metadata["downloads"]["client"]["sha1"]
        got=hashlib.sha1(jarpath.read_bytes()).hexdigest()
        if got!=expected:raise RuntimeError(f"Minecraft {version} JAR hash mismatch {got} != {expected}")
        with zipfile.ZipFile(jarpath) as archive:
            en=json.loads(archive.read("assets/minecraft/lang/en_us.json"))
        dst.write_text(json.dumps(en,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        jarpath.unlink()
        print("Official Minecraft",version,len(en),"keys",flush=True)
def addon(script):
    scriptpath=ROOT/"scripts"/script
    name=script.removeprefix("audit_").removesuffix("_upstream.py")
    logfile=OUT/f"audit_{name}.log"
    try:
        proc=subprocess.run([sys.executable,str(scriptpath)],cwd=ROOT,capture_output=True,text=True,
            encoding="utf-8",errors="replace",timeout=180)
        logfile.write_text(proc.stdout+"\n"+proc.stderr,encoding="utf-8")
        print("ADDON",name,"OK" if proc.returncode==0 else f"CODE {proc.returncode}",
              "source files",len(list((ROOT/"build").glob("*/upstream_en_us.json"))),flush=True)
        return name,proc.returncode
    except Exception as e:
        logfile.write_text(str(e),encoding="utf-8")
        print("ADDON",name,"ERROR",repr(e),flush=True)
        return name,-1
def main():
    scripts=["audit_medievalorigins_upstream.py","audit_ibarnorigins_upstream.py",
        "audit_origins_fantasy_upstream.py","audit_origins_backgrounds_upstream.py",
        "audit_origins_more_backgrounds_upstream.py","audit_origins_backgrounds_iss_upstream.py",
        "audit_origins_furries_upstream.py","audit_origins_classes_extended_upstream.py",
        "audit_origins_classes_iss_upstream.py","audit_origin_architect_upstream.py",
        "audit_pathfinder_origins_upstream.py"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        future=[pool.submit(minecraft)]
        future.extend(pool.submit(addon,s) for s in scripts)
        for f in concurrent.futures.as_completed(future):
            try:f.result()
            except Exception as e:print("SOURCE FETCH ERROR",repr(e),flush=True)
    print("Finished source retrieval; inspect audit logs for nonzero codes.",flush=True)
if __name__=="__main__":main()
