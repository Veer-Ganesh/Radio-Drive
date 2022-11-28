from face_wise_v1 import FaceWise_V1
import redis
import sys

class SearchFaces():

    def __init__(self):
        print("Initializing model !")
        self.face_wise_v1 = FaceWise_V1()
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        if self.r:
            print("Connected to Redis !")

    def search_faces(self,img_path):
        face_names = self.face_wise_v1.find_faces(img_path)
        for face in face_names:
            print("Person detected : "+face)
            redis_keys = [k.decode() for k in self.r.keys()]
            if face in redis_keys:
                print(self.r.get(face))
            else:
                print("No History of Photos")



if __name__ == "__main__":
    file_name = sys.argv[1]
    test_img = f"./storage/{file_name}.jpg"
    search = SearchFaces()
    search.search_faces(test_img)