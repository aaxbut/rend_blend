from aiohttp import web
import asyncio
import logging
import uvloop
import json

import aiohttp_session
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64
from cryptography import fernet

import ssl


import multiprocessing as mp
from multiprocessing import Process, freeze_support
from queue import Empty
import bpy
from datetime import datetime
import time




@asyncio.coroutine
def handle(request):
    #pass
    logging.info('in test module {0}'.format(request.json))
    if request.method == 'POST':
        print('post!!!!!')
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


@asyncio.coroutine
def wshandler(request):
    if request.method == 'POST':
        print('post!!!!!')
    logging.info('in wshandler module {0}'.format(request.json))
    ws = web.WebSocketResponse()
    ws.prepare(request)
    for msg in ws:
        if msg.type == web.MsgType.text:
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break
    return ws


@asyncio.coroutine
def check_data(data):
    data['start_frame']=0
    data['end_frame']=50

    return data


@asyncio.coroutine
def transmit(request):
    request.post()
    data = yield from request.text()
    #args = yield from get_session(request)
    #yield data

    req_json = json.loads(data)
   # req_json = check_data(req_json)
    #print(req_json)
    logging.info('Session method : {}, session type : {}, messages is : {} : {}'.format(request.method, request, request, req_json))


        

        

        #ses = await get_session(request)
        #ses['key'] = 'sdsdsd'
        #print('session aio http__ ',ses)
        #for x in request:
         #   logging.info('request in  : {}'.format(x))


    if request.content_type == 'application/json': 
        # logging.info('Session method : {}, session type : {}, messages is : {}'.format(request.method, request.content_type, req_json))

            # run render 
        k = yield from run_render_multi(req_json)

        return web.json_response(k)
    return web.Response(body=json.dumps({'ok': req_json}).encode('utf-8'),
        content_type='application/json')#(yield from request.text())


### start render module
#before render 
BLEND_DIR =r'blend_pr'
USERS_DIR =r'/home/aaxbut/python/rend_blend/users'


#for x in bpy.data.scenes['Scene'].sequence_editor.sequences_all:
#    if x.type == 'IMAGE':
#        seq_elem = x.strip_elem_from_frame(0)
#        #print(x.name.split('.')[0])
#        if x.name.split('.')[0] in task['files_png']:
#            print('test', task['files_png'][x.name.split('.')[0]])
#            seq_elem.filename = task['files_png'][x.name.split('.')[0]]


def find_before(task):


    for entry in os.scandir(os.path.join(BLEND_DIR, task['project_name'])):

        if not entry.name.startswith('.') and entry.is_file():

            if entry.name == task['project_name'] +'.blend':
           #     print ('found file project  : {} '.format(entry.name))
                #bpy.path = os.path.join(BLEND_DIR, task['name'])
                ##print('work dir ',bpy.path.basename(os.path.join(BLEND_DIR, task['name'])))
             #   print ('directory in : ',os.getcwd())
                # set directory where file place    
                os.chdir(os.path.abspath(os.path.join(BLEND_DIR, task['project_name'])))

               # print ('directory in :2 : ',os.getcwd())    
                bpy.ops.wm.open_mainfile(filepath=entry.name)
                name_file =task['user']+entry.name
                bpy.ops.wm.save_as_mainfile(filepath=name_file)

                #print('os dir now',os.path.abspath(os.path.join(USERS_DIR, task['user'])))
    bpy.ops.wm.open_mainfile(filepath=name_file)


    for entry1 in os.listdir(os.path.join(USERS_DIR, task['user'])):
        for entry2 in os.listdir(os.path.join(USERS_DIR, task['user'], entry1)):
            for x in bpy.data.scenes['Scene'].sequence_editor.sequences_all:
                if x.type == 'IMAGE':
                    seq_elem = x.strip_elem_from_frame(0)
                    #print(x.name.split('.')[0])
                    if x.name.split('.')[0] in task['files_png']:
                       # print('test', task['files_png'][x.name.split('.')[0]])
                       # print('dfddfdf',os.path.join(USERS_DIR, task['user'], entry1))

                        seq_elem.filename = task['files_png'][x.name.split('.')[0]]

                        x.directory = os.path.join(USERS_DIR, task['user'], entry1)

    bpy.ops.wm.save_as_mainfile(filepath=name_file)
    return '{ok}'


##

def worker(q,task):

    logging.info('{}: TASK:{} Q: {}'.format(datetime.now().strftime('%c'),task,type(q)))
    while True:
        try:
            
            q.get_nowait()
            logging.info('{} : WORKER: {} and file name {}'.format(datetime.now().strftime('%c'), task,task['project_name']))
            ## before render we create new file project of blender, and run render it self

            #bpy.ops.wm.open_mainfile(filepath=task['file_name'])
            find_before(task)
            bpy.context.scene.render.filepath =r'/tmp/'+str(time.time())
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.device='CPU'
            bpy.context.scene.frame_start = 0
            bpy.context.scene.frame_end = 200

            l = bpy.ops.render.render(animation=True,scene=bpy.context.scene.name)
            logging.info('render  name {} complete at {}'.format(l,datetime.now().strftime('%c')))
            if l == {'FINISHED'}: 
                q.task_done()
           ## logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
        except Empty:
           # logging.info('in worker have exception: {} and file name {}'.format(task,task['file_name']))
           # logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
            logging.info('render  name {} complete at {}'.format(task['project_name'],datetime.now().strftime('%c')))
            break
            

# --


@asyncio.coroutine
def run_render_multi(data_for_render):
    
    tasks = []
    server_info()
    if data_for_render['message'] =='We did it!':
        logging.info('render file name {} complete at {} CPU count {}'.format(data_for_render['project_name'],datetime.now().strftime('%c'),os.cpu_count()))
        freeze_support()
        num_procs = os.cpu_count();
        q =  mp.JoinableQueue(2)
        logging.info('in test module {0}'.format(data_for_render['sender']))
        
        tasks.append(data_for_render)

        for task in tasks:
                q.put(task)
                    #logging.info('task name {} and file name {}'.format(task,x['file_name']))
        procs = (mp.Process(target= worker, args=(q,task,)) for _ in range(num_procs))
        for p in procs:
        #p.daemon = True
            p.start()
           # p.join()
        for p in procs: 
            p.join()
    return data_for_render

### end render module 


### server info
import sys, os, platform, shutil


def server_info():
    sysname, nodename, release, version, machine, processor = platform.uname()
    logging.info('{} SRV: {} '.format(datetime.now().strftime('%c'), nodename))




### end server info 

#if __name__ == '__main__':
# log level debug
def init(loop):
    logging.basicConfig(level=logging.DEBUG)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    
    app = web.Application()


    app.router.add_route('GET','/echo', wshandler)
    app.router.add_post('/tr', transmit)
   # app.router.add_route('POST','/tr', transmit)
    app.router.add_route('GET','/', handle)
    app.router.add_route('POST','/', handle)
    app.router.add_route('GET','/{name}', handle)
    #setup(app, EncryptedCookieStorage(secret_key))
    #setup(app, EncryptedCookieStorage(secret_key))
    
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    #loop = asyncio.get_event_loop()
    f = yield from loop.create_server(app.make_handler(),'0.0.0.0',781)
    return f


app = web.Application()
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try: 
    loop.run_forever()
except KeyboardInterrupt:  
    pass