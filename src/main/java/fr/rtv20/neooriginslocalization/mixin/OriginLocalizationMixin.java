package fr.rtv20.neooriginslocalization.mixin;

import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * NeoOrigins' Origins-pack compatibility layer converts imported origin names
 * and descriptions into literal text. Literal components bypass Minecraft's
 * language system, so an external fr_fr.json cannot replace them.
 *
 * This client-side bridge restores the conventional Origins translation keys
 * at display time whenever such a key exists in the active language table.
 * Official translations still win naturally because this mod's resource pack
 * stays at low priority.
 */
@Mixin(targets = "com.cyberday1.neoorigins.api.origin.Origin", remap = false)
public abstract class OriginLocalizationMixin {

    @Shadow @Final private ResourceLocation id;

    @Inject(method = "name", at = @At("HEAD"), cancellable = true, remap = false)
    private void neooriginsLocalization$localizedName(CallbackInfoReturnable<Component> cir) {
        String key = translationKey("name");
        if (Language.getInstance().has(key)) {
            cir.setReturnValue(Component.translatable(key));
        }
    }

    @Inject(method = "description", at = @At("HEAD"), cancellable = true, remap = false)
    private void neooriginsLocalization$localizedDescription(CallbackInfoReturnable<Component> cir) {
        String key = translationKey("description");
        if (Language.getInstance().has(key)) {
            cir.setReturnValue(Component.translatable(key));
        }
    }

    private String translationKey(String field) {
        String path = id.getPath().replace('/', '.');
        return "origin." + id.getNamespace() + "." + path + "." + field;
    }
}
