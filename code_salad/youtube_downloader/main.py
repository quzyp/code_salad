#!/usr/bin/env python3

import json
import pathlib
import sys
import time
import urllib

import requests


def download_file(url: str, path: pathlib.Path) -> None:
    """ Download a file in chunks using http GET parameters which the
    server accepts as DASH requests. """

    r = requests.get(url, stream=True)
    filesize = int(r.headers['Content-Length'])
    chunk_size = 1024 * 1024 * 10
    dl_chunk_size = 1024 * 128
    chunk_start = 0
    progress = 0
    time_start = time.time()
    while progress < filesize:
        chunk_end = chunk_start + chunk_size - 1
        params = {'range': f'{chunk_start}-{chunk_end}'}
        response = requests.get(url, stream=True, params=params)
        with open(path, 'ab') as f:
            for chunk in response.iter_content(dl_chunk_size):
                f.write(chunk)
                progress += sys.getsizeof(chunk)
                avg_dl_rate = progress / 1024 / (time.time() - time_start)
                print(f'\r{avg_dl_rate:.0f} kb/s', end='')
        chunk_start = chunk_end + 1


def get_metadata(video_id: str) -> dict:
    """ Extract the metadata, including video streams, from a
    youtube video. """
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
                       'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en'}
    params = {'pbj': '1', 'v': video_id}
    #r = requests.get('https://m.youtube.com/watch', params=params, headers=headers)
    #j = json.loads(r.text)
    with open('pbj.txt', 'r') as f:
        j = json.load(f)
    title = 'foo'# j['content']['video']['title']
    stream_info = j['JSON'][2]['player']['args']['player_response']
    jj = json.loads(stream_info)
    streams = jj['streamingData']['adaptiveFormats']
    #for s in stream_info.split(','):
    #    stream = dict()
    #    for parameter in s.split('&'):
    #        try:
    #            key, value = parameter.split('=')
    #        except ValueError:
    #            continue
    #        value = urllib.parse.unquote(value)
    #        stream[key] = value
    #    streams.append(stream)
    return dict(title=title, streams=streams)


if __name__ == '__main__':
    video_id = '2_e3lfnkrlY'
    md = get_metadata(video_id)
    # print(md['streams'])
    video = [x for x in md['streams'] if x['mimeType'].startswith('video/mp4')][0]
    audio = [x for x in md['streams'] if x['mimeType'].startswith('audio/mp4')][0]
    download_file(video['url'], pathlib.Path('video.mp4'))
    download_file(audio['url'], pathlib.Path('audio.mp4a'))
