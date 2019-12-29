import requests


def down_pic(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
               "Referer": url}
    r = requests.get(url, headers=headers, stream=True)  # 增加headers, 模拟浏览器  stream=分块下载
    i=0
    if r.status_code == 200:
        with open("1.mp4", 'ab') as f:
            for content in r.iter_content():
                f.write(content)

                print("下载中{}".format(i))
                i+=1


def dd():
    url = 'https://mm006.xyz/v.php?v=NDEwMjU1OTcvXw=='
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
               "Referer": url}
    r = requests.get(url, headers=headers)  # 增加headers, 模拟浏览器

    return r.text

if __name__ == '__main__':
     url='https://video-hw.xvideos-cdn.com/videos/mp4/7/6/7/xvideos.com_767fbdf7090b72626e0271a956ebc6ca.mp4?e=1577381165&ri=1024&rs=85&h=92b7cb5831593e0e6f8354307c103e9a'
     down_pic(url)
     print()



