from flask import Flask, render_template, jsonify
from flask_cors import CORS
from Code.scheduler import main

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('cow dung is not sweet!')


@app.route('/amortize', methods=['POST', 'GET'])
def algorithm():
    output = main()
    refined_output = output.split('&')
    return jsonify(refined_output)


if __name__ == '__main__':
    app.run()
