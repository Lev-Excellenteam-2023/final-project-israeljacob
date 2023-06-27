from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home_page():
    return 'Hi there'


if __name__ == '__main__':
    app.run()