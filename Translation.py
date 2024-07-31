from .translat_text import TEXT
import bpy

def baidu_translat(text):
    pass

def Translat(text):
    try:
        return TEXT[bpy.context.preferences.view.language][text]
    except KeyError:
        print(bpy.context.preferences.view.language,'没有对应翻译')
        return text

if __name__ == "__main__":
    x = Translat("Batch Rendering",type = 'zh_HANS')
    pass