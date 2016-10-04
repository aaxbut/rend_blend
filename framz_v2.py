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
    meta_strip =0
    channelid=1
    bpy.context.scene.sequence_editor_create()
    meta_strip = []
    for x in os.listdir(dir_in):
        try:
            if x.split('.')[4] == 'txt':           
                d = os.path.join(dir_in, x)
                #meta_strip.append(x.split(".")[1])
                #print(x,x.split(".")[0],x.split(".")[1],x.split(".")[2],x.split(".")[3])
                print('file name in : ',d)
                k = coords_fo_frames_xy(d, x.split(".")[0], x.split(".")[3],channelid,int(x.split(".")[1]),int(x.split(".")[2]))
                meta_strip.append(k)
                #print('this is K :', k)
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
    return meta_strip


def insert_moview_file(pathaaf, file_cords_name, file_extension,channelid):
    file_name = file_cords_name+'.'+file_extension
    fpath = pathaaf+file_name
    #print(pathaaf)
    #print('+')
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
    #dd1.sequences.blend_type='ALPHA_UNDER'
    return '{OK}'
    
    
def coords_fo_frames_xy(pathaaf, file_cords_name, file_extension,channelid,meta_strip_number, coord_type):
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
        
        xy_coordframe = re.match(r'(\t(\d+))(\t*\-*(\d+).\d+)(\t*\-*(\d+).\d+)', x) # x,y
       #print(xy_coordframe)
        #scalecoord = re.match(r'(\t(\d+))(\t(\d+.)*\-*\d+)(?<!(\t))',x)
        scalecoord = re.match(r'(\t(\d+))(\t*\-*(\d+).\d+)(\t*\-*(\d+).\d+)', x) # x,y
        if source_hw is not None: # ok we find them
            #print(source_hw.group().split()[2])
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
                print(int(xy_coordframe.group().split()[0]),float(xy_coordframe.group().split()[1]),float(xy_coordframe.group().split()[2]))
        elif s_flag==1:
            scalecoord = re.match(r'(\t(\d+))(\t(\d+.)*\-*\d+)(?<!(\t))',x)
            if scalecoord is not None:
                #print('scale + +',int(scalecoord.group().split()[0]),float(scalecoord.group().split()[1]))
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
               # print('anchor + +',int(anchor_point_c.group().split()[0]),float(anchor_point_c.group().split()[1]),float(anchor_point_c.group().split()[2]))
                anchor_xy.append([int(anchor_point_c.group().split()[0]),float(anchor_point_c.group().split()[1]),float(anchor_point_c.group().split()[2])])
       # elif asix_flag==1:
       #     if xy_coordframe is not None:
       #         osi_xy.append([int(xy_coordframe.group().split()[0]),float(xy_coordframe.group().split()[1]),float(xy_coordframe.group().split()[2])])

    axis_of_good = set_axis(osi_xy,rotation,scalexyz,anchor_xy,file_cords_name)
    #print('ffffff')
#    transform_hw_cle = list(dict(zip(transform_hw_befor,transform_hw_befor)).values())

    frameInsert(file_cords_name, file_extension,axis_of_good,channelid,rotation,scalexyz,coord_type)
    
    #for xc in axis_of_good:
    #    print (xc)
    return file_cords_name, axis_of_good, meta_strip_number, coord_type


def set_axis(osi_xy,rotation,scalexyz,anchor_xy,file_cords_name):
    x3=[]


    #print('rotation : ', rotation,'scale : ', scalexyz,'anchor : ',anchor_xy)
    for frame_coords in osi_xy:
        
        r_date = [val for val in rotation if val[0]==frame_coords[0]]
        s_date = [val for val in scalexyz if val[0]==frame_coords[0]]
        a_date = [val for val in anchor_xy if val[0]==frame_coords[0]]
        #print('in set axis : ','frame : ',x1, 'Rotation : ',r_date,'Scale',s_date,'Anchor',a_date)
        if r_date is not None:
            #print('r_date not None')
            for frame_rotation in r_date: pass
        if s_date is not None:
            #print('s_date not None')
            for frame_scale in s_date: pass
        if a_date is not None:
            #print('a_date not None')
            for frame_anchor in a_date: pass
        
        #print('in set axis : ','frame : ',frame_coords[0], 'Rotation : ',frame_rotation[0],'Scale',frame_scale[0],'Anchor',frame_anchor[0])
        x3.append([frame_coords[0],frame_coords[1],frame_coords[2],frame_rotation[1],frame_scale[1],frame_anchor[1],frame_anchor[2]])
               
    return x3

def frameInsert(nameimg, file_extension, axis, channelid,rotation,scalexyz,cord_type):
    scn = bpy.context.scene
    seq = scn.sequence_editor
    file_name =nameimg+"."+file_extension
    metastrip_list=[]
    trans_name =nameimg+'_transform'
    image = seq.sequences.new_image(nameimg, file_name, channelid, axis[0][0])
    image_transform = seq.sequences.new_effect(trans_name, "TRANSFORM", channelid, axis[0][0], len(image.elements), image)
    #print('Len elements : ',len(image.elements))
    image_transform.translation_unit='PIXELS'
    #trans.scale_start_x=0.94
    #trans.update()
    image_transform.update()
    image.frame_final_duration =(axis[-1][0])+1
    image.directory=dir_in
    image.colorspace_settings.name = 'sRGB'
    image_transform.blend_type='ALPHA_OVER'
    image_transform.use_uniform_scale = True
    image.use_translation=True
    for frame in axis:
        r_date = [val for val in rotation if val[0]==frame[0]]
        s_date = [val for val in scalexyz if val[0]==frame[0]]
        scn.frame_current = int(frame[0])
        if int(cord_type) == 2:
            k_x = (frame[5]-427)*(frame[4]/100)
            k_y = (frame[6]-240)*(frame[4]/100)
            image_transform.translate_start_x=(frame[1]+k_x)-427
            
            image_transform.keyframe_insert(data_path="translate_start_x", frame=int(frame[0]))
            image_transform.update()
            image_transform.translate_start_y=((240-frame[2])+k_y)
                 ##print(frame[2])
            image_transform.keyframe_insert(data_path="translate_start_y", frame=int(frame[0]))
            for r_id in r_date:
                if r_id[0] == frame[0]:
                    image_transform.rotation_start=float(frame[3])/(-1)
                    image_transform.keyframe_insert(data_path="rotation_start", frame=int(frame[0]))
            for s_id in s_date:
                if s_id[0] == frame[0]:
                    image_transform.scale_start_x=float(frame[4])/100
                    image_transform.use_uniform_scale=1
                    image_transform.keyframe_insert(data_path="scale_start_x", frame=int(frame[0]))
                    image_transform.scale_start_y=float(frame[4])/100
                    image_transform.keyframe_insert(data_path="scale_start_y", frame=int(frame[0]))

        elif int(cord_type) == 1:
            for s_id in s_date:
                if s_id[0] == frame[0]:
                    #image_transform.scale_start_x=float(frame[4])/100
                    image_transform.scale_start_x=0.5
                    image_transform.use_uniform_scale=1
                    image_transform.keyframe_insert(data_path="scale_start_x", frame=int(frame[0]))
                    #image_transform.scale_start_y=float(frame[4])/100
                    image_transform.scale_start_y=0.5
                    image_transform.keyframe_insert(data_path="scale_start_y", frame=int(frame[0]))
    
    override_end_rend.append(axis[-1][0])
    


    return '{OK}'


def makemake(k):
    i=0
    scn = bpy.context.scene
    seq = scn.sequence_editor
    
    for max_value_mets in k:
       # print('++++++')
    #    xx = [x1 for x1 in x]
        #print('this makemake :', x[0],'meta_numb:',x[2],'cord_type',x[3],'cords :',x[1])
        if i < int(max_value_mets[2]):
            i+=1
        #print(max_value_mets[1][0])
    #    for cords in x[1]:
    #        print(cords)
    #    print(xx[0],xx[1],xx[2],xx[3])
   # print('++++++')
    #    print(x[0])
    #    print('++++++')
    #print(i)
    for seq_meta_in in range(i):
        seq_meta_in+=1
        for s2 in scn.sequence_editor.sequences_all:
            bpy.context.scene.sequence_editor.active_strip = None
            bpy.ops.sequencer.meta_toggle('EXEC_AREA')
            s2.select = False
            #print(s2.name,'set status false',':',s2.select)
        meta_sort = [meta_sort for meta_sort in k if meta_sort[2] == seq_meta_in]
        #print('metasort3:',meta_sort)
        trans_start = [meta_sort for meta_sort in k if meta_sort[2] == seq_meta_in and meta_sort[3] == 1]
        select_strip = [strip_name for strip_name in scn.sequence_editor.sequences_all for x2 in meta_sort if strip_name.name == x2[0] or strip_name.name == x2[0]+'_transform']
        for seq_tra in select_strip:
            seq_tra.select = True
            #print(seq_tra.type,seq_tra.name,seq_tra.select)
    #print(xxx1)
        #print('tip coordinat: ',trans_start[0][3])
        bpy.ops.sequencer.meta_make()
        meta = scn.sequence_editor.active_strip
        meta.name = str(seq_meta_in)
        meta_transform_name = str(seq_meta_in)+'_transform'
        #print('ddddddsdfsdasdasd',trans_start[0][1][0][0])
        meta_transform_obj = seq.sequences.new_effect(meta_transform_name, "TRANSFORM", seq_meta_in, trans_start[0][1][0][0], 1, meta)
        meta_transform_obj.blend_type='ALPHA_OVER'
        meta_transform_obj.translation_unit='PIXELS'
        meta_transform_obj.use_uniform_scale = True
        rotation_x_state=0.0
        for frame_c in trans_start[0][1]:
            #print(frame_c)
            if trans_start[0][3] == 1:
                #print('name file : ', frame_c[0])
                #print(frame_c)
                scn.frame_current = frame_c[0]
    #        k_x, k_y = 0,0
                k_x = (float(frame_c[5])-427)*(float(frame_c[4])/100)
                k_y = (float(frame_c[6])-240)*(float(frame_c[4])/100)
                print(frame_c[0],'koef :x  ',k_x,'koef :y ',k_y,'anchor x :',frame_c[5],'anchor y: ',frame_c[6],'x : ',frame_c[1], 'y : ', frame_c[2],'scale: ',frame_c[4])

                meta_transform_obj.translate_start_x=(frame_c[1]+k_x)-427
                #print(frame_c[0],'test frame 313 : ',meta_transform_obj.translate_start_x)
                
                meta_transform_obj.keyframe_insert(data_path="translate_start_x", frame=int(frame_c[0]))
                
                meta_transform_obj.translate_start_y=((240-frame_c[2])+k_y)

                
                meta_transform_obj.keyframe_insert(data_path="translate_start_y", frame=int(frame_c[0]))
                
                
                if rotation_x_state == float(frame_c[3])/(-1):
                    pass
                    #print('rotation_x_state',rotation_x_state)
                    
                else:
                    #print('rotation_x_state !=',rotation_x_state)
                    meta_transform_obj.rotation_start=float(frame_c[3])/(-1)
                    meta_transform_obj.keyframe_insert(data_path="rotation_start", frame=int(frame_c[0]))

               


                meta_transform_obj.scale_start_x=(float(frame_c[4])/(100))*2
                meta_transform_obj.use_uniform_scale=1
                meta_transform_obj.keyframe_insert(data_path="scale_start_x", frame=int(frame_c[0]))
                meta_transform_obj.scale_start_y=(float(frame_c[4])/(100))*2
                meta_transform_obj.keyframe_insert(data_path="scale_start_y", frame=int(frame_c[0]))

               # print(xcc)
                rotation_x_state=float(frame_c[3])/(-1)
                meta_transform_obj.update()
        #print(xxx1)



        #print(x)



if __name__ == '__main__':
    bpy.context.scene.render.resolution_x=854
    bpy.context.scene.render.resolution_y=480
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.fps = 25
    #print(meta_strip)
    k=main()
    makemake(k)
    str_name_file=str(datetime.datetime.now())
    name_file_time = re.match(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+).(\d+)', str_name_file)
    name_file= name_file_time.group(7).split()[0]+'.blend'
    print(name_file)
    bpy.context.scene.frame_end=int(override_end_rend[-1])
    bpy.ops.wm.save_as_mainfile(filepath=name_file)