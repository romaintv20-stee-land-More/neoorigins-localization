package fr.rtv20.neooriginslocalization;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.AddPackFindersEvent;

/**
 * Client-side localization companion for NeoOrigins and its add-ons.
 *
 * Translations are shipped as always-enabled built-in resource packs at
 * Pack.Position.BOTTOM. Official mod resources remain higher priority.
 */
@Mod(value = NeoOriginsLocalization.MOD_ID, dist = Dist.CLIENT)
public final class NeoOriginsLocalization {
    public static final String MOD_ID = "neoorigins_localization";

    public NeoOriginsLocalization(IEventBus modBus) {
        modBus.addListener(this::registerFallbackPacks);
    }

    private void registerFallbackPacks(AddPackFindersEvent event) {
        if (event.getPackType() != PackType.CLIENT_RESOURCES) {
            return;
        }

        // Register this first: another BOTTOM pack registered afterwards sits below it,
        // so this contextual override wins over our generic fallback while remaining
        // below the installed mods' own resources.
        if (hasBackgroundAddon()) {
            registerPack(
                    event,
                    "resourcepacks/background_orb_localizations",
                    "NeoOrigins Localization - Background Orb translations"
            );
        }

        registerPack(
                event,
                "resourcepacks/fallback_localizations",
                "NeoOrigins Localization - fallback translations"
        );
    }

    private static boolean hasBackgroundAddon() {
        ModList modList = ModList.get();
        return modList.isLoaded("origins_backgrounds")
                || modList.isLoaded("origins_backgrounds_two");
    }

    private static void registerPack(AddPackFindersEvent event, String path, String title) {
        event.addPackFinders(
                ResourceLocation.fromNamespaceAndPath(MOD_ID, path),
                PackType.CLIENT_RESOURCES,
                Component.literal(title),
                PackSource.BUILT_IN,
                true,
                Pack.Position.BOTTOM
        );
    }
}
