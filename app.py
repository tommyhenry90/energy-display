from flask import Flask, jsonify, render_template
from flask_cors import CORS
from PublicationService.publication_service import app

CORS(app)

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8090)
