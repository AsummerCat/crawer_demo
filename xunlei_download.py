import os

from pyaria2 import Aria2RPC

def download(url, filename):
    jsonrpc = Aria2RPC()
    set_dir = os.path.dirname(__file__)
    options = {"dir": set_dir, "out": filename, }
    res = jsonrpc.addUri([url], options=options)



if __name__ == '__main__':
    link = 'http://music.163.com/song/media/outer/url?id=400162138.mp3'
    filename = '海阔天空.mp3'

    download(link, filename)
