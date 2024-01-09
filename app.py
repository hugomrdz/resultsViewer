import os
from flask import Flask
from views import views

app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
