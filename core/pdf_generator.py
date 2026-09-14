import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import (
    A4,
    LETTER,
    landscape,
    portrait
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def get_page_size(design=None):

    if design is None:
        design = {}

    page_size = design.get(
        "page_size",
        "A4"
    )

    orientation = design.get(
        "orientation",
        "portrait"
    )


    if page_size == "LETTER":

        page = LETTER

    else:

        page = A4


    if orientation == "landscape":

        page = landscape(page)

    else:

        page = portrait(page)


    return page


def generate_student_pdf(
    student_result,
    profile,
    output_path
):
    """
    Generate PDF result for one student.
    """

    design = profile.get(
        "design",
        {}
    )


    page_size = get_page_size(
        design
    )


    document = SimpleDocTemplate(
        output_path,
        pagesize=page_size,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "ResultTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=8
    )


    center_style = ParagraphStyle(
        "Center",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10
    )


    story = []


    # --------------------------------
    # College / Profile Information
    # --------------------------------

    department = profile.get(
        "department",
        ""
    )

    course = profile.get(
        "course",
        ""
    )

    class_name = profile.get(
        "class",
        ""
    )

    semester = profile.get(
        "semester",
        ""
    )

    academic_year = profile.get(
        "academic_year",
        ""
    )

    examination = profile.get(
        "examination",
        ""
    )


    if department:

        story.append(
            Paragraph(
                department,
                title_style
            )
        )


    if course:

        story.append(
            Paragraph(
                course,
                center_style
            )
        )

        story.append(
            Spacer(1, 4)
        )


    story.append(
        Paragraph(
            "STUDENT RESULT",
            title_style
        )
    )


    if class_name:

        story.append(
            Paragraph(
                f"<b>Class:</b> {class_name}",
                center_style
            )
        )


    if semester:

        story.append(
            Paragraph(
                f"<b>Semester:</b> {semester}",
                center_style
            )
        )


    if academic_year:

        story.append(
            Paragraph(
                f"<b>Academic Year:</b> {academic_year}",
                center_style
            )
        )


    if examination:

        story.append(
            Paragraph(
                f"<b>Examination:</b> {examination}",
                center_style
            )
        )


    story.append(
        Spacer(1, 12)
    )


    # --------------------------------
    # Student Information
    # --------------------------------

    student_info = [

        [
            "Student Name",
            str(
                student_result.get(
                    "Student Name",
                    ""
                )
            )
        ],

        [
            "Roll No",
            str(
                student_result.get(
                    "Roll No",
                    ""
                )
            )
        ]

    ]


    student_table = Table(
        student_info,
        colWidths=[
            45 * mm,
            110 * mm
        ]
    )


    student_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])
    )


    story.append(
        student_table
    )


    story.append(
        Spacer(1, 12)
    )


    # --------------------------------
    # Subject Result Table
    # --------------------------------

    subject_table_data = [

        [
            "Subject",
            "Marks",
            "Grade",
            "Grade Point",
            "Credit",
            "Credit Point",
            "Status"
        ]

    ]


    subjects = student_result.get(
        "subjects",
        {}
    )


    for subject, data in subjects.items():

        subject_table_data.append([

            str(subject),

            str(
                data.get(
                    "marks",
                    ""
                )
            ),

            str(
                data.get(
                    "grade",
                    ""
                )
            ),

            str(
                data.get(
                    "grade_point",
                    ""
                )
            ),

            str(
                data.get(
                    "credit",
                    ""
                )
            ),

            str(
                data.get(
                    "credit_point",
                    ""
                )
            ),

            str(
                data.get(
                    "status",
                    ""
                )
            )

        ])


    subject_table = Table(
        subject_table_data,
        repeatRows=1
    )


    subject_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                5
            )

        ])
    )


    story.append(
        subject_table
    )


    story.append(
        Spacer(1, 12)
    )


    # --------------------------------
    # Result Summary
    # --------------------------------

    summary_data = [

        [
            "Total Marks",
            f"{student_result.get('total', 0)} / "
            f"{student_result.get('maximum_marks', 0)}"
        ],

        [
            "Percentage",
            f"{student_result.get('percentage', 0)}%"
        ],

        [
            "Total Credits",
            str(
                student_result.get(
                    "total_credits",
                    0
                )
            )
        ],

        [
            "Total Credit Points",
            str(
                student_result.get(
                    "total_credit_points",
                    0
                )
            )
        ],

        [
            "SGPA",
            str(
                student_result.get(
                    "sgpa",
                    0
                )
            )
        ],

        [
            "CGPA",
            str(
                student_result.get(
                    "cgpa",
                    0
                )
            )
        ],

        [
            "Overall Result",
            str(
                student_result.get(
                    "result",
                    ""
                )
            )
        ]

    ]


    summary_table = Table(
        summary_data,
        colWidths=[
            60 * mm,
            70 * mm
        ]
    )


    summary_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, 4),
                (-1, 5),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 0),
                (1, -1),
                "CENTER"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])
    )


    story.append(
        summary_table
    )


    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "Generated by Resultra",
            center_style
        )
    )


    # --------------------------------
    # Build PDF
    # --------------------------------

    document.build(
        story
    )


    return output_path