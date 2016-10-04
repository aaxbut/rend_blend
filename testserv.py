import asyncio
import logging
import uvloop
import json
import aiohttp
import time
import base64
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import MultiDict


import multiprocessing as mp
from multiprocessing import Process, freeze_support
from queue import Empty
import bpy
from datetime import datetime
from urllib.parse import parse_qsl
from aiohttp import web
# -- multiprocessing

def worker(q,task):
	while True:
		try:
			q.get_nowait()
			logging.info('worker: {} and file name {}'.format(task,task['file_name']))
			bpy.ops.wm.open_mainfile(filepath=task['file_name'])
			bpy.context.scene.render.filepath =r'/tmp/'+str(time.time())
			bpy.context.scene.render.engine = 'CYCLES'
			bpy.context.scene.cycles.device='CPU'
			bpy.context.scene.frame_start = 0
			bpy.context.scene.frame_end = 10

			bpy.ops.render.render(animation=True,scene=bpy.context.scene.name)
			q.task_done()
		except Empty:
			break
	logging.info('render file name {} complete at {}'.format(task['file_name'],datetime.now().strftime('%c')))

# --


@asyncio.coroutine	
def run_render_multi(data_for_render):
	tasks = []

	if data_for_render['message'] =='We did it!':
			freeze_support()
			num_procs = 1
			q =  mp.JoinableQueue()
			logging.info('in test module {0}'.format(data_for_render['sender']))
			tasks.append(data_for_render)

			for task in tasks:
					q.put(task)
					#logging.info('task name {} and file name {}'.format(task,x['file_name']))
			procs = (mp.Process(target=worker, args=(q,task,)) for _ in range(num_procs))
			for p in procs:
		#p.daemon = True
				p.start()
		
			for p in procs: p.join()


    	
    
class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
    @asyncio.coroutine
    def handle_request(self, message, payload):
        app = web.Application()
        app.router.add_route('GET', '/{name}', self.variable_handler)
        e_data={}
        response = aiohttp.Response(
			self.writer, 200, http_version=message.version
			)
        response.add_header('Content-Type', 'text/html')
        response.add_header('Content-Length', '18')
        response.send_headers()
        response.write(b'<h1>ddd</h>')
		#print(response)
        yield from response.write_eof()
		#session = await get_session(self.request)
        try:
            data = yield from payload.read()
			#print('payload.read ',data)
			#post_params = MultiDict(parse_qsl(data))
			#response.write(b'{ok}}')
			# - run render -# yield from run_render_multi(json.loads(data.decode("utf-8")))
            print('test yield in try : ', data.decode('utf-8'))
        except Exception as e:
            logging.info('Err {0}'.format(e))
            e_data = {
						'status':False,
						'error_message':str(e),
			}
			#e_data = yield from response(body=json.dumps(e_data).encode('utf-8'))
			#print('test yield : ',e_data)
        finally:
			#print(e_data)
			#response.write(e_data)
			#yield from response.write_eof()
            return e_data

    @asyncio.coroutine
    def variable_handler(request):
        print('dsfsdfsdfsdfsdff')
        return web.Response(
            request,
            "hello, {}".format(request.math_info['name']).encode('utf-8'))




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
		#
    app = web.Application()
    app.router.add_route('GET', '/{name}',HttpRequestHandler.variable_handler)		
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    f = loop.create_server(lambda: HttpRequestHandler(debug=True, keep_alive=100),'0.0.0.0', '8080')
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass 