import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,PatternMatchingEventHandler,EVENT_TYPE_MOVED,EVENT_TYPE_CREATED,EVENT_TYPE_DELETED
from matplotlib import pyplot as plt
from face_wise_v1 import FaceWise_V1
import redis
import ast,sys

class Watcher:
    DIRECTORY_TO_WATCH = "./cloud"
    FILE_FACE_MAP={}

    def __init__(self,learn=False):
        self.observer = Observer()
        self.learn=learn
        self.r = redis.Redis(host='localhost', port=6379, db=0,retry_on_timeout=True)
        if self.r:
            print("Connected to Redis !")
        else:
            print("Error connecting to redis !")
        print("Initializing Model !...")
        self.face_wise_v1 = FaceWise_V1(self.learn)

    def detect_faces(self,file_name,img_path):
        face_names = self.face_wise_v1.find_faces(img_path)
        print(face_names)
        for face in face_names:
            if face:
                key = self.r.get(face)
                if not key:
                    self.r.set(face,str([file_name]))
                    print("Face is new , Added (Cache)")
                else:
                    li = key.decode()
                    new_li = ast.literal_eval(li)
                    new_li.append(file_name)
                    self.r.set(face,str(new_li))
                    print("Face is known , Added (Cache)")
            else:
                print("Face is None")


    def on_any_event(self,event):
        
        if event.event_type == EVENT_TYPE_CREATED:
            print("created",event.src_path)
            file_name = event.src_path.split("/")[-1]
            if file_name.endswith(".jpg"):
                abs_file_name = file_name.split(".")[0]
                print(abs_file_name)
                self.detect_faces(abs_file_name,event.src_path)

        if event.event_type == EVENT_TYPE_MOVED:
            print("modified",event.src_path,event.dest_path)

        if event.event_type == EVENT_TYPE_DELETED:
            print("deleted",event.src_path)
            file_name = event.src_path.split("/")[-1]
            if file_name.endswith(".jpg"):
                abs_file_name = file_name.split(".")[0]
                print(abs_file_name)

                redis_keys = [k.decode() for k in self.r.keys()]
                for key in redis_keys:
                    d = self.r.get(key).decode()
                    li = ast.literal_eval(d)
                    new_li = list(filter(lambda v: v!=abs_file_name ,li))
                    if len(new_li)==0:
                        self.r.delete(key)
                    else:
                        self.r.set(key,str(new_li))

    def run(self):
        event_handler = PatternMatchingEventHandler(
            patterns=["*.jpg"],
            ignore_directories=True,
            case_sensitive=False,
        )
        event_handler.on_any_event = self.on_any_event
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()


if __name__ == '__main__':
    learn = sys.argv[1].split("=")[1]=="true" if len(sys.argv)>1 and sys.argv[1].find("=") else False
    w = Watcher(learn)
    w.run()