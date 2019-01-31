
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


class Label:

    def __init__(self, id_, callback):
        self.id_ = id_
        self.callback = callback
        self.type = 'label'
        self.__dict__['text'] = ''
        self.code = f'<p id="{self.id_}" class="widget"></p>'

    def __setattr__(self, key, value):
        if key not in ('id_', 'callback', 'type', 'code'):
            self.code = f'<p id="{self.id_}" class="widget">{self.text}</p>'
            self.callback(self.id_, key, value)
        self.__dict__[key] = value
