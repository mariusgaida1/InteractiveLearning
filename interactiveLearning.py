import csv
import random 
from datetime import datetime
import ast


class Question:
    """
    Class representing a question.

    Attributes:
        filename (str): The filename of the CSV file containing questions.
        question_id (int): The ID of the question.
        text (str): The text of the question.
        answer (str): The answer to the question.
        is_quiz (bool): Indicates whether the question is a quiz or not.
        is_active (bool): Indicates whether the question is active or not.
        shown (int): The number of times the question has been shown.
        correct (int): The number of times the question has been answered correctly.
        options (list): The options for the quiz question.
    """
    @classmethod
    def find_max_question_id(cls, filename):
        """
        Find the maximum question ID from the CSV file.

        Parameters:
            filename (str): The filename of the CSV file.

        Returns:
            int: The maximum question ID.
        """
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

    def add_question(self):
        """
        Add the question to the CSV file.
        """
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
    """
    Class for managing questions.

    Attributes:
        filename (str): The filename of the CSV file containing questions.
        questions (list): A list of dictionaries representing questions.
    """
    def __init__(self, filename="questions.csv"):
        self.filename = filename
        self.questions = []

    def load_questions(self):
        """
        Load questions from the CSV file into memory.
        """
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

    def get_active_questions(self):
        """
        Get active questions.

        Returns:
            list: A list of active questions.
        """
        return [
            question for question in self.questions if question["is_active"] == "True"
        ]

    def disable_enable_question(self, question_id):
        """
        Disable or enable a question based on the given question ID.

        Parameters:
            question_id (str): The ID of the question to be disabled or enabled.
        """
        for question in self.questions:
            if question["question_id"] == question_id:
                # Confirm user action
                print(type(question["question_id"]))
                if question["is_active"] == "True":
                    confirm = input('Type "Yes" to confirm question disabling: ')
                    if confirm.lower().strip() == "yes":
                        question["is_active"] = "False"
                        break
                elif question["is_active"] == "False":
                    confirm = input('Type "Yes" to confirm question enabling: ')
                    if confirm.lower().strip() == "yes":
                        question["is_active"] = "True"
                        break

        # Update the CSV file after modification
        self.update_csv_file()

    def update_field(self, question_id, field_name):
        """
        Update a field of a question.

        Parameters:
            question_id (str): The ID of the question.
            field_name (str): The name of the field to update.
        """
        for question in self.questions:
            if question["question_id"] == question_id:
                # Increment the specified field value
                question[field_name] = int(question[field_name]) + 1
                break

        # Update the CSV file after modification
        self.update_csv_file()

    def update_csv_file(self):
        """
        Update the CSV file with the modified questions.
        """
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

    def view_statistics(self):
        """
        View statistics for all questions.
        """
        print("Statistics for all questions:")
        print("-----------------------------------------------------")
        print(
            "{:<10} {:<10} {:<50} {:<15} {:<15}".format(
                "ID", "Active", "Question Text", "Times Shown", "Accuracy (%)"
            )
        )
        print("-----------------------------------------------------")
        for question in self.questions:
            question_id = question["question_id"]
            is_active = question["is_active"]
            question_text = question["text"]
            times_shown = int(question["shown"])
            correct = int(question["correct"])
            if times_shown > 0:
                accuracy = (correct / times_shown) * 100
            else:
                accuracy = 0
            print(
                "{:<10} {:<10} {:<50} {:<15} {:<15.2f}".format(
                    question_id, is_active, question_text[:50], times_shown, accuracy
                )
            )
        print("-----------------------------------------------------")

    def check_answer(self, question):
        """
        Check if the user's answer is correct.

        Parameters:
            question (dict): The question to check.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        if question["is_quiz"].lower().strip() == "yes":

            # Display answer options for quiz questions
            print(question["text"] + "\n")
            options = ast.literal_eval(question["options"])
            random.shuffle(options)
            for index, option in enumerate(options, start=1):
                print(f"{index}. {option}")
            user_choice = int(input("Enter your choice (1, 2, 3, ...): "))
            user_answer = options[user_choice - 1]
        else:
            user_answer = input(question["text"] + "\n")

        if user_answer.strip().lower() == question["answer"].strip().lower():
            self.update_field(question["question_id"], "correct")
            return True
        else:
            return False


class PracticeMode:
    def __init__(self, question_manager):
        self.question_manager = question_manager
        """
        Initializes a PracticeMode instance with a given QuestionManager.

        Parameters:
            question_manager (QuestionManager): An instance of QuestionManager to manage questions.
        """

    def practice(self):
        """
        Starts the practice mode.
        """
        active_questions = self.question_manager.get_active_questions()

        # Check if there are enough active questions to start practice
        if len(active_questions) < 5:
            print("Practice mode requires at least 5 active questions.")
            return
        
        # Loop through practice session until user decides to exit
        while True:
            # Select a question for practice
            question = self._select_question(active_questions)

            # Check the user's answer and provide feedback
            if self.question_manager.check_answer(question):
                print("Correct!")
            else:
                print("Incorrect!")

            # Update the field to indicate the question has been shown
            self.question_manager.update_field(question["question_id"], "shown")
            print()

            # Ask the user if they want to continue practicing or exit
            if (
                input(
                    'Type "done" to go back to the Main Menu or press "Enter" to continue: '
                )
                .lower()
                .strip()
                == "done"
            ):
                print()
                break
            print()

    def _select_question(self, questions):
        """
        Selects a question for practice based on the weights.

        Parameters:
            questions (list): A list of questions to choose from.

        Returns:
            dict: The selected question.
        """
        # Calculate weights for each question based on the number of times it has been shown
        weights = [1 / (int(question["shown"]) + 1) for question in questions]

        # Choose a question randomly based on the weights
        return random.choices(questions, weights=weights, k=1)[0]


class TestMode:
    def __init__(self, question_manager):
        self.question_manager = question_manager
        """
        Initializes TestMode with a QuestionManager instance.

        Parameters:
            question_manager (QuestionManager): The QuestionManager instance to manage questions.
        """

    def take_test(self, num_questions):
        """
        Takes a test with a specified number of questions.

        Parameters:
            num_questions (int): The number of questions to include in the test.
        """

        # Retrieve active questions
        active_questions = self.question_manager.get_active_questions()
        num_questions = int(num_questions)

        # Check if there are enough active questions to conduct the test
        if len(active_questions) < num_questions:
            print("Not enough active questions to take the test.")
            return
        elif len(active_questions) < 5:
            print("Test mode requires at least 5 active questions.")
            return
        
        # Select random questions for the test
        selected_questions = random.sample(active_questions, num_questions)
        print()

        score = 0

        # Loop through each question in the test
        for question in selected_questions:
            if self.question_manager.check_answer(question):
                print("Correct!")
                score += 1
            else:
                print("Incorect!")

            # Update the field to indicate the question has been shown
            self.question_manager.update_field(question["question_id"], "shown")
            print()

        # Calculate and display the score percentage
        score_percentage = (score / num_questions) * 100
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score_info = f"Score: {score}/{num_questions} ({score_percentage:.2f}%) - {current_time}\n"
        
        # Write the score information to a file
        with open("results.txt", "a") as file:
            file.write(score_info)

        # Print test completion message with score
        print(f"Test completed. Score: {score}/{num_questions}")


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
            print("\nAdding questions mode:")
            try:

                # Prompt user to input question text, answer, and quiz type
                text = input("Enter question text: ")
                answer = input("Enter question answer: ")
                is_quiz = input(
                    'Type "Yes" to make quiz question or press "Enter" to have free form question: '
                )

                # Check if the question is a quiz question
                if is_quiz.lower().strip() == "yes":
                    options = []
                    # Prompt user to input options for the quiz question
                    while True:
                        option = input("Enter an option (or type 'done' to finish): ")
                        if option.lower() == "done":
                            break
                        options.append(option)
                    options.append(answer)
                    # Create a new Question instance for the quiz question
                    question = Question(text, answer, is_quiz, options)
                else:
                    # Create a new Question instance for a free form question
                    question = Question(text, answer, is_quiz)

                # Add the question to the question list
                question.add_question()
            except ValueError as e:
                # Handle the case where there's a value error (e.g., empty question text or answer)
                print(e)

        elif choice == "2":
            question_manager = QuestionManager()
            question_manager.load_questions()
            print("\nStatistics viewing mode:")
            question_manager.view_statistics()
        elif choice == "3":
            question_manager = QuestionManager()
            question_manager.load_questions()
            print("\nDisable/Enable questions mode:")
            question_id = input("Please enter question id for enabling or disabling: ")
            question_manager.disable_enable_question(question_id)
        elif choice == "4":
            question_manager = QuestionManager()
            question_manager.load_questions()
            practice_mode = PracticeMode(question_manager)
            print("\nPractice mode:\n")
            practice_mode.practice()

        elif choice == "5":
            question_manager = QuestionManager()
            question_manager.load_questions()
            test_mode = TestMode(question_manager)
            print("\nTest mode:\n")
            test_mode.take_test(input("How many questions? "))

        elif choice == "6":
            # Exit the program
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()


# Pair programming commits https://github.com/mariusgaida1/WarGame/commits/main/