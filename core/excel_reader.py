import pandas as pd


def detect_excel_format(file_path):
    """
    Detect whether the Excel file uses:
    1. All subjects in one sheet
    2. Separate sheet for each subject
    """

    excel_file = pd.ExcelFile(file_path)

    sheet_names = excel_file.sheet_names

    if len(sheet_names) == 1:
        return "single_sheet"

    return "subject_wise"


def read_single_sheet(file_path):
    """
    Read Excel file where all subjects are stored
    as columns in one sheet.
    """

    data = pd.read_excel(file_path)

    return data


def read_subject_wise(file_path):
    """
    Read Excel file where each subject has
    a separate worksheet.
    """

    excel_file = pd.ExcelFile(file_path)

    subject_data = {}

    for sheet_name in excel_file.sheet_names:

        data = pd.read_excel(
            file_path,
            sheet_name=sheet_name
        )

        subject_data[sheet_name] = data

    return subject_data


def combine_subject_wise_data(subject_data):
    """
    Combine subject-wise sheets into one student-wise
    DataFrame using Roll No as the common identifier.
    """

    combined_data = None

    for subject, data in subject_data.items():

        subject_data_frame = data[
            ["Roll No", "Student Name", "Marks"]
        ].copy()

        subject_data_frame = subject_data_frame.rename(
            columns={
                "Marks": subject
            }
        )

        if combined_data is None:

            combined_data = subject_data_frame

        else:

            combined_data = pd.merge(
                combined_data,
                subject_data_frame[
                    ["Roll No", subject]
                ],
                on="Roll No",
                how="outer"
            )

    if combined_data is None:

        return pd.DataFrame()

    return combined_data


def read_excel(file_path):
    """
    Detect the Excel format and read the data.
    """

    excel_format = detect_excel_format(file_path)

    if excel_format == "single_sheet":

        data = read_single_sheet(file_path)

        return {
            "format": "single_sheet",
            "data": data
        }


    # ------------------------------------------
    # Subject-Wise Excel
    # ------------------------------------------

    subject_data = read_subject_wise(
        file_path
    )

    combined_data = combine_subject_wise_data(
        subject_data
    )

    return {
        "format": "subject_wise",

        # Combined data is used for calculation
        "data": combined_data,

        # Original sheets are used for validation
        "raw_data": subject_data
    }