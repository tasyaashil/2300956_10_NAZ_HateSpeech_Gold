import re

import pandas as pd

from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_provider_class = LazyJSONEncoder 
app.json = LazyJSONEncoder(app)

kamus = pd.read_csv('new_kamusalay.csv', encoding='latin-1')
abusive = pd.read_csv('abusive.csv', encoding='latin-1')

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version' : LazyString(lambda: '1.0.0'),
        'description' : LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    }, 
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, 
                  config=swagger_config)

@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status_code' : 200,
        'description' : "Menyapa Hello World",
        'data' : "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text.yml", methods=['GET'])
@app.route('/text', methods=['GET'])
def text():
    json_response = {
        'status_code' : 200,
        'description' : "Original Teks",
        'data' : "Halo, apa kabar semua?",
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_clean.yml", methods=['GET'])
@app.route('/text-clean', methods=['GET'])
def text_clean():
    json_response = {
        'status_code' : 200,
        'description' : "Original Teks",
        'data' : re.sub(r'[^a-zA-z0-9]', ' ', "Halo, apa kabar semua?"),
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    file = request.files.getlist('file')[0]
    df = pd.read_csv(file, encoding='latin-1')
    texts = df.Tweet.to_list()
    cleaned_text = []
    for Tweet in texts:
        cleaned_text.append(re.sub(r'[^a-zA-Z0-9]', ' ', Tweet))
        json_response = {
        'status_code': 200,
        'description': "Teks yang akan diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run(debug=True ,port=8080,use_reloader=False)