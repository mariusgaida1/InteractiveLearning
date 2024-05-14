import unittest
from interactiveLearning import Question, QuestionManager

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