import asyncio
import tornado.web
import tornado.gen
from tornado.httpserver import HTTPServer
from tornado.routing import RuleRouter,Rule,PathMatches
from handlers.login_handler import LoginHandler
from handlers.upload_handler import UploadHandler
from handlers.search_handler import SearchHandler
from handlers.getImage_handler import GetImageHandler
from handlers.ui_handler import UIHandler,UIDataHandler

PORT = 80
YELLOW='\033[1;33m'
NC='\033[0m'

async def main():
    server_app = tornado.web.Application([
        (r"/api/login", LoginHandler),
        (r"/api/upload", UploadHandler),
        (r"/api/search", SearchHandler),
        (r"/api/get_image", GetImageHandler),
    ])

    react_app = tornado.web.Application([
        (r"/",UIHandler),
        (r"/static/css/(.*)",tornado.web.StaticFileHandler, {"path": "./react/static/css"},),
        (r"/static/js/(.*)",tornado.web.StaticFileHandler, {"path": "./react/static/js"},),
        (r"/static/media/(.*)",tornado.web.StaticFileHandler, {"path": "./react/static/media"},),
         (r"/.*",UIDataHandler),
    ])

    router = RuleRouter([
            Rule(PathMatches("/api/.*"), server_app),
            Rule(PathMatches("/.*"), react_app),
            ])

    server = HTTPServer(router)
    server.listen(PORT)
    print(f"\n{YELLOW}Server started at {PORT}{NC}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())