import os
import sys
from flask import Flask
from flask import request
sys.path.append(os.path.abspath('../'))
from run import run
import requests
from flask import send_from_directory


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        IMAGE_INPUT=root_dir() + "/input/",
        IMAGE_OUTPUT=root_dir() + "/output/"
    )

    # ensure the instance folder exists
    try:
        print(app.instance_path)
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Image depth endpoint
    @app.route('/generate-depth', methods=(['GET']))
    def depth():
        imageUrl = request.args.get('url')
        img_data = requests.get(imageUrl).content
        with open(app.config['IMAGE_INPUT'] + 'image.jpg', 'wb') as handler:
            handler.write(img_data)
        run()
        return send_from_directory(app.config['IMAGE_OUTPUT'] + 'image.png', mimetype='image/png')

    return app
