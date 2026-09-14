from core.rule_engine import (
    apply_subject_rule,
    get_overall_result,
    DEFAULT_RULES
)


def calculate_student_result(
    student_data,
    rules=None
):
    """
    Calculate complete result of one student.

    Includes:
    - Marks
    - Grade
    - Grade Point
    - Credit
    - Credit Point
    - Total Marks
    - Percentage
    - SGPA
    - CGPA
    - Overall Result
    """

    if rules is None:
        rules = DEFAULT_RULES


    roll_no = student_data[
        "Roll No"
    ]


    student_name = student_data[
        "Student Name"
    ]


    subject_data = {}

    subject_statuses = []

    total_marks = 0

    total_credits = 0

    total_credit_points = 0

    subject_count = 0


    # Get subject credits
    subject_credits = rules.get(
        "subject_credits",
        {}
    )


    if subject_credits is None:
        subject_credits = {}


    # --------------------------------
    # Calculate Subject Results
    # --------------------------------

    for subject, marks in student_data.items():

        if subject in [
            "Roll No",
            "Student Name"
        ]:
            continue


        try:
            marks = float(marks)

        except (
            ValueError,
            TypeError
        ):
            continue


        # Apply grade rules
        result = apply_subject_rule(
            marks,
            rules
        )


        grade_point = result[
            "grade_point"
        ]


        # Get subject credit
        credit = subject_credits.get(
            subject,
            0
        )


        try:
            credit = float(credit)

        except (
            ValueError,
            TypeError
        ):
            credit = 0


        # Credit Point
        credit_point = (
            grade_point * credit
        )


        subject_data[subject] = {

            "marks": marks,

            "grade": result[
                "grade"
            ],

            "grade_point": grade_point,

            "credit": credit,

            "credit_point": credit_point,

            "status": result[
                "status"
            ]

        }


        subject_statuses.append(
            result["status"]
        )


        total_marks += marks

        total_credits += credit

        total_credit_points += (
            credit_point
        )

        subject_count += 1


    # --------------------------------
    # No Subjects
    # --------------------------------

    if subject_count == 0:

        return {

            "Roll No": roll_no,

            "Student Name": student_name,

            "subjects": {},

            "total": 0,

            "maximum_marks": 0,

            "percentage": 0,

            "total_credits": 0,

            "total_credit_points": 0,

            "sgpa": 0,

            "cgpa": 0,

            "result": "FAIL"

        }


    # --------------------------------
    # Maximum Marks
    # --------------------------------

    max_marks_per_subject = rules.get(
        "max_marks_per_subject",
        DEFAULT_RULES[
            "max_marks_per_subject"
        ]
    )


    maximum_marks = (
        subject_count
        * float(max_marks_per_subject)
    )


    # --------------------------------
    # Percentage
    # --------------------------------

    percentage = (
        total_marks
        / maximum_marks
    ) * 100


    # --------------------------------
    # SGPA
    # --------------------------------

    if total_credits > 0:

        sgpa = (
            total_credit_points
            / total_credits
        )

    else:

        sgpa = 0


    # --------------------------------
    # CGPA
    #
    # Current version:
    # No previous semester records.
    #
    # Therefore:
    # CGPA = SGPA
    #
    # This can be replaced in future
    # when semester history is added.
    # --------------------------------

    cgpa = sgpa


    # --------------------------------
    # Overall Result
    # --------------------------------

    overall_result = (
        get_overall_result(
            subject_statuses
        )
    )


    # --------------------------------
    # Final Result
    # --------------------------------

    return {

        "Roll No": roll_no,

        "Student Name": student_name,

        "subjects": subject_data,

        "total": round(
            total_marks,
            2
        ),

        "maximum_marks": round(
            maximum_marks,
            2
        ),

        "percentage": round(
            percentage,
            2
        ),

        "total_credits": round(
            total_credits,
            2
        ),

        "total_credit_points": round(
            total_credit_points,
            2
        ),

        "sgpa": round(
            sgpa,
            2
        ),

        "cgpa": round(
            cgpa,
            2
        ),

        "result": overall_result

    }