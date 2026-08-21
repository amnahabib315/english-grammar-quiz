from database import Database

def accuracy_by_category(db):
    db.cursor.execute("""
        SELECT category, 
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct_count,
               COUNT(*) AS total_count
        FROM attempts
        GROUP BY category
    """)
    results = db.cursor.fetchall()

    accuracy_data = []
    for row in results:
        category, correct_count, total_count = row
        accuracy_percentage = (correct_count / total_count) * 100 if total_count > 0 else 0
        accuracy_data.append((category, total_count, correct_count, accuracy_percentage))

    return accuracy_data #list of tuples

def accuracy_by_difficulty(db):
    db.cursor.execute("""
        SELECT difficulty, 
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct_count,
               COUNT(*) AS total_count
        FROM attempts
        GROUP BY difficulty
    """)
    results = db.cursor.fetchall()

    accuracy_data = []
    for row in results:
        difficulty, correct_count, total_count = row
        accuracy_percentage = (correct_count / total_count) * 100 if total_count > 0 else 0
        accuracy_data.append((difficulty, total_count, correct_count, accuracy_percentage))

    return accuracy_data #list with tuples

def overall_stats(db):
    db.cursor.execute("""
        SELECT 
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct_count,
            COUNT(*) AS total_count
        FROM attempts
    """)
    result = db.cursor.fetchone()
    #fetchone gives 1 row directly instead of list of1 row which in this case is our query result

    correct_count, total_count = result #unpacking the tuple returned by fetchone
    accuracy_percentage = (correct_count / total_count) * 100 if total_count > 0 else 0

    return total_count, correct_count, accuracy_percentage


def weakest_category(db):
    db.cursor.execute("""
        SELECT category, 
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct_count,
               COUNT(*) AS total_count,
               (SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS accuracy
               --* 1.0 forces decimal division so the accuracy ratio is treated as a float
        FROM attempts
        GROUP BY category
        ORDER BY accuracy ASC
        LIMIT 1
    """)
    result = db.cursor.fetchone()

    if result:
        category, correct_count, total_count, accuracy = result
        accuracy_percentage = accuracy * 100
        if accuracy_percentage < 60:   # only meaningful if genuinely weak
            return category, total_count, correct_count, accuracy_percentage
        else:
            return None
    else:
        return None

def show_report(db):
    total, correct, accuracy = overall_stats(db)
    output = ""

    if total == 0:
        return "No quiz attempts recorded yet."

    output += "Overall Quiz Performance:\n"
    output += f" Total Questions Attempted: {total}\n"
    output += f" Total Correct Answers: {correct}\n"
    output += f" Overall Accuracy: {accuracy:.2f}%\n"

    category_accuracy = accuracy_by_category(db)
    for category in category_accuracy:
        cat, total_count, correct_count, accuracy_percentage = category
        output += f"\nCategory: {cat}\n"
        output += f"  Total Questions Attempted: {total_count}\n"
        output += f"  Total Correct Answers: {correct_count}\n"
        output += f"  Accuracy: {accuracy_percentage:.2f}% {'needs practice' if accuracy_percentage < 60 else 'performing well'}\n"

    difficulty_accuracy = accuracy_by_difficulty(db)
    for difficulty in difficulty_accuracy:
        diff, total_count, correct_count, accuracy_percentage = difficulty
        output += f"\nDifficulty: {diff}\n"
        output += f"  Total Questions Attempted: {total_count}\n"
        output += f"  Total Correct Answers: {correct_count}\n"
        output += f"  Accuracy: {accuracy_percentage:.2f}% {'needs practice' if accuracy_percentage < 60 else 'performing well'}\n"

    weakest_cat = weakest_category(db)
    if weakest_cat:
        cat, total_count, correct_count, accuracy_percentage = weakest_cat
        output += f"\nWeakest Category: {cat}\n"
        output += f"  Accuracy: {accuracy_percentage:.2f}% - Focus on this category for improvement.\n"
    else:
        output += "\nGreat job! No category is significantly weaker than others.\n"

    return output
#here we changed prit statments to storing everyting in single stringd bcz this will
#then go to our gui.py  instead of printing to console

def accuracy_by_date(db, limit=8):
    db.cursor.execute("""SELECT date, SUM(is_correct) * 100.0 / COUNT(*) AS accuracy
FROM attempts
GROUP BY date
ORDER BY date DESC
LIMIT ?""", (limit,))
    result = db.cursor.fetchall()
    return result