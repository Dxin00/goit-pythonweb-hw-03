from flask import Flask, render_template
import json
import os  # добавлено
from datetime import datetime
from flask import request, redirect, url_for  
from datetime import datetime  

DATA_FILE = "storage/data.json"

# создаём папку и файл, если нужно
os.makedirs("storage", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

app = Flask(__name__)


@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        data = request.form
        timestamp = str(datetime.now())
        new_message = {
            timestamp: {
                "username": data.get("username"),
                "message": data.get("message"),
            }
        }

        with open(DATA_FILE, "r+", encoding="utf-8") as f:
            messages = json.load(f)
            messages.update(new_message)
            f.seek(0)
            json.dump(messages, f, indent=2, ensure_ascii=False)

        return redirect(url_for("read"))  # покажем список сообщений
    return render_template("message.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


@app.route("/read")
def read():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
    return render_template("read.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
