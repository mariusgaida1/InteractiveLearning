import csv
import random
from datetime import datetime


class Question:
    @classmethod
    def find_max_question_id(cls, filename):
        max_id = 0
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                max_id = max(max_id, int(row["question_id"]))
        return max_id

    def __init__(
        self,
        text,
        answer,
        is_quiz,
        options=None,
        is_active=True,
        shown=0,
        correct=0,
        filename="questions.csv",
    ):
        self.filename = filename
        self.question_id = self.find_max_question_id(filename) + 1
        self.text = text
        self.answer = answer
        self.is_quiz = is_quiz
        self.is_active = is_active
        self.shown = 0
        self.correct = 0
        self.options = options

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, _text):
        if _text == "":
            raise ValueError("Question text cannot be empty")
        self._text = _text

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, _answer):
        if _answer == "":
            raise ValueError("Question answer cannot be empty")
        self._answer = _answer

    def disable(self):
        self.is_active = False

    def enable(self):
        self.is_active = True

    def add_question(self):
        with open(self.filename, "a", newline="") as csvfile:
            fieldnames = [
                "question_id",
                "text",
                "answer",
                "is_quiz",
                "options",
                "is_active",
                "shown",
                "correct",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {
                    "question_id": self.question_id,
                    "text": self.text,
                    "answer": self.answer,
                    "is_quiz": self.is_quiz,
                    "options": self.options,
                    "is_active": self.is_active,
                    "shown": 0,
                    "correct": 0,
                }
            )


class QuestionManager:
    def __init__(self, filename="questions.csv"):
        self.filename = filename
        self.questions = []

    def load_questions(self):
        with open(self.filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = {
                    "question_id": row["question_id"],
                    "text": row["text"],
                    "answer": row["answer"],
                    "is_quiz": row["is_quiz"],
                    "options": row["options"],
                    "is_active": row["is_active"],
                    "shown": row["shown"],
                    "correct": row["correct"],
                }
                self.questions.append(question)

    # def get_questions(self):
    #   return self.questions

    def get_active_questions(self):
        return [
            question for question in self.questions if question["is_active"] == "True"
        ]

    def disable_question(self, question_id):
        for question in self.questions:
            if question["question_id"] == question_id:
                question["is_active"] = "False"
                return True
        return False

    def enable_question(self, question_id):
        for question in self.questions:
            if question["question_id"] == question_id:
                question["is_active"] = "True"
                return True
        return False

    def update_shown_field(self, question_id):
        for question in self.questions:
            if question["question_id"] == question_id:
                question["shown"] = int(question["shown"]) + 1
                break

        # Update the CSV file
        with open(self.filename, "w", newline="") as csvfile:
            fieldnames = [
                "question_id",
                "text",
                "answer",
                "is_quiz",
                "options",
                "is_active",
                "shown",
                "correct",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.questions)

    def update_correct_field(self, question_id):
        for question in self.questions:
            if question["question_id"] == question_id:
                question["correct"] = int(question["correct"]) + 1
                break

        # Update the CSV file
        with open(self.filename, "w", newline="") as csvfile:
            fieldnames = [
                "question_id",
                "text",
                "answer",
                "is_quiz",
                "options",
                "is_active",
                "shown",
                "correct",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.questions)


class PracticeMode:
    def __init__(self, question_manager):
        self.question_manager = question_manager

    def practice(self):
        active_questions = self.question_manager.get_active_questions()
        if len(active_questions) < 5:
            print("Practice mode requires at least 5 active questions.")
            return

        while True:
            question = self._select_question(active_questions)
            user_answer = input(question["text"] + "\n")

            if question["is_quiz"].lower().strip() == "yes":
                # Display answer options for quiz questions
                for index, option in enumerate(question["options"]):
                    print(f"{index + 1}. {option}")
                user_choice = int(input("Enter your choice (1, 2, 3, ...): "))
                user_answer = question.options[user_choice - 1]

            if self.check_answer(user_answer, question):
                # if Question(question["text"], question["answer"], question["is_quiz"],question["options"],question["is_active"],question["shown"],question["correct"]).check_answer(user_answer):
                print("Correct!")
                self.question_manager.update_correct_field(question["question_id"])
            else:
                print("Incorrect!")

            self.question_manager.update_shown_field(question["question_id"])

    def _select_question(self, questions):
        weights = [1 / (int(question["shown"]) + 1) for question in questions]
        return random.choices(questions, weights=weights, k=1)[0]

    def check_answer(self, user_answer, question):
        # self.shown += 1
        if user_answer.strip().lower() == question["answer"].strip().lower():
            # self.correct += 1
            return True
        return False


class TestMode:
    def __init__(self, question_manager):
        self.question_manager = question_manager

    def take_test(self, num_questions):
        active_questions = self.question_manager.get_active_questions()
        num_questions = int(num_questions)
        if len(active_questions) < num_questions:
            print("Not enough active questions to take the test.")
            return
        elif len(active_questions) < 5:
            print("Practice mode requires at least 5 active questions.")
            return

        selected_questions = random.sample(active_questions, num_questions)
        score = 0
        for question in selected_questions:
            user_answer = input(question["text"] + "\nYour answer: ")
            if self.check_answer(user_answer, question):
                score += 1

        score_percentage = (score / num_questions) * 100
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score_info = f"Score: {score}/{num_questions} ({score_percentage:.2f}%) - {current_time}\n"

        with open("results.txt", "a") as file:
            file.write(score_info)

        print(f"Test completed. Score: {score}/{num_questions}")

    def check_answer(self, user_answer, question):
        # self.shown += 1
        if user_answer.strip().lower() == question["answer"].strip().lower():
            # self.correct += 1
            return True
        return False


def main():
    question_manager = QuestionManager()
    question_manager.load_questions()
    practice_mode = PracticeMode(question_manager)
    test_mode = TestMode(question_manager)

    # Main menu loop
    while True:
        print("\nMain Menu:")
        print("1. Adding questions")
        print("2. Statistics viewing")
        print("3. Disable/Enable questions")
        print("4. Practice mode")
        print("5. Test mode")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Enter Adding questions mode
            print("\nAdding questions mode:")
            try:
                text = input("Enter question text: ")
                answer = input("Enter question answer: ")
                is_quiz = input("Is quiz: ")
                if is_quiz.lower().strip() == "yes":
                    options = []
                    while True:
                        option = input("Enter an option (or type 'done' to finish): ")
                        if option.lower() == "done":
                            break
                        options.append(option)
                    question = Question(text, answer, is_quiz, options)
                else:
                    question = Question(text, answer, is_quiz)
                question.add_question()
            except ValueError as e:
                print(e)

        elif choice == "2":
            # Enter Statistics viewing mode
            print("\nStatistics viewing mode:")
        elif choice == "3":
            # Enter Disable/Enable questions mode
            print("\nDisable/Enable questions mode:")
            pass
        elif choice == "4":
            # Enter Practice mode
            print("\nPractice mode:")
            practice_mode.practice()

        elif choice == "5":
            # Enter Test mode
            print("\nTest mode:")
            test_mode.take_test(input("How many questions? "))

        elif choice == "6":
            # Exit the program
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
