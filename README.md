English Grammar Quiz — with Performance Analytics

Database (database.py)
SQLite schema with two tables: questions (grammar questions across categories and difficulty levels) and attempts (logs every answered question, linked to questions via a foreign key)

Quiz Logic (models.py)
Question class — stores a single question's data, prompts the user for an answer, validates input, and checks correctness
Quiz class — runs a full quiz session over a list of Question objects, tracks the running score, and builds a category-wise accuracy breakdown as it goes

Tech Stack
Python (OOP)
SQLite (sqlite3)
SQL (schema design, constraints)

How to Run
bash
python database.py   # sets up the database and seeds sample questions
python models.py      # runs a test quiz using sample data
