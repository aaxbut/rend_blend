
import asyncio
import json
import aiohttp
import uvloop

@asyncio.coroutine
def fetch2(session, url): 
    with aiohttp.Timeout(10):
        response = yield from session.get(url)
        try:
            # other statements
            return (yield from response.text())
        finally:
            if sys.exc_info()[0] is not None:
                # on exceptions, close the connection altogether
                response.close()
            else:
                yield from response.release()
@asyncio.coroutine
def fetch():
	with aiohttp.Timeout(10):
		url = "http://127.0.0.1:8080"
		data = {'sender': 'Todd', 'receiver': 'Bob', 'message': 'We did it!','file_name':'500265.blend'}
		headers = {'Content-type': 'application/json'}
		#, 'Accept': 'text/plain'}
		#r = requests.post(url, data=data, headers=headers)
		payload={'date':'c:\\ddd\\ddd'}
		#e= aiohttp.request('GET',url,data=json.dumps(data),headers=headers)
		#connector = aiohttp.TCPConnector(verify_ssl=False)
		#asyncio.async(aiohttp.request('post', url, data = json.dumps(data), headers = headers, connector=connector)).add_done_callback(lambda future: future.result())
		#resp = yield from asyncio.wait_for(aiohttp.request('POST',url,data=json.dumps(data),headers=headers),0.3)
		r = yield from aiohttp.request('get',url,data=data)
		yield from r.text()
		
		#yield from resp.release()
		print(r)
		#assert  resp.status == 200
		


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch())
loop.close()
try:

	loop.close()
except Exception as err:
	print('client in ',err)
