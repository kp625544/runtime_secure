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
import monkey_patch

class StaticHandler(tornado.web.RequestHandler):

    def get(self, path):
        #print "GET ", self.request.uri
        path = 'static/' + path
        base = os.path.join(os.path.dirname(__file__))
        static_file = os.path.join(base, path)
        mime_type, _ = mimetypes.guess_type(static_file)
        if mime_type:
            self.set_header("Content-Type", mime_type)
        with open(static_file, "r") as fpl:
            self.write(fpl.read())


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        print( "GET ", self.request.uri)
        self.render("index.html")


class UploadHandler(tornado.web.RequestHandler):

    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = monkey_patch.patch_fileupload(file1['filename'])
        #print original_fname
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(
            string.ascii_lowercase + string.digits) for x in range(6))
        final_filename = fname + extension
        output_file = io.open("/home/hydra/Desktop/AUR/project/monkey_patching/Tornade/patch_Tornado/upload/" + final_filename, 'wb')
        output_file.write(file1['body'])
        output_file.close()
        self.finish("file" + final_filename + " is uploaded")


class ContentHandler(tornado.web.RequestHandler):

    def get(self):
        file_name = monkey_patch.patch_lfi(self.get_argument("file", default="car"))
        content = ''
        read_file = io.open("read/" + file_name, 'rb')
        content = read_file.read()
        #print dir(content)
        read_file.close()
        self.write(content)


class SearchHandler(tornado.web.RequestHandler):

    def get(self):
        print ("GET ", self.request.uri)
        query = monkey_patch.patch_xss(self.get_argument("q", default="Query"))
        #print query
        self.set_header('X-XSS-Protection', '0')
        self.render("search.html", query=query, link=query)


class UsersHandler(tornado.web.RequestHandler):

    def get(self):
        print ("GET ", self.request.uri)
        self.render("login.html", msg="")

    def post(self):
        print ("POST ", self.request.uri, "\nBODY ", self.request.body)
        con = lite.connect('test.db')
        dat = ""
        uname = monkey_patch.patch_sqli(self.get_argument('username'))
        pwd = monkey_patch.patch_sqli(self.get_argument('password'))
        #print uname, pwd
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Users WHERE User ='" +
                        uname + "' AND Password ='" + pwd + "'")
            cur_resp = cur.fetchone()
        if not cur_resp:
            dat = "Login Failed"
        else:
            dat = "Login Success, Hello " + str(cur_resp[1])
        self.render("login.html", msg=dat)


class ServerHandler(tornado.web.RequestHandler):

    def get(self):
        print ("GET ", self.request.uri)
        self.render("server.html", msg="", cmd="127.0.0.1")

    def post(self):
        print ("POST ", self.request.uri, "\nBODY ", self.request.body)
        server = monkey_patch.patch_rce(self.get_argument('server'))
        #print server
        process = os.popen('ping -c 4 ' + server)
        preprocessed = process.read()
        process.close()
        self.render("server.html", msg=preprocessed, cmd=server)


def create_db():
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'Users'")
        exc = cur.fetchone()[0]
        if exc == 0:
            cur.execute("CREATE TABLE Users(Id INT PRIMARY KEY, User TEXT, Password TEXT)")
            cur.execute("INSERT INTO Users VALUES(1,'admin','admin')")
            cur.execute("INSERT INTO Users VALUES(2,'test-user','test@123')")
            cur.execute("INSERT INTO Users VALUES(3,'sagar','lall0l')")
            cur.execute("INSERT INTO Users VALUES(4,'alias','ohrealli')")
            cur.execute("INSERT INTO Users VALUES(5,'jacky','st40ngp@55')")
            cur.execute("INSERT INTO Users VALUES(6,'sam','tomTOM123')")
            cur.execute("INSERT INTO Users VALUES(7,'maxi','D@ni3lDizaark')")
            cur.execute("INSERT INTO Users VALUES(8,'lelol','Leeee@Looo@!$')")
            cur.fetchone()
