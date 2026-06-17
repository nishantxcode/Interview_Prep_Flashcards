import json
import random
import os
from datetime import datetime, timezone, timedelta

# Paths
QUESTION_FILES = {
    "dbms": "assets/dbms_100_questions.json",
    "dsa": "assets/dsa_100_questions.json",
    "hr": "assets/hr_100_questions.json",
    "java": "assets/java_100_questions.json",
    "networking": "assets/networking_100_questions.json",
    "oop": "assets/oop_100_questions.json",
    "os": "assets/os_100_questions.json",
    "python": "assets/python_100_questions.json",
    "sql": "assets/sql_100_questions.json",
    "system_design": "assets/system_design_100_questions.json",
}
OUTPUT_PATH = "assets/daily_questions.json"
JS_OUTPUT_PATH = "assets/daily_questions.js"
QUESTIONS_PER_SUBJECT = 2
IST = timezone(timedelta(hours=5, minutes=30))

def generate_daily_deck():
    daily_deck = []

    # 1. Load each subject question file and sample a fixed number from it.
    for category, file_path in QUESTION_FILES.items():
        if not os.path.exists(file_path):
            print(f"Warning: Question file not found for '{category}' at {file_path}")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)

        if len(questions) >= QUESTIONS_PER_SUBJECT:
            daily_deck.extend(random.sample(questions, QUESTIONS_PER_SUBJECT))
        else:
            print(f"Warning: Only {len(questions)} questions found in '{category}'. Using all available.")
            daily_deck.extend(questions)

    # 2. Shuffle the final deck so topics are mixed up.
    random.shuffle(daily_deck)

    # 3. Meta-data for the frontend.
    quiz_data = {
        "date": datetime.now(IST).strftime("%Y-%m-%d"),
        "questions": daily_deck
    }

    # 4. Write to the assets folder for the frontend to consume.
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)

    with open(JS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("window.DAILY_QUESTIONS = ")
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    
    print(f"Successfully generated daily quiz with {len(daily_deck)} questions for {quiz_data['date']}.")

if __name__ == "__main__":
    generate_daily_deck()
