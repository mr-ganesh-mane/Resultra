from flask import Flask, render_template, request

import config

from core.excel_reader import read_excel
from core.excel_validator import validate_excel
from core.result_calculator import calculate_student_result


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

        # Read Excel
        result = read_excel(file_path)

        # Validate Excel
        errors = validate_excel(result)

        if errors:

            return render_template(
                "upload.html",
                errors=errors
            )

        # Check format
        if result["format"] != "single_sheet":

            return render_template(
                "upload.html",
                error="Subject-wise Excel format will be added next."
            )

        data = result["data"]

        # Calculate student results
        student_results = []

        for _, row in data.iterrows():

            student_data = row.to_dict()

            student_result = calculate_student_result(
                student_data
            )

            student_results.append(student_result)

        return render_template(
            "result.html",
            results=student_results,
            excel_format=result["format"]
        )

    except Exception as error:

        return render_template(
            "upload.html",
            error=f"Error processing Excel file: {error}"
        )


if __name__ == "__main__":
    app.run(debug=True)