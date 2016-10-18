import aiohttp
import asyncio
import json


def f(loop):
    url = "http://127.0.0.1:781/tr"
    data = {'sender': 'Todd', 'receiver': 'Bob', 'message': 'We did it!','file_name':'500265.blend'}
    headers = {'Content-type': 'application/json'}
    #, 'Accept': 'text/plain'}
    #r = requests.post(url, data=data, headers=headers)
    payload={'date':'c:\\ddd\\ddd'}
    #async with aiohttp.request('POST',url,data=json.dumps(data),headers=headers) as resp:
    resp = yield from asyncio.wait_for(aiohttp.request('GET',url,data=json.dumps(data),headers=headers,loop=loop),0.3)
    #response = yield from aiohttp.request('GET','http://127.0.0.1:8080',loop=loop)
    body = yield from resp.read()
    print(body)
    return body



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f(loop))