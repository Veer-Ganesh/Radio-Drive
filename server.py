import asyncio
import tornado.web
from handlers.login_handler import LoginHandler
from handlers.upload_handler import UploadHandler
from handlers.search_handler import SearchHandler
from handlers.getImage_handler import GetImageHandler

PORT = 8888
YELLOW='\033[1;33m'
NC='\033[0m'


def make_app():
    return tornado.web.Application([
        (r"/api/login", LoginHandler),
        (r"/api/upload", UploadHandler),
        (r"/api/search", SearchHandler),
        (r"/api/get_image", GetImageHandler),
    ])

async def main():
    app = make_app()
    app.listen(PORT)
    print("started!")
    print(f"\n{YELLOW}Server started at {PORT}{NC}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())