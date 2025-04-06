import bpy # type: ignore
    
class Collection_display(bpy.types.Operator):
    """显示所有集合"""
    bl_idname = "mode.display"
    bl_label = "Collection display"

    def conversion(self): # 主进程筛选对象并处理
        view_layer = bpy.context.view_layer
        for collection in view_layer.layer_collection.children:
            collection.hide_viewport = False
    
    def execute(self, context): # 程序入口
        self.conversion()
        return {'FINISHED'}