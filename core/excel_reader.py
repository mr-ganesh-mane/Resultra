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
        data = pd.read_excel(file_path, sheet_name=sheet_name)

        subject_data[sheet_name] = data

    return subject_data


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

    data = read_subject_wise(file_path)

    return {
        "format": "subject_wise",
        "data": data
    }