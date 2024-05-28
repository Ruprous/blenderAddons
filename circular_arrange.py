bl_info = {
    "name": "Circular Arrange",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import math

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
        
        radius = 5.0  # 円の半径
        angle_increment = 2 * math.pi / num_objects
        
        for i, obj in enumerate(selected_objects):
            angle = i * angle_increment
            obj.location.x = math.cos(angle) * radius
            obj.location.y = math.sin(angle) * radius

        self.report({'INFO'}, "Objects arranged in a circle")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_circular_arrange.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_circular_arrange)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_circular_arrange)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()


#made by Ruprous
#X/Twitter:@Ruprous
