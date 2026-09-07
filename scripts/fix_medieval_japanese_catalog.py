#!/usr/bin/env python3
from pathlib import Path
import json
p = Path('catalog.json')
data = json.loads(p.read_text(encoding='utf-8'))
for project in data.get('supported_projects', []):
    if project.get('id') == 'medievalorigins':
        ja = project.get('languages', {}).get('ja_jp', {})
        ja.pop('file', None)
        ja['files_glob'] = 'src/main/resources/resourcepacks/fallback_localizations/assets/medievalorigins_ja_*/lang/ja_jp.json'
        break
else:
    raise SystemExit('medievalorigins not found')
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
