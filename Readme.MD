# ExamHub — 7th Sem Electrical Engineering

A clean, fast exam prep website for electrical engineering students. No login. No ads. Fully free.

## Features
- 5 subjects: SGP, CSE, SGT, PPE, EMD
- Questions sorted by exam frequency (most repeated on top)
- ⭐ Important section = questions that appeared 2+ times
- Copy answer button
- AI-powered Q&A (Ask AI anything)
- Works on mobile

---

## How to Add Questions & Answers

### For SGP (already has questions):
Open `data/sgp.py`. Find the question, paste your answer between the triple quotes:

```python
"answer": """Your answer goes here.

Can be multiple paragraphs.
Just write normally."""
```

### For other subjects (CSE, SGT, PPE, EMD):
Open `data/cse.py` (or whichever subject). Copy this block and paste inside the unit's `questions` list:

```python
{
    "id": "cse_1_1",          # unique ID: subject_unit_number
    "question": "Your question here",
    "frequency": 2,           # how many times it came in exam
    "exams": ["S-2022", "W-2023"],  # which exams
    "answer": """Your answer here"""
},
```

---

## Run Locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python app.py
```
Open http://localhost:5000

---

## Deploy on Render (Free)

1. Push this folder to GitHub
2. Go to render.com → New Web Service → Connect your repo
3. Add environment variable: `ANTHROPIC_API_KEY = your_key`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy ✅

---

## Project Structure

```
examhub/
├── app.py                  # Flask backend + AI route
├── requirements.txt
├── Procfile                # for deployment
├── data/
│   ├── sgp.py              # ✅ SGP questions (paste answers here)
│   ├── cse.py              # paste CSE questions here
│   ├── sgt.py              # paste SGT questions here
│   ├── ppe.py              # paste PPE questions here
│   └── emd.py              # paste EMD questions here
├── templates/
│   ├── index.html          # landing page
│   └── subject.html        # question/answer page
└── static/
    ├── css/style.css       # ALL styles
    └── js/main.js          # copy, tabs, AI chat
```