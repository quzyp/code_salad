#!/usr/bin/env python3

from urllib3 import HTTPSConnectionPool

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en'}
http_mainhost = HTTPSConnectionPool('m.youtube.com', headers=headers)

