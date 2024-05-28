bl_info = {
    "name": "Circular Arrange",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import math

class CircularArrangePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Circular Arrange"
    bl_idname = "OBJECT_PT_circular_arrange"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout

        # 半径の設定
        layout.prop(context.scene, "circular_radius")

        # ボタン
        layout.operator("object.circular_arrange")


class OBJECT_OT_circular_arrange(bpy.types.Operator):
    """Arrange selected objects in a circle"""
    bl_idname = "object.circular_arrange"
    bl_label = "Circular Arrange"

    def execute(self, context):
        # 選択したオブジェクトを取得
        selected_objects = context.selected_objects
        num_objects = len(selected_objects)
        
        if num_objects < 1:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        radius = context.scene.circular_radius
        angle_increment = 2 * math.pi / num_objects
        
        for i, obj in enumerate(selected_objects):
            angle = i * angle_increment
            obj.location.x = math.cos(angle) * radius
            obj.location.y = math.sin(angle) * radius

        self.report({'INFO'}, "Objects arranged in a circle")
        return {'FINISHED'}

classes = (
    CircularArrangePanel,
    OBJECT_OT_circular_arrange
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.circular_radius = bpy.props.FloatProperty(
        name="Radius",
        description="Radius of the circular arrangement",
        default=5.0,
        min=0.1,
        max=100.0
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.circular_radius

if __name__ == "__main__":
    register()

#made by Ruprous
#X/Twitter:@Ruprous
