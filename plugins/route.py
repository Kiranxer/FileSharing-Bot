from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("🎊 HELLO FROM NEON 🎊")




# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
