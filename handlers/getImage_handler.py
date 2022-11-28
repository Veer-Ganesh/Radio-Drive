import json,uuid,io,os
import tornado.web
import tornado.gen
import base64
import glob

class GetImageHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')

    def if_file_exists(self,id):
        file_path = os.path.join("./cloud/"+id)
        exist = os.path.exists(file_path)
        return exist,file_path

    def get_image_binary(self,file_path):
        with open(file_path, "rb") as image:
            img_string = base64.b64encode(image.read())
            return "data:image/jpg;base64,"+img_string.decode()

    @tornado.gen.coroutine
    def options(self):
        self.set_status(200)
        self.write({})
        self.finish()

    @tornado.gen.coroutine
    def delete(self):
        id = self.request.arguments.get("id")
        if len(id) > 0 and id[0].decode() != "all":
            file_exist,file_path = self.if_file_exists(id[0].decode())
            if file_exist:
                os.remove(file_path)
                self.set_status(200)
                self.write({"status":"OK"})
                return
            else:
                self.set_status(404)
                self.write({"status":"Not Found"})
                return
        elif(len(id) > 0 and id[0].decode() == "all"):
            files = glob.glob(f'./cloud/*')
            for f in files:
                os.remove(f)
            self.set_status(200)
            self.write({"status":"OK"})
            return
        self.set_status(400)
        self.write({"status":"Bad Request"})
        return


    @tornado.gen.coroutine
    def get(self):
        id = self.request.arguments.get("id")
        if len(id) > 0 and id[0].decode() != "all":
            file_exist,file_path = self.if_file_exists(id[0].decode())
            if file_exist:
                image_binary = self.get_image_binary(file_path)
                self.set_status(200)
                self.write({"status":"OK","data":image_binary,"name":id[0].decode()})
            else:
                self.set_status(404)
                self.write({"status":"Not Found"})
            return
        else:
            for name,subDir,files in os.walk("./cloud/"):
                self.set_status(200)
                self.write({"status":"OK","data":files})
                return
        self.set_status(400)
        self.write({"status":"Bad Request"})
        return