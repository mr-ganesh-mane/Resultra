from flask import Flask, render_template, request

import config

from core.excel_reader import read_excel
from core.excel_validator import validate_excel


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["PROFILE_FOLDER"] = config.PROFILE_FOLDER
app.config["GENERATED_FOLDER"] = config.GENERATED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "GET":
        return render_template("upload.html")

    if "excel_file" not in request.files:
        return render_template(
            "upload.html",
            error="Please select an Excel file."
        )

    file = request.files["excel_file"]

    if file.filename == "":
        return render_template(
            "upload.html",
            error="Please select an Excel file."
        )

    file_path = config.UPLOAD_FOLDER + "/" + file.filename

    file.save(file_path)

    try:
        result = read_excel(file_path)

        errors = validate_excel(result)

        if errors:
            return render_template(
                "upload.html",
                errors=errors
            )

        return render_template(
            "upload.html",
            success="Excel file uploaded and validated successfully.",
            excel_format=result["format"]
        )

    except Exception as error:

        return render_template(
            "upload.html",
            error=f"Error processing Excel file: {error}"
        )


if __name__ == "__main__":
    app.run(debug=True)