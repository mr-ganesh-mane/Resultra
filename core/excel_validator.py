import pandas as pd


def validate_single_sheet(data):

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


    if data["Student Name"].isnull().any():

        errors.append(
            "Student Name contains empty values."
        )


    if data["Roll No"].duplicated().any():

        errors.append(
            "Duplicate Roll No found."
        )


    # ------------------------------------------
    # Subject Validation
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
        # Roll No
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
        # Student Name
        # --------------------------------------

        if data["Student Name"].isnull().any():

            errors.append(
                f"Empty Student Name found "
                f"in subject '{subject}'."
            )


        # --------------------------------------
        # Marks
        # --------------------------------------

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


    return errors


def validate_excel(result):

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

        # Use original subject sheets
        raw_data = result.get(
            "raw_data"
        )

        return validate_subject_wise(
            raw_data
        )


    return [
        "Unknown Excel format."
    ]