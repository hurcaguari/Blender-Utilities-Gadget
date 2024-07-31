import bpy
import os

class Multie_Render(bpy.types.Operator):
    """批量渲染场景内所有开启渲染的摄像机"""
    bl_idname = "render.multi"
    bl_label = "Render multiple times"
    
    # Define some variables to register
    _timer = None
    shots = None
    stop = None
    rendering = None
    
    
    # Define the handler functions. I use pre and
    # post to know if Blender "is rendering"
    @classmethod
    def poll(self, context): # 摄像机检测
        self.camera_list = list(filter(None,[obj.name if obj.type == 'CAMERA' and obj.hide_render == False and context.scene.name == obj.users_scene[0].name else None for obj in bpy.data.objects])) 
        return len(self.camera_list) > 0
    
    def pre(self, scene, context=None):
        self.rendering = True
        
    def post(self, scene, context=None):
        self.shots.pop(0) # This is just to render the next
                          # image in another path
        self.rendering = False
        bpy.context.scene.render.filepath = self.path

    def cancelled(self, scene, context=None):
        self.stop = True

    def execute(self, context):
        self.path = bpy.context.scene.render.filepath
        # Define the variables during execution. This allows
        # to define when called from a button
        self.stop = False
        self.rendering = False
        self.shots = self.camera_list
        
        context.scene.render.filepath = self.path
        
        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        
        # The timer gets created and the modal handler
        # is added to the window manager
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
        
    def modal(self, context, event):
        if event.type == 'TIMER': # This event is signaled every half a second
                                  # and will start the render if available
            
            # If cancelled or no more shots to render, finish.
            if True in (not self.shots, self.stop is True): 
                
                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)
                
                return {"FINISHED"} # I didn't separate the cancel and finish
                                    # events, because in my case I don't need to,
                                    # but you can create them as you need
            
            elif self.rendering is False: # Nothing is currently rendering.
                                          # Proceed to render.
                sc = context.scene
                
                # I'm using cameras named just as the output files,
                # but adapt to your needs
                sc.camera = bpy.data.objects[self.shots[0]]

                sc.render.filepath = self.path + self.shots[0]
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)


        return {"PASS_THROUGH"}
        # This is very important! If we used "RUNNING_MODAL", this new modal function
        # would prevent the use of the X button to cancel rendering, because this
        # button is managed by the modal function of the render operator,
        # not this new operator!