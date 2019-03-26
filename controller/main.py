import tornado.web

def fn():
    print('thhis')
class main(tornado.web.RequestHandler):
    def get(self):
        self.write('hell-----------------')