# =====================================================
# ExamHub Answer Regenerator
# Part 1 - Imports + API + Prompt + AI
# =====================================================

import os
import json
import time

from dotenv import load_dotenv
from openai import OpenAI

# =====================================================
# Load Environment
# =====================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("\n❌ GROQ_API_KEY not found in .env")
    exit()

# =====================================================
# Groq Client
# =====================================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"

# =====================================================
# Subject Names
# =====================================================

SUBJECTS = {
    "sgp": "Switchgear & Protection",
    "cse": "Control System Engineering",
    "sgt": "Smart Grid Technology",
    "ppe": "Power Plant Engineering",
    "emd": "Electrical Machine Design"
}

# =====================================================
# Prompt Builder
# =====================================================

def build_prompt(subject, question):

    return f"""
You are an expert Electrical Engineering professor.

Subject:
{subject}

Question:
{question}

Answer ONLY the student's question.

STRICT RULES

1. Use very simple English.
2. University exam style answer.
3. 180-280 words.
4. Never use Markdown.
5. Never generate diagrams.
6. Never repeat points.
7. Use proper headings whenever applicable.
8. Use bullet points.
9. If question asks Working, give numbered steps at least 6,7 steps.
10. If question asks Advantages, give exactly 5 points.
11. If question asks Disadvantages, give exactly 5 points.
12. If question asks Characteristics, give at least 7 point-wise answer.
13. If question asks Applications, give exactly 5 points.
14. If question asks Construction, write Construction heading.
15. If multiple parts are asked, answer every part at least 150 wordswith proper bullet point and then answer.
16. Return ONLY the answer.
"""

# =====================================================
# AI Generator
# =====================================================

def generate_answer(subject, question):

    for attempt in range(3):

        try:

            response = client.chat.completions.create(

                model=MODEL,

                temperature=0.1,

                messages=[
                    {
                        "role": "user",
                        "content": build_prompt(subject, question)
                    }
                ]
            )

            return response.choices[0].message.content.strip()

        except Exception as e:

            print(f"\n⚠ Attempt {attempt+1} Failed")

            if attempt < 2:
                print("Retrying in 3 seconds...\n")
                time.sleep(3)

    return None

# =====================================================
# Part 2 - Menu + JSON Loader + Utilities
# =====================================================

# =====================================================
# Main Menu
# =====================================================

def show_menu():

    print("\n===================================")
    print(" ExamHub Answer Regenerator")
    print("===================================")
    print("1. Regenerate One Answer")
    print("2. Regenerate Multiple Answers")
    print("3. Regenerate One Unit")
    print("4. Regenerate Whole Subject")
    print("5. Search Question")
    print("6. Exit")
    print("===================================")

    return input("Choose Option : ").strip()


# =====================================================
# Subject Selection
# =====================================================

def select_subject():

    print("\nAvailable Subjects\n")

    for code, name in SUBJECTS.items():

        print(f"{code.upper()} - {name}")

    while True:

        subject = input("\nSubject Code : ").lower().strip()

        if subject in SUBJECTS:

            return subject

        print("Invalid Subject.")


# =====================================================
# JSON Loader
# =====================================================

def load_json(subject):

    path = f"data/json/{subject}.json"

    if not os.path.exists(path):

        print("\nJSON File Not Found.")
        return None, None

    with open(path, "r", encoding="utf-8") as f:

        data = json.load(f)

    return data, path


# =====================================================
# Save JSON
# =====================================================

def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# Find Question By ID
# =====================================================

def find_question(data, question_id):

    for unit in data["units"]:

        for question in unit["questions"]:

            if question["id"] == question_id:

                return question

    return None


# =====================================================
# Search Question
# =====================================================

def search_questions(data, keyword):

    results = []

    keyword = keyword.lower()

    for unit in data["units"]:

        for question in unit["questions"]:

            if keyword in question["question"].lower():

                results.append(question)

    return results


# =====================================================
# Preview
# =====================================================

def preview(question):

    print("\n---------------------------------------")
    print("Question")
    print("---------------------------------------")

    print(question["question"])

    print("\n---------------------------------------")
    print("Current Answer")
    print("---------------------------------------")

    answer = question["answer"].strip()

    if answer == "":

        print("No Answer Available")

    else:

        if len(answer) > 600:

            print(answer[:600] + "...\n")

        else:

            print(answer)

    print("---------------------------------------")

    # =====================================================
# Part 3 - Regenerate One / Multiple Answers
# =====================================================

# =====================================================
# Regenerate One Answer
# =====================================================

def regenerate_one(data, path):

    question_id = input("\nQuestion ID : ").strip()

    question = find_question(data, question_id)

    if question is None:

        print("\n❌ Question ID not found.")
        return

    preview(question)

    choice = input("\nGenerate New Answer? (Y/N): ").lower()

    if choice != "y":

        print("\nCancelled.")
        return

    print("\nGenerating...\n")

    answer = generate_answer(

        data["name"],

        question["question"]

    )

    if answer is None:

        print("❌ Failed.")
        return

    question["answer"] = answer

    save_json(path, data)

    print("✅ Answer Updated Successfully")


# =====================================================
# Regenerate Multiple Answers
# =====================================================

def regenerate_multiple(data, path):

    ids = input(

        "\nEnter Question IDs (comma separated): "

    ).strip()

    ids = [

        x.strip()

        for x in ids.split(",")

        if x.strip()

    ]

    if len(ids) == 0:

        print("No IDs entered.")
        return

    total = len(ids)

    completed = 0

    for question_id in ids:

        question = find_question(

            data,

            question_id

        )

        if question is None:

            print(f"\n❌ {question_id} Not Found")

            continue

        completed += 1

        print("\n================================")

        print(f"[{completed}/{total}]")

        print(question["question"])

        print("Generating...")

        answer = generate_answer(

            data["name"],

            question["question"]

        )

        if answer is None:

            print("❌ Failed")

            continue

        question["answer"] = answer

        save_json(path, data)

        print("✅ Saved")

    print("\n================================")
    print("Finished")
    print("================================")

    # =====================================================
# Part 4 - Regenerate Unit / Whole Subject
# =====================================================

# =====================================================
# Regenerate One Unit
# =====================================================

def regenerate_unit(data, path):

    try:

        unit_no = int(input("\nUnit Number : "))

    except:

        print("Invalid Unit.")
        return

    if unit_no < 1 or unit_no > len(data["units"]):

        print("Unit Not Found.")
        return

    unit = data["units"][unit_no - 1]

    print("\n================================")
    print(unit["title"])
    print(f"Questions : {len(unit['questions'])}")
    print("================================")

    c = input("\nRegenerate ALL answers of this unit? (Y/N): ").lower()

    if c != "y":

        print("Cancelled.")
        return

    total = len(unit["questions"])

    for i, question in enumerate(unit["questions"], start=1):

        print("\n--------------------------------")
        print(f"[{i}/{total}]")
        print(question["question"])
        print("--------------------------------")

        answer = generate_answer(

            data["name"],

            question["question"]

        )

        if answer is None:

            print("❌ Failed")
            continue

        question["answer"] = answer

        save_json(path, data)

        print("✅ Saved")

    print("\n================================")
    print("✅ Unit Regenerated Successfully")
    print("================================")


# =====================================================
# Regenerate Whole Subject
# =====================================================

def regenerate_subject(data, path):

    total = 0

    for unit in data["units"]:

        total += len(unit["questions"])

    print("\n================================")
    print("WARNING")
    print("================================")
    print(f"Subject : {data['name']}")
    print(f"Questions : {total}")
    print("All existing answers will be replaced.")
    print("================================")

    c = input("\nType YES to continue : ")

    if c != "YES":

        print("Cancelled.")
        return

    current = 0

    for unit in data["units"]:

        print(f"\n===== {unit['title']} =====")

        for question in unit["questions"]:

            current += 1

            print(f"\n[{current}/{total}]")

            print(question["question"])

            answer = generate_answer(

                data["name"],

                question["question"]

            )

            if answer is None:

                print("❌ Failed")
                continue

            question["answer"] = answer

            save_json(path, data)

            print("✅ Saved")

    print("\n================================")
    print("🎉 Subject Regenerated Successfully")
    print("================================")
    # =====================================================
# Part 5 - Search + Main Menu
# =====================================================

# =====================================================
# Search Question
# =====================================================

def search_question(data, path):

    keyword = input("\nEnter Keyword : ").strip()

    results = search_questions(data, keyword)

    if len(results) == 0:

        print("\nNo Questions Found.")
        return

    print("\n================================")

    for i, q in enumerate(results, start=1):

        print(f"{i}. {q['id']}")
        print(q["question"])
        print()

    print("================================")

    try:

        choice = int(input("Select Number (0 Cancel): "))

    except:

        return

    if choice == 0:

        return

    if choice < 1 or choice > len(results):

        print("Invalid Selection")
        return

    question = results[choice - 1]

    preview(question)

    c = input("\nGenerate New Answer? (Y/N): ").lower()

    if c != "y":

        return

    print("\nGenerating...\n")

    answer = generate_answer(

        data["name"],

        question["question"]

    )

    if answer is None:

        print("❌ Failed")
        return

    question["answer"] = answer

    save_json(path, data)

    print("\n✅ Updated Successfully")


# =====================================================
# Main Program
# =====================================================

def main():

    while True:

        option = show_menu()

        if option == "6":

            print("\nGood Bye.")
            break

        subject = select_subject()

        data, path = load_json(subject)

        if data is None:

            continue

        if option == "1":

            regenerate_one(data, path)

        elif option == "2":

            regenerate_multiple(data, path)

        elif option == "3":

            regenerate_unit(data, path)

        elif option == "4":

            regenerate_subject(data, path)

        elif option == "5":

            search_question(data, path)

        else:

            print("Invalid Option")


# =====================================================
# Start Program
# =====================================================

if __name__ == "__main__":

    main()
    # =====================================================
# Part 6 - Final Improvements
# =====================================================

SUCCESS = 0
FAILED = 0


# =====================================================
# Update Counters
# =====================================================

def mark_success():

    global SUCCESS

    SUCCESS += 1


def mark_failed():

    global FAILED

    FAILED += 1


# =====================================================
# Final Summary
# =====================================================

def show_summary():

    print("\n======================================")
    print(" ExamHub Regeneration Summary")
    print("======================================")
    print(f"Successful : {SUCCESS}")
    print(f"Failed     : {FAILED}")
    print("======================================")


# =====================================================
# Replace print("✅ Saved")
# with these 2 lines everywhere
# =====================================================

# mark_success()
# print("✅ Saved Successfully")


# =====================================================
# Replace every
#
# print("❌ Failed")
#
# with
#
# mark_failed()
# print("❌ Failed")
# =====================================================


# =====================================================
# Show summary before program exits
# =====================================================

# In main(), replace:

# if option == "6":
#
#     print("\nGood Bye.")
#     break

# with:

# if option == "6":
#
#     show_summary()
#
#     print("\nThank you for using ExamHub AI.")
#
#     break


# =====================================================
# Unexpected Error Protection
# =====================================================

try:

    if __name__ == "__main__":

        main()

except KeyboardInterrupt:

    print("\n\nStopped By User.")

    show_summary()

except Exception as e:

    print("\nUnexpected Error")

    print(e)

    show_summary()