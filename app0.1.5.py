import tornado.web
import tornado.ioloop
import importlib
import os
# from tornado.options import options, define
import tornado.options
import tornado.log
import logging

# tornado.options.define("log_file_prefix", default="/log/log.log")
tornado.options.options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'log/log.log')


class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
#
# import Static Root Controller and make controller list
def getControllerList(path):
    controller_list=list()
    handler=dict()
    for item in os.walk(path):
        if item[0].find('__pycache__')==-1:
            for model in item[2]:
                modelname=os.path.join(item[0],model.replace('.py','')).replace('\\','.')
                path=os.path.join(item[0],model.replace('.py','')).replace('\\','/')
                handler[modelname]=importlib.import_module(modelname)
                controller_list.append([
                    path[10:len(path)],
                    eval('handler[modelname].'+model.replace('.py',''))
                ])
    return controller_list


settings={
    'cookie_secret':"__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/",
    'static_path':'static',
    # 'log_function':xxx
    'static_hash_cache':False,

}
        
def app():
    return tornado.web.Application(getControllerList('controller'),**settings)

if __name__ == '__main__':
    tornado.options.define("port", default="80", help="run on the port", type=int)
    tornado.options.parse_command_line()
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    app=app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()