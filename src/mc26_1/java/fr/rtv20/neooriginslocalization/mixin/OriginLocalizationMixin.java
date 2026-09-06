package fr.rtv20.neooriginslocalization.mixin;

import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Restores conventional Origins translation keys for imported origin names
 * and descriptions on Minecraft 26.1.x.
 */
@Mixin(targets = "com.cyberday1.neoorigins.api.origin.Origin", remap = false)
public abstract class OriginLocalizationMixin {

    @Shadow @Final private Identifier id;

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
