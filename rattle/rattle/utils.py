#!/usr/bin/env python3

from flask import Flask


class EndpointAction:

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        response = self.action()
        return response


class FlaskAppWrapper:
    app = None

    def __init__(self, name):
        self.app = Flask(name, static_url_path='')

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
