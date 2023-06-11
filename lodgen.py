bl_info = {
    "name" : "LOD Generation",
    "author" : "Marc Ueberall",
    "version" : (1, 0),
    "blender" : (3, 4, 0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Optimize Mesh",
}

import bpy

class LODGEN_Properties(bpy.types.PropertyGroup):
    lod_count : bpy.props.IntProperty(name = "LODs", default = 3, soft_min = 1, soft_max = 7)
    lod_ratio : bpy.props.FloatProperty(name = "Ratio", default = 0.5, min = 0.1, max = 1.0)

class LODGEN_PT_panel(bpy.types.Panel):
    bl_label = "LOD Generator"
    bl_idname = "PT_LODGenerator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LOD Generator"
    
    def draw(self, context):
        props = context.scene.lodgen

        self.layout.label(text = "Settings")
        self.layout.prop(props, "lod_count")
        self.layout.prop(props, "lod_ratio", slider = True)
        self.layout.separator()
        self.layout.operator("object.lodgen")

class LODGEN_OT_operator(bpy.types.Operator):
    bl_idname = "object.lodgen"
    bl_label = "Generate"
    bl_options = { "REGISTER", "UNDO" }
    
    def execute(self, context):
        props = context.scene.lodgen
        obj = bpy.context.active_object
        
        if obj is None:
            self.report({ "ERROR" }, "No active object found")
            
            return { "CANCELLED" }
        
        name = obj.name
        
        for i in range(0, props.lod_count):
            bpy.ops.object.duplicate(linked = False)
            
            obj = bpy.context.active_object
            obj.name = name + "_LOD" + str(i)

            if i > 0:
                obj.modifiers.new(name = "LOD", type = "DECIMATE").ratio = props.lod_ratio
            
            for m in obj.modifiers:
                if m is not None:
                    bpy.ops.object.modifier_apply(modifier = m.name)

        return { "FINISHED" }

classes = [ LODGEN_Properties, LODGEN_PT_panel, LODGEN_OT_operator ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.lodgen = bpy.props.PointerProperty(type = LODGEN_Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.lodgen

if __name__ == "__main__":
    register()