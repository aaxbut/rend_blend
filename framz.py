# -*- coding : utf-8 -*-
import os, re
from bpy import context
import bpy, aud
import datetime


bpy.path.abspath("//")
dir_in = 'in'
dir_out = 'out'
override_end_rend = []
override_end_rend.append(1)
def main():
    channelid=1
    bpy.context.scene.sequence_editor_create()
    for x in os.listdir(dir_in):
        try:
            if x.split('.')[2] == 'txt':           
                d = os.path.join(dir_in, x)
                coords_fo_frames_xy(d, x.split(".")[0], x.split(".")[1],channelid)
                channelid+=2
        except IndexError:
             print(x,'is not cords file')
        try:
            if x.split('.')[1] == 'mp4':           
                d = os.path.join(dir_in, x)
                
                print('is clip file')
                insert_moview_file(d, x.split(".")[0], x.split(".")[1],channelid)
                channelid+=3
        except IndexError:
             print(x,'is not clip file file')


def insert_moview_file(pathaaf, file_cords_name, file_extension,channelid):
    file_name = file_cords_name+'.'+file_extension
    fpath = pathaaf+file_name
    print(pathaaf)
    print('+')
    dd = bpy.context.scene.sequence_editor
    dd1 = bpy.context.scene.sequence_editor
    try:
        T=dd1.sequences.new_movie(name = file_cords_name, filepath = pathaaf, channel = channelid, frame_start = 0)
        T.blend_type='ALPHA_UNDER'
        
    except:
        print('exept add clip')
    
    #dd.update()
    try:
        dd.sequences.new_sound(name = file_cords_name, filepath = r'//'+pathaaf, channel = channelid+1, frame_start = 0)
        dd.animation_offset_start=1
                  
    except:
        print('can''t add clip')
    # dd1.sequences.blend_type='ALPHA_UNDER'
    return 'ok'
    
    
def coords_fo_frames_xy(pathaaf, file_cords_name, file_extension,channelid):
    d_flag = 0  
    s_flag = 0  # scale find
    r_flag = 0  # rotation find
    a_flag = 0 # anchor find
    asix_flag = 0 # axis find
    rotation = []
    scalexyz = []
    osi_xy = []
    anchor_xy = []
    transform_hw_befor = []
    transform_hw_cle = []
    f={}
    source_wh_patterm = re.compile(r"(\t(\w+)) (\w+)\t\d+")
    source_h_patterm = re.compile(r"(Source Height)\t(\d+)")
    tr=False
    # regex transform compile



    for x in open(pathaaf,'r'):
#        transform_hw_cle.append(source_h_patterm.findall(x))
        # looking height and width
        source_hw = source_wh_patterm.match(x)
        positioncords_flag = re.match(r'^Transform\tP', x)
        rotationcoord_flag = re.match(r'^Transform\tRotation', x)
        scalecoord_flag = re.match(r'^Transform\tScale', x)
        anchor_flag = re.match(r'^Transform\tAnchor', x)
        
        xy_coordframe = re.match(r'(\t(\d+))(\t(\d+).(\d+))(\t(\d+)*.(\d+))', x) # x,y
        #print(xy_coordframe)
        scalecoord = re.match(r'(\t(\d+))(\t(\d+.)*\-*\d+)(?<!(\t))',x)
        if source_hw is not None: # ok we find them
            print(source_hw.group().split()[2])
            transform_hw_befor.append(source_hw.group().split()[2])
            d_flag = 0
                    
        if rotationcoord_flag is not None:
            #print('rotation +')
            r_flag = 1
            d_flag = 0
            s_flag = 0
            a_flag = 0
            asix_flag = 0
        elif scalecoord_flag is not None:
           # print('scale +')
            s_flag = 1
            d_flag = 0
            r_flag = 0
            a_flag = 0
            asix_flag = 0
        elif anchor_flag is not None:
           # print('anchor +')
            s_flag = 0
            d_flag = 0
            r_flag = 0
            asix_flag = 0
            a_flag = 1
        elif positioncords_flag is not None:
           #print('position +')
            s_flag = 0
            d_flag = 0
            r_flag = 0
            a_flag = 0
            asix_flag = 1


            
           
        #print (asix_flag)   
        if asix_flag == 1:
            #print (asix_flag) 
            if xy_coordframe is not None:
                #print('position + +')
                osi_xy.append([int(xy_coordframe.group().split()[0]),float(xy_coordframe.group().split()[1]),float(xy_coordframe.group().split()[2])])
        elif s_flag==1:
             
             scalecoord = re.match(r'(\t(\d+))(\t(\d+.)*\-*\d+)(?<!(\t))',x)
             if scalecoord is not None:
                #print('scale + +')
                 #scalexyz.append(scalecoord.group().split())
                 scalexyz.append([int(scalecoord.group().split()[0]),float(scalecoord.group().split()[1])])
        elif r_flag==1:
            rotationcords = re.match(r'(\t(\d+))(\t)(\-*)(\d+)*\.*(\d+)',x)
            if rotationcords is not None:
                #print('rotation + + ')
                rotation.append([int(rotationcords.group().split()[0]),float(rotationcords.group().split()[1])])
        elif a_flag==1:
            
            anchor_point_c = re.match(r'(\t(\d+))(\t(\d+).(\d+))(\t(\d+)*.(\d+))', x) # anchor point x,y
            if anchor_point_c is not None:
                #print('anchor + +')
                anchor_xy.append([int(xy_coordframe.group().split()[0]),float(xy_coordframe.group().split()[1]),float(xy_coordframe.group().split()[2])])
       # elif asix_flag==1:
       #     if xy_coordframe is not None:
       #         osi_xy.append([int(xy_coordframe.group().split()[0]),float(xy_coordframe.group().split()[1]),float(xy_coordframe.group().split()[2])])

    axis_of_good = set_axis(osi_xy,rotation,scalexyz,anchor_xy)
    #print('ffffff')
#    transform_hw_cle = list(dict(zip(transform_hw_befor,transform_hw_befor)).values())
    frameInsert(file_cords_name, file_extension,axis_of_good,channelid,rotation,scalexyz)
    
    #for xc in axis_of_good:
    #    print (xc)
    #return "ok"


def set_axis(osi_xy,rotation,scalexyz,anchor_xy):
    x3=[]
    #ced1=[]
    #ced=[]
    r_factor = 0 # point of rotation    
    r_factor_summ = 0 # rotation summ
    r_factor_way = 0
    s_factor = 0 #scale factor
    s_factor_summ = 0 # scale factor summ

    print('rotation : ', rotation,'scale : ', scalexyz,'anchor : ',anchor_xy)
    for x1 in osi_xy:
        #print(x1)
        r_date = [val for val in rotation if val[0]==x1[0]]
        s_date = [val for val in scalexyz if val[0]==x1[0]]
        a_date = [val for val in anchor_xy if val[0]==x1[0]]
       # print(a_date)
        if r_date is not None:
            for ced in r_date:
                if r_factor_way is None:
                    r_factor_way = 0
                else:
                    r_factor_way = 1
               
                if ced[1] < 0:
                    #print('< 0')
                    r_factor = 0.3
                    r_factor_summ = ced[1]

                    
                else:
                    #print('> 0')
                    r_factor_summ = ced[1]
                    r_factor = -0.7 
        if s_date is not None:

            for ced1 in s_date:
                if r_factor_way == 0:
                    #print('< 0')
                    s_factor = 0.1
                    s_factor_summ = ced1[1]

                   
                else:
                    #print('> 0')
                    s_factor = ced1[1]
                    s_factor_summ = 0.1 
        if a_date is not None:
            for ced2 in a_date:pass
        
       # print('fff', ced[1], 'dfdfd :',r_factor_summ, round(r_factor_summ, 2))
        print('rotation1 : ',ced1[0])
        if ced[0] == x1[0]:
            print ('rotation find',ced[0],'cc : ',ced[1])
            
        x3.append([x1[0],x1[1],x1[2],r_factor_summ,ced1[1],ced2[1],ced2[2]])
        #print('sdfsdfsfs')
       # print('frame : ',x1[0],'x :',x1[1],'y : ',x1[2]) 
       #print('frame : ',x1[0],'x :',x1[1],'y : ',x1[2],'rotation : ',round(r_factor_summ, 2),'scale : ',ced1[1],'anchor x :',ced2[1],'anchor y :',ced2[2])
        r_factor_summ+=r_factor
        s_factor_summ+= s_factor
    return x3

def frameInsert(nameimg, file_extension, axis, channelid,rotation,scalexyz):
    scn = bpy.context.scene
    seq = scn.sequence_editor
    file_name =nameimg+"."+file_extension
    #print(axis[1][0],'sssssss')
    
    image = seq.sequences.new_image(nameimg, file_name, channelid, axis[0][0])
    trans1 = seq.sequences.new_effect(nameimg, "TRANSFORM", channelid, axis[0][0], len(image.elements), image)
    bpy.ops.sequencer.meta_make()
    
    meta = scn.sequence_editor.active_strip
    
    
    meta.frame_final_duration = (axis[-1][0])+1
    #seq_meta = bpy.types.MetaSequence(image)
    
    trans = seq.sequences.new_effect(nameimg, "TRANSFORM", channelid+1, axis[0][0], len(image.elements), meta)
    
    trans.translation_unit='PIXELS'
    #trans.scale_start_x=0.94
    trans.update()
    
    image.frame_final_duration =(axis[-1][0])+1
    
    image.directory=dir_in
    image.colorspace_settings.name = 'sRGB'
    trans.blend_type='ALPHA_OVER'
    trans.use_uniform_scale = True

    trans1.blend_type='ALPHA_OVER'
    trans1.use_uniform_scale = True
    image.use_translation=True
    for frame in axis:
        r_date = [val for val in rotation if val[0]==frame[0]]
        s_date = [val for val in scalexyz if val[0]==frame[0]]

        #print(frame[0])
        scn.frame_current = int(frame[0])
#        k_x, k_y = 0,0
        k_x = (frame[5]-427)*(frame[4]/100)
        k_y = (frame[6]-240)*(frame[4]/100)
        trans.translate_start_x=(frame[1]+k_x)-427
        #print('frameszzz:',frame[5])
        trans.keyframe_insert(data_path="translate_start_x", frame=int(frame[0]))
        trans.update()
        trans.translate_start_y=((240-frame[2])+k_y)
        #print(frame[2])
        trans.keyframe_insert(data_path="translate_start_y", frame=int(frame[0]))

        for r_id in r_date:
            if r_id[0] == frame[0]:
                trans.rotation_start=float(frame[3])/(-1)
                trans.keyframe_insert(data_path="rotation_start", frame=int(frame[0]))
                #trans1.rotation_start=float(frame[3])/(-1)
                #trans1.keyframe_insert(data_path="rotation_start", frame=int(frame[0]))
        for s_id in s_date:
            if s_id[0] == frame[0]:
                trans.scale_start_x=float(frame[4])/(100)+0.025
                trans.use_uniform_scale=1
                trans.keyframe_insert(data_path="scale_start_x", frame=int(frame[0]))
                trans.scale_start_y=float(frame[4])/(100)+0.025
                trans.keyframe_insert(data_path="scale_start_y", frame=int(frame[0]))

                trans1.scale_start_x=float(0.80)
                trans1.use_uniform_scale=1
                trans1.keyframe_insert(data_path="scale_start_x", frame=int(frame[0]))
                trans1.scale_start_y=float(0.80)
                trans1.keyframe_insert(data_path="scale_start_y", frame=int(frame[0]))
    #if int(override_end_rend[-1]) > int(frame[-1][0]):print('frame>>>>>>')
    
    
    
    override_end_rend.append(axis[-1][0])    
    return '{OK}'


def addimage(frames_osi_xy, nameimg, file_extension, resolution, rotation, channelid, scalexyz):
    bpy.context.scene.sequence_editor
    print(frames_osi_xy[-1][0],'sssssss')
    print(resolution[0], 'in here')
    scene =  bpy.context.scene
    file_name =nameimg+"."+file_extension
    imageinscene = scene.sequence_editor.sequences.new_image(nameimg, file_name, channelid, int(frames_osi_xy[0][0]))
    seqtransf = scene.sequence_editor.sequences.new_effect(nameimg, "TRANSFORM", channelid,int(frames_osi_xy[0][0]), len(imageinscene.elements), imageinscene)
    seqtransf.translation_unit='PIXELS'
    seqtransf.scale_start_x=0.94
    seqtransf.update()
    imageinscene.frame_final_duration =int(frames_osi_xy[-1][0])
    imageinscene.directory=dir_in
    print(type(imageinscene))
    print(len(frames_osi_xy))
    imageinscene.colorspace_settings.name = 'sRGB'
    seqtransf.blend_type='ALPHA_OVER'
    seqtransf.use_uniform_scale = True
    imageinscene.use_translation=True
    imageinscene.transform.offset_x = 0#int(resolution[0])/2
    imageinscene.transform.offset_y = 0#int(resolution[1])/2
    for resolution_transfom in frames_osi_xy:
        print('Resolution x,y:',resolution_transfom)
        asix_x=(float(resolution_transfom[1])-427)
        seqtransf.translate_start_x=float(asix_x)

        seqtransf.keyframe_insert(data_path="translate_start_x", frame=int(resolution_transfom[0]))
        asix_y=((float(resolution_transfom[2])-240))
        seqtransf.translate_start_y=float(asix_y)
        seqtransf.keyframe_insert(data_path="translate_start_y", frame=int(resolution_transfom[0]))
        print('set x asix',seqtransf.translate_start_x, ' and we find axis is',asix_x,' y axis is ',asix_y)
    for rotation_in in rotation:
        seqtransf.rotation_start=float(rotation_in[1])/(-1)
        seqtransf.keyframe_insert(data_path="rotation_start", frame=int(rotation_in[0]))
    
    for scalexyz_in in scalexyz:
        seqtransf.scale_start_x=float(scalexyz_in[1])/(100)
        seqtransf.use_uniform_scale=1
        seqtransf.keyframe_insert(data_path="scale_start_x", frame=int(scalexyz_in[0]))
        seqtransf.keyframe_insert(data_path="scale_start_y", frame=int(scalexyz_in[0]))
        #seqtransf.use_uniform_scale=1
         
    if int(override_end_rend[-1]) > int(frames_osi_xy[-1][0]):print('frame>>>>>>')
    override_end_rend.append(frames_osi_xy[-1][0])
    return 'ok'

if __name__ == '__main__':
    bpy.context.scene.render.resolution_x=854
    bpy.context.scene.render.resolution_y=480
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.fps = 25

    main()
    str_name_file=str(datetime.datetime.now())
    name_file_time = re.match(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+).(\d+)', str_name_file)
    name_file= name_file_time.group(7).split()[0]+'.blend'
    bpy.context.scene.frame_end=int(override_end_rend[-1])
    bpy.ops.wm.save_as_mainfile(filepath=name_file)