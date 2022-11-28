import os,shutil,glob
import uuid
import time

def camera_to_cloud(reset_cloud=False):

    print("Snoozing....Please wait")
    time.sleep(20)
    
    _from = "cloud"
    _to = "camera"

    '''Remove images in cloud sim'''
    if(reset_cloud):
            files = glob.glob(f'./{_from}/*')
            for f in files:
                os.remove(f)

    '''Upload images to cloud sim'''
    for image in os.listdir(f"./{_to}"):
        new_uuid = uuid.uuid4().hex
        shutil.copy(f"./{_to}/"+image,"./cloud/"+new_uuid+".jpg")
        print("Data Added to Cloud !")
        time.sleep(15)

camera_to_cloud(reset_cloud=True)