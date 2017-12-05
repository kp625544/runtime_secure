from cgi import escape
#import io

import sys

class sqli_patch():
    def __init__(self):
        print "init"
        self.responselist = []
    def initcon(self, con):
        self.newcon = con
        return self
    def fetchone(self):
        return self.responselist
    def cursor(self):
        print("here comes connection var")
        print(dir(self.newcon))
        self.cursor = self.newcon.cursor()
        return self
    def execute(self, url):
        print url
        stripchars = "1\\*,/"
        startq = url[:32]
        b = url[32:]
        for char in stripchars: b=b.replace(char,"")
        url = startq + b
        print url
        try:
            with self.newcon:
                cur = self.newcon.cursor()
                cur.execute(url)
                #print(cur.fetchone())
                cur_resp = cur.fetchone()
                #print cur_resp[1]
            [self.responselist.append(i) for i in cur_resp]
        except:
            self.responselist = []
        return self
    def __exit__(self, error1, error2, error3):
        print error1, error2, error3
        return self
    def __enter__(self):
        return self

class patch():
    def __init__(self):
        import os
        import io
        import tornado.web
        import sqlite3 as lite
        self.ospath = os.path
        self.oscommand = os.popen
        self.iocommand = io.open
        self.sqlfunctions = lite.connect

    def patch_xss(self, uri):
        return escape(uri)


    def patch_sqli(self, uri):
        print uri
        con = self.sqlfunctions(uri)
        return sqli_patch().initcon(con)

    def patch_file(self, filename, permission):
        if (filename.lower().endswith(("png", "jpg", "jpeg"))):
            return self.iocommand(filename, permission)
        elif ((filename.lower().endswith(("py", "db", "exe")) != True) and ("../" not in filename)):
            return self.iocommand(filename, permission)
        else:
            return self.iocommand("not_a_shell.txt", permission)

    def patch_rce(self, commandname):
        #print (os.popen)

        if (("&" not in commandname) and ("|" not in commandname)):
            command = self.oscommand(commandname)
        else:
            command =  self.oscommand("ping -c 4 127.0.0.1")
        return command
        sys.exit(0)
#return patch_file, patch_rce

def patcher():
    final_patch = patch()
    return final_patch.patch_file, final_patch.patch_rce, final_patch.patch_sqli
