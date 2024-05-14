import unittest
from interactiveLearning import Question

class TestQuestion(unittest.TestCase):
    def test_question_text_empty(self):
        # Test if ValueError is raised when text is empty
        with self.assertRaises(ValueError):
            question = Question("", "Answer", "")