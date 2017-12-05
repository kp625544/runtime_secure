"""
Intentionally Vulnerable Web Application
"""
import os
import io
import mimetypes
import sqlite3 as lite
import tornado.web
import tornado.httpserver
import string
import random
import class_patch

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/static/(.*)", class_patch.StaticHandler),
            (r"/", class_patch.MainHandler),
            (r"/index.html", class_patch.MainHandler),
            (r"/search", class_patch.SearchHandler),
            (r"/login.html", class_patch.UsersHandler),
            (r"/server.html", class_patch.ServerHandler),
            (r"/upload", class_patch.UploadHandler),
            (r"/read", class_patch.ContentHandler),
        ]
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
			"static_path": os.path.join(os.path.dirname(__file__), 'static'),
            "debug": True
        }
        tornado.web.Application.__init__(self, handlers, **settings)
