class Question:
    def __init__(self,id, question, option_a, option_b, option_c, option_d, correct_option, category, difficulty):
        self.id=id
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_option = correct_option
        self.category = category
        self.difficulty = difficulty
        self.current_index = 0   # tracks which question we're currently on
    def get_answer(self):
        while True:
            self.user_answer = input("Enter your answer (a/b/c/d): ").strip().lower()
            if self.user_answer in ['a', 'b', 'c', 'd']:
                return self.user_answer
            else:
                print("Invalid input. Please enter a, b, c, or d.")
                
    def check_answer(self):
        return self.user_answer == self.get_answer()
    
    def get_current_question(self):
        # returns the Question object the GUI should currently display,
        # or None if we've gone through all of them
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
    
    def submit_answer(self, user_choice):
        # called by the GUI when a button (a/b/c/d) is clicked
        q = self.get_current_question()
        is_correct = q.check_answer(user_choice)

        if is_correct:
            self.score += 1

        category = q.category
        if category not in self.category_results: 
            #category_result is liscreated everytime when quiz is taken everytime each category ques comes
            #if its dict isnt created it get creates and if its created this if part gets skipped 
            #and then total and correct count gets updated for that category
            self.category_results[category] = {"correct": 0, "total": 0}
        self.category_results[category]["total"] += 1
        if is_correct:
            self.category_results[category]["correct"] += 1

        self.attempt_log.append({
            "question_id": q.id,
            "category": category,
            "difficulty": q.difficulty,
            "is_correct": 1 if is_correct else 0
        })

        self.current_index += 1   # move to the next question
        return is_correct
    
    def is_finished(self): 
        return self.current_index >= len(self.questions)

class Quiz:
    def __init__(self,questions):
        self.attempt_log = []
        self.questions=questions
        self.score=0
        self.total=len(self.questions)
        self.category_results = {}
    def run(self):
        for i, q in enumerate(self.questions, start=1):
            print(f"{i}. {q.question}")
            print(f"a. {q.option_a}")
            print(f"b. {q.option_b}")
            print(f"c. {q.option_c}")
            print(f"d. {q.option_d}")

            Q = q.check_answer()
            if Q:
                self.score += 1

            category = q.category
            if category not in self.category_results:
                self.category_results[category] = {"correct": 0, "total": 0}
            self.category_results[category]["total"] += 1
            if Q:
                self.category_results[category]["correct"] += 1
            self.attempt_log.append({
    "question_id": q.id,
    "category": category,
    "difficulty": q.difficulty,
    "is_correct": 1 if Q else 0
})

    def show_summary(self):
        output=""
        output += f"\nFinal Score: {self.score}/{self.total}"
        output += "\nCategory Breakdown:"
        weak_categories = []
        for category, results in self.category_results.items():
            accuracy = results['correct'] / results['total']
            if accuracy < 0.6:
                output += f"\n  {category}: {results['correct']}/{results['total']} needs practice"
                weak_categories.append(category)
            else:
                output += f"\n  {category}: {results['correct']}/{results['total']}"
        if not weak_categories:
            output += "\nGreat job! No major weak areas this session."
        return output
        
if __name__ == "__main__":
    sample_questions = [
        (1, "She ___ to school every day.", "go", "goes", "going", "gone", "b", "Tenses", "easy"),
        (2, "They ___ watching a movie right now.", "is", "am", "are", "was", "c", "Tenses", "easy"),
        (3, "Choose the noun: 'The dog ran quickly.'", "ran", "quickly", "dog", "the", "c", "Parts of Speech", "easy"),
        (4, "Choose the correct sentence:", "He go to market.", "He goes to market.", "He going to market.", "He gone to market.", "b", "Subject-Verb Agreement", "easy"),
        (5, "Choose the correct word: 'Their/There/They're going home.'", "Their", "There", "They're", "There's", "c", "Common Errors", "easy"),
    ]

    questions = []
    #data here is tuple from sample_questions 
    for data in sample_questions:
        q = Question(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
        questions.append(q)
    #every data from sample_ques gets append to question list
    Q1 = Quiz(questions)
    Q1.run()
    Q1.show_summary()