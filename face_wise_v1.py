import face_recognition
import os,uuid
import numpy as np
import pickle
import asyncio

class FaceWise_V1():

    DATASET_PATH = "./dataset/actual"
    reload = False

    def __init__(self,learn=False):
        self.known_face_encodings=[]
        self.known_face_names=[]
        self.all_face_encodings={}
        self.learn=learn
        self.learn_faces()
        

    def learn_new_faces(self,name,face_encoding):
        print("Unknown ",name)

        np.append(self.known_face_encodings,[face_encoding])
        np.append(self.known_face_names,[name])

        self.all_face_encodings[name]=face_encoding
        with open('model.dat', 'wb') as f:
            pickle.dump(self.all_face_encodings, f)
        print('Learned new encoding for', len(self.known_face_encodings), 'images.')
        self.reload = True
        self.learn_faces()
        
    def learn_faces(self):
        if self.learn :
            print("Learning from Dataset...")
            for folder in os.listdir(self.DATASET_PATH):
                if not folder.startswith("."):
                    for file in os.listdir(self.DATASET_PATH+"/"+folder):
                        if not file.startswith("."):
                            image = face_recognition.load_image_file(self.DATASET_PATH+"/"+folder+"/"+file)
                            try:
                                face_encoding = face_recognition.face_encodings(image)[0]
                                self.known_face_encodings.append(face_encoding)
                                self.known_face_names.append(folder)
                                self.all_face_encodings[folder]=face_encoding
                            except Exception as e:
                                print(e)
                            

            with open('model.dat', 'wb') as f:
                pickle.dump(self.all_face_encodings, f)
            print('Learned encoding for', len(self.known_face_encodings), 'images.')
        elif not self.learn or self.reload:
            print(f"{'Re-Loading' if self.reload else 'Loading'} Model into Memory !")
            with open("model.dat",'rb') as f:
                self.all_face_encodings = pickle.load(f)
            self.known_face_names=list(self.all_face_encodings.keys())
            self.known_face_encodings=np.array(list(self.all_face_encodings.values()))
            
            
    def find_faces(self,img_path):
        people = []

        unknown_image = face_recognition.load_image_file(img_path)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding,0.6)
            name = None
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            if name:
                people.append(name)
            else:
                people.append(None)
                self.learn_new_faces(uuid.uuid4().hex,face_encoding)

        return people