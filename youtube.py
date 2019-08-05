from pytube import Playlist, YouTube
from bs4 import BeautifulSoup

# pl = Playlist("https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK")
pl = Playlist("https://www.youtube.com/playlist?list=PL4uGfvjHzbw19ACxODupvIi4nMUGkZBKf")
base_url = 'https://www.youtube.com'
links = pl.parse_links()

# 注意!!!
# 當前版本pytube抓title功能有問題
# 請參考這篇的修正：
# https://github.com/ndg63276/alexa-youtube/commit/94d671dbd5c214a88df6d568b745c36b272b2dc4
# 修改下面這個檔案：
# python3.7/site-packages/pytube/__main__.py

hash_text_dict = []
for link in links:
    _link = base_url + link
    y = YouTube(_link)
    text = link.split("=")[1]
    dict_ = {'file_name': y.title, 'text': text}
    hash_text_dict.append(dict_)
    print(y.title, ",", text)
    # print(base_url + link, y.title, text)
