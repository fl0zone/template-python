import os
from flask import Flask

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

@app.route("/")
def hello_world():
    return "<p>Hello from FL0!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)