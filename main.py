from encodings import utf_8
from multiprocessing import Pool
from unittest import result
from urllib.parse import urlparse, unquote
import requests
import re

import xml.etree.ElementTree as ET
import zlib
import logging
import io


final_results: list[tuple[str, list[str]]] = []



def read_gzip_stream(url, size):
    req = requests.get(url, stream=True)
    zlib_decompressor = zlib.decompressobj(16+zlib.MAX_WBITS)
    for chunk in req.iter_content(chunk_size=size):
        yield zlib_decompressor.decompress(chunk)
        del chunk


def collect_results(res : tuple[str, list[str]]):
    final_results.append(res)



def process_file(url):
    parser = ET.XMLPullParser(["start", "end", "start-ns"])
    tagName = "loc"
    filterTag = tagName
    results = []
    for c in read_gzip_stream(url, 4*1024):
        parser.feed(c.decode('utf-8'))
        for event, elem in parser.read_events():
            if event == "start-ns":
                filterTag = f"{{{elem[1]}}}{tagName}"
            if event == "end" and elem.tag == filterTag:
                url = urlparse(elem.text)
                query = unquote(url.query)
                if url.path == '/define.php' and re.match('^term=', query):
                    results.append(str.lower(query.split('=')[1]))
    return (url, results)

def main():
    with Pool(processes=8) as pool:
        parser = ET.XMLPullParser(["start", "end", "start-ns"])
        tagName = "loc"
        filterTag = tagName
        for c in read_gzip_stream("https://www.urbandictionary.com/sitemap-https.xml.gz", 1024):
            print(len(c))
            parser.feed(c.decode('utf-8'))
            for event, elem in parser.read_events():
                if event == "start-ns":
                    filterTag = f"{{{elem[1]}}}{tagName}"
                if event == "end" and elem.tag == filterTag:
                    r = pool.apply_async(process_file, args=(elem.text,), callback=collect_results)

        # block on completion
        pool.close()
        pool.join()

        with io.open("low.txt", "w", encoding='utf-8') as f:
            for r in final_results:
                f.write('\n'.join(r[1]))
        f.close()


if __name__ == "__main__":
    main()