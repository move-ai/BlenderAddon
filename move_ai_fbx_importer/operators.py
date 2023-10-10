import bpy
import tempfile
from .utils.api import FileManager, CodeNotValidError, APIHandler


class MOVEAI_IMPORTER_OT_download_anim(bpy.types.Operator):
    """
    Blender operator that manages the process of importing animation.
    """
    bl_idname = "moveai.download_anim"
    bl_label = "Move AI import"
    bl_description = "Import animation and add to scene"
    bl_options = {"REGISTER", "UNDO"}

    def _validate_otp(self, context: bpy.types.Context) -> bool:
        """
        Validate the one-time password (OTP) provided by the user.

        Parameters:
            context (bpy.types.Context): Current Blender context.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        if not context.scene.moveai.file_otp:
            return False
        elif len(context.scene.moveai.file_otp) != 8:
            return False
        elif not context.scene.moveai.file_otp.isnumeric():
            return False
        return True

    def _download_and_import(self, context: bpy.types.Context, file_url: str):
        context.window_manager.progress_update(50)
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.report({"INFO"}, f"Path {tmp_dir}")
            try:
                file_content = FileManager.download_file(file_url)
                tmp_file_path = FileManager.write_to_temp_file(
                    file_content, tmp_dir)
                self.report({"INFO"}, f"Importing file {tmp_file_path}")
                context.window_manager.progress_update(75)
                FileManager.import_file(tmp_file_path)
            except Exception as exc:
                self.report({"ERROR"}, str(exc))
            finally:
                context.scene.moveai.file_otp = ""

    def invoke(self, context, event) -> "set[str]":
        self.report({"INFO"}, str(self._validate_otp(context)))
        context.window_manager.progress_begin(0, 100)
        context.window_manager.progress_update(25)
        if not self._validate_otp(context):
            self.report({"ERROR"}, "Invalid code")
            return {"CANCELLED"}
        try:
            response = APIHandler.fetch_file_data(
                context.scene.moveai.file_otp)
            file_obj = response.json()
            self.file_url = file_obj["url"]
        except CodeNotValidError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        return self.execute(context)

    def execute(self, context: bpy.types.Context) -> "set[str]":
        self._download_and_import(context, self.file_url)
        context.scene.moveai.file_otp = ""

        context.window_manager.progress_update(100)
        context.window_manager.progress_end()
        return {"FINISHED"}
