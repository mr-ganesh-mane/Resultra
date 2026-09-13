from core.rule_engine import apply_subject_rule, get_overall_result


def calculate_student_result(student_data, rules=None):
    """
    Calculate the complete result of one student.

    student_data should contain:
    Roll No
    Student Name
    Subject marks
    """

    if rules is None:
        from core.rule_engine import DEFAULT_RULES
        rules = DEFAULT_RULES

    roll_no = student_data["Roll No"]
    student_name = student_data["Student Name"]

    subject_results = {}
    subject_statuses = []

    total_marks = 0
    subject_count = 0

    for subject, marks in student_data.items():

        if subject in ["Roll No", "Student Name"]:
            continue

        marks = float(marks)

        result = apply_subject_rule(marks, rules)

        subject_results[subject] = result
        subject_statuses.append(result["status"])

        total_marks += marks
        subject_count += 1

    if subject_count == 0:
        return {
            "Roll No": roll_no,
            "Student Name": student_name,
            "subjects": {},
            "total": 0,
            "percentage": 0,
            "result": "FAIL"
        }

    max_marks = rules.get("max_marks_per_subject", 100)
    maximum_marks = subject_count * max_marks

    percentage = (total_marks / maximum_marks) * 100

    overall_result = get_overall_result(subject_statuses)

    return {
        "Roll No": roll_no,
        "Student Name": student_name,
        "subjects": subject_results,
        "total": total_marks,
        "maximum_marks": maximum_marks,
        "percentage": round(percentage, 2),
        "result": overall_result
    }