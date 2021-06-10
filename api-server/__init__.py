import os
import sys
from flask import Flask
from flask import request
sys.path.append(os.path.abspath('../'))
from run import init
from run import process
import requests
from flask import send_from_directory, abort
from urllib import parse


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    imageName, input_path, optimize, device, model, output_path, transform = init()
    app.config.from_mapping(
        IMAGE_INPUT=root_dir() + "/input/",
        IMAGE_OUTPUT=root_dir() + "/output/",
        HEADERS={
            'User-Agent':
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Cookie': 'cache_bypass=True',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        },
        OPTIMIZE=optimize,
        DEVICE=device,
        MODEL=model,
        TRANSFORM=transform
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
        splitUrl = parse.urlsplit(imageUrl)
        imageName = splitUrl.path.split('/')[-1].split('.')[0]
        img_data = requests.get(
            imageUrl, headers=app.config['HEADERS'])
        if img_data.status_code != 200:
            app.logger.error(
                f'Unexpected return code ({img_data.status_code}) when downloading asset: {imageUrl}')
            abort(500)
        with open(app.config['IMAGE_INPUT'] + imageName + '.jpg', 'wb') as handler:
            handler.write(img_data.content)
        process(imageName, app.config['IMAGE_INPUT'], app.config['OPTIMIZE'],
                app.config['DEVICE'], app.config['MODEL'], app.config['IMAGE_OUTPUT'], app.config['TRANSFORM'])
        os.remove(app.config['IMAGE_INPUT'] + imageName + '.jpg')
        return send_from_directory(app.config['IMAGE_OUTPUT'], imageName + '.png', mimetype='image/png')

    return app
