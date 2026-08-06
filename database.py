import sqlite3
class Database:
    def __init__(self, db_name="quiz.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # execute() sends SQL commands to SQLite
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT UNIQUE NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_option TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                attempt_id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question_id INTEGER NOT NULL,
                is_correct INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        """)

        print("Tables created successfully.")

    def insert_sample_questions(self):
        sample_questions = [
            ("She ___ to school every day.", "go", "goes", "going", "gone", "b", "Tenses", "easy"),
            ("They ___ watching a movie right now.", "is", "am", "are", "was", "c", "Tenses", "easy"),
            ("Choose the noun: 'The dog ran quickly.'", "ran", "quickly", "dog", "the", "c", "Parts of Speech", "easy"),
            ("Choose the correct sentence:", "He go to market.", "He goes to market.", "He going to market.", "He gone to market.", "b", "Subject-Verb Agreement", "easy"),
            ("Choose the correct word: 'Their/There/They're going home.'", "Their", "There", "They're", "There's", "c", "Common Errors", "easy"),
        ]

        # executemany() runs like a loop
        # OR IGNORE tells SQLite: if a question with this exact text
        # already exists (violates UNIQUE), skip it silently instead of
        # throwing an error — so re-running this is always safe
        self.cursor.executemany("""
            INSERT OR IGNORE INTO questions
            (question, option_a, option_b, option_c,
             option_d, correct_option, category, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_questions)

        print(f"Insert attempted for {len(sample_questions)} questions (duplicates skipped automatically).")

    def commit(self):
        # Save changes made by CREATE TABLE or INSERT
        self.conn.commit()

    def close(self):
        # Close database connection
        self.conn.close()
def main():
    db = Database()
    db.create_tables()
    db.insert_sample_questions()
    db.commit()
    db.close()
if __name__ == "__main__":
    main()