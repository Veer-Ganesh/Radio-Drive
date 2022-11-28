import tornado.web
from face_wise_v1 import FaceWise_V1
from io import BytesIO
import redis,ast
import tornado.gen

class SearchHandler(tornado.web.RequestHandler):

    face_wise_v1 = FaceWise_V1()
    r = redis.Redis(host='localhost', port=6379, db=0)    
    print("Connected to Redis !" if r else "Error Connecting to Redis...")

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def search_faces(self,img):
        face_names = self.face_wise_v1.find_faces(BytesIO(img))
        resp = {}
        for face in face_names:
            if face:
                print("Person detected : "+face)
                if self.r.exists(face):
                    d = self.r.get(face).decode()
                    resp[face]=ast.literal_eval(d)
        return resp

    @tornado.gen.coroutine
    def post(self):
        file = self.request.files
        if "file" in file:
            fileInfo= file["file"][0]
            file_name= fileInfo["filename"]
            file_data=fileInfo["body"]
            try:
                resp = self.search_faces(file_data)
                if len(resp.keys()) > 0:
                    self.set_status(200)
                    self.write({"status":"OK","data":resp})
                    return 
                else:
                    self.set_status(404)
                    self.write("Not Found")
                    return
            except Exception as e:
                print(e)
                self.set_status(500)
                self.write({"status":"Internal Server Error"})
                return
        self.set_status(400)
        self.write({"status":"Bad Request"})
        return 