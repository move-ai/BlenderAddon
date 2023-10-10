
import bpy


class MoveaiImporterProperties(bpy.types.PropertyGroup):
    file_otp: bpy.props.StringProperty(
        name="One-time Code",
        description="Enter the one-time code generated"
    )
    download_anim_button_label: bpy.props.StringProperty(
        name="Button Label",
        description="Label for the button",
        default="Download Animation"
    )
