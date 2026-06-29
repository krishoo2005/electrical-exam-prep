import json
import os

# ==========================
# Configuration
# ==========================

SUBJECTS = {
    "sgp": "Switchgear & Protection",
    "cse": "Control System Engineering",
    "sgt": "Smart Grid Technology",
    "ppe": "Power Plant Engineering",
    "emd": "Electrical Machine Design"
}

TOTAL_UNITS = 5
QUESTIONS_PER_UNIT = 8

# ==========================
# Create data folder
# ==========================

os.makedirs("data", exist_ok=True)

# ==========================
# Generate JSON files
# ==========================

for code, name in SUBJECTS.items():

    subject = {
        "code": code.upper(),
        "name": name,
        "description": "Previous Year Exam Questions",
        "units": []
    }

    for unit in range(1, TOTAL_UNITS + 1):

        unit_data = {
            "title": f"Unit {unit}",
            "questions": []
        }

        for q in range(1, QUESTIONS_PER_UNIT + 1):

            unit_data["questions"].append({

                "id": f"{code}_{unit}_{q}",

                "question": "",

                "frequency": 0,

                "exams": [],

                "answer": ""

            })

        subject["units"].append(unit_data)

    filename = f"data/{code}.json"

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(subject, f, indent=4)

print("\n====================================")
print(" ExamHub JSON Files Generated")
print("====================================")
print("Subjects :", len(SUBJECTS))
print("Units    :", TOTAL_UNITS)
print("Questions:", QUESTIONS_PER_UNIT, "per unit")
print("Total Slots:", len(SUBJECTS) * TOTAL_UNITS * QUESTIONS_PER_UNIT)
print("====================================")