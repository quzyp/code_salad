Creating a GUI as a Local Web App Using Flask
=============================================

By Fledermann_, 2019-01-31

*Note: the source code is in this very GitHub directory if you want to dive
right in*

    <p align="center">
        <img src="img/cast.gif" width="50%">
    </p>

Have you heard of tkinter? PyQT5? WxPython? Kivy? PyGTK, no, wait, PyGObject?
PySide? PySimpleGUI, which strings some of the formerly mentioned together?

All of these come up if you try to create a graphical user interface
for your python program. Most of these are cross-platform, but not all of them,
and to varying degrees. Some have licensing issues and some bring a plethora
of external dependencies. All in all, the current situation is highly
unsatisfying. I can put my regular python projects on GitHub and be
relatively certain than everyone can run it (as long as python is available),
but that is not the case if I try to slap a GUI on top of it. At least not
without creating a potential 99% of overhead and not knowing how
exactly the interface will look like on a different platform. I don't like
interfaces which look foreign compared to the rest of my windows. Additionally,
creating and styling interfaces using only HTML and CSS sounds like a much
better idea than painstakingly trying to learn how to do anything in a
toolkit library.

"Build a webapp!" I hear countless entrepreneurs shout. "No, thanks, " I answer
politely, "I don't want to host stuff for more or less useless scripts which
may not even be used by anyone." Also, I don't want to write JavaScript, I
want to write Python.

As I set out to find a solution, I discovered many projects which aim to
string JavaScript and Python together:

* pyjs_, which transpiled Python to JS (dead)
* reahl_, which is so pythonic that it chose to abstract away even HTML and CSS (why?)
* flexx_, which also transpiles to JS (active)
* pypyjs_


and many smaller ones, like WDOM_. WDOM is propably pretty close to what I
imagined: a locally running web server (Tornado in this case) serving a page,
while JavaScript is not doing much more than recognising events and sending
them to our server. The reasonable decision here would have been to use
one of these working, full-featured and tested libraries, but then I wondered
how much it takes to implement the most basic functionality myself.

Usage
_____

Let's start by writing the source files for ``my_app`` how we would want to
write them if that toolkit already existed. I went with html in jinja-style where
we can define widgets and give them an name (which serve as an ID):

.. code-block:: html

    my_app.html

    <h1>Square a number!</h1>
    {{ input#number_input }} <br>
    {{ label#result }}

Nothing too exiting. For CSS, a default template would propably be a good idea.
The user can then just edit the template (or delete everything and start from
scratch). For now, let's just outline the label, which should propably
be a ``<p>``:

.. code-block:: css

    static/default.css

    p {
        display: inline-block;
        border: 2px solid green;
        height: 20px;
        min-width: 200px;
    }


The rest is just python code. Subclassing from a base class is usually the way
to do it in most toolkits as it makes things a lot easier as the project
grows. But we want to keep it simple for starters:

.. code-block:: python

    my_app.py

    def square_input():
        value = my_app('number_input').value
        try:
            result = int(value) ** 2
        except ValueError:
            result = 'Not a number!'
        my_app('result').innerText = result


    my_app = App('my_app: Advanced Maths', 'my_app.html')
    my_app('number_input').on_input = square_input
    my_app.run()

Create an app with a title, point to our html source, bind a function to
the input element and run. Inside the function, take the value from ``number_input``,
square it and write the result to the label ``result``.

The 'widgets' are accessible by calling our app with their name, which I think
is a nice and short way to handle this. The widgets' methods and attributes
have names which correspond to JavaScript attributes (or rather properties) -
because we don't actually want to implement them. That means that things like
``my_app('number_input').value`` can be passed directly to JavaScript.
``.on_input`` is a bit of a compromise as that translates to ``obj.on('input')``,
and just calling it ``.input`` wouldn't be very nice. So we need to remove
the ``on_`` later on.

The Backend
___________

*Note: JavaScript is not my strong suit. You could even say I know nothing
about it at all. I have never written a line of JS in my life. Big shoutout
Stackoverflow.*

Now comes the JS. We want to register certain events (like click, input, scroll
and potentially many more) and send them back to python. As we can't manipulate
the page from python directly, the server then makes a response and tells
JS what to do.

.. code-block:: javascript

    static/default.js

    $('.widget').on('click input', (function(event) {
       $.post('/',
              {'event' : event.type,
               'id_' : $(this).attr('id'),
                'props' : JSON.stringify(get_props($(this)))},
          function(response){
            json_ = JSON.parse(response);
            for (var k in json_) {
                $('#'+json_[k].id_).prop(json_[k].key, json_[k].value);
            }
       });
    }));

    function get_props(obj) {
        return {
            'value': obj.val()
        };
    }

Yes, that's jQuery. It's most propably completely unnecessary because it
creates additional overhead for such a simple script, but since I can barely
write JavaScript I have to keep it simple for now.
Every ``click`` or ``input`` event from the ``widget``-class gets registered
and causes a POST containing the event type, the widget id and it's current
properties. These are not *properties* in the Python sense, they are
actually functions returning a current property. For now, ``obj.val()`` is
enough information.

The response is, to use python types, a list of dictionaries: each entry
contains an id, a property name and a value. The script then proceeds to
blindly set all properties.

Now for the widgets. This will be our input element:

.. code-block:: python

    widgets.py

    class Input:

        def __init__(self, id_, callback):
            self.id_ = id_
            self.callback = callback
            self.type = 'input'
            self.code = f'<input type="text" id="{self.id_}" class="widget">'

        def __setattr__(self, key, value):
            if key not in ('id_', 'callback', 'type', 'code'):
                self.callback(self.id_, key, value)
            self.__dict__[key] = value

The label isn't going to be too different. We need an id, a type and
the html code. We also need ``__setattr__`` to call back whenever something changes.
We don't even know the properties our ``Input`` is going to use - we already
used ``value`` in ``my_app.py``, but we actually don't need to care or
define them here.
A widget base class would be a good idea, but that's for later.

Now there's only one piece missing: the web server. I'll be using Flask simply
because I know it, but Tornado et. al. are equally suited for the task (or even better).

Our class will be called ``App``, and to handle Flask responses inside
the class we need a wrapper and define the endpoints manually. Since
there is only one endpoint anyway (``/``) that's not a big deal.

What do we need? Let's start by reading ``my_app.hmtl`` and creating the
widgets:

.. code-block:: python

    rattle.py

    def make_widgets(self):
        widget_objs = {'input': Input, 'label': Label}
        with open(self.html_src, 'r') as f:
            html = f.read()
        pattern = re.compile(r'{{ (.*?) }}')
        widgets = re.findall(pattern, html)
        for w in widgets:
            type_, id_ = w.split('#')
            new_widget = widget_objs[type_](id_, self.callback_widget)
            self.widgets[id_] = new_widget

Manually defining the available widgets certainly isn't the best solution
but acceptable for a prototype.

Replacing the widget tags in the users' html file with html code is
straightforward:

.. code-block:: python

    def make_html_response(self):
        with open(self.html_src, 'r') as f:
            html = f.read()
        for w in self.widgets.values():
            tag = f'{{{{ {w.type}#{w.id_} }}}}'
            html = html.replace(tag, w.code)
        self.html = html

This code will be the first served page - everything else that happens from
that moment on gets send by ajax requests: we programmed the JS file to
fire a request on all kinds of events (click and input so far), so we
can interpret that data here:

.. code-block:: python

            event = request.form['event']
            id_ = request.form['id_']
            props = json.loads(request.form['props'])
            widget = self.widgets[id_]
            for prop, value in props.items():
                setattr(widget, prop, value)
            try:
                getattr(widget, f'on_{event}')()
            except AttributeError:
                pass
            return json.dumps(self.queue)

The widgets' attributes get set as they come. If an event comes in which
we have defined previously (like ``on_input``), call the function.
The ``queue`` here is a list of widgets and their attributes which have changed
since the last request, so we can then send these back for JS to manipulate the
DOM.

And that's it. Clone and run ``my_app.py`` to try it out. It's not much, 
but it is at least easily extensible. A few potential problems:

* I don't know how expensive firing so many requests is
* I don't know if the ``obj.prop()`` method works for all elements, like ``<select>``` and hundreds of others
* a timer is needed for things which don't depend on user input, like a loading bar

Still, it was an interesting little project which may someday have a future.
Alternatively, I could just use a real library.

.. _Fledermann: https://github.com/Fledermann
.. _pyjs: https://github.com/pyjs/pyjs
.. _reahl: https://github.com/reahl/reahl
.. _flexx: https://github.com/flexxui/flexx
.. _pypyjs: https://github.com/pypyjs/pypyjs
.. _WDOM: https://github.com/miyakogi/wdom