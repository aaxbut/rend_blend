from aiohttp import web
import asyncio
import logging
import json

import aiohttp_session
from aiohttp_session import setup, get_session, session_middleware
#from aiohttp_session.cookie_storage import EncryptedCookieStorage

import multiprocessing as mp
from multiprocessing import Process, freeze_support
from queue import Empty
import bpy
from datetime import datetime
import time

# import config settings
import configparser


conf = configparser.RawConfigParser()
conf.read('wb.conf')
BLEND_DIR = conf.get('bl_path','BLEND_DIR')
USERS_DIR = conf.get('bl_path','USERS_DIR')
dbconnectionhost = conf.get('base','dbconnectionhost')
dbname = conf.get('base','dbname')
dbusername = conf.get('base','dbusername')
dbpassword = conf.get('base','dbpassword')

# base connect
#import MySQLdb as mysql

#db = mysql.connect(host=dbconnectionhost,user=dbusername,passwd=dbpassword,db=dbname)
# end import config settings

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
    ts = []
    data = yield from request.text()
    req_json = json.loads(data)
    logging.info('Session method : {}, session type : {}, messages is : {} : {}'.format(request.method, request, request, req_json))


        

        

        #ses = await get_session(request)
        #ses['key'] = 'sdsdsd'
        #print('session aio http__ ',ses)
        #for x in request:
         #   logging.info('request in  : {}'.format(x))


    if request.content_type == 'application/json':

        yield from run_render_multi(req_json)
        
        #logging.info(__name__)
        logging.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!YIELD FROM REND_BLRND_MULTI RETURN MESSAGES : {}'.format(req_json['user']))

        return web.json_response(req_json)
    return web.Response(body=json.dumps({'ok': req_json}).encode('utf-8'),
        content_type='application/json')#(yield from request.text())


### start render module
#before render 




#for x in bpy.data.scenes['Scene'].sequence_editor.sequences_all:
#    if x.type == 'IMAGE':
#        seq_elem = x.strip_elem_from_frame(0)
#        #print(x.name.split('.')[0])
#        if x.name.split('.')[0] in task['files_png']:
#            print('test', task['files_png'][x.name.split('.')[0]])
#            seq_elem.filename = task['files_png'][x.name.split('.')[0]]


def find_before(task):
    name_file=''


    for entry in os.scandir(os.path.join(BLEND_DIR, task['project_name'])):

        if not entry.name.startswith('.') and entry.is_file():

            if entry.name == task['project_name'] +'.blend':
           #     print ('found file project  : {} '.format(entry.name))
                #bpy.path = os.path.join(BLEND_DIR, task['name'])
                print('work dir ',bpy.path.basename(os.path.join(BLEND_DIR, task['name'])))
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
    return os.path.abspath(os.path.join(BLEND_DIR,name_file))



from bpy.app.handlers import persistent
##
@persistent
def render_complete(scene):
    logging.info('#####################{} #########################{}#########{}####'.format(scene,bpy.data.filepath,bpy.context.scene.render.filepath))
    logging.info('#####{}####{}##'.format(os.path.abspath(bpy.data.filepath),bpy.data.filepath))

    try:
        ins()
        os.remove(os.path.abspath(bpy.data.filepath))
        os.remove(os.path.abspath(bpy.data.filepath+'1'))
    except:
        pass


#@asyncio.coroutine
def worker(q,task):
    

    logging.info('{}: TASK:{} Q: {}'.format(datetime.now().strftime('%c'),task,type(q)))
    while True:
        try:
            
            q.get_nowait()
            logging.info('{} : WORKER: {} and file name {}'.format(datetime.now().strftime('%c'), task,task['project_name']))
            ## before render we create new file project of blender, and run render it self

            #bpy.ops.wm.open_mainfile(filepath=task['file_name'])
            o = find_before(task)
            bpy.context.scene.render.filepath =str(task['result_dir'])+str(time.time())
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.device='CPU'
            bpy.context.scene.frame_start = 0
            bpy.context.scene.frame_end = 10
            
            bpy.ops.render.render(animation=True,scene=bpy.context.scene.name)
            
            #logging.info(' ###########{} ###################: render  name {} '.format(g,task['project_name']))
           # yield from p
            #    logging.info(' {} ###################: render  name {} path {}: {}'.format(q.get(),task['project_name'],datetime.now().strftime('%c'),o))
            #    try:
            #        os.remove(o)
            #    except: pass

            q.task_done()
           ## logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
        except Empty: break
           # logging.info('in worker have exception: {} and file name {}'.format(task,task['file_name']))
           # logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))
            #logging.info(' render  name {} complete at {}'.format(task['project_name'],datetime.now().strftime('%c')))
            
            

# --


@asyncio.coroutine
def run_render_multi(data_for_render):
    
    tasks = []
    g=[]
    server_info()
   
    if data_for_render['message'] =='We did it!':
        
        logging.info('render file name {} start at {} CPU count {}'.format(data_for_render['project_name'],datetime.now().strftime('%c'),os.cpu_count()))
        freeze_support()
        num_procs = os.cpu_count();
        q =  mp.JoinableQueue()
        
        
        tasks.append(data_for_render)
        logging.info('!!!!!len of TASK {}:  QUE SIZE {}'.format(len(tasks), q.qsize()))
        for task in tasks:
                q.put(task)
                
                    #logging.info('task name {} and file name {}'.format(task,x['file_name']))

        procs = (mp.Process(target=worker, args=(q,task,)) for _ in range(3))
        logging.info('!!!!!!!!!!!!!!!!!!!!! {} ******************'.format(procs))
        #procs[0].start()
        #time.sleep(1)
        for p in procs:
            p.daemon = True
            #g.append(1)
            logging.info('!!!!!!!!!!!!!!!!!!!!! {} ******************'.format(p))
            p.start()
           #p.join()
           
           
        
           # p.join()
        for p in procs: 
            p.join()
           # time.sleep(1)
            if not p.is_alive():
                logging.info('!!!!!!!!!!!!!!!!!!!!! {} ******************'.format(p))
                sys.stdout.flush()
           
        

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
    bpy.app.handlers.render_complete.append(render_complete)

   # fernet_key = fernet.Fernet.generate_key()
   # secret_key = base64.urlsafe_b64decode(fernet_key)
    
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
srv = loop.run_until_complete(init(loop))
#srv = loop.run_until_complete(f)
    
try: 
    loop.run_forever()
    print('serving on', srv.sockets[0].getsockname())
except KeyboardInterrupt:
    loop.close()  
    #pass