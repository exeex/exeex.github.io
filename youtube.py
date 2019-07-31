from pytube import Playlist, YouTube
from bs4 import BeautifulSoup

pl = Playlist("https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK")
base_url = 'https://www.youtube.com'
links = pl.parse_links()


# 注意!!!
# 當前版本pytube抓title功能有問題
# 請參考這篇的修正：
# https://github.com/ndg63276/alexa-youtube/commit/94d671dbd5c214a88df6d568b745c36b272b2dc4
# 修改下面這個檔案：
# python3.7/site-packages/pytube/__main__.py


for link in links[:10]:
    _link = base_url + link
    y = YouTube(_link)
    print(base_url+link, y.title)


