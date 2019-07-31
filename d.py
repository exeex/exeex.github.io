import urllib.parse
import urllib.request
import time
# Download the file from `url`, save it in a temporary directory and get the
# path to it (e.g. '/tmp/tmpb48zma.txt') in the `file_name` variable:


url_pattern = 'https://d1q8jl7i9mxhvr.cloudfront.net/AUDIO/REF/test/{}/vocals.m4a'

with open('list.csv', 'r') as f:
    for idx, line in enumerate(f.readlines()):

        if idx > 16:
            name = line.strip()
            url = url_pattern.replace('https://', '')
            _name = name.replace(' ', '%20')
            _name = _name.replace('amp;', '')
            url = url.format(_name)
            url = 'https://' + url
            print(url)
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent',
                                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")]
            urllib.request.install_opener(opener)

            file_name = f'vocals-{name}.m4a'

            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                data = response.read()  # a `bytes` object
                out_file.write(data)

            print(file_name)

            time.sleep(5)



