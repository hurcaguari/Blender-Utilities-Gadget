import bpy
    
class Model_Conversion(bpy.types.Operator):
    """批量处理场景内所有可选择的模型转换为独立的几何体"""
    bl_idname = "mode.conversion"
    bl_label = "Model Conversion"

    @classmethod
    def poll(self,context): # 循环判断大纲列表内的可处理对象列表
        self.obj_list = list(filter(None,[obj if obj.type in ['CURVE','FONT','MESH','EMPTY'] else None for obj in bpy.data.objects]))
        return len(self.obj_list) > 0

    def mesh(self,obj): # 网格处理没有修改器则不处理
        if len(obj.modifiers) > 0:
            self.conve(obj)

    def empty(self,obj): # 实例处理实现实例
        if self.select(obj):
            bpy.ops.object.duplicates_make_real()

    def conve(self,obj): # 基础处理选择并执行可视几何到网格
        if self.select(obj):
            obj = self.duplicate(obj)
            self.curve(obj)

    def conversion(self): # 主进程筛选对象并处理
        for obj in self.obj_list:
            print(obj.name,obj.type)
            if obj.type in ['CURVE','FONT']:
                self.conve(obj)
            elif obj.type == 'MESH':
                self.mesh(obj)
            elif obj.type == 'EMPTY':
                self.empty(obj)
    
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