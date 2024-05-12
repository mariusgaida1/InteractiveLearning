import csv


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
        self.attempts = 0
        self.correct_attempts = 0
        self.options = options
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


def main():
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
                        if option.lower() == 'done':
                            break
                        options.append(option)
                    question = Question(text, answer, is_quiz, options)
                else:
                    question = Question(text, answer, is_quiz)
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
        elif choice == "5":
            # Enter Test mode
            print("\nTest mode:")
            pass
        elif choice == "6":
            # Exit the program
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
