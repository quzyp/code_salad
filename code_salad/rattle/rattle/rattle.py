#!/usr/bin/env python3

import re
import json
from flask import render_template, request
from .widgets import Input, Label
from .utils import FlaskAppWrapper


class App:

    def __init__(self, title, template):
        self.app = FlaskAppWrapper(__name__)
        self.app.add_endpoint('/', 'http_response', handler=self.http_response, methods=['GET', 'POST'])
        self.title = title
        self.html = ''
        self.html_src = template
        self.widgets = dict()
        self.make_widgets()
        self.queue = dict()

    def __call__(self, name):
        return self.widgets[name]

    def callback_widget(self, id_, key, value):
        self.queue = [dict(id_=id_, key=key, value=value)]

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

    def make_html_response(self):
        with open(self.html_src, 'r') as f:
            html = f.read()
        for w in self.widgets.values():
            tag = f'{{{{ {w.type}#{w.id_} }}}}'
            html = html.replace(tag, w.code)
        self.html = html

    def run(self):
        self.app.run()

    def http_response(self):
        if not request.form:
            self.make_html_response()
            return render_template('default.html', title=self.title, body=self.html)
        else:
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
