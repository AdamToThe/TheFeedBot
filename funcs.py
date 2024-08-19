import requests
import io
import mimetypes


class File:
    def __init__(self, content, url, type, extension):
        self.content = content
        self.url = url
        self.type = type
        self.extension = extension


def get_files_from(msg, **kwargs) -> list:
    video = kwargs.pop('video', False)
    image = kwargs.pop('image', True)
    no_tenor = kwargs.pop('no_tenor', True)
     
    urls = []
    for att in msg.attachments:
        urls.append(att.url)

    for e in msg.embeds:
        if (e.type == 'video' and video) or (e.type == 'image' and image):
            urls.append(e.url)
        elif e.type == 'gifv' and image:
            urls.append(e.thumbnail.url)
    return list(filter(lambda x: 'tenor' not in x, urls)) if no_tenor else urls

def get_mime(url: str):
    m, _ = mimetypes.guess_type(url)
    if m is None:
        return None, None

    ext = mimetypes.guess_extension(m)
    return m, ext

def download_bytes(url: str) -> bytes:
    r = requests.get(url)
    b = io.BytesIO(r.content)
    b.seek(0)
    return b

