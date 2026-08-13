import sqlite3
import csv
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

    def commit(self):
        # Save changes made by CREATE TABLE or INSERT
        self.conn.commit()

    def close(self):
        # Close database connection
        self.conn.close()
    
    def load_questions_from_csv(self,filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            questions = []
            for row in reader:
                questions.append((
                    row['question'],
                    row['option_a'],
                    row['option_b'],
                    row['option_c'],
                    row['option_d'],
                    row['correct_option'],
                    row['category'],
                    row['difficulty']
                ))
            self.cursor.executemany("""
                INSERT OR IGNORE INTO questions
                (question, option_a, option_b, option_c,
                 option_d, correct_option, category, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, questions)
            print(f"Inserted {len(questions)} questions from CSV.")
def main():
    db = Database()
    db.create_tables()
    db.load_questions_from_csv("questions.csv")
    db.commit()
    db.close()
if __name__ == "__main__":
    main()
