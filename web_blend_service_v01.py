from aiohttp import web
import asyncio
import logging
import uvloop


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
    yield from ws.prepare(request)

    for msg in ws:
        if msg.type == web.MsgType.text:
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break

    return ws


@asyncio.coroutine
def transmit(request):
    if request.method == 'POST':
        print('transmit!!!!!',request)
    logging.info('in transmit module {0}'.format(request.json))
    ws = web.WebSocketResponse()
    yield from ws.prepare(request)
    print(ws)
    for msg in ws:
        if msg.type == web.MsgType.text:
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break

    return ws








#web.run_app(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    app.router.add_route('GET','/echo', wshandler)
    app.router.add_route('POST','/echo', transmit)
    app.router.add_route('GET','/', handle)
    app.router.add_route('POST','/', handle)
    app.router.add_route('GET','/{name}', handle)
    
    #asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    f = loop.create_server(app.make_handler(),'0.0.0.0',8080)
    
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        print(type(loop.run_forever()))
        loop.run_forever()
        
    except KeyboardInterrupt:
        pass 