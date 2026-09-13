# RESULTRA

### Configurable Excel-Based Student Result PDF Generator

Resultra is a web-based student result generation system that converts student marks stored in Excel files into customized result PDFs.

The system reads student data, validates the uploaded Excel file, applies configurable result rules, calculates results, applies a reusable result template, provides a preview, and generates downloadable PDF result sheets.

---

## 1. Project Overview

Preparing student result sheets manually from Excel data can be time-consuming and may lead to calculation, formatting, and data-entry errors.

**Resultra** automates this process by providing a centralized web interface where users can:

* Upload student marks through Excel.
* Automatically detect supported Excel formats.
* Validate student and marks data.
* Apply configurable result rules.
* Calculate totals, percentages, grades, and result status.
* Use reusable customized result profiles.
* Customize result PDF layouts.
* Preview results before generating PDFs.
* Generate a PDF for an individual student.
* Generate PDFs for multiple students.
* Download generated results.

---

## 2. Main Workflow

```text
Open Resultra
      ↓
Upload Excel
      ↓
Detect Excel Format
      ↓
Read Excel Data
      ↓
Validate Data
      ↓
Select Saved Profile
      ↓
Configure Changeable Fields
      ↓
Apply Result Rules
      ↓
Calculate Result
      ↓
Apply PDF Template
      ↓
Preview Result
      ↓
Generate PDF / PDFs
      ↓
Download
```

---

## 3. Supported Excel Formats

Resultra supports two main Excel formats.

### Format 1: All Subjects in One Sheet

Example:

| Roll No | Student Name | DS | DBMS | Python | Maths | SE |
| ------- | ------------ | -: | ---: | -----: | ----: | -: |
| 101     | Student 1    | 72 |   65 |     81 |    75 | 69 |
| 102     | Student 2    | 61 |   70 |     76 |    68 | 73 |

The system automatically identifies the subjects from the Excel columns.

---

### Format 2: Separate Sheet for Each Subject

Example:

```text
Marklist.xlsx
│
├── DS
├── DBMS
├── Python
├── Maths
└── SE
```

Each sheet can contain:

| Roll No | Student Name | Marks |
| ------- | ------------ | ----: |
| 101     | Student 1    |    72 |
| 102     | Student 2    |    61 |

Students are matched using a unique identifier such as **Roll No/PRN**, rather than relying only on student names.

---

## 4. Result Calculation

Resultra can apply configurable rules such as:

* Maximum marks
* Passing marks
* Total marks
* Percentage
* Grade
* Pass/Fail status
* Subject-wise passing
* Overall passing
* Grade ranges

Example:

```text
Total Marks = Sum of Subject Marks

Percentage = (Total Marks / Maximum Total Marks) × 100
```

Grade ranges can be configured through the result-rule system rather than being permanently hardcoded.

---

## 5. Reusable Result Profiles

One of the main features of Resultra is the **customizable result profile**.

A profile can contain:

```text
Profile
│
├── PDF Layout
├── Header Design
├── Footer Design
├── Logo
├── Table Design
├── Page Size
├── Orientation
├── Result Rules
├── Grade Rules
└── Changeable Fields
```

Example:

```text
B.Sc CS Result Profile
```

The same profile can be reused for:

```text
FY → Semester I
FY → Semester II
SY → Semester III
SY → Semester IV
TY → Semester V
TY → Semester VI
```

### Profile does NOT permanently store:

* Student names
* Roll numbers
* PRN
* Student marks
* Subject names

These details are obtained from the currently uploaded Excel file.

---

## 6. Customizable Fields

The user can change selected fields when generating a result, such as:

* Department
* Course
* Class
* Semester
* Academic Year
* Examination

For example:

```text
Department : Computer Science
Course     : B.Sc Computer Science
Class      : TY
Semester   : VI
Academic Year : 2026-27
```

---

## 7. PDF Customization

Resultra is designed to support customized result PDF layouts.

Possible customization options include:

* College/institution name
* College logo
* Department
* Course
* Class
* Semester
* Academic year
* Examination name
* Student information
* Subject table
* Total marks
* Percentage
* Grade
* Result status
* Header
* Footer
* Borders
* Page size
* Portrait/Landscape orientation
* Selected result fields

---

## 8. Preview

Before generating the final PDF, Resultra provides a **preview** of the result.

```text
Excel Data
    ↓
Calculation
    ↓
Template
    ↓
Preview
    ↓
Generate PDF
```

This allows the user to verify the result layout and calculated information before downloading the final PDF.

---

## 9. PDF Generation

Resultra can generate:

### Individual Result

```text
Student_101_Result.pdf
```

### Multiple Results

```text
Results/
├── Student_101_Result.pdf
├── Student_102_Result.pdf
├── Student_103_Result.pdf
└── ...
```

A future version may also provide ZIP download for multiple generated PDFs.

---

## 10. Technology Stack

### Backend

* Python
* Flask

### Excel Processing

* Pandas
* OpenPyXL

### PDF Generation

* ReportLab

### Frontend

* HTML
* CSS
* JavaScript

### Storage

The initial version does not require a traditional database.

Reusable profiles can be stored locally using browser storage and/or local project files depending on the implementation.

### Version Control

* Git
* GitHub

---

## 11. Project Structure

```text
Resultra/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── excel_reader.py
│   ├── excel_validator.py
│   ├── result_calculator.py
│   ├── rule_engine.py
│   ├── profile_manager.py
│   └── pdf_generator.py
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── rules.html
│   ├── template.html
│   ├── profiles.html
│   ├── preview.html
│   └── result.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── default_logo.png
│
└── data/
    ├── uploads/
    ├── profiles/
    └── generated/
```

---

## 12. Core Modules

### `excel_reader.py`

Responsible for:

* Reading Excel files
* Detecting supported Excel structure
* Reading single-sheet format
* Reading subject-wise sheets
* Converting input data into a common internal format

### `excel_validator.py`

Responsible for:

* Checking required columns
* Checking missing values
* Checking duplicate Roll No/PRN
* Checking invalid marks
* Checking inconsistent subject data

### `rule_engine.py`

Responsible for:

* Applying passing rules
* Applying grading rules
* Applying configurable result conditions

### `result_calculator.py`

Responsible for:

* Subject totals
* Overall total
* Percentage
* Grade
* Pass/Fail result

### `profile_manager.py`

Responsible for:

* Creating profiles
* Saving profiles
* Loading profiles
* Updating profiles
* Reusing profiles

### `pdf_generator.py`

Responsible for:

* Applying the selected template
* Creating result PDFs
* Formatting student information
* Formatting subject tables
* Generating individual/multiple PDFs

### `app.py`

Responsible for:

* Flask application
* Web routes
* File upload
* Connecting frontend with core modules
* Preview
* PDF generation/download

---

## 13. Current Scope

The current Resultra version focuses on:

* Excel-based marks input
* Two Excel formats
* Automatic data processing
* Configurable result calculation
* Reusable profiles
* Customized PDF layout
* Result preview
* PDF generation
* PDF download
* Git-based development

### Not included in the current version

* User login
* Online marks entry
* Cloud database
* Multi-college management
* Teacher accounts
* Online student access

These can be considered future enhancements.

---

## 14. Future Enhancements

Possible future features include:

* User login and authentication
* Teacher-specific profiles
* Database integration
* Cloud storage
* Online marks entry
* College-specific configurations
* Subject-wise teacher uploads
* Automatic subject combination
* Student result portal
* Result history
* ZIP download
* Result analytics
* Rank generation
* Email result delivery
* Deployment on a cloud server

---

## 15. Installation

### Clone the repository

```bash
git clone <repository-url>
```

### Open the project

```bash
cd Resultra
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Then open the local Flask address shown in the terminal.

---

## 16. Git Workflow

The project uses Git for version control.

Example:

```bash
git status
git add .
git commit -m "Add Excel reader"
git push
```

Suggested commit style:

```text
Initial project structure
Add Excel reader
Add Excel validation
Add result calculation
Add grading rules
Add profile management
Add PDF generator
Add Flask interface
Add result preview
Improve PDF template
Fix Excel validation
Final testing
```

---

## 17. Development Principle

Resultra is designed using a **modular architecture**.

The Excel processing, validation, result calculation, rule engine, profile management, and PDF generation are kept separate from the Flask web interface.

This makes the system:

* Easier to develop
* Easier to test
* Easier to maintain
* Easier to modify
* Easier to extend with future features

---

## 18. Project Objective

The main objective of Resultra is to provide a simple and configurable system that reduces the manual effort required to convert student marks from Excel into professionally formatted result PDFs.

---

## 19. Project Name

**Resultra**

### Tagline

**Smart Results. Simple Generation.**

---

## 20. License

This project is developed as an academic project.
#   R e s u l t r a  
 