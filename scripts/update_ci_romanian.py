#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/build-0.9.0.yml"
text = WORKFLOW.read_text(encoding="utf-8")

if "Strict audit Romanian NeoOrigins coverage" in text:
    print("Romanian CI integration already present")
    raise SystemExit(0)

# Matrix fields, packaging switch and expected counts. The 1.21.1 JAR contains
# only 9 Romanian add-on fallback files because Origin Architect already ships
# 22/22 Romanian strings officially upstream.
for old, new in [
    ("            norwegian_extra_namespace: 'neoorigins_no_121'\n", "            norwegian_extra_namespace: 'neoorigins_no_121'\n            romanian_extra_namespace: 'neoorigins_ro_121'\n"),
    ("            norwegian_extra_namespace: 'neoorigins_26_1'\n", "            norwegian_extra_namespace: 'neoorigins_26_1'\n            romanian_extra_namespace: 'neoorigins_26_1'\n"),
    ("            norwegian_extra_namespace: 'neoorigins_26_2'\n", "            norwegian_extra_namespace: 'neoorigins_26_2'\n            romanian_extra_namespace: 'neoorigins_26_2'\n"),
    ("            include_norwegian_121_translations: true\n", "            include_norwegian_121_translations: true\n            include_romanian_121_translations: true\n"),
    ("            include_norwegian_121_translations: false\n", "            include_norwegian_121_translations: false\n            include_romanian_121_translations: false\n"),
    ("            expected_norwegian_files: '27'\n", "            expected_norwegian_files: '27'\n            expected_romanian_files: '26'\n"),
    ("            expected_norwegian_files: '17'\n", "            expected_norwegian_files: '17'\n            expected_romanian_files: '17'\n"),
]:
    if old not in text:
        raise RuntimeError(f"Romanian CI matrix anchor missing: {old!r}")
    text = text.replace(old, new)

marker = "\n      - name: Restrict add-on audits to Danish\n"
block = """
      - name: Strict audit Romanian NeoOrigins coverage
        run: |
          python3 scripts/audit_neoorigins_upstream.py \\
            --ref '${{ matrix.upstream_ref }}' \\
            --output 'build/romanian-audit-${{ matrix.target }}' \\
            --locale ro_ro \\
            --fallback-namespace-glob 'neoorigins_ro_common_*' \\
            --extra-namespace '${{ matrix.romanian_extra_namespace }}' \\
            --fail-on-overlap --fail-on-missing --fail-on-placeholders
"""
if marker not in text:
    raise RuntimeError("Romanian NeoOrigins insertion marker missing")
text = text.replace(marker, "\n" + block + marker, 1)

validate_marker = "\n      - name: Validate localization files\n"
addon_block = """
      - name: Restrict add-on audits to Romanian
        if: matrix.include_addon_translations == true
        run: |
          python3 - <<'PY'
          from pathlib import Path
          import re
          scripts = [
              'scripts/audit_medievalorigins_upstream.py',
              'scripts/audit_ibarnorigins_upstream.py',
              'scripts/audit_origins_fantasy_upstream.py',
              'scripts/audit_origins_backgrounds_upstream.py',
              'scripts/audit_origins_more_backgrounds_upstream.py',
              'scripts/audit_origins_backgrounds_iss_upstream.py',
              'scripts/audit_origins_furries_upstream.py',
              'scripts/audit_origins_classes_extended_upstream.py',
              'scripts/audit_origins_classes_iss_upstream.py',
              'scripts/audit_origin_architect_upstream.py',
          ]
          for filename in scripts:
              path = Path(filename)
              source = path.read_text(encoding='utf-8')
              updated, count = re.subn(r'^LOCALES\\s*=.*$', 'LOCALES = ("ro_ro",)', source, count=1, flags=re.M)
              if count == 0:
                  updated, count = re.subn(r'^DEFAULT_LOCALES\\s*=.*$', 'DEFAULT_LOCALES = ("ro_ro",)', source, count=1, flags=re.M)
              if count != 1:
                  raise SystemExit(f'Could not patch locale list in {filename}')
              path.write_text(updated, encoding='utf-8')
          PY

      - name: Strict audit Romanian 1.21.1 add-ons
        if: matrix.include_addon_translations == true
        run: |
          python3 scripts/audit_medievalorigins_upstream.py --ref 1.21.1-fabric --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_ibarnorigins_upstream.py --ref multiloader-1.21.1-new-pack-format --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_fantasy_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_more_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_backgrounds_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_furries_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_classes_extended_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origins_classes_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
          python3 scripts/audit_origin_architect_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
"""
if validate_marker not in text:
    raise RuntimeError("Romanian add-on insertion marker missing")
text = text.replace(validate_marker, "\n" + addon_block + validate_marker, 1)

gradle_anchor = '            "-Pinclude_norwegian_121_translations=${{ matrix.include_norwegian_121_translations }}" \\\n'
if gradle_anchor not in text:
    raise RuntimeError("Romanian Gradle anchor missing")
text = text.replace(gradle_anchor, gradle_anchor + '            "-Pinclude_romanian_121_translations=${{ matrix.include_romanian_121_translations }}" \\\n', 1)

text = text.replace("      - name: Verify Danish, Finnish and Norwegian packaging\n", "      - name: Verify Danish, Finnish, Norwegian and Romanian packaging\n", 1)
no_count = "          NO_COUNT=$(grep -cE '(^|/)lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\" || true)\n"
text = text.replace(no_count, no_count + "          RO_COUNT=$(grep -cE '(^|/)lang/ro_ro\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\" || true)\n", 1)
no_echo = '          echo "Norwegian localization files in ${{ matrix.target }}: $NO_COUNT (expected ${{ matrix.expected_norwegian_files }})"\n'
text = text.replace(no_echo, no_echo + '          echo "Romanian localization files in ${{ matrix.target }}: $RO_COUNT (expected ${{ matrix.expected_romanian_files }})"\n', 1)
no_test = "          test \"$NO_COUNT\" -eq '${{ matrix.expected_norwegian_files }}'\n"
text = text.replace(no_test, no_test + "          test \"$RO_COUNT\" -eq '${{ matrix.expected_romanian_files }}'\n", 1)
no_common = '            grep -Eq "(^|/)assets/neoorigins_no_common_${index}/lang/no_no\\.json$" "build/jar-contents-${{ matrix.target }}.txt"\n'
text = text.replace(no_common, no_common + '            grep -Eq "(^|/)assets/neoorigins_ro_common_${index}/lang/ro_ro\\.json$" "build/jar-contents-${{ matrix.target }}.txt"\n', 1)

# 1.21.1: verify the NeoOrigins delta and the nine fallback add-ons; explicitly
# ensure no Romanian Origin Architect fallback is bundled.
anchor = "            grep -Eq '(^|/)assets/neoorigins_no_121/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(anchor, anchor + "            grep -Eq '(^|/)assets/neoorigins_ro_121/lang/ro_ro\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)
anchor = "            grep -Eq '(^|/)assets/medievalorigins/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(anchor, anchor + "            grep -Eq '(^|/)assets/medievalorigins/lang/ro_ro\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n            ! grep -Eq '(^|/)assets/originsmodernui/lang/ro_ro\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)
anchor = '              grep -Eq "(^|/)assets/$ns/lang/no_no.json$" "build/jar-contents-${{ matrix.target }}.txt"\n'
text = text.replace(anchor, anchor + '              if [ "$ns" != "originsmodernui" ]; then grep -Eq "(^|/)assets/$ns/lang/ro_ro.json$" "build/jar-contents-${{ matrix.target }}.txt"; fi\n', 1)
anchor = "            ! grep -Eq '(^|/)assets/neoorigins_26_(1|2)/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(anchor, anchor + "            ! grep -Eq '(^|/)assets/neoorigins_26_(1|2)/lang/ro_ro\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)

# 26.x: Romanian 1.21.1 delta is absent, while the correct version delta is present.
anchor = "            ! grep -Eq '(^|/)assets/neoorigins_no_121/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(anchor, anchor + "            ! grep -Eq '(^|/)assets/neoorigins_ro_121/lang/ro_ro\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)
for version, other in (("26_1", "26_2"), ("26_2", "26_1")):
    req = f"              grep -Eq '(^|/)assets/neoorigins_{version}/lang/no_no\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    add_req = f"              grep -Eq '(^|/)assets/neoorigins_{version}/lang/ro_ro\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    forbid = f"              ! grep -Eq '(^|/)assets/neoorigins_{other}/lang/no_no\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    add_forbid = f"              ! grep -Eq '(^|/)assets/neoorigins_{other}/lang/ro_ro\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    if req not in text or forbid not in text:
        raise RuntimeError(f"Romanian 26.x anchors missing for {version}")
    text = text.replace(req, req + add_req, 1)
    text = text.replace(forbid, forbid + add_forbid, 1)

for marker in ["romanian_extra_namespace", "Strict audit Romanian NeoOrigins coverage", "Strict audit Romanian 1.21.1 add-ons", "include_romanian_121_translations", "expected_romanian_files", "neoorigins_ro_common_${index}"]:
    if marker not in text:
        raise RuntimeError(f"Romanian CI marker missing: {marker}")

WORKFLOW.write_text(text, encoding="utf-8")
print("build-0.9.0.yml updated for permanent Romanian auditing and packaging")
