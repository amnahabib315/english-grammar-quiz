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
    # ---- EASY ----
    ("She ___ to school every day.", "go", "goes", "going", "gone", "b", "Tenses", "easy"),
    ("They ___ watching a movie right now.", "is", "am", "are", "was", "c", "Tenses", "easy"),
    ("Choose the noun: 'The dog ran quickly.'", "ran", "quickly", "dog", "the", "c", "Parts of Speech", "easy"),
    ("Choose the verb: 'She sings beautifully.'", "she", "sings", "beautifully", "the", "b", "Parts of Speech", "easy"),
    ("Choose the correct sentence: ____ to market or He goes to market?", "He go to market.", "He goes to market.", "He going to market.", "He gone to market.", "b", "Subject-Verb Agreement", "easy"),
    ("Choose the correct sentence: They walks fast or They walk fast?", "They walks fast.", "They walk fast.", "They walking fast.", "They walked fast.", "b", "Subject-Verb Agreement", "easy"),
    ("Choose the correct word: '____ going home.'", "Their", "There", "They're", "There's", "c", "Common Errors", "easy"),
    ("Choose the correct word: '____ raining outside.'", "Its", "It's", "It'", "Its's", "b", "Common Errors", "easy"),

    # ---- MEDIUM ----
    ("By next year, she ___ her degree.", "completes", "will complete", "will have completed", "completed", "c", "Tenses", "medium"),
    ("She ___ dinner when the phone rang.", "cooks", "was cooking", "cooked", "cook", "b", "Tenses", "medium"),
    ("Identify the adverb: 'He runs very quickly.'", "runs", "very", "quickly", "he", "c", "Parts of Speech", "medium"),
    ("Identify the preposition: 'The book is on the table.'", "book", "is", "on", "table", "c", "Parts of Speech", "medium"),
    ("Choose the correct sentence about 'neither': which is correct?", "Neither of them are ready.", "Neither of them is ready.", "Neither of them be ready.", "Neither of them was ready.", "b", "Subject-Verb Agreement", "medium"),
    ("Choose the correct sentence about 'the team': which is correct?", "The team are winning.", "The team is winning.", "The team be winning.", "The team were winning.", "b", "Subject-Verb Agreement", "medium"),
    ("Choose the correct word: 'I could ____ done better.'", "of", "have", "off", "half", "b", "Common Errors", "medium"),
    ("Choose the correct word: '____ going to love this.'", "Your", "You're", "Yore", "Yours", "b", "Common Errors", "medium"),

    # ---- HARD ----
    ("If she ___ earlier, she wouldn't have missed the bus.", "left", "leaves", "had left", "was leaving", "c", "Tenses", "hard"),
    ("By the time you arrive, we ___ already left.", "have", "had", "will have", "has", "c", "Tenses", "hard"),
    ("Identify the conjunction: 'She stayed although it rained.'", "stayed", "although", "rained", "she", "b", "Parts of Speech", "hard"),
    ("Identify the interjection: 'Wow, that's amazing!'", "wow", "that's", "amazing", "is", "a", "Parts of Speech", "hard"),
    ("Choose the correct sentence about 'each student': which is correct?", "Each of the students have submitted.", "Each of the students has submitted.", "Each of the students submit.", "Each of the students submitting.", "b", "Subject-Verb Agreement", "hard"),
    ("Choose the correct sentence about 'the news': which is correct?", "The news are surprising.", "The news is surprising.", "The news were surprising.", "The news be surprising.", "b", "Subject-Verb Agreement", "hard"),
    ("Choose the correct word: 'The ____ of the policy was huge.'", "effect", "affect", "affects", "effecting", "a", "Common Errors", "hard"),
    ("Choose the correct word: '____ she left.'", "Then", "Than", "Their", "There", "a", "Common Errors", "hard"),
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