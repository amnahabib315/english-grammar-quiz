class Question:
    def __init__(self, id, question, option_a, option_b, option_c, option_d, correct_option, category, difficulty):
        self.id = id
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_option = correct_option
        self.category = category
        self.difficulty = difficulty
    def get_answer(self):
        while True:
            self.user_answer = input("Enter your answer (a/b/c/d): ").strip().lower()
            if self.user_answer in ['a', 'b', 'c', 'd']:
                return self.user_answer
            else:
                print("Invalid input. Please enter a, b, c, or d.")
    def check_answer(self):
        user_choice = self.get_answer()
        if user_choice == self.correct_option:
            print("Correct!")
            return True
        else:
            print(f"Incorrect. The correct answer was {self.correct_option}.")
            return False
q=Question(1,"She ___ to school every day.", "go", "goes", "going", "gone", "b", "Tenses", "easy")
q.check_answer()
