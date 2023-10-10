import bpy


class MOVEAI_IMPORTER_PT_download_panel(bpy.types.Panel):
    """
    UI Panel that provides the user interface for the Move AI Importer.
    """
    bl_idname = "MOVEAI_IMPORTER_PT_download_panel"
    bl_label = "Move.ai Importer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move AI"

    def draw(self, context: bpy.types.Context) -> None:
        """
        Draw the UI elements for the Move AI Importer panel.

        Parameters:
            context (bpy.types.Context): Current Blender context.
        """
        scene = context.scene
        layout = self.layout
        layout.label(text="Move One FBX Importer.")
        layout.label(text="1. Open Move One iOS app")
        layout.label(text="2. Generate code for .fbx")
        layout.label(text="3. Enter code below")
        layout.label(text="4. Click download animation")

        box = layout.box()
        box.label(text="Import FBX", icon='ANIM_DATA')
        box.prop(scene.moveai, "file_otp", text="Code", icon='KEYINGSET')
        box.operator("moveai.download_anim",
                     text=scene.moveai.download_anim_button_label, icon='IMPORT')
