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
actually provides useful json responses outside of the api. 
Here's how to use it.

First, we need a mobile user-agent:

.. code-block:: python

    >>> headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en'}
    >>>

We take the request library of our choice (I went with urllib3 for reasons
I can't remember) and make a request to the mobile youtube site:

.. code-block:: python

    >>> from urllib3 import HTTPSConnetionPool
    >>> http_mainhost = HTTPSConnectionPool('m.youtube.com', headers=headers)



.. _Fledermann: https://github.com/Fledermann
.. _youtube-dl: https://github.com/rg3/youtube-dl/
.. _`extractor folder`: https://github.com/rg3/youtube-dl/tree/master/youtube_dl/extractor
.. _pafy: https://github.com/mps-youtube/pafy
