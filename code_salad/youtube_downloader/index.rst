Youtube Downloader
==================

By Fledermann_, 2019-01-26


.. raw:: html

    <p align="center">
        <img src="img/screen_ff_ajax.png" width="50%">
    </p>





After using the very capable tool youtube-dl_ for a while I wanted to
to use it as a module in a script, but quickly realised that the user
interface leaves much to desire. I took a peek at the source code and
unsurprisingly, it's a mess. The program has grown so big and supports
so many websites that even opening the `extractor folder`_ in my browser
takes several seconds. I think I would need maybe 0.1% of the functionality
youtube-dl offers.

Then I discovered pafy_ - what a nice and beatiful interface! Unfortunately,
it used youtube-dl as a backend for downloading videos as it's own
downloader had performance problems (that's what I read at the time, it may
be fixed already). So, still youtube-dl required, only with a nicer wrapping.

After fiddling around with the firefox developer tools for a while I stumbled
on a quick and easy way to gather metadata and get to the video streams.
Initially I tried just emulating what my browser does to crawl the source
code and extract the information, but then I realised that youtube
actually provides useful json responses outside of the api. Here's how to
use it.

First, we need a mobile user-agent:

.. code-block:: python

    >>> headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en'}
    >>>

Then we take the request library of our choice and make a request to the mobile 
youtube site. I will be using requests_ in this example, but any other method will do.
I chose a short Numberphile video with the regular url `https://www.youtube.com/watch?v=Mfk_L4Nx2ZI`.
The part after `?v=` is the video ID. 

.. code-block:: python

    >>> import requests
    >>> video_id = 'Mfk_L4Nx2ZI'
    >>> params = {'ajax': '1', 'v': video_id}
    >>> r = requests.get('https://m.youtube.com/watch', params=params, headers=headers)

The `params` are just the http GET parameters - the equivalent browser url would
look like `https://m.youtube.com/watch?v=Mfk_L4Nx2ZI&ajax=1`. 

If we take a look at the response content we see that it looks like json - great!
The first four characters are garbage, though, so we need to cut them off.

.. code-block:: python

    >>> import json
    >>> j = json.loads(r.text[4:])

The json is deeply nested, so it takes a bit of digging and prettyprinting to
find the data we're interested in. For now, I only need the title and the
streams.

.. code-block:: python

    >>> title = j['content']['video']['title']
    >>> stream_info = j['content']['swfcfg']['args']['adaptive_fmts']

It turns out there are plenty of streams for this video - which makes sense
considering that every video is available in different resolutions, frame rates 
and codecs. Since the information in 'adaptive_fmts' is several long urls
with all the information as parameters, let's extract the parameters to
make it more readable.

.. code-block:: python

    import urllib

    streams = list()
    for s in stream_info.split(','):
        stream = dict()
        for parameter in s.split('&'):
            key, value = parameter.split('=')
            value = urllib.parse.unquote(value)
            stream[key] = value
        streams.append(stream)

       

.. _Fledermann: https://github.com/Fledermann
.. _youtube-dl: https://github.com/rg3/youtube-dl/
.. _`extractor folder`: https://github.com/rg3/youtube-dl/tree/master/youtube_dl/extractor
.. _pafy: https://github.com/mps-youtube/pafy
.. _requests: http://docs.python-requests.org/en/master/
