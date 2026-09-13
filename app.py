from flask import Flask, render_template, request, session

import config

from core.excel_reader import read_excel
from core.excel_validator import validate_excel
from core.result_calculator import calculate_student_result
from core.rule_engine import DEFAULT_RULES

from core.profile_manager import (
    save_profile,
    load_profile,
    list_profiles,
    delete_profile
)


app = Flask(__name__)

app.secret_key = "resultra-secret-key"

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

    selected_profile = session.get(
        "selected_profile"
    )

    if request.method == "GET":

        return render_template(
            "upload.html",
            selected_profile=selected_profile
        )


    if "excel_file" not in request.files:

        return render_template(
            "upload.html",
            error="Please select an Excel file.",
            selected_profile=selected_profile
        )


    file = request.files["excel_file"]


    if file.filename == "":

        return render_template(
            "upload.html",
            error="Please select an Excel file.",
            selected_profile=selected_profile
        )


    file_path = config.UPLOAD_FOLDER + "/" + file.filename

    file.save(file_path)


    try:

        # ------------------------------------------
        # Read Excel
        # ------------------------------------------

        excel_result = read_excel(file_path)


        # ------------------------------------------
        # Validate Excel
        # ------------------------------------------

        errors = validate_excel(excel_result)


        if errors:

            return render_template(
                "upload.html",
                errors=errors,
                selected_profile=selected_profile
            )


        # ------------------------------------------
        # Check Excel format
        # ------------------------------------------

        if excel_result["format"] != "single_sheet":

            return render_template(
                "upload.html",
                error="Subject-wise Excel format will be added next.",
                selected_profile=selected_profile
            )


        data = excel_result["data"]


        # ------------------------------------------
        # Load selected profile
        # ------------------------------------------

        profile = None

        rules = DEFAULT_RULES


        if selected_profile:

            profile = load_profile(
                config.PROFILE_FOLDER,
                selected_profile
            )


            if profile:

                rules = profile.get(
                    "rules",
                    DEFAULT_RULES
                )


        # ------------------------------------------
        # Calculate student results
        # ------------------------------------------

        student_results = []


        for _, row in data.iterrows():

            student_data = row.to_dict()


            student_result = calculate_student_result(
                student_data,
                rules
            )


            student_results.append(
                student_result
            )


        # ------------------------------------------
        # Show Results
        # ------------------------------------------

        return render_template(
            "result.html",
            results=student_results,
            excel_format=excel_result["format"],
            profile=profile,
            profile_name=selected_profile
        )


    except Exception as error:

        return render_template(
            "upload.html",
            error=f"Error processing Excel file: {error}",
            selected_profile=selected_profile
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
# View Profile
# --------------------------------------------------

@app.route("/profile/<profile_name>")
def view_profile(profile_name):

    profile = load_profile(
        config.PROFILE_FOLDER,
        profile_name
    )


    if profile is None:

        return render_template(
            "profiles.html",
            profiles=list_profiles(
                config.PROFILE_FOLDER
            ),
            error="Profile not found."
        )


    return render_template(
        "profile.html",
        profile_name=profile_name,
        profile=profile
    )


# --------------------------------------------------
# Use Profile
# --------------------------------------------------

@app.route("/profile/<profile_name>/use")
def use_profile(profile_name):

    profile = load_profile(
        config.PROFILE_FOLDER,
        profile_name
    )


    if profile is None:

        return render_template(
            "profiles.html",
            profiles=list_profiles(
                config.PROFILE_FOLDER
            ),
            error="Profile not found."
        )


    session["selected_profile"] = profile_name


    return render_template(
        "upload.html",
        selected_profile=profile_name,
        success=f"Profile '{profile_name}' selected successfully."
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

        "rules": DEFAULT_RULES,

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