import bpy
    
class ModelConversion(bpy.types.Operator):
    bl_idname = "mode.conversion"
    bl_label = "Model Conversion"
    obj_list = list(bpy.data.objects)
    
    def conversion(self): # 主进程筛选对象并处理
        for obj in self.obj_list:
            print(obj.name,obj.type)
            if obj.type == 'CURVE' or obj.type == 'FONT':
                if self.select(obj):
                    obj = self.duplicate(obj)
                    self.curve(obj)
    
    def select(self,obj): # 高亮选择对象
        try:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[obj.name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
        except RuntimeError:
            return False
        else:
            return True
    
    def duplicate(self,obj): # 复制并删除原版对象提取关联对象返回复制后的对象
        self.select(obj)
        bpy.ops.object.duplicate(linked=False,mode='TRANSLATION')
        out_obj = bpy.data.objects[bpy.context.active_object.name]
        self.select(obj)
        bpy.ops.object.delete(use_global=False)
        return out_obj
        
    def curve(self,obj): # 曲线与文本处理可视几何到网格操作
        self.select(obj)
        bpy.ops.object.convert(target='MESH')
    
    def execute(self, context): # 程序入口
        self.conversion()
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(ModelConversion.bl_idname, text="Model Conversionr")


if __name__ == "__main__":
    bpy.utils.register_class(ModelConversion)
    bpy.types.VIEW3D_MT_view.append(menu_func)
    bpy.ops.mode.conversion()
