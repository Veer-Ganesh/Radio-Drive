# Radio-Drive

ML Based Image Filtering ❤️

## Cloud Watcher Service : (cloud_watcher.py)

Watches over cloud directory for file changes ( uses [watchdog](https://pypi.org/project/watchdog/) ) =>

    read faces from files :
    	get face encoding :
    		known face ?
    			stores file_name in redis
    		else :
    			ML Model learns through reinforcement
    	No face ? ## skip

## Server (server.py)

![Tornado](https://www.tornadoweb.org/en/stable/_images/tornado.png)

Async Server Implemented with Tornado

    Serves following route :

    1.*/api/upload => to upload image to cloud ( cloud here is nothing but a local directory )

    2.*/api/login => login api ( default cred :=> USERNAME = "veer" PASSWORD = "password")

    3.*/api/search => gets image in multipart request :

## Search API Working

    face encodes from images :
    	check redis for any images related to it !
    	send array of known_image filenames

4./api/get_image => pass in id through Query params and get corresponding base64 encoded image served from cloud.

    if id == "uuid":
    	returns particular image
    else if id == "all":
    	returns all image from cloud (Directory)

### Access UI on http://localhost:8888

### Note :

    1. All data are volatile, meaning if container is delete. Uploaded images get deleted as well ! (Since this is a POC app)

    2. Internally uses Redis to store mapping and encodings.

    3. More improvisations are on the way.

## Test images are provided in camera, storage directory

    Step 1 : U can upload images from camera directory. (Typical use-case uploading from mobile)[dont bulk upload]=> for now not designed for prod

    Step 2 : Once uploaded to cloud.

    Step 3 : Search from images in storage directory.

Note:

    you can also Upload and Test it against your own images

# Starting service locally (Without Dockerization):

    cd /${WORKING_DIR} && sh ./start.sh

# To Train against your own Dataset :

Replace data in dataset/actual with label/images.jpg

    IF ( Note if running in virtual env provided from /bin/activate ):

    RUN =>

    python cloud_watcher.py --learn=true

    ELSE => Just install dependency by running below cmd :

    pip install -r requirements.txt

    python cloud_watcher.py --learn=true

    ONCE_LEARNT => it saved the model to modal.dat file ( Clever, so that can be loaded next time !)

# Supervisor :

![Supervisord](https://avatars.githubusercontent.com/u/5429470?s=280&v=4)

We have used supervisord to run multiple process inside same docker-container

Feel free to read => [Multi-process Docker](https://docs.docker.com/config/containers/multi-service_container/)

# Wanna pull Docker Image ? No Issues !

Checkout => [MyDocker](https://hub.docker.com/r/veyro9/radio-drive)

    docker pull veyro9/radio-drive

    docker run -p 8888:8888 -p -d veyro9/radio-drive


(Feel free to map to any PORT of your choice)

Design & Developed with ❤️ by [Veer](https://www.linkedin.com/in/veerganesh/)
