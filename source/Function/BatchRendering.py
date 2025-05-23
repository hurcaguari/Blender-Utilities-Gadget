import bpy # type: ignore
import os

class Multie_Render(bpy.types.Operator):
    """批量渲染场景内所有开启渲染的摄像机"""
    bl_idname = "render.multi"
    bl_label = "Batch Rendering"
    
    # 定义一些变量以进行注册
    _timer = None
    shots = None
    stop = None
    rendering = None
    
    # 定义处理函数。我使用 pre 和 post 来判断 Blender 是否正在渲染
    @classmethod
    def poll(self, context): # 摄像机检测
        # 这里我们检查是否有任何摄像机可以渲染
        # 这将返回一个列表，包含所有可以渲染的摄像机名称
        # 你可以在这里添加更多的条件来过滤摄像机
        # 例如，检查摄像机是否在场景中可见，或者是否在特定的集合中
        # 你可以使用 obj.hide_render 来检查摄像机是否在渲染中可见
        # 你可以使用 obj.users_collection[0].hide_render 来检查摄像机是否在集合中可见
        # 你可以使用 obj.users_scene[0].name 来检查摄像机是否在特定的场景中
        # 你可以使用 obj.name 来检查摄像机的名称
        # 你可以使用 obj.type 来检查对象的类型
        # 你可以使用 obj.users_scene[0].name 来检查对象的场景名称
        self.camera_list = list(filter(None,[obj.name if obj.type == 'CAMERA' and self.if_render(obj) == False and context.scene.name == obj.users_scene[0].name else None for obj in bpy.data.objects])) 
        return len(self.camera_list) > 0
    @staticmethod
    def if_render(obj):
        coll = obj.users_collection[0].hide_render
        if obj.hide_render == True:
            return obj.hide_render
        else:
            return coll

    def pre(self, scene, context=None):
        self.rendering = True
        
    def post(self, scene, context=None):
        self.shots.pop(0) # 这只是为了在另一个路径中渲染下一张图像
        self.rendering = False
        bpy.context.scene.render.filepath = self.path

    def cancelled(self, scene, context=None):
        self.stop = True

    def execute(self, context):
        self.path = bpy.context.scene.render.filepath
        # 在执行期间定义变量。这允许从按钮调用时定义
        self.stop = False
        self.rendering = False
        self.shots = self.camera_list
        
        context.scene.render.filepath = self.path
        
        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        
        # 定时器被创建，模态处理程序被添加到窗口管理器
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
        
    def modal(self, context, event):
        if event.type == 'TIMER': # 这个事件每半秒钟发出一次信号，并在可用时开始渲染
            
            # 如果取消或没有更多的镜头要渲染，则完成。
            if True in (not self.shots, self.stop is True): 
                
                # 我们移除处理程序和模态定时器以清理所有内容
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)
                
                return {"FINISHED"} # 我没有分离取消和完成事件，因为在我的情况下不需要，但你可以根据需要创建它们
            
            elif self.rendering is False: # 当前没有渲染。继续渲染。
                sc = context.scene
                
                # 我使用的摄像机名称与输出文件相同，但可以根据需要进行调整
                sc.camera = bpy.data.objects[self.shots[0]]

                sc.render.filepath = self.path + self.shots[0]
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
        return {"PASS_THROUGH"}
        # 这非常重要！如果我们使用 "RUNNING_MODAL"，这个新的模态函数将阻止使用 X 按钮取消渲染，因为这个按钮由渲染操作符的模态函数管理，而不是这个新的操作符！

    def operator(self, layout,Translation):
        row = layout.row()
        return row.operator(self.bl_idname, text = Translation(self.bl_label))