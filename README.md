# Smart University Management System

A Python, console-based **Smart University Management System** for managing:

- Students
- Faculty
- Courses
- Course registrations
- Attendance
- Results (marks, grades, CGPA)
- Fees (payments & balances)
- Library (books, issue/return, search)
- Reports (in-memory + CSV export)
- Data persistence (save/load as JSON)

---

## Project Structure

- `main.py` — CLI menu + user interaction
- `university.py` — core application state & operations
- `student.py` — `Student` model
- `faculty.py` — `Faculty` model
- `course.py` — `Course` model
- `attendance.py` — `Attendance` record
- `result.py` — `Result` record (grades & CGPA)
- `fee.py` — `Fee` tracking (paid vs balance)
- `library.py` — `Library` operations
- `person.py` — `Person` abstract base class
- `utils.py` — helper utilities (logging decorator, generator, etc.)
- `data/university.json` — saved persistence file
- `data/csv_reports/*` — exported CSV reports

---

## Architecture Diagram

```text
                         ┌──────────────────────┐
                         │      User (CLI)      │
                         └──────────┬───────────┘
                                    │ menu option
                                    v
                         ┌──────────────────────┐
                         │        main.py       │
                         └──────────┬───────────┘
                                    │ calls
                                    v
                         ┌──────────────────────┐
                         │     University       │
                         │    (university.py)   │
                         └───┬─────┬─────┬──────┘
                             │     │     │
                             v     v     v
                    ┌────────────┐ ┌────────────┐ ┌────────────┐
                    │   Students │ │   Faculty  │ │   Courses  │
                    │  (student) │ │  (faculty  │ │  (course)  │
                    └────────────┘ └────────────┘ └────────────┘

                             ┌───────────────────────┐
                             │  Records/Operations   │
                             └──────────┬────────────┘
                                        │
      ┌─────────────────────────────────┼──────────────────────────────┐
      v                                 v                               v
┌───────────────┐           ┌────────────────┐              ┌──────────────────┐
│ Attendance    │           │ Results        │              │ Fees & Library   │
│(attendance.py)│           │ (result.py)    │              │ (fee.py,         │
└───────────────┘           └────────────────┘              │ library.py)      │
                                                            └──────────────────┘

Persistence & export:
- University.save_data() -> data/university.json
- University.export_csv_reports() -> data/csv_reports/*.csv
```


---

## How to Run

### Requirements

- Python 3.x

### Steps

1. Open a terminal in this folder.
2. Run:

```bash
python3 main.py
```

3. Use the on-screen menu to manage university data.

---

## Main Menu Options

1. Add Student
2. Add Faculty
3. Create Course
4. Register Student in Course
5. Assign Faculty to Course
6. Attendance Menu
7. Result Menu
8. Pay Fee
9. Library Menu
10. Generate Report
11. Export CSV Reports
12. Save Data (writes to `data/university.json`)
13. Load Data (reads from `data/university.json`)
14. Exit

---

## Notes

- **Attendance** is stored per `(student_id, course_id)` key.
- **Results** store marks per subject, compute grades and CGPA.
- **Fees** track `paid_fee` and `balance_fee`.
- **Library** keeps a list of available books and a per-student issued list.

---

## CSV Output

When you select **Export CSV Reports**, CSV files are written to:

- `data/csv_reports/students.csv`
- `data/csv_reports/faculty.csv`
- `data/csv_reports/courses.csv`
- `data/csv_reports/fees.csv`
- `data/csv_reports/attendance.csv`
- `data/csv_reports/results.csv`
