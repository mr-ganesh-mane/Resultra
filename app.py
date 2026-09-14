from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    session
)

import os

import config

from core.excel_reader import read_excel
from core.excel_validator import validate_excel

from core.result_calculator import (
    calculate_student_result
)

from core.rule_engine import (
    DEFAULT_RULES
)

from core.profile_manager import (
    save_profile,
    load_profile,
    list_profiles,
    delete_profile,
    save_profile_rules,
    load_profile_rules
)

from core.pdf_generator import (
    generate_student_pdf
)


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = (
    config.UPLOAD_FOLDER
)

app.config["PROFILE_FOLDER"] = (
    config.PROFILE_FOLDER
)

app.config["GENERATED_FOLDER"] = (
    config.GENERATED_FOLDER
)

app.config["MAX_CONTENT_LENGTH"] = (
    config.MAX_CONTENT_LENGTH
)

app.secret_key = "resultra-secret-key"


# ----------------------------------------
# Create Required Folders
# ----------------------------------------

os.makedirs(
    config.UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    config.PROFILE_FOLDER,
    exist_ok=True
)

os.makedirs(
    config.GENERATED_FOLDER,
    exist_ok=True
)


# ----------------------------------------
# Home
# ----------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ----------------------------------------
# Upload Excel
# ----------------------------------------

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    selected_profile = session.get(
        "selected_profile"
    )


    if request.method == "GET":

        return render_template(
            "upload.html",
            selected_profile=selected_profile
        )


    # Check file
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


    # Check extension
    if "." not in file.filename:

        return render_template(
            "upload.html",
            error="Invalid file type.",
            selected_profile=selected_profile
        )


    extension = (
        file.filename
        .rsplit(".", 1)[1]
        .lower()
    )


    if extension not in config.ALLOWED_EXTENSIONS:

        return render_template(
            "upload.html",
            error="Only Excel files are allowed.",
            selected_profile=selected_profile
        )


    # Save Excel file
    file_path = os.path.join(
        config.UPLOAD_FOLDER,
        file.filename
    )


    file.save(file_path)


    try:

        # Read Excel
        excel_result = read_excel(
            file_path
        )


        # Validate Excel
        errors = validate_excel(
            excel_result
        )


        if errors:

            return render_template(
                "upload.html",
                errors=errors,
                selected_profile=selected_profile
            )


        # Get student data
        data = excel_result["data"]


        # Detect subjects dynamically
        subjects = [

            column

            for column in data.columns

            if column not in [
                "Roll No",
                "Student Name"
            ]

        ]


        # Store upload information
        session["subjects"] = subjects

        session["excel_format"] = (
            excel_result["format"]
        )

        session["uploaded_file"] = (
            file.filename
        )


        # --------------------------------
        # Do NOT calculate here.
        #
        # First configure subject credits.
        # --------------------------------

        if not selected_profile:

            return redirect(
                url_for("profiles")
            )


        return redirect(
            url_for("configure_credits")
        )


    except Exception as error:

        return render_template(
            "upload.html",
            error=(
                "Error processing Excel file: "
                f"{error}"
            ),
            selected_profile=selected_profile
        )


# ----------------------------------------
# Configure Subject Credits
# ----------------------------------------

@app.route(
    "/configure-credits",
    methods=["GET", "POST"]
)
def configure_credits():

    selected_profile = session.get(
        "selected_profile"
    )


    subjects = session.get(
        "subjects",
        []
    )


    uploaded_file = session.get(
        "uploaded_file"
    )


    # --------------------------------
    # Check required session data
    # --------------------------------

    if not subjects:

        return redirect(
            url_for("upload")
        )


    if not uploaded_file:

        return redirect(
            url_for("upload")
        )


    if not selected_profile:

        return redirect(
            url_for("profiles")
        )


    # --------------------------------
    # Load Profile
    # --------------------------------

    profile = load_profile(
        config.PROFILE_FOLDER,
        selected_profile
    )


    if profile is None:

        return redirect(
            url_for("profiles")
        )


    rules = profile.get(
        "rules",
        DEFAULT_RULES
    ).copy()


    subject_credits = rules.get(
        "subject_credits",
        {}
    ).copy()


    # --------------------------------
    # GET
    # --------------------------------

    if request.method == "GET":

        return render_template(
            "credits.html",
            profile_name=selected_profile,
            subjects=subjects,
            subject_credits=subject_credits
        )


    # --------------------------------
    # POST
    # --------------------------------

    submitted_subjects = (
        request.form.getlist(
            "subject"
        )
    )


    submitted_credits = (
        request.form.getlist(
            "credit"
        )
    )


    subject_credits = {}


    for subject, credit in zip(
        submitted_subjects,
        submitted_credits
    ):

        subject = subject.strip()


        if subject == "":
            continue


        try:

            credit = float(credit)

        except ValueError:

            return render_template(
                "credits.html",
                profile_name=selected_profile,
                subjects=subjects,
                subject_credits=subject_credits,
                error=(
                    f"Invalid credit value "
                    f"for {subject}."
                )
            )


        if credit < 0:

            return render_template(
                "credits.html",
                profile_name=selected_profile,
                subjects=subjects,
                subject_credits=subject_credits,
                error=(
                    f"Credit cannot be negative "
                    f"for {subject}."
                )
            )


        subject_credits[subject] = credit


    # --------------------------------
    # Make sure all subjects have credits
    # --------------------------------

    for subject in subjects:

        if subject not in subject_credits:

            return render_template(
                "credits.html",
                profile_name=selected_profile,
                subjects=subjects,
                subject_credits=subject_credits,
                error=(
                    f"Please enter credit "
                    f"for {subject}."
                )
            )


    # --------------------------------
    # Update Rules
    # --------------------------------

    rules["subject_credits"] = (
        subject_credits
    )


    # --------------------------------
    # Save Rules
    # --------------------------------

    save_profile_rules(
        config.PROFILE_FOLDER,
        selected_profile,
        rules
    )


    # --------------------------------
    # Read Excel Again
    # --------------------------------

    file_path = os.path.join(
        config.UPLOAD_FOLDER,
        uploaded_file
    )


    try:

        excel_result = read_excel(
            file_path
        )


        # Validate again
        errors = validate_excel(
            excel_result
        )


        if errors:

            return render_template(
                "credits.html",
                profile_name=selected_profile,
                subjects=subjects,
                subject_credits=subject_credits,
                errors=errors
            )


        data = excel_result["data"]


        # --------------------------------
        # Calculate Student Results
        # --------------------------------

        student_results = []


        for _, row in data.iterrows():

            student_data = row.to_dict()


            student_result = (
                calculate_student_result(
                    student_data,
                    rules
                )
            )


            student_results.append(
                student_result
            )


        # Store results
        session["student_results"] = (
            student_results
        )


        # --------------------------------
        # Result Preview
        # --------------------------------

        return render_template(
            "result.html",
            results=student_results,
            excel_format=excel_result["format"],
            profile=profile,
            profile_name=selected_profile,
            preview=True
        )


    except Exception as error:

        return render_template(
            "credits.html",
            profile_name=selected_profile,
            subjects=subjects,
            subject_credits=subject_credits,
            error=(
                "Error calculating result: "
                f"{error}"
            )
        )


# ----------------------------------------
# Profiles
# ----------------------------------------

@app.route("/profiles")
def profiles():

    profile_list = list_profiles(
        config.PROFILE_FOLDER
    )


    return render_template(
        "profiles.html",
        profiles=profile_list
    )


# ----------------------------------------
# View Profile
# ----------------------------------------

@app.route(
    "/profile/<profile_name>"
)
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


# ----------------------------------------
# Use Profile
# ----------------------------------------

@app.route(
    "/profile/<profile_name>/use"
)
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


    session["selected_profile"] = (
        profile_name
    )


    return redirect(
        url_for("upload")
    )


# ----------------------------------------
# New Profile
# ----------------------------------------

@app.route(
    "/profile/new",
    methods=["GET", "POST"]
)
def new_profile():

    if request.method == "GET":

        return render_template(
            "profile.html",
            new_profile=True
        )


    profile_name = request.form.get(
        "profile_name",
        ""
    ).strip()


    if profile_name == "":

        return render_template(
            "profile.html",
            new_profile=True,
            error="Please enter a profile name."
        )


    existing_profiles = list_profiles(
        config.PROFILE_FOLDER
    )


    if profile_name in existing_profiles:

        return render_template(
            "profile.html",
            new_profile=True,
            error="Profile already exists."
        )


    profile = {

        "department": request.form.get(
            "department",
            ""
        ).strip(),

        "course": request.form.get(
            "course",
            ""
        ).strip(),

        "class": request.form.get(
            "class",
            ""
        ).strip(),

        "semester": request.form.get(
            "semester",
            ""
        ).strip(),

        "academic_year": request.form.get(
            "academic_year",
            ""
        ).strip(),

        "examination": request.form.get(
            "examination",
            ""
        ).strip(),

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


    return redirect(
        url_for("profiles")
    )


# ----------------------------------------
# Delete Profile
# ----------------------------------------

@app.route(
    "/profile/<profile_name>/delete"
)
def delete_profile_route(profile_name):

    delete_profile(
        config.PROFILE_FOLDER,
        profile_name
    )


    if session.get(
        "selected_profile"
    ) == profile_name:

        session.pop(
            "selected_profile",
            None
        )


    return redirect(
        url_for("profiles")
    )


# ----------------------------------------
# Profile Rules
# ----------------------------------------

@app.route(
    "/profile/<profile_name>/rules",
    methods=["GET", "POST"]
)
def profile_rules(profile_name):

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


    # --------------------------------
    # GET
    # --------------------------------

    if request.method == "GET":

        rules = load_profile_rules(
            config.PROFILE_FOLDER,
            profile_name
        )


        if rules is None:

            rules = DEFAULT_RULES.copy()


        detected_subjects = session.get(
            "subjects",
            []
        )


        subject_credits = rules.get(
            "subject_credits",
            {}
        ).copy()


        for subject in detected_subjects:

            if subject not in subject_credits:

                subject_credits[subject] = 0


        rules["subject_credits"] = (
            subject_credits
        )


        return render_template(
            "rules.html",
            profile_name=profile_name,
            rules=rules
        )


    # --------------------------------
    # Basic Rules
    # --------------------------------

    passing_marks = request.form.get(
        "passing_marks",
        type=float
    )


    max_marks = request.form.get(
        "max_marks_per_subject",
        type=float
    )


    if (
        passing_marks is None
        or max_marks is None
    ):

        return render_template(
            "rules.html",
            profile_name=profile_name,
            rules=DEFAULT_RULES,
            error="Please enter valid marks."
        )


    if (
        passing_marks < 0
        or max_marks <= 0
    ):

        return render_template(
            "rules.html",
            profile_name=profile_name,
            rules=DEFAULT_RULES,
            error="Please enter valid marks."
        )


    if passing_marks > max_marks:

        return render_template(
            "rules.html",
            profile_name=profile_name,
            rules=DEFAULT_RULES,
            error=(
                "Passing marks cannot be greater "
                "than maximum marks."
            )
        )


    # --------------------------------
    # Grade Rules
    # --------------------------------

    grade_ranges = []


    grades = request.form.getlist(
        "grade"
    )


    minimum_marks = request.form.getlist(
        "min"
    )


    grade_points = request.form.getlist(
        "grade_point"
    )


    for grade, minimum, grade_point in zip(
        grades,
        minimum_marks,
        grade_points
    ):

        if grade.strip() == "":
            continue


        try:

            minimum = float(minimum)

            grade_point = float(
                grade_point
            )

        except ValueError:

            continue


        if minimum < 0:
            continue


        if grade_point < 0:
            continue


        grade_ranges.append({

            "min": minimum,

            "grade": grade.strip(),

            "grade_point": grade_point

        })


    grade_ranges.sort(
        key=lambda item: item["min"],
        reverse=True
    )


    # --------------------------------
    # Subject Credits
    # --------------------------------

    subjects = request.form.getlist(
        "subject"
    )


    credits = request.form.getlist(
        "credit"
    )


    subject_credits = {}


    for subject, credit in zip(
        subjects,
        credits
    ):

        subject = subject.strip()


        if subject == "":
            continue


        try:

            credit = float(credit)

        except ValueError:

            continue


        if credit < 0:
            continue


        subject_credits[subject] = (
            credit
        )


    # --------------------------------
    # Save Rules
    # --------------------------------

    rules = {

        "passing_marks": passing_marks,

        "max_marks_per_subject": max_marks,

        "grade_ranges": grade_ranges,

        "subject_credits": subject_credits

    }


    save_profile_rules(
        config.PROFILE_FOLDER,
        profile_name,
        rules
    )


    return render_template(
        "rules.html",
        profile_name=profile_name,
        rules=rules,
        success=(
            "Result rules saved successfully."
        )
    )

# ----------------------------------------
# PDF Template & Design
# ----------------------------------------

@app.route(
    "/profile/<profile_name>/design",
    methods=["GET", "POST"]
)
def profile_design(profile_name):

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


    # Get existing design
    design = profile.get(
        "design",
        {}
    ).copy()


    # --------------------------------
    # GET
    # --------------------------------

    if request.method == "GET":

        return render_template(
            "design.html",
            profile_name=profile_name,
            design=design
        )


    # --------------------------------
    # POST
    # --------------------------------

    page_size = request.form.get(
        "page_size",
        "A4"
    )


    orientation = request.form.get(
        "orientation",
        "portrait"
    )


    header_title = request.form.get(
        "header_title",
        ""
    ).strip()


    header_subtitle = request.form.get(
        "header_subtitle",
        ""
    ).strip()


    footer_text = request.form.get(
        "footer_text",
        ""
    ).strip()


    # --------------------------------
    # Validate Page Size
    # --------------------------------

    if page_size not in [
        "A4",
        "LETTER"
    ]:

        page_size = "A4"


    # --------------------------------
    # Validate Orientation
    # --------------------------------

    if orientation not in [
        "portrait",
        "landscape"
    ]:

        orientation = "portrait"


    # --------------------------------
    # Save Design
    # --------------------------------

    design = {

        "page_size": page_size,

        "orientation": orientation,

        "header_title": header_title,

        "header_subtitle": header_subtitle,

        "footer_text": footer_text

    }


    profile["design"] = design


    save_profile(
        config.PROFILE_FOLDER,
        profile_name,
        profile
    )


    return render_template(
        "design.html",
        profile_name=profile_name,
        design=design,
        success=(
            "PDF template and design "
            "saved successfully."
        )
    )

# ----------------------------------------
# Generate Individual PDF
# ----------------------------------------

@app.route(
    "/generate-pdf/<roll_no>"
)
def generate_pdf(roll_no):

    student_results = session.get(
        "student_results",
        []
    )


    profile_name = session.get(
        "selected_profile"
    )


    if not profile_name:

        return redirect(
            url_for("profiles")
        )


    profile = load_profile(
        config.PROFILE_FOLDER,
        profile_name
    )


    if profile is None:

        return redirect(
            url_for("profiles")
        )


    student_result = None


    for result in student_results:

        if str(
            result["Roll No"]
        ) == str(roll_no):

            student_result = result

            break


    if student_result is None:

        return redirect(
            url_for("home")
        )


    file_name = (
        f"{roll_no}_result.pdf"
    )


    output_path = os.path.join(
        config.GENERATED_FOLDER,
        file_name
    )


    generate_student_pdf(
        student_result,
        profile,
        output_path
    )


    return redirect(
        url_for(
            "download_pdf",
            filename=file_name
        )
    )


# ----------------------------------------
# Download PDF
# ----------------------------------------

@app.route(
    "/download-pdf/<filename>"
)
def download_pdf(filename):

    return send_from_directory(
        config.GENERATED_FOLDER,
        filename,
        as_attachment=True
    )


# ----------------------------------------
# Preview PDF
# ----------------------------------------

@app.route(
    "/preview-pdf/<roll_no>"
)
def preview_pdf(roll_no):

    student_results = session.get(
        "student_results",
        []
    )


    profile_name = session.get(
        "selected_profile"
    )


    if not profile_name:

        return redirect(
            url_for("profiles")
        )


    profile = load_profile(
        config.PROFILE_FOLDER,
        profile_name
    )


    if profile is None:

        return redirect(
            url_for("profiles")
        )


    student_result = None


    for result in student_results:

        if str(
            result["Roll No"]
        ) == str(roll_no):

            student_result = result

            break


    if student_result is None:

        return redirect(
            url_for("home")
        )


    file_name = (
        f"{roll_no}_preview.pdf"
    )


    output_path = os.path.join(
        config.GENERATED_FOLDER,
        file_name
    )


    generate_student_pdf(
        student_result,
        profile,
        output_path
    )


    return send_from_directory(
        config.GENERATED_FOLDER,
        file_name,
        mimetype="application/pdf"
    )


# ----------------------------------------
# Generate All PDFs
# ----------------------------------------

@app.route(
    "/generate-all-pdfs",
    methods=["POST"]
)
def generate_all_pdfs():

    student_results = session.get(
        "student_results",
        []
    )


    profile_name = session.get(
        "selected_profile"
    )


    if not profile_name:

        return redirect(
            url_for("profiles")
        )


    profile = load_profile(
        config.PROFILE_FOLDER,
        profile_name
    )


    if profile is None:

        return redirect(
            url_for("profiles")
        )


    generated_files = []


    for student_result in student_results:

        roll_no = student_result[
            "Roll No"
        ]


        file_name = (
            f"{roll_no}_result.pdf"
        )


        output_path = os.path.join(
            config.GENERATED_FOLDER,
            file_name
        )


        generate_student_pdf(
            student_result,
            profile,
            output_path
        )


        generated_files.append(
            file_name
        )


    return render_template(
        "result.html",
        results=student_results,
        excel_format=session.get(
            "excel_format"
        ),
        profile=profile,
        profile_name=profile_name,
        generated_files=generated_files,
        preview=True
    )


# ----------------------------------------
# Run Application
# ----------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )