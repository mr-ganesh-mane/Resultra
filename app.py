from flask import Flask, render_template, request, redirect, url_for, session, send_file

import config
import os

from core.excel_reader import read_excel
from core.excel_validator import validate_excel
from core.result_calculator import calculate_student_result
from core.rule_engine import DEFAULT_RULES
from core.pdf_generator import generate_student_pdf

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

    selected_profile = session.get("selected_profile")

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

    file_path = (
        config.UPLOAD_FOLDER
        + "/"
        + file.filename
    )

    file.save(file_path)

    try:

        # ------------------------------------------
        # Read Excel
        # ------------------------------------------

        excel_result = read_excel(
            file_path
        )


        # ------------------------------------------
        # Validate Excel
        # ------------------------------------------

        errors = validate_excel(
            excel_result
        )

        if errors:

            return render_template(
                "upload.html",
                errors=errors,
                selected_profile=selected_profile
            )


        # ------------------------------------------
        # Check Excel Format
        # ------------------------------------------

        if excel_result["format"] != "single_sheet":

            return render_template(
                "upload.html",
                error=(
                    "Subject-wise Excel format "
                    "will be added next."
                ),
                selected_profile=selected_profile
            )


        data = excel_result["data"]


        # ------------------------------------------
        # Load Selected Profile
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
        # Calculate Student Results
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
        # Store Results in Session
        # ------------------------------------------

        session["student_results"] = student_results

        session["excel_format"] = (
            excel_result["format"]
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
            error=(
                f"Error processing Excel file: "
                f"{error}"
            ),
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
        success=(
            f"Profile '{profile_name}' "
            "selected successfully."
        )
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
# Generate PDF
# --------------------------------------------------

@app.route("/generate-pdf/<int:student_index>")
def generate_pdf(student_index):

    selected_profile_name = session.get(
        "selected_profile"
    )

    if not selected_profile_name:

        return render_template(
            "upload.html",
            error="Please select a profile first."
        )


    profile = load_profile(
        config.PROFILE_FOLDER,
        selected_profile_name
    )

    if profile is None:

        return render_template(
            "upload.html",
            error="Selected profile not found."
        )


    student_results = session.get(
        "student_results"
    )

    if not student_results:

        return render_template(
            "upload.html",
            error=(
                "Please upload and process "
                "an Excel file first."
            )
        )


    if student_index < 0 or student_index >= len(student_results):

        return render_template(
            "upload.html",
            error="Student result not found."
        )


    student_result = student_results[
        student_index
    ]


    file_name = (
        str(student_result["Roll No"])
        + "_"
        + str(
            student_result["Student Name"]
        ).replace(
            " ",
            "_"
        )
        + ".pdf"
    )


    output_path = (
        config.GENERATED_FOLDER
        + "/"
        + file_name
    )


    generate_student_pdf(
        student_result,
        profile,
        output_path
    )


    return render_template(
        "result.html",
        results=student_results,
        excel_format=session.get(
            "excel_format"
        ),
        profile=profile,
        profile_name=selected_profile_name,
        pdf_generated=file_name
    )


# --------------------------------------------------
# Download PDF
# --------------------------------------------------

@app.route("/download-pdf/<filename>")
def download_pdf(filename):

    file_path = (
        config.GENERATED_FOLDER
        + "/"
        + filename
    )

    if not os.path.exists(file_path):

        return render_template(
            "upload.html",
            error="PDF file not found."
        )

    return send_file(
        file_path,
        as_attachment=True
    )


# --------------------------------------------------
# Generate All PDFs
# --------------------------------------------------

@app.route("/generate-all-pdfs")
def generate_all_pdfs():

    # ----------------------------------------------
    # Get Selected Profile
    # ----------------------------------------------

    selected_profile_name = session.get(
        "selected_profile"
    )

    if not selected_profile_name:

        return render_template(
            "upload.html",
            error="Please select a profile first."
        )


    # ----------------------------------------------
    # Load Profile
    # ----------------------------------------------

    profile = load_profile(
        config.PROFILE_FOLDER,
        selected_profile_name
    )

    if profile is None:

        return render_template(
            "upload.html",
            error="Selected profile not found."
        )


    # ----------------------------------------------
    # Get Student Results
    # ----------------------------------------------

    student_results = session.get(
        "student_results"
    )

    if not student_results:

        return render_template(
            "upload.html",
            error=(
                "Please upload and process "
                "an Excel file first."
            )
        )


    # ----------------------------------------------
    # Generate PDF for Every Student
    # ----------------------------------------------

    generated_files = []

    for student_result in student_results:

        file_name = (
            str(student_result["Roll No"])
            + "_"
            + str(
                student_result["Student Name"]
            ).replace(
                " ",
                "_"
            )
            + ".pdf"
        )

        output_path = (
            config.GENERATED_FOLDER
            + "/"
            + file_name
        )

        generate_student_pdf(
            student_result,
            profile,
            output_path
        )

        generated_files.append(
            file_name
        )


    # ----------------------------------------------
    # Show Results
    # ----------------------------------------------

    return render_template(
        "result.html",
        results=student_results,
        excel_format=session.get(
            "excel_format"
        ),
        profile=profile,
        profile_name=selected_profile_name,
        generated_files=generated_files,
        bulk_generated=True
    )


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)