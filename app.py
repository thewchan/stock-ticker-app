"""Display a stock ticker visualization based on user input.

A Simple Stock Ticker Visualization Web App
Copyright (C) 2020 Matthew Chan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import json
import os
from flask import Flask, render_template, request, send_from_directory
from bokeh.embed import json_item
from ticker import ticker


app = Flask(__name__)
app.vars = {'symbol': '', 'error': ''}


def create_ticker(symbol):
    """Render ticker json object from stock symbol."""
    p = ticker(symbol)

    return p


@app.route('/', methods=('GET', 'POST'))
def index():
    """Render the app's main page."""
    if request.method == 'GET':
        # Default gives IBM's ticker when first loaded.
        app.vars['symbol'] = 'IBM'
        return render_template('index.html',
                               symbol=app.vars['symbol'],
                               error=app.vars['error']
                               )

    else:
        # User submitted a ticker symbol aka method = 'POST'
        app.vars['symbol'] = request.form['symbol']
        return render_template('index.html',
                               symbol=app.vars['symbol'],
                               error=app.vars['error']
                               )


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/plot')
def plot():
    """Render json item from bokeh plot."""
    try:
        app.vars['error'] = ''
        p = create_ticker(app.vars['symbol'])

    except KeyError:
        app.vars['error'] = (f'{app.vars["symbol"]}: '
                             f'Entered stock ticker symbol does not exist.')

    return json.dumps(json_item(p, 'myplot'))


@app.route('/favicon.ico')
def favicon():
    """Redirect to favicon."""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


if __name__ == '__main__':
    app.run(port=33507)
