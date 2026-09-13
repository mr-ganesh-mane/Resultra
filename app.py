from flask import Flask, render_template, request

import config

from core.excel_reader import read_excel
from core.excel_validator import validate_excel
from core.result_calculator import calculate_student_result

from core.profile_manager import (
    save_profile,
    load_profile,
    list_profiles,
    delete_profile
)


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["PROFILE_FOLDER"] = config.PROFILE_FOLDER
app.config["GENERATED_FOLDER"] = config.GENERATED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# Excel Upload
# --------------------------------------------------

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


        # Currently calculate results
        # only for single-sheet format

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


            student_results.append(
                student_result
            )


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


# --------------------------------------------------
# Profiles
# --------------------------------------------------

@app.route("/profiles")
def profiles():

    profile_names = list_profiles(
        config.PROFILE_FOLDER
    )


    return render_template(
        "profiles.html",
        profiles=profile_names
    )


# --------------------------------------------------
# Create New Profile
# --------------------------------------------------

@app.route("/profile/new", methods=["GET", "POST"])
def new_profile():

    if request.method == "GET":

        return render_template(
            "profile.html"
        )


    profile_name = request.form.get(
        "profile_name"
    )


    if not profile_name:

        return render_template(
            "profile.html",
            error="Profile name is required."
        )


    profile = {

        "department": request.form.get(
            "department",
            ""
        ),

        "course": request.form.get(
            "course",
            ""
        ),

        "class": request.form.get(
            "class",
            ""
        ),

        "semester": request.form.get(
            "semester",
            ""
        ),

        "academic_year": request.form.get(
            "academic_year",
            ""
        ),

        "examination": request.form.get(
            "examination",
            ""
        ),


        "rules": {

            "passing_marks": 40

        },


        "design": {

            "page_size": "A4",

            "orientation": "portrait"

        }

    }


    save_profile(
        config.PROFILE_FOLDER,
        profile_name,
        profile
    )


    return render_template(
        "profile.html",
        success="Profile saved successfully."
    )


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)