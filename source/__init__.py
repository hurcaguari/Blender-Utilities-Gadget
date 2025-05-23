# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Utilities Gadget",
    "author": "INEINST MACH",
    "version": (1, 1, 3),
    "blender": (4, 2, 0),
    "location": "View3D",
    "description": "Utilities Gadget",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}


import bpy # type: ignore
from .Function import Multie_Render
from .Function import Model_Conversion
from .Translat import Translat
from .Function import Collection_display

from random import randint


class CustomPanel(bpy.types.Panel): # 面板绘制
    bl_label = "Utilities"
    bl_idname = "UTILITIES_PT_gadget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Utilities"   

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.operator(Multie_Render.bl_idname, text = Translat(Multie_Render.bl_label))
        row = layout.row()
        row.operator(Collection_display.bl_idname, text = Translat(Collection_display.bl_label))
        row = layout.row()
        row.operator(Model_Conversion.bl_idname, text = Translat(Model_Conversion.bl_label))




_classes = [ # 按钮激活列表
    CustomPanel,
    Multie_Render,
    Model_Conversion,
    Collection_display,
]

def register(): # 按钮注册
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister(): # 按钮销毁
    for cls in _classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
