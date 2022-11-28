import json
import tornado.web
import tornado.gen


class LoginHandler(tornado.web.RequestHandler):

    DEFAULT_USERNAME = "veer"
    DEFAULT_PASSWORD = "password"

  
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.gen.coroutine
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()

    @tornado.gen.coroutine
    def post(self):
        body = self.request.body
        body = json.loads(body)
        if "username" in body and "password" in body:
            if body["username"] == self.DEFAULT_USERNAME and body["password"] == self.DEFAULT_PASSWORD :
                self.set_status(200)
                self.write({"status":"OK"})
                return 
            else:
                self.set_status(401)
                self.write({"status":"Invalid Credentials"})
                return
        self.set_status(400)
        self.write({"status":"Bad Request"})
        return 

