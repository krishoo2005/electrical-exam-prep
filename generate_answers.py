import os
import json
import time

from dotenv import load_dotenv
from openai import OpenAI

# ==========================================
# Load Environment
# ==========================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("❌ GROQ_API_KEY not found in .env")
    exit()

# ==========================================
# Groq Client
# ==========================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"

# ==========================================
# Subjects
# ==========================================

SUBJECTS = {
    "1": ("sgp", "Switchgear & Protection"),
    "2": ("cse", "Control System Engineering"),
    "3": ("sgt", "Smart Grid Technology"),
    "4": ("ppe", "Power Plant Engineering"),
    "5": ("emd", "Electrical Machine Design")
}

print("\n==============================")
print(" ExamHub AI Answer Generator")
print("==============================")
print("1. Switchgear & Protection")
print("2. Control System Engineering")
print("3. Smart Grid Technology")
print("4. Power Plant Engineering")
print("5. Electrical Machine Design")
print("6. All Subjects")
print("==============================")

choice = input("Enter Choice : ").strip()

json_files = []

if choice == "6":

    for code, name in SUBJECTS.values():

        path = os.path.join("data", "json", f"{code}.json")

        if os.path.exists(path):
            json_files.append(path)

elif choice in SUBJECTS:

    code, name = SUBJECTS[choice]

    path = os.path.join("data", "json", f"{code}.json")

    if os.path.exists(path):
        json_files.append(path)

    else:

        print("❌ JSON File Not Found")
        exit()

else:

    print("❌ Invalid Choice")
    exit()

print("\nSelected Files:")

for file in json_files:
    print("✔", file)

print()

# ==========================================
# Prompt Builder
# ==========================================

def build_prompt(subject, question):

    return f"""


Answer ONLY the question.

You are an experienced Electrical Engineering professor and university paper setter.

Subject:
{subject}

Question:
{question}

Generate ONLY the answer.

Rules:

1. Use simple English suitable for Diploma and B.E. students.
2. Write between 220 and 400 words.
3. Follow the question exactly. Never add unrelated information.
4. Do not write long paragraphs.
5. Use proper headings whenever applicable.
6. Use bullet points wherever possible.
7. Never repeat the same point.
8. Never generate diagrams or images.
9. Do not use Markdown, tables or code blocks.
10. Return only the answer.

Answer Structure Rules:

• If the question starts with "What is" or "Define"
  - Definition
  - Explanation
  - Key Points (if applicable)

• If the question starts with "Explain"
  - Definition
  - Construction (if applicable)
  - Working / Operation (step by step)
  - Advantages
  - Disadvantages
  - Applications
  - Conclusion only if useful

• If the question asks "Construction and Working"
  - Definition
  - Construction
  - Working (numbered steps)
  - Advantages
  - Applications

• If the question asks "Working"
  - Principle
  - Working (5-8 numbered steps)
  - Advantages
  - Applications

• If the question asks "Advantages"
  - Short Definition
  - Exactly 6-8 advantages

• If the question asks "Disadvantages"
  - Short Definition
  - Exactly 6-8 disadvantages

• If the question asks "Applications"
  - Short Definition
  - Exactly 6-8 applications

• If the question asks "Compare" or "Differentiate"
  - Return comparison points only.

• If the question asks "Need", "Importance", "Purpose" or "Why"
  - Short Definition
  - Reasons (6-8 points)
  - Benefits

Electrical Engineering Rules:

- Explain electrical terms correctly.
- Use standard engineering terminology.
- Mention important formulas only if required.
- Mention ratings or standards only if relevant.
- Never invent facts.
- Never use filler sentences.

The answer should look like it is written by an experienced Electrical Engineering professor for university examination.
"""


# ==========================================
# Generate Answer
# ==========================================

def generate_answer(subject, question):

    prompt = build_prompt(subject, question)

    try:

        response = client.chat.completions.create(

            model=MODEL,

            temperature=0.2,

            max_tokens=900,

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Electrical Engineering professor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        answer = response.choices[0].message.content.strip()

        return answer

    except Exception as e:

        print("\n❌ AI Error")
        print(e)

        return None
    
    # ==========================================
# Process JSON Files
# ==========================================

for json_file in json_files:

    print("\n" + "=" * 50)
    print("Processing :", json_file)
    print("=" * 50)

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    subject_name = data["name"]

    total = 0
    completed = 0

    # Count pending questions
    for unit in data["units"]:
        for q in unit["questions"]:

            if (
                q["question"].strip() != ""
                and q["answer"].strip() == ""
            ):
                total += 1

    print(f"\nPending Answers : {total}\n")

    if total == 0:

        print("✅ Nothing to generate.")
        continue

    # Generate Answers
    for unit in data["units"]:

        print(f"\n📘 {unit['title']}")

        for q in unit["questions"]:

            question = q["question"].strip()
            answer = q["answer"].strip()

            # Skip blank question
            if question == "":
                continue

            # Skip already generated answer
            if answer != "":
                continue

            completed += 1

            print(f"\n[{completed}/{total}] {question}")

            ai_answer = generate_answer(subject_name, question)

            if ai_answer:

                q["answer"] = ai_answer

                # Save immediately
                with open(json_file, "w", encoding="utf-8") as file:

                    json.dump(
                        data,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )

                print("✅ Saved Successfully")

                # Prevent rate limit
                time.sleep(2)

            else:

                print("❌ Failed")
                print("Retrying after 5 seconds...\n")

                time.sleep(5)

                ai_answer = generate_answer(subject_name, question)

                if ai_answer:

                    q["answer"] = ai_answer

                    with open(json_file, "w", encoding="utf-8") as file:

                        json.dump(
                            data,
                            file,
                            indent=4,
                            ensure_ascii=False
                        )

                    print("✅ Saved Successfully")

                else:

                    print("❌ Skipped")

print("\n")
print("=" * 50)
print("🎉 All Done!")
print("=" * 50)

# ==========================================
# Clean AI Answer
# ==========================================

def clean_answer(answer):

    if not answer:
        return ""

    # Remove unwanted markdown
    answer = answer.replace("**", "")
    answer = answer.replace("###", "")
    answer = answer.replace("##", "")
    answer = answer.replace("#", "")

    # Remove code blocks
    answer = answer.replace("```", "")

    # Remove AI phrases
    remove_lines = [
        "Here is the answer",
        "Here's the answer",
        "Sure!",
        "Certainly!",
        "Of course!",
        "I hope this helps.",
        "Let me know if",
        "As an AI",
        "In conclusion",
        "Conclusion:",
        "Summary:",
        "Overall,"
    ]

    lines = []

    for line in answer.split("\n"):

        skip = False

        for word in remove_lines:

            if word.lower() in line.lower():
                skip = True
                break

        if not skip:
            lines.append(line.strip())

    answer = "\n".join(lines)

    # Remove extra blank lines
    while "\n\n\n" in answer:
        answer = answer.replace("\n\n\n", "\n\n")

    return answer.strip()


# ==========================================
# Replace this line in Part 3
#
# q["answer"] = ai_answer
#
# with
#
# q["answer"] = clean_answer(ai_answer)
#
# Do this in BOTH places.
# ==========================================


print("\n===================================")
print(" ExamHub AI Generator Completed")
print("===================================")
print("✔ Existing answers preserved")
print("✔ Blank answers generated")
print("✔ JSON updated automatically")
print("===================================")