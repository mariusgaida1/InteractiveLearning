import unittest
from interactiveLearning import Question, QuestionManager, PracticeMode

class TestQuestion(unittest.TestCase):
    def test_question_text_empty(self):
        # Test if ValueError is raised when text is empty
        with self.assertRaises(ValueError):
            question = Question("", "Answer", "")

class TestQuestionManager(unittest.TestCase):
    def setUp(self):
        # Initialize a QuestionManager object for testing
        self.question_manager = QuestionManager("questions.csv")
    
    def test_load_questions(self):
        # Test if questions are loaded properly from a CSV file
        self.question_manager.load_questions()
        self.assertTrue(len(self.question_manager.questions) > 0)

class TestPracticeMode(unittest.TestCase):
    
    def setUp(self):
        # Initialize a QuestionManager object for testing
        self.question_manager = QuestionManager("questions.csv")
        # Initialize a PracticeMode object for testing
        self.practice_mode = PracticeMode(self.question_manager)
    
    def test_select_question(self):
        # Test if a question is selected properly based on weights
        # Prepare some mock active questions with different shown counts
        active_questions = [
            {"question_id": 1, "shown": 0},
            {"question_id": 2, "shown": 100},
            {"question_id": 3, "shown": 200}
        ]
        for _ in range(20):
            selected_question = self.practice_mode._select_question(active_questions)
            # Ensure that the selected question has the highest weight
            self.assertEqual(selected_question["question_id"], 1)