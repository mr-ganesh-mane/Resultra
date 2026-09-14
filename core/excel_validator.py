import pandas as pd


def validate_single_sheet(data):
    """
    Validate Excel file where all subjects
    are stored in one worksheet.
    """

    errors = []

    required_columns = [
        "Roll No",
        "Student Name"
    ]

    # ------------------------------------------
    # Required Columns
    # ------------------------------------------

    for column in required_columns:

        if column not in data.columns:

            errors.append(
                f"Missing required column: {column}"
            )

    if errors:
        return errors

    # ------------------------------------------
    # Roll No Validation
    # ------------------------------------------

    if data["Roll No"].isnull().any():

        errors.append(
            "Roll No contains empty values."
        )

    if data["Roll No"].duplicated().any():

        errors.append(
            "Duplicate Roll No found."
        )

    # ------------------------------------------
    # Student Name Validation
    # ------------------------------------------

    if data["Student Name"].isnull().any():

        errors.append(
            "Student Name contains empty values."
        )

    # ------------------------------------------
    # Subject Detection
    # ------------------------------------------

    subject_columns = [
        column
        for column in data.columns
        if column not in [
            "Roll No",
            "Student Name"
        ]
    ]

    if not subject_columns:

        errors.append(
            "No subject columns found."
        )

        return errors

    # ------------------------------------------
    # Marks Validation
    # ------------------------------------------

    for subject in subject_columns:

        if data[subject].isnull().any():

            errors.append(
                f"Empty marks found in subject: {subject}"
            )

        numeric_marks = pd.to_numeric(
            data[subject],
            errors="coerce"
        )

        if numeric_marks.isnull().any():

            errors.append(
                f"Invalid marks found in subject: {subject}"
            )

        if (numeric_marks < 0).any():

            errors.append(
                f"Negative marks found in subject: {subject}"
            )

    return errors


def validate_subject_wise(subject_data):
    """
    Validate subject-wise Excel data.

    All errors are collected and returned together.
    Roll No is used as the unique student identifier.
    """

    errors = []

    # ------------------------------------------
    # Check Subject Sheets
    # ------------------------------------------

    if not subject_data:

        errors.append(
            "No subject sheets found."
        )

        return errors


    # ------------------------------------------
    # Store Students of Every Subject
    # ------------------------------------------

    subject_students = {}


    # ------------------------------------------
    # Validate Each Subject
    # ------------------------------------------

    for subject, data in subject_data.items():

        required_columns = [
            "Roll No",
            "Student Name",
            "Marks"
        ]

        # --------------------------------------
        # Required Columns
        # --------------------------------------

        for column in required_columns:

            if column not in data.columns:

                errors.append(
                    f"Missing column '{column}' "
                    f"in subject '{subject}'."
                )

        if not all(
            column in data.columns
            for column in required_columns
        ):

            continue


        # --------------------------------------
        # Roll No Validation
        # --------------------------------------

        if data["Roll No"].isnull().any():

            errors.append(
                f"Empty Roll No found "
                f"in subject '{subject}'."
            )


        if data["Roll No"].duplicated().any():

            errors.append(
                f"Duplicate Roll No found "
                f"in subject '{subject}'."
            )


        # --------------------------------------
        # Student Name Validation
        # --------------------------------------

        if data["Student Name"].isnull().any():

            errors.append(
                f"Empty Student Name found "
                f"in subject '{subject}'."
            )


        # --------------------------------------
        # Marks Validation
        # --------------------------------------

        if data["Marks"].isnull().any():

            errors.append(
                f"Empty marks found "
                f"in subject '{subject}'."
            )


        numeric_marks = pd.to_numeric(
            data["Marks"],
            errors="coerce"
        )


        if numeric_marks.isnull().any():

            errors.append(
                f"Invalid marks found "
                f"in subject '{subject}'."
            )


        if (numeric_marks < 0).any():

            errors.append(
                f"Negative marks found "
                f"in subject '{subject}'."
            )


        # --------------------------------------
        # Store Roll No + Student Name
        # --------------------------------------

        students = {}

        for _, row in data.iterrows():

            roll_no = row["Roll No"]

            if pd.isnull(roll_no):
                continue

            roll_no = str(roll_no).strip()

            student_name = str(
                row["Student Name"]
            ).strip()

            students[roll_no] = student_name


        subject_students[subject] = students


    # ------------------------------------------
    # Stop If No Valid Subject Data
    # ------------------------------------------

    if not subject_students:

        return errors


    # ------------------------------------------
    # Create Complete Roll No Set
    # ------------------------------------------

    all_roll_numbers = set()

    for students in subject_students.values():

        all_roll_numbers.update(
            students.keys()
        )


    # ------------------------------------------
    # Compare Every Subject
    # ------------------------------------------

    for subject, students in subject_students.items():

        # --------------------------------------
        # Missing Students
        # --------------------------------------

        missing_students = (
            all_roll_numbers
            - set(students.keys())
        )


        for roll_no in sorted(
            missing_students
        ):

            errors.append(
                f"Student with Roll No "
                f"'{roll_no}' is missing "
                f"in subject '{subject}'."
            )


        # --------------------------------------
        # Student Name Consistency
        # --------------------------------------

        for roll_no, student_name in students.items():

            names = set()

            for other_subject, other_students in (
                subject_students.items()
            ):

                if roll_no in other_students:

                    names.add(
                        other_students[roll_no]
                    )


            if len(names) > 1:

                errors.append(
                    f"Student Name mismatch "
                    f"for Roll No '{roll_no}' "
                    f"in subject '{subject}'."
                )


    return errors

def validate_excel(result):
    """
    Validate Excel data according to
    the detected Excel format.
    """

    excel_format = result["format"]

    # ------------------------------------------
    # Single Sheet
    # ------------------------------------------

    if excel_format == "single_sheet":

        data = result["data"]

        return validate_single_sheet(
            data
        )

    # ------------------------------------------
    # Subject Wise
    # ------------------------------------------

    if excel_format == "subject_wise":

        raw_data = result.get(
            "raw_data"
        )

        return validate_subject_wise(
            raw_data
        )

    return [
        "Unknown Excel format."
    ]