from aiohttp import web
import asyncio
import logging
import uvloop
import json


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





async def handle(request):
        #pass
        logging.info('in test module {0}'.format(request.json))
        if request.method == 'POST':
            print('post!!!!!')
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)



async def wshandler(request):
        if request.method == 'POST':
            print('post!!!!!')
        logging.info('in wshandler module {0}'.format(request.json))
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        for msg in ws:
            if msg.type == web.MsgType.text:
                ws.send_str("Hello, {}".format(msg.data))
            elif msg.type == web.MsgType.binary:
                ws.send_bytes(msg.data)
            elif msg.type == web.MsgType.close:
                break
        return ws



async def check_data(data):
    

    data['start_frame']=0
    data['end_frame']=50

    return data



async def transmit(request):
        request.post()
        req_json = json.loads(await request.text())
        req_json = await check_data(req_json)
        

        

        #ses = await get_session(request)
        #ses['key'] = 'sdsdsd'
        #print('session aio http__ ',ses)
        #for x in request:
         #   logging.info('request in  : {}'.format(x))


        if request.content_type == 'application/json':
            logging.info('Session method : {}, session type : {}, messages is : {}'.format(request.method, request.content_type, req_json))
            # run render 
           # k = await run_render_multi(req_json) 

        return web.json_response(await run_render_multi(req_json))


### start render module

def worker(q,task):

    logging.info('{}: TASK:{} Q: {}'.format(datetime.now().strftime('%c'),task,type(q)))
    while True:
        try:
            
            q.get_nowait()
            logging.info('{} : WORKER: {} and file name {}'.format(datetime.now().strftime('%c'), task,task['file_name']))
            bpy.ops.wm.open_mainfile(filepath=task['file_name'])
            bpy.context.scene.render.filepath =r'/tmp/'+str(time.time())
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.device='CPU'
            bpy.context.scene.frame_start = 0
            bpy.context.scene.frame_end = 10

            #bpy.ops.render.render(animation=True,scene=bpy.context.scene.name)
            q.task_done()
           ## logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
        except Empty:
           # logging.info('in worker have exception: {} and file name {}'.format(task,task['file_name']))
           # logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
            logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
            break
            

# --



async def run_render_multi(data_for_render):
    
    tasks = []
    server_info()
    if data_for_render['message'] =='We did it!':
        logging.info('render file name {} complete at {} CPU count {}'.format(data_for_render['file_name'],datetime.now().strftime('%c'),os.cpu_count()))
        freeze_support()
        num_procs = os.cpu_count();
        q =  mp.JoinableQueue()
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
        for p in procs: p.join()
    return '{OK}'

### end render module 


### server info
import sys, os, platform, shutil


def server_info():
    sysname, nodename, release, version, machine, processor = platform.uname()
    logging.info('{} SRV: {} '.format(datetime.now().strftime('%c'), nodename))




### end server info 

if __name__ == '__main__':
# log level debug

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

    setup(app, EncryptedCookieStorage(secret_key))
    
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    loop = asyncio.get_event_loop()
    f = loop.create_server(app.make_handler(),'0.0.0.0',8080)
    
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        print(type(loop.run_forever()))
        loop.run_forever()
        
    except KeyboardInterrupt:
        pass 