bl_info = {
    "name": "Duplicate Randomize",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 1, 0),
    "author": "Ruprous",
    "location": "View3D > Sidebar > Tool Tab",
    "doc_url": "https://github.com/Ruprous/blenderAddons"
    #made by Ruprous
    #X/Twitter:@Ruprous
}

import bpy
import random

class DuplicateAndRandomize(bpy.types.Operator):
    bl_idname = "object.duplicate_and_randomize"
    bl_label = "Duplicate and Randomize"
    bl_options = {'REGISTER', 'UNDO'}
    
    count: bpy.props.IntProperty(
        name="Number of Duplicates",
        default=1,
        min=1
    )
    range: bpy.props.FloatProperty(
        name="Range",
        default=10.0,
        min=0.0
    )
    join: bpy.props.BoolProperty(
        name="Join Duplicates",
        default=False
    )
    random_scale: bpy.props.BoolProperty(
        name="Randomize Scale",
        default=False
    )
    
    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}
        
        original_location = obj.location
        new_objects = []
        
        for _ in range(self.count):
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            new_obj.location = (
                original_location.x + random.uniform(-self.range, self.range),
                original_location.y + random.uniform(-self.range, self.range),
                original_location.z + random.uniform(-self.range, self.range)
            )
            if self.random_scale:
                # オブジェクトの比率を維持してランダムにスケール変更
                scale_factor = random.uniform(0.5, 1.5)
                new_obj.scale = (
                    scale_factor * obj.scale.x,
                    scale_factor * obj.scale.y,
                    scale_factor * obj.scale.z
                )
            context.collection.objects.link(new_obj)
            new_objects.append(new_obj)
        
        if self.join and new_objects:
            bpy.ops.object.select_all(action='DESELECT')
            for new_obj in new_objects:
                new_obj.select_set(True)
            context.view_layer.objects.active = new_objects[0]
            bpy.ops.object.join()
        
        return {'FINISHED'}


class DuplicateAndRandomizePanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_duplicate_and_randomize"
    bl_label = "Duplicate and Randomize"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "duplicate_and_randomize_count")
        layout.prop(scene, "duplicate_and_randomize_range")
        layout.prop(scene, "duplicate_and_randomize_join")
        layout.prop(scene, "duplicate_and_randomize_random_scale")
        op = layout.operator("object.duplicate_and_randomize", text="Duplicate and Randomize")
        op.count = scene.duplicate_and_randomize_count
        op.range = scene.duplicate_and_randomize_range
        op.join = scene.duplicate_and_randomize_join
        op.random_scale = scene.duplicate_and_randomize_random_scale


def register():
    bpy.utils.register_class(DuplicateAndRandomize)
    bpy.utils.register_class(DuplicateAndRandomizePanel)
    
    bpy.types.Scene.duplicate_and_randomize_count = bpy.props.IntProperty(
        name="Count",
        description="Number of duplicates",
        default=1,
        min=1
    )
    bpy.types.Scene.duplicate_and_randomize_range = bpy.props.FloatProperty(
        name="Range",
        default=10.0,
        min=0.0
    )
    bpy.types.Scene.duplicate_and_randomize_join = bpy.props.BoolProperty(
        name="Merge Objects",
        description="Merge duplicated objects into one",
        default=False,
    )
    bpy.types.Scene.duplicate_and_randomize_random_scale = bpy.props.BoolProperty(
        name="Randomize Scale",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(DuplicateAndRandomize)
    bpy.utils.unregister_class(DuplicateAndRandomizePanel)
    
    del bpy.types.Scene.duplicate_and_randomize_count
    del bpy.types.Scene.duplicate_and_randomize_range
    del bpy.types.Scene.duplicate_and_randomize_join
    del bpy.types.Scene.duplicate_and_randomize_random_scale


if __name__ == "__main__":
    register()
