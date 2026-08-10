from database import Database
from models import Question, Quiz

def get_questions(db, difficulty, categories, count):
    # 'db' is the Database object — it OWNS db.cursor, which OWNS execute().
    # Only the 'params' tuple below ever fills the '?' placeholders — nothing else.

    if len(categories) == 0:
        # "all" was chosen — no category filter, so only 2 placeholders needed:
        # one for difficulty, one for the LIMIT count.
        query = "SELECT * FROM questions WHERE difficulty = ? LIMIT ?"
        params = (difficulty, count)
    else:
        # Build exactly as many '?' as there are categories chosen
        placeholders = ", ".join(["?"] * len(categories))

        query = f"SELECT * FROM questions WHERE difficulty = ? AND category IN ({placeholders}) LIMIT ?"
        #placeholder get fills from this params when db.cursor.execute runs
#*categories is used to unpcak tuple
        params = (difficulty, *categories, count)

    db.cursor.execute(query, params)
    rows = db.cursor.fetchall()

    # Same conversion pattern as always — raw tuples become real Question objects
    questions = []
    for row in rows:
        q = Question(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        questions.append(q)

    return questions

VALID_CATEGORIES = ["Tenses", "Parts of Speech", "Subject-Verb Agreement", "Common Errors"]

def get_difficulty():
    print("\nDifficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
    choice = input("Choose difficulty (1/2/3): ").strip()

    while choice not in difficulty_map:
        print("Invalid choice.")
        choice = input("Choose difficulty (1/2/3): ").strip()

    return difficulty_map[choice]


def get_categories():
    print("\nCategories:")
    print("1. Tenses")
    print("2. Parts of Speech")
    print("3. Subject-Verb Agreement")
    print("4. Common Errors")
    print("5. All Categories")

    category_map = {
        "1": "Tenses",
        "2": "Parts of Speech",
        "3": "Subject-Verb Agreement",
        "4": "Common Errors",
    }

    choice_input = input("Enter numbers separated by commas (e.g. 1,3) or 5 for all: ").strip()

    if choice_input == "5":
        return []

    choices = [c.strip() for c in choice_input.split(",")]
    categories = []
    for c in choices:
        if c in category_map:
            categories.append(category_map[c])
        else:
            print(f"Warning: '{c}' is not a valid option and will be skipped.")

    return categories


def get_user_choices():
    difficulty = get_difficulty()
    categories = get_categories()
    count = int(input("\nHow many questions? "))
    return difficulty, categories, count

def main():
    db = Database()

    print("=== English Grammar Quiz ===")
    difficulty, categories, count = get_user_choices()

    questions = get_questions(db, difficulty, categories, count)

    if len(questions) == 0:
        print("No questions found matching your choices. Try again.")
        db.close()
        return
    print(f"\nStarting quiz with {len(questions)} questions...\n")
    quiz = Quiz(questions)
    quiz.run()
    quiz.show_summary()

    db.close()


if __name__ == "__main__":
    main()

        