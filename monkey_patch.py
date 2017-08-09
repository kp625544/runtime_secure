from cgi import escape
import server2

server2.main()

def patch_xss(uri):
    return escape(uri)


def patch_sqli(uri):
    b = "'\\* ,/"
    for char in b: uri=uri.replace(char,"")
    return uri

def patch_fileupload(filename):
    if (filename.lower().endswith(("png", "jpg", "jpeg"))):
        return filename
    else:
        return "garbage.txt"


def patch_lfi(filename):
    if "../" not in filename:
        return filename
    else:
        return "car"

def patch_rce(filename):
    if ((" " not in filename) and ("|" not in filename)):
        return filename
    else:
        return "127.0.0.1"
