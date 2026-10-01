#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/build-0.9.0.yml"
text = WORKFLOW.read_text(encoding="utf-8")

if "Strict audit Norwegian NeoOrigins coverage" in text:
    print("Norwegian CI integration already present")
    raise SystemExit(0)

# Matrix: target-specific delta namespace, packaging switch and expected file count.
replacements = {
    "            finnish_extra_namespace: 'neoorigins_fi_121'\n":
        "            finnish_extra_namespace: 'neoorigins_fi_121'\n"
        "            norwegian_extra_namespace: 'neoorigins_no_121'\n",
    "            finnish_extra_namespace: 'neoorigins_26_1'\n":
        "            finnish_extra_namespace: 'neoorigins_26_1'\n"
        "            norwegian_extra_namespace: 'neoorigins_26_1'\n",
    "            finnish_extra_namespace: 'neoorigins_26_2'\n":
        "            finnish_extra_namespace: 'neoorigins_26_2'\n"
        "            norwegian_extra_namespace: 'neoorigins_26_2'\n",
    "            include_finnish_121_translations: true\n":
        "            include_finnish_121_translations: true\n"
        "            include_norwegian_121_translations: true\n",
    "            include_finnish_121_translations: false\n":
        "            include_finnish_121_translations: false\n"
        "            include_norwegian_121_translations: false\n",
    "            expected_finnish_files: '27'\n":
        "            expected_finnish_files: '27'\n"
        "            expected_norwegian_files: '27'\n",
    "            expected_finnish_files: '17'\n":
        "            expected_finnish_files: '17'\n"
        "            expected_norwegian_files: '17'\n",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"CI matrix anchor not found: {old!r}")
    text = text.replace(old, new)

# NeoOrigins strict audit on all three targets.
marker = "\n      - name: Restrict add-on audits to Danish\n"
norwegian_neo = """
      - name: Strict audit Norwegian NeoOrigins coverage
        run: |
          python3 scripts/audit_neoorigins_upstream.py \\
            --ref '${{ matrix.upstream_ref }}' \\
            --output 'build/norwegian-audit-${{ matrix.target }}' \\
            --locale no_no \\
            --fallback-namespace-glob 'neoorigins_no_common_*' \\
            --extra-namespace '${{ matrix.norwegian_extra_namespace }}' \\
            --fail-on-overlap --fail-on-missing --fail-on-placeholders
"""
if marker not in text:
    raise RuntimeError("Danish audit marker not found")
text = text.replace(marker, "\n" + norwegian_neo + marker, 1)

# 1.21.1 add-on audits for Norwegian.
validate_marker = "\n      - name: Validate localization files\n"
norwegian_addons = """
      - name: Restrict add-on audits to Norwegian
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
              updated, count = re.subn(r'^LOCALES\\s*=.*$', 'LOCALES = ("no_no",)', source, count=1, flags=re.M)
              if count == 0:
                  updated, count = re.subn(r'^DEFAULT_LOCALES\\s*=.*$', 'DEFAULT_LOCALES = ("no_no",)', source, count=1, flags=re.M)
              if count != 1:
                  raise SystemExit(f'Could not patch locale list in {filename}')
              path.write_text(updated, encoding='utf-8')
          PY

      - name: Strict audit Norwegian 1.21.1 add-ons
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
    raise RuntimeError("Validation marker not found")
text = text.replace(validate_marker, "\n" + norwegian_addons + validate_marker, 1)

# Pass target-specific Norwegian delta packaging switch to Gradle.
gradle_anchor = '            "-Pinclude_finnish_121_translations=${{ matrix.include_finnish_121_translations }}" \\\n'
if gradle_anchor not in text:
    raise RuntimeError("Finnish Gradle property anchor not found")
text = text.replace(
    gradle_anchor,
    gradle_anchor + '            "-Pinclude_norwegian_121_translations=${{ matrix.include_norwegian_121_translations }}" \\\n',
    1,
)

# JAR packaging verification.
text = text.replace(
    "      - name: Verify Danish and Finnish packaging\n",
    "      - name: Verify Danish, Finnish and Norwegian packaging\n",
    1,
)

fi_count = "          FI_COUNT=$(grep -cE '(^|/)lang/fi_fi\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\" || true)\n"
if fi_count not in text:
    raise RuntimeError("Finnish count anchor not found")
text = text.replace(fi_count, fi_count + "          NO_COUNT=$(grep -cE '(^|/)lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\" || true)\n", 1)

fi_echo = '          echo "Finnish localization files in ${{ matrix.target }}: $FI_COUNT (expected ${{ matrix.expected_finnish_files }})"\n'
text = text.replace(fi_echo, fi_echo + '          echo "Norwegian localization files in ${{ matrix.target }}: $NO_COUNT (expected ${{ matrix.expected_norwegian_files }})"\n', 1)
fi_test = "          test \"$FI_COUNT\" -eq '${{ matrix.expected_finnish_files }}'\n"
text = text.replace(fi_test, fi_test + "          test \"$NO_COUNT\" -eq '${{ matrix.expected_norwegian_files }}'\n", 1)

fi_common = '            grep -Eq "(^|/)assets/neoorigins_fi_common_${index}/lang/fi_fi\\.json$" "build/jar-contents-${{ matrix.target }}.txt"\n'
text = text.replace(fi_common, fi_common + '            grep -Eq "(^|/)assets/neoorigins_no_common_${index}/lang/no_no\\.json$" "build/jar-contents-${{ matrix.target }}.txt"\n', 1)

# 1.21.1 required files and prohibition of version deltas.
fi_121 = "            grep -Eq '(^|/)assets/neoorigins_fi_121/lang/fi_fi\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(fi_121, fi_121 + "            grep -Eq '(^|/)assets/neoorigins_no_121/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)
fi_med = "            grep -Eq '(^|/)assets/medievalorigins/lang/fi_fi\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(fi_med, fi_med + "            grep -Eq '(^|/)assets/medievalorigins/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)
fi_ns = '              grep -Eq "(^|/)assets/$ns/lang/fi_fi.json$" "build/jar-contents-${{ matrix.target }}.txt"\n'
text = text.replace(fi_ns, fi_ns + '              grep -Eq "(^|/)assets/$ns/lang/no_no.json$" "build/jar-contents-${{ matrix.target }}.txt"\n', 1)
fi_version_forbid = "            ! grep -Eq '(^|/)assets/neoorigins_26_(1|2)/lang/fi_fi\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(fi_version_forbid, fi_version_forbid + "            ! grep -Eq '(^|/)assets/neoorigins_26_(1|2)/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)

# 26.x: no 1.21.1 delta and only the correct version delta.
fi_121_forbid = "            ! grep -Eq '(^|/)assets/neoorigins_fi_121/lang/fi_fi\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n"
text = text.replace(fi_121_forbid, fi_121_forbid + "            ! grep -Eq '(^|/)assets/neoorigins_no_121/lang/no_no\\.json$' \"build/jar-contents-${{ matrix.target }}.txt\"\n", 1)

for version, other in (("26_1", "26_2"), ("26_2", "26_1")):
    fi_required = f"              grep -Eq '(^|/)assets/neoorigins_{version}/lang/fi_fi\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    no_required = f"              grep -Eq '(^|/)assets/neoorigins_{version}/lang/no_no\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    if fi_required not in text:
        raise RuntimeError(f"Finnish required delta anchor missing for {version}")
    text = text.replace(fi_required, fi_required + no_required, 1)

    fi_forbid = f"              ! grep -Eq '(^|/)assets/neoorigins_{other}/lang/fi_fi\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    no_forbid = f"              ! grep -Eq '(^|/)assets/neoorigins_{other}/lang/no_no\\.json$' \"build/jar-contents-${{{{ matrix.target }}}}.txt\"\n"
    if fi_forbid not in text:
        raise RuntimeError(f"Finnish forbidden delta anchor missing for {other}")
    text = text.replace(fi_forbid, fi_forbid + no_forbid, 1)

required_markers = [
    "norwegian_extra_namespace",
    "Strict audit Norwegian NeoOrigins coverage",
    "Strict audit Norwegian 1.21.1 add-ons",
    "include_norwegian_121_translations",
    "expected_norwegian_files",
    "neoorigins_no_common_${index}",
]
for marker in required_markers:
    if marker not in text:
        raise RuntimeError(f"Norwegian CI marker missing after update: {marker}")

WORKFLOW.write_text(text, encoding="utf-8")
print("build-0.9.0.yml updated for permanent Norwegian auditing and packaging")
