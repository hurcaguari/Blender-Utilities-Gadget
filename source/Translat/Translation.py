from .text import TEXT
import bpy # type: ignore

def baidu_translat(text):
    pass

def Translat(text):
    try:
        return TEXT[bpy.context.preferences.view.language][text]
    except KeyError:
        print(bpy.context.preferences.view.language,'没有对应翻译')
        return text