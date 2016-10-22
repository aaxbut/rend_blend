import aiohttp
import asyncio
import json


async def fetch(client):
        url = "http://127.0.0.1:781/tr"
        data = {'sender':'node-1','user': '14', 'result_dir': '/var/www/cmex.ru/data/uploads/users_rollers/504/video','message': 'We did it!','project_name':'88','user_roller_id': '504','files_png':{'head1':'cut//cutface_1471249972.png','head2':'cut//cutface_1471249972.png','head3':'cut//cutface_1471249972.png'}}
        #data = {'sendaemonder':'node-1','user': 'nebob', 'file_h1': 'head1.png', 'message': 'We did it!','project_name':'Rauf','file_name':'500265.blend','files_png':{'head1':'head1.png','mouth1':'mouth1.png'}}
        #data = {'sender':'node-1','user': 'aaxbut', 'file_h1': 'head1.png', 'message': 'We did it!','requestproject_name':'Rauf','file_name':'500265.blend','files_png':{'head1':'head12.png','mouth1':'mouth12.png'}}
        headers = {'Content-type': 'application/json'}
        #async with client.get(url,data=data) as session:
        #    assert session.status == 200
        #    u = await session.text()
        #    print('{} , {} ,sesrequestrequestrequestrequestsion state closed : {}**{}'.format(session.read(),client,client.closed,u))
        #s = await client.post(url, data = json.dumps(data) ,headers = headers)
        async with await client.post(url, data = json.dumps(data) ,headers = headers) as post_session:
            #assert post_session.status == 405
            u =  json.loads(await post_session.text())
            #print(u['name'])
            
            #print('Session method "{}", session state closed  : {} : {} json data:{}, session k'.format(post_session.method, client.closed,u,data))
#            await post_session.release()

        return await post_session.text()

async def main(loop):
        async with aiohttp.ClientSession(loop=loop) as client:
            html = await fetch(client)
            print('html ',html)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))