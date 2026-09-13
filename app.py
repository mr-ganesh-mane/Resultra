from flask import Flask, render_template

import config


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["PROFILE_FOLDER"] = config.PROFILE_FOLDER
app.config["GENERATED_FOLDER"] = config.GENERATED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)