DEFAULT_RULES = {
    "passing_marks": 40,

    "grade_ranges": [
        {"min": 90, "grade": "A+"},
        {"min": 80, "grade": "A"},
        {"min": 70, "grade": "B+"},
        {"min": 60, "grade": "B"},
        {"min": 50, "grade": "C"},
        {"min": 40, "grade": "D"},
        {"min": 0, "grade": "F"}
    ]
}


def is_subject_pass(marks, passing_marks):
    """
    Check whether a subject is passed.
    """

    return marks >= passing_marks


def get_grade(marks, grade_ranges):
    """
    Calculate grade based on marks.
    """

    for rule in grade_ranges:

        if marks >= rule["min"]:
            return rule["grade"]

    return "F"


def get_overall_result(subject_results):
    """
    Calculate overall result.

    If any subject is failed,
    overall result is FAIL.
    """

    for result in subject_results:

        if result == "FAIL":
            return "FAIL"

    return "PASS"


def apply_subject_rule(marks, rules=None):
    """
    Apply pass/fail and grade rules to a subject.
    """

    if rules is None:
        rules = DEFAULT_RULES

    passing_marks = rules["passing_marks"]
    grade_ranges = rules["grade_ranges"]

    if is_subject_pass(marks, passing_marks):
        status = "PASS"
    else:
        status = "FAIL"

    grade = get_grade(marks, grade_ranges)

    return {
        "marks": marks,
        "grade": grade,
        "status": status
    }