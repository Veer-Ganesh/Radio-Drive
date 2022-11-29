import tornado.web
import os

class UIHandler(tornado.web.RequestHandler):
  
    @tornado.gen.coroutine
    def get(self):
        self.render("../react/index.html")
        return

class UIDataHandler(tornado.web.RequestHandler):

    img_format = ["png","jpg"]
    onlyfiles = [f for f in os.listdir("./react") if os.path.isfile(os.path.join("./react", f))]
    print(onlyfiles)
  
    @tornado.gen.coroutine
    def get(self):
        if self.request.path[1:] not in self.onlyfiles:
            self.redirect("/")
            return
        l = self.request.path.split(".")
        if len(l) > 1 and l[1] not  in self.img_format:
            self.render("../react/"+self.request.path)
                
