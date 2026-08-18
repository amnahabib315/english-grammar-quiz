# English Grammar Quiz — with Performance Analytics

A console-based English Grammar Quiz application built with Python and SQLite.

## What's built so far

**Database (`database.py`)**
- SQLite schema with two tables: `questions` (grammar questions across categories and difficulty levels) and `attempts` (logs every answered question, linked to `questions` via a foreign key)
- Sample questions seeded across four categories: Tenses, Parts of Speech, Subject-Verb Agreement, and Common Errors/Confusing Words
- Duplicate-safe inserts (`INSERT OR IGNORE` with a `UNIQUE` constraint) so the seed script can run repeatedly without creating duplicate rows

**Quiz Logic (`models.py`)**
- `Question` class — stores a single question's data, prompts the user for an answer, validates input, and checks correctness
- `Quiz` class — runs a full quiz session over a list of `Question` objects, tracks the running score, and builds a category-wise accuracy breakdown as it goes

**Quiz Controller (`main.py`)**

- User selection of difficulty level (Easy, Medium, Hard)
- User selection of one or more grammar categories
- Random question retrieval from the database
- Automatic logging of quiz attempts to the database

**Analytics (`analytics.py`)**
- Aggregates all-time performance from the `attempts` table using SQL `GROUP BY`
- Reports accuracy by category and by difficulty level
- Identifies the weakest category (if any falls below a practice threshold) and flags it for the user

**Question Data (`questions.csv`)**
- 36 questions across 4 categories and 3 difficulty levels (3 questions each)
- Loaded into the database via `load_questions_from_csv()`, using `INSERT OR IGNORE` so re-running never creates duplicates
- New questions can be added anytime by appending rows to `questions.csv` and re-running `database.py`

**Charts (`charts.py`)**
- Visualizes performance using matplotlib: accuracy by category (bar), accuracy by difficulty (bar), accuracy over time (line, last 8 days), and correct vs incorrect answers (pie)
- Color-coded thresholds (green ≥60%, orange 40-59%, red <40%) with an overall average reference line
- Best/weakest category and difficulty highlighted as a caption on each chart
- Optional save-to-PNG after viewing any chart
- Combined "Performance Dashboard" view showing all four charts together in one window
- Accessed via the "View Performance Charts" submenu in the app

## Tech Stack
- Python (OOP)
- SQLite (`sqlite3`)
- SQL (schema design, constraints)

## How to Run
```bash
pip install matplotlib   # required for performance charts
python database.py   # generates quiz.db, seeds questions from questions.csv
python main.py       # starts the quiz application
```

