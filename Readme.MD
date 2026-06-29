# ⚡ Electrical Exam Prep

An AI-powered Electrical Engineering Exam Preparation Platform designed for diploma and engineering students.

The platform helps students prepare for semester examinations by providing previous year questions, AI-generated answers, unit-wise organization, and an intelligent chatbot for doubt solving.

---

## 🚀 Features

### 📚 Previous Year Questions
- Subject-wise organization
- Unit-wise questions
- Exam frequency tracking
- Simple and clean interface

### 🤖 AI Answer Generation
- Automatically generates university-style answers
- Simple English
- Structured format with headings
- Point-wise explanations
- Supports definitions, working, advantages, disadvantages, applications, characteristics, etc.
- No unnecessary repetition

### 🔄 AI Answer Regeneration Tool
Built a Python utility that can:

- Regenerate a single answer
- Regenerate multiple answers
- Regenerate an entire unit
- Regenerate a complete subject
- Search questions by keyword
- Preserve JSON structure automatically

### 💬 AI Chatbot
- Integrated Google Gemini API
- Answers student doubts instantly
- Context-aware responses

### 📂 JSON-Based Database
- Stores all questions and answers
- Fast loading
- Easy maintenance
- Scalable for new subjects

### 🎯 Exam Focused
- Previous year question frequency
- Unit-wise preparation
- Easy revision
- Student-friendly UI

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## AI

- Google Gemini API
- Groq API
- Llama 3.3 70B Versatile

## Database

- JSON

## Python Libraries

- OpenAI SDK
- python-dotenv
- json
- os
- time

---

# 📂 Project Structure

```
electrical-exam-prep
│
├── app.py
├── requirements.txt
├── generate_json.py
├── generate_answers.py
├── regenerate_answer.py
│
├── data
│   └── json
│
├── templates
│   ├── index.html
│   └── subject.html
│
├── static
│   ├── css
│   ├── js
│   └── images
│
└── README.md
```

---

# ✨ Key Functionalities

- AI-powered answer generation
- AI chatbot
- Previous year questions
- Unit-wise navigation
- Frequency analysis
- Search functionality
- Automatic JSON generation
- Automatic JSON updating
- Responsive interface
- Fast loading
- Easy content management

---

# 🔧 Automation Tools

The project includes Python automation scripts for maintaining the question bank.

### generate_json.py

Automatically creates JSON files for all subjects and units.

### generate_answers.py

Automatically generates answers only for questions whose answers are blank.

### regenerate_answer.py

Allows regeneration of:

- Single Answer
- Multiple Answers
- Complete Unit
- Entire Subject

without affecting other existing answers.

---

# 📈 Future Improvements

- PDF Notes
- Cheat Sheet Generator
- Infographic Answers
- Diagram Library
- Bookmark Questions
- Advanced Search
- RAG-based AI Assistant
- User Authentication
- Admin Dashboard

---

# 🎯 Target Users

- Diploma Students
- Electrical Engineering Students
- Semester Examination Preparation


---

# 📜 License

This project is developed for educational purposes.

---

# 👨‍💻 Developer

Krushna

GitHub:
https://github.com/krishoo2005