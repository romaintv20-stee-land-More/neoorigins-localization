package fr.rtv20.neooriginslocalization.client;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ScreenEvent;

/** Search vanilla languages on Minecraft 1.21.1 only; 26.x has native search. */
@EventBusSubscriber(modid = "neoorigins_localization", value = Dist.CLIENT)
public final class LanguageSearchEvents {
    private LanguageSearchEvents() {}

    @SubscribeEvent
    public static void onInit(ScreenEvent.Init.Post event) {
        LanguageSearch1211.install(event.getScreen(), event::addListener);
    }

    @SubscribeEvent
    public static void onClosing(ScreenEvent.Closing event) {
        LanguageSearch1211.close(event.getScreen());
    }

    @SubscribeEvent
    public static void onRender(ScreenEvent.Render.Pre event) {
        LanguageSearch1211.resume(event.getScreen());
    }
}
