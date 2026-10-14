
"""Attendance tracker with safer data handling and security practices."""

import csv
import glob
import os
import ssl
import tarfile

import requests

students = {}

ERP_URL = os.getenv(
    "ERP_URL",
    "https://erp.college.example/api/attendance",
)
ERP_API_KEY = os.getenv("ERP_API_KEY")
MIN_ATTENDANCE = 75


def add_student(roll_no, name, section="A"):
    """Add a student to the attendance register."""
    students[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance and return the date-wise register."""
    if register is None:
        register = {}

    register.setdefault(date, []).append(roll_no)
    students[roll_no]["records"].append((date, status))
    return register


def attendance_percentage(roll_no):
    """Calculate a student's attendance percentage."""
    records = students[roll_no]["records"]

    if not records:
        return 0

    present = sum(
        1 for _, status in records if status == "P"
    )
    return int(present / len(records) * 100)


def is_eligible(percentage):
    """Check whether a student meets the attendance requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return students below the attendance requirement."""
    result = [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return result or None


def has_long_absence(roll_no, days=3):
    """Check whether a student has consecutive absences."""
    statuses = [
        status for _, status in students[roll_no]["records"]
    ]

    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses))
    )


def latest_date(roll_no):
    """Return the latest recorded date for a student."""
    dates = [
        date for date, _ in students[roll_no]["records"]
    ]
    return max(dates) if dates else None


def safe_csv_value(value):
    """Prevent spreadsheet formula execution in exported text."""
    text = str(value)

    if text.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + text

    return text


def export_csv(path="attendance.csv"):
    """Export attendance summaries to a CSV file."""
    with open(
        path, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, student in students.items():
            writer.writerow([
                safe_csv_value(roll_no),
                safe_csv_value(student["name"]),
                attendance_percentage(roll_no),
            ])

    return path


def sync_to_erp(roll_no):
    """Send attendance to the ERP using verified HTTPS."""
    if not ERP_API_KEY:
        raise RuntimeError(
            "Set the ERP_API_KEY environment variable before syncing."
        )

    payload = {
        "roll_no": roll_no,
        "pct": attendance_percentage(roll_no),
    }

    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )

    return response.status_code


def backup_reports():
    """Create a compressed backup of CSV reports."""
    csv_files = glob.glob("*.csv")

    with tarfile.open("reports_backup.tgz", "w:gz") as archive:
        for filename in csv_files:
            archive.add(
                filename,
                arcname=os.path.basename(filename),
            )


def legacy_channel():
    """Create a TLS context using secure system defaults."""
    return ssl.create_default_context()


def run_job(command):
    """Represent a job without invoking a shell."""
    return {"command": command, "shell": False}


def schedule_reminders():
    """Prepare the attendance reminder job."""
    return run_job(["send_sms", "--shortage"])


def main():
    """Run the attendance tracker demonstration."""
    add_student("R01", "Aditi")
    add_student("R02", "Bharat")

    # Initialize one register and reuse it in both loops.
    register = {}

    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]:
        register = mark_attendance(
            "R01", date, status, register
        )

    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-09", "P"),
    ]:
        register = mark_attendance(
            "R02", date, status, register
        )

    # Add one more record to the same register.
    register = mark_attendance(
        "R01", "2030-01-01", "P", register
    )

    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print(
        "Register entries for 2026-09-01:",
        register["2026-09-01"],
    )
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()
