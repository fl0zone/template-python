from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/test_call")
def user():    
    return {
            "user": {
                "id": 1,
                "username": "Raul",
                "email" : "raulgvc1997@gmail.com"
            }
        } 