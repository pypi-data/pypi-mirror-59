## Desciption

Python utility to get the partial content of the web file or to unarchive a single file from a huge remote web zip.


## Installation

```shell
$ python3 -m pip install partial_web_file
```

## Usage

To get a part of the file from the Web:

```python
import partial_web_file

test_url = 'https://alexapps.net/files/mobile_app_boxingitimer_icon.png'
partial_content = partial_web_file.get_partial_web_file(test_url, start_position=1, length=3)
print(partial_content)  # prints "b'PNG'"
```

Imagine there is a huge zip file on the Web server. Downloading it takes time and network traffic. But you need only small file from that zip. Here is how to get that small file without full download:

```python
import partial_web_file

url_to_huge_zip = 'http://remote.server.com/data/library-1.3.8.zip'
file_to_unzip = 'common/keywords.txt'
local_destination = 'keywords.txt'

content = partial_web_file.get_file_content_from_web_zip(url, file)
with open(local_destination, 'w') as fout:
  fout.write(content)
print('Done. Check the', local_destination, 'file.')
```
