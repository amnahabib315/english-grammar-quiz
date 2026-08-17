from database import Database
from models import Question, Quiz
from datetime import date
import random
from analytics import show_report
from charts import plot_category_accuracy, plot_difficulty_accuracy, plot_accuracy_over_time

VALID_CATEGORIES = ["Tenses", "Parts of Speech", "Subject-Verb Agreement", "Common Errors"]

def get_questions(db, difficulty, categories, count):
    if len(categories) == 0:
        categories = VALID_CATEGORIES   

    base_count = count // len(categories)  # =7//3 = 2
    #base_count tells how many questions each category will get
    remainder = count % len(categories)   #=7%3 = 1
    #rem controls how many categ. get that one extra
    #rem= 3, that means 3 different categories each get +1
    rows = []
    for i, category in enumerate(categories):
        this_category_count = base_count + (1 if i < remainder else 0)
        # = 2 + (1 if 0 < 1 else 0) = 3 for first category
        # i<rem is bcz after equal distri. we will distribute+1 to each category till the count ends
                        
        if this_category_count > 0:
            db.cursor.execute(
                "SELECT * FROM questions WHERE difficulty = ? AND category = ? ORDER BY RANDOM() LIMIT ?",
                (difficulty, category, this_category_count)
            )
            rows.extend(db.cursor.fetchall())
    random.shuffle(rows)

    questions = []
    for row in rows:
        q = Question(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        questions.append(q)

    return questions


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

def log_attempts(db, quiz):
    today = str(date.today())
    for attempt in quiz.attempt_log:
        db.cursor.execute("""
            INSERT INTO attempts (date, category, difficulty, question_id, is_correct)
            VALUES (?, ?, ?, ?, ?)
        """, (today, attempt["category"], attempt["difficulty"], attempt["question_id"], attempt["is_correct"]))
    db.conn.commit()
    print(f"\n{len(quiz.attempt_log)} attempts logged to database.")

        
def main():
    db = Database()

    print("=== English Grammar Quiz ===")

    while True:
        print("\n1. Take Quiz")
        print("2. View Performance Report")
        print("3. View Performance Charts")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            difficulty, categories, count = get_user_choices()
            questions = get_questions(db, difficulty, categories, count)
            if len(questions) == 0:
                print("No questions found matching your choices. Try again.")
                continue
            if len(questions) < count:
                print(f"\nNote: Only {len(questions)} questions available for your selection (you requested {count}).")
            print(f"\nStarting quiz with {len(questions)} questions...\n")
            quiz = Quiz(questions)
            quiz.run()
            quiz.show_summary()
            log_attempts(db, quiz)
        elif choice == "2":
            show_report(db)
        elif choice == "3":
            while True:
                print("\n1. Accuracy by Category")
                print("2. Accuracy by Difficulty")
                print("3. Accuracy Over Time")
                print("4. Back to Main Menu")
                chart_choice = input("Choose an option: ").strip()
                if chart_choice == "1":
                    plot_category_accuracy(db)
                elif chart_choice == "2":
                    plot_difficulty_accuracy(db)
                elif chart_choice == "3":
                    plot_accuracy_over_time(db)
                elif chart_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    db.close()

if __name__ == "__main__":
    main()

        