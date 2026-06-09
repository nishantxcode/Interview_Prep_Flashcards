import json
import random
import os
from datetime import datetime
from datetime import datetime, timezone
# Paths
BANK_PATH = "data/question_bank.json"
OUTPUT_PATH = "assets/daily_questions.json"

def generate_daily_deck():
    # 1. Load the master question bank
    if not os.path.exists(BANK_PATH):
        print(f"Error: Master question bank not found at {BANK_PATH}")
        return

    with open(BANK_PATH, 'r', encoding='utf-8') as f:
        master_bank = json.load(f)

    categories = ["system_design", "dsa", "oops", "dbms", "networking"]
    daily_deck = []

    # 2. Sample 2 random questions from each category
    for category in categories:
        if category in master_bank and len(master_bank[category]) >= 2:
            sampled = random.sample(master_bank[category], 2)
            daily_deck.extend(sampled)
        else:
            print(f"Warning: Insufficient questions in category '{category}'")
            # Fallback: take whatever is available
            daily_deck.extend(master_bank.get(category, []))

    # 3. Shuffle the final 10 questions so topics are mixed up
    random.shuffle(daily_deck)

    # 4. Meta-data for the frontend (e.g., Daily Quiz Date)
    quiz_data = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "questions": daily_deck
    }

    # 5. Write to the assets folder for the frontend to consume
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated daily quiz with {len(daily_deck)} questions for {quiz_data['date']}.")

if __name__ == "__main__":
    generate_daily_deck()
