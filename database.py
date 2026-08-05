import sqlite3

def create_tables():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    #cursor a tool helps in running sql comands

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_option TEXT,
            category TEXT,
            difficulty TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            attempt_id INTEGER PRIMARY KEY,
            date TEXT,
            category TEXT,
            difficulty TEXT,
            question_id INTEGER,
            is_correct INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")


def insert_sample_questions():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    sample_questions = [
        ("She ___ to school every day.", "go", "goes", "going", "gone", "b", "Tenses", "easy"),
        ("They ___ watching a movie right now.", "is", "am", "are", "was", "c", "Tenses", "easy"),
        ("Choose the noun: 'The dog ran quickly.'", "ran", "quickly", "dog", "the", "c", "Parts of Speech", "easy"),
        ("Choose the correct sentence:", "He go to market.", "He goes to market.", "He going to market.", "He gone to market.", "b", "Subject-Verb Agreement", "easy"),
        ("Choose the correct word: 'Their/There/They're going home.'", "Their", "There", "They're", "There's", "c", "Common Errors", "easy"),
    ]
#same as  execute but it loops through all questions one by one
    cursor.executemany("""
        INSERT INTO questions 
        (question, option_a, option_b, option_c, option_d, correct_option, category, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_questions)

    conn.commit()
    conn.close()
    print(f"{len(sample_questions)} sample questions inserted.")


if __name__ == "__main__":
    create_tables()
    insert_sample_questions()