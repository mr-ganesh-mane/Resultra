DEFAULT_RULES = {
    "passing_marks": 40,
    "max_marks_per_subject": 100,

    "grade_ranges": [
        {
            "min": 90,
            "grade": "A+",
            "grade_point": 10
        },
        {
            "min": 80,
            "grade": "A",
            "grade_point": 9
        },
        {
            "min": 70,
            "grade": "B+",
            "grade_point": 8
        },
        {
            "min": 60,
            "grade": "B",
            "grade_point": 7
        },
        {
            "min": 50,
            "grade": "C",
            "grade_point": 6
        },
        {
            "min": 40,
            "grade": "D",
            "grade_point": 5
        },
        {
            "min": 0,
            "grade": "F",
            "grade_point": 0
        }
    ],

    "subject_credits": {}
}


def is_subject_pass(
    marks,
    passing_marks
):

    return marks >= passing_marks


def get_grade(
    marks,
    grade_ranges
):

    if not grade_ranges:

        grade_ranges = DEFAULT_RULES[
            "grade_ranges"
        ]


    sorted_ranges = sorted(
        grade_ranges,
        key=lambda item: float(
            item["min"]
        ),
        reverse=True
    )


    for rule in sorted_ranges:

        if marks >= float(
            rule["min"]
        ):

            return rule["grade"]


    return "F"


def get_grade_rule(
    marks,
    grade_ranges
):

    if not grade_ranges:

        grade_ranges = DEFAULT_RULES[
            "grade_ranges"
        ]


    sorted_ranges = sorted(
        grade_ranges,
        key=lambda item: float(
            item["min"]
        ),
        reverse=True
    )


    for rule in sorted_ranges:

        if marks >= float(
            rule["min"]
        ):

            return rule


    return {
        "min": 0,
        "grade": "F",
        "grade_point": 0
    }


def get_grade_point(
    marks,
    grade_ranges
):

    rule = get_grade_rule(
        marks,
        grade_ranges
    )


    try:

        return float(
            rule.get(
                "grade_point",
                0
            )
        )

    except (
        ValueError,
        TypeError
    ):

        return 0


def get_overall_result(
    subject_results
):

    for result in subject_results:

        if result == "FAIL":

            return "FAIL"


    return "PASS"


def apply_subject_rule(
    marks,
    rules=None
):

    if rules is None:

        rules = DEFAULT_RULES


    passing_marks = rules.get(
        "passing_marks",
        DEFAULT_RULES[
            "passing_marks"
        ]
    )


    grade_ranges = rules.get(
        "grade_ranges",
        DEFAULT_RULES[
            "grade_ranges"
        ]
    )


    # If grade ranges are empty
    # use default grade rules
    if not grade_ranges:

        grade_ranges = DEFAULT_RULES[
            "grade_ranges"
        ]


    if is_subject_pass(
        marks,
        passing_marks
    ):

        status = "PASS"

    else:

        status = "FAIL"


    grade = get_grade(
        marks,
        grade_ranges
    )


    grade_point = get_grade_point(
        marks,
        grade_ranges
    )


    return {

        "marks": marks,

        "grade": grade,

        "grade_point": grade_point,

        "status": status

    }