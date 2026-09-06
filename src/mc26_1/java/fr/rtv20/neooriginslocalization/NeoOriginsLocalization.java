package fr.rtv20.neooriginslocalization;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.AddPackFindersEvent;

/**
 * Client-side localization companion for NeoOrigins and its add-ons.
 * Minecraft 26.1.x uses Identifier in place of ResourceLocation.
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
                Identifier.fromNamespaceAndPath(
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
