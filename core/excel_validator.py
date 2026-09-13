import pandas as pd


def validate_single_sheet(data):
    """
    Validate Excel data where all subjects are
    present in one sheet.
    """

    errors = []

    required_columns = ["Roll No", "Student Name"]

    # Check required columns
    for column in required_columns:
        if column not in data.columns:
            errors.append(f"Missing required column: {column}")

    if errors:
        return errors

    # Check empty Roll No
    if data["Roll No"].isnull().any():
        errors.append("Roll No contains empty values.")

    # Check empty Student Name
    if data["Student Name"].isnull().any():
        errors.append("Student Name contains empty values.")

    # Check duplicate Roll No
    if data["Roll No"].duplicated().any():
        errors.append("Duplicate Roll No found.")

    # Identify subject columns
    subject_columns = [
        column for column in data.columns
        if column not in ["Roll No", "Student Name"]
    ]

    if not subject_columns:
        errors.append("No subject columns found.")
        return errors

    # Check marks
    for subject in subject_columns:

        if data[subject].isnull().any():
            errors.append(f"Empty marks found in subject: {subject}")

        numeric_marks = pd.to_numeric(data[subject], errors="coerce")

        if numeric_marks.isnull().any():
            errors.append(f"Invalid marks found in subject: {subject}")

        if (numeric_marks < 0).any():
            errors.append(f"Negative marks found in subject: {subject}")

    return errors


def validate_subject_wise(subject_data):
    """
    Validate Excel data where each subject
    has a separate worksheet.
    """

    errors = []

    if not subject_data:
        errors.append("No subject sheets found.")
        return errors

    for subject, data in subject_data.items():

        required_columns = ["Roll No", "Student Name", "Marks"]

        # Check required columns
        for column in required_columns:
            if column not in data.columns:
                errors.append(
                    f"Missing column '{column}' in subject '{subject}'."
                )

        if not all(column in data.columns for column in required_columns):
            continue

        # Check empty Roll No
        if data["Roll No"].isnull().any():
            errors.append(
                f"Empty Roll No found in subject '{subject}'."
            )

        # Check duplicate Roll No
        if data["Roll No"].duplicated().any():
            errors.append(
                f"Duplicate Roll No found in subject '{subject}'."
            )

        # Check empty Student Name
        if data["Student Name"].isnull().any():
            errors.append(
                f"Empty Student Name found in subject '{subject}'."
            )

        # Check marks
        numeric_marks = pd.to_numeric(
            data["Marks"],
            errors="coerce"
        )

        if numeric_marks.isnull().any():
            errors.append(
                f"Invalid marks found in subject '{subject}'."
            )

        if (numeric_marks < 0).any():
            errors.append(
                f"Negative marks found in subject '{subject}'."
            )

    return errors


def validate_excel(result):
    """
    Validate data returned by excel_reader.py.
    """

    excel_format = result["format"]
    data = result["data"]

    if excel_format == "single_sheet":
        return validate_single_sheet(data)

    if excel_format == "subject_wise":
        return validate_subject_wise(data)

    return ["Unknown Excel format."]