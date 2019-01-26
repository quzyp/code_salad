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


.. _Fledermann: https://github.com/Fledermann
.. _youtube-dl: https://github.com/rg3/youtube-dl/
.. _`extractor folder`: https://github.com/rg3/youtube-dl/tree/master/youtube_dl/extractor
.. _pafy: https://github.com/mps-youtube/pafy
