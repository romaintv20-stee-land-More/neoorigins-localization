#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRADLE = ROOT / "build.gradle"

ANCHOR = "sourceSets.main.resources.srcDir generateModMetadata\nneoForge.ideSyncTask generateModMetadata\n"
BLOCK = '''sourceSets.main.resources.srcDir generateModMetadata
neoForge.ideSyncTask generateModMetadata

def backgroundOrbTranslationsFile = file("localization/background_orb_translations.json")
def generatedBackgroundOrbResources = layout.buildDirectory.dir("generated/backgroundOrbResources")
def generateBackgroundOrbTranslations = tasks.register("generateBackgroundOrbTranslations") {
    inputs.file backgroundOrbTranslationsFile
    inputs.property 'resource_pack_format', targetResourcePackFormat
    outputs.dir generatedBackgroundOrbResources
    doLast {
        def outputDir = generatedBackgroundOrbResources.get().asFile
        outputDir.deleteDir()
        def packDir = new File(outputDir, "resourcepacks/background_orb_localizations")
        def langDir = new File(packDir, "assets/neoorigins/lang")
        langDir.mkdirs()
        def packMeta = [pack: [pack_format: Integer.parseInt(targetResourcePackFormat), description: "NeoOrigins Localization - contextual Background Orb translations"]]
        new File(packDir, "pack.mcmeta").text = groovy.json.JsonOutput.prettyPrint(groovy.json.JsonOutput.toJson(packMeta)) + "\\n"
        def translations = new groovy.json.JsonSlurper().parse(backgroundOrbTranslationsFile)
        translations.each { locale, values ->
            new File(langDir, "${locale}.json").text = groovy.json.JsonOutput.prettyPrint(groovy.json.JsonOutput.toJson(values)) + "\\n"
        }
    }
}
sourceSets.main.resources.srcDir generateBackgroundOrbTranslations
'''

text = GRADLE.read_text(encoding="utf-8")
if "backgroundOrbTranslationsFile" not in text:
    if ANCHOR not in text:
        raise SystemExit("Background Orb Gradle anchor not found")
    text = text.replace(ANCHOR, BLOCK, 1)

EXCLUDE = "        exclude 'resourcepacks/background_orb_localizations/**'\n"
ADDON_ANCHOR = "        exclude 'resourcepacks/fallback_localizations/assets/originsmodernui/**'\n"
if EXCLUDE not in text:
    if ADDON_ANCHOR not in text:
        raise SystemExit("Add-on exclusion anchor not found")
    text = text.replace(ADDON_ANCHOR, ADDON_ANCHOR + EXCLUDE, 1)

GRADLE.write_text(text, encoding="utf-8")
print("1.0.0 Background Orb Gradle packaging patch applied")
