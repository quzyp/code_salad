#!/usr/bin/env python3

from rattle.rattle import App


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
