# ==================================================
# ExamHub
# Flask + Gemini + JSON
# PART 1
# ==================================================

from flask import Flask, render_template, request, jsonify
from openai import OpenAI

import os
import json

from dotenv import load_dotenv




# ----------------------------
# Load .env
# ----------------------------

load_dotenv()



# ----------------------------
# Groq API
# ----------------------------

client = OpenAI(

    api_key=os.getenv("GROQ_API_KEY"),

    base_url="https://api.groq.com/openai/v1"

)

# ----------------------------
# Flask
# ----------------------------

app = Flask(__name__)


# ----------------------------
# Subject List
# ----------------------------

SUBJECTS = {

    "sgp": "Switchgear & Protection",

    "cse": "Control System Engineering",

    "sgt": "Smart Grid Technology",

    "ppe": "Power Plant Engineering",

    "emd": "Electrical Machine Design"

}
# ==================================================
# PART 2
# JSON Loader + Routes
# ==================================================

# ----------------------------
# Load JSON File
# ----------------------------

def load_subject(code):

    file_path = os.path.join(

        "data",
        "json",
        f"{code}.json"

    )

    if not os.path.exists(file_path):

        return None

    with open(

        file_path,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)


# ----------------------------
# Home Page
# ----------------------------

@app.route("/")
def index():

    subjects = []

    for code, name in SUBJECTS.items():

        subjects.append({

            "code": code,

            "name": name

        })

    return render_template(

        "index.html",

        subjects=subjects

    )


# ----------------------------
# Subject Page
# ----------------------------

@app.route("/subject/<code>")
def subject(code):

    code = code.lower()

    if code not in SUBJECTS:

        return "Subject Not Found", 404

    data = load_subject(code)

    if data is None:

        return "JSON File Not Found", 404


    # ----------------------------
    # Sort Questions
    # ----------------------------

    important = []

    for unit in data["units"]:

        unit["questions"] = sorted(

            unit["questions"],

            key=lambda q: q["frequency"],

            reverse=True

        )

        for q in unit["questions"]:

            if q["frequency"] >= 2:

                important.append(q)


    important = sorted(

        important,

        key=lambda q: q["frequency"],

        reverse=True

    )


    return render_template(

        "subject.html",

        data=data,

        important=important,

        code=code

    )
# ==================================================
# PART 3
# Gemini AI API
# ==================================================

@app.route("/api/ask", methods=["POST"])
def ask_ai():

    body = request.get_json()

    question = body.get("question", "").strip()

    context = body.get("context", "Electrical Engineering")


    if question == "":

        return jsonify({

            "error": "Please enter a question."

        }), 400


    prompt = f"""
You are an expert Electrical Engineering professor helping diploma and engineering students.


Subject:
{context}

Student Question:
{question}

Answer ONLY the student's question.

Rules:

1. Write between 180 and 250 words.
2. Use simple and easy English.
3. Give an exam-oriented answer.
4. Start with a short definition if applicable.
5. Use clear headings whenever needed.
6. Use bullet points wherever possible.
7. If the question asks for working or operation, explain it in 5 to 7 numbered steps.
8. If the question asks for advantages, disadvantages or applications, give exactly 5 to 7 points.
9. If the question asks for comparison or difference, answer in comparison points.
10. If the question asks for construction, explain construction first and then working.
11. Never repeat the same information.
12. Keep paragraphs short (maximum 2 to 3 lines).
13. Do not use Markdown, tables, code blocks or emojis.
14. Do not add unnecessary introduction.
15. Add conclusion only if it improves understanding.
16. Understand common abbreviations such as:
    - adv = advantages
    - disadv = disadvantages
    - app = applications
    - def = definition
    - exp = explain
    - wkg = working
    - op = operation
    - char = characteristics
    - imp = importance
    - diff = difference
    - comp = compare
17. If the student's wording is informal but the meaning is clear, answer the intended question.
18. If the question is too short or ambiguous, reply only:
    "Your question is not clear. Please write the complete question."
19. If the question is outside Electrical Engineering, reply only:
    "Please ask an Electrical Engineering related question."
20. Make the answer look like a university exam answer written by an Electrical Engineering professor.0
"""


    try:

        response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.2,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

        answer = response.choices[0].message.content

        return jsonify({

        "answer": answer

    })

    except Exception as e:

        print("Groq Error:", repr(e))

        return jsonify({

        "error": "⚠ AI service is temporarily unavailable. Please try again later."

    }), 500
    # ==================================================
# PART 4
# Health Check + Error Pages + Run
# ==================================================

# ----------------------------
# Health Check
# ----------------------------

@app.route("/health")
def health():

    return jsonify({

        "status": "online",

        "project": "Electrical Exam Hub",

        "ai": "Groq",

        "subjects": len(SUBJECTS)

    })


# ----------------------------
# 404 Page
# ----------------------------

@app.errorhandler(404)
def page_not_found(error):

    return (

        "<h1>404</h1>"
        "<h3>Page Not Found</h3>"
        "<p>Please go back to the Home Page.</p>",

        404

    )


# ----------------------------
# 500 Page
# ----------------------------

@app.errorhandler(500)
def server_error(error):

    return (

        "<h1>500</h1>"
        "<h3>Internal Server Error</h3>"
        "<p>Please try again after some time.</p>",

        500

    )


# ----------------------------
# Run Application
# ----------------------------

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )