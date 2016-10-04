import bpy
import threading
import time
#import bge


def run_render_in_th(n):
    sce = bpy.context.scene
    #sce.render.filepath ='c:\\out\\'+'fff'
    print ('trhead',n,time.time())
    sce.frame_start = 0
    sce.frame_end = 10
    print(sce.frame_start,sce.frame_end)
    sce.render.threads = 3
    #sce.render.use_antialiasing = True
    #bpy.ops.render.render(write_still=True)
    data_context = {"blend_data": bpy.context.blend_data,"scene": n}
    try:
        print('+ in try  ')
        bpy.ops.render.render(data_context,animation=True)
    except w:
        print('Error',w)

    #bpy.context.scene.render.filepath = '11'+".png"
    #bpy.data.scenes['Scene'].render.filepath = '1'
    #bpy.data.scenes["Scene"].render.filepath='0'
    #bpy.ops.render.render(animation=True)
    
    return '{ok}'

def run_render_in_th1(n):
    print ('trhead',n,time.time())
    sce1 = bpy.context.scene
    sce1.render.filepath ='c:\\out\\'+n
    sce1.frame_start = 20
    sce1.frame_end = 40
    print(sce1.frame_start,sce1.frame_end)
    sce1.render.threads = 3
    sce1.render.use_antialiasing = True
    
    #bpy.data.scenes["Scene"].render.filepath='1'
    #bpy.ops.render.filepath("/tmp/"+'1')
    #bpy.context.scene.render.filepath = '12'+".png"
   # bpy.data.scenes['Scene'].render.filepath = '2'
    #bpy.ops.render.render(animation=True) 
    
    return '{ok}'



#scenes = bge.logic.getSceneList() for i in C.scene.sequence_editor.sequences_all:
print('dfdf')
bpy.ops.scene.new(type='FULL_COPY')
yes=0
for i in bpy.data.scenes:
    if yes ==0:
        #print(i)
        p1 = threading.Thread(target=run_render_in_th, name="t1", args=[i])
        p1.start()


#my_scene = [scene for scene in scenes if scene.name=="My Scene"][0]
#object = my_scene.objects['My Object']

p1 = threading.Thread(target=run_render_in_th, name="t1", args=["1"])
#p2 = threading.Thread(target=run_render_in_th1, name="t2", args=["2"])


#p2.start()
#for count, Scn in enumerate(bpy.data.scenes):
#    print(count,Scn)
#    data_context = {"blend_data": bpy.context.blend_data,"scene": Scn}
#    bpy.ops.render.render(data_context, animation=True)

