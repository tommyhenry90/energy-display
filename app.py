from flask import Flask, render_template
from flask_cors import CORS
from PublicationService.publication_service import *

CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
