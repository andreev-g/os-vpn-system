import redis
from aiohttp import web

r = redis.Redis(
    host='10.8.0.1',
    port=6379,
    db=0
)
routes = web.RouteTableDef()


@web.middleware
async def logger_middleware(request, handler):
    print(f"process response: {request.url}")
    return await handler(request)


@routes.get("/getall")
async def get_values(request):
    return web.json_response({
        key.decode(): r.get(key).decode()
        for key in r.keys()
    })


@routes.get('/set')
async def set_value(request):
    key = request.query.get("key")
    value = request.query.get("value")
    if not key or not value:
        return web.json_response({"error": "specify 'key', 'value' params, please"})
    r.set(key, value)
    return web.json_response({"status": "ok"})


if __name__ == "__main__":
    app = web.Application(middlewares=[logger_middleware])
    app.add_routes(routes)
    web.run_app(app, port=80,)
