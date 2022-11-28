import json,uuid,io
import tornado.web
import tornado.gen

class UploadHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def store_image(self,fileName,fileData):
        output_file = open("./cloud/" + fileName+".jpg", 'wb')
        output_file.write(fileData)
        output_file.close()
    
    @tornado.gen.coroutine
    def post(self):
        file = self.request.files
        if "file" in file:
            fileInfo= file["file"][0]
            file_name= fileInfo["filename"]
            file_data=fileInfo["body"]
            new_uuid = uuid.uuid4().hex
            try:
                self.store_image(new_uuid,file_data)
                self.set_status(200)
                self.write({"status":"OK"})
                return 
            except Exception as e:
                self.set_status(500)
                self.write({"status":"Internal Server Error"})
                return
        self.set_status(400)
        self.write({"status":"Bad Request"})
        return