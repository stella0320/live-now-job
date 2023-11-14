from flask import *
import time
from flask import request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4500)