package fr.rtv20.neooriginslocalization;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.AddPackFindersEvent;

/**
 * Client-side localization companion for NeoOrigins and its add-ons.
 *
 * Translations are shipped as an always-enabled built-in resource pack at
 * Pack.Position.BOTTOM. This is intentional: translations supplied directly
 * by installed mods/resource packs should remain higher priority, while this
 * project only fills missing localization keys.
 */
@Mod(value = NeoOriginsLocalization.MOD_ID, dist = Dist.CLIENT)
public final class NeoOriginsLocalization {
    public static final String MOD_ID = "neoorigins_localization";

    public NeoOriginsLocalization(IEventBus modBus) {
        modBus.addListener(this::registerFallbackPack);
    }

    private void registerFallbackPack(AddPackFindersEvent event) {
        if (event.getPackType() != PackType.CLIENT_RESOURCES) {
            return;
        }

        event.addPackFinders(
                ResourceLocation.fromNamespaceAndPath(
                        MOD_ID,
                        "resourcepacks/fallback_localizations"
                ),
                PackType.CLIENT_RESOURCES,
                Component.literal("NeoOrigins Localization - fallback translations"),
                PackSource.BUILT_IN,
                true,
                Pack.Position.BOTTOM
        );
    }
}
