class Question:
    def __init__(self, id, type, text, options=None, answer=None):
        pass

class QuestionManager:
    def __init__(self):
        pass

    def add_question(self, question):
        pass

    def disable_question(self, id):
        pass

    def enable_question(self, id):
        pass

    def view_statistics(self):
        pass

    def save_questions(self):
        pass

    def load_questions(self):
        pass

class PracticeSession:
    def __init__(self, question_manager):
        pass

    def start(self):
        pass

class TestSession:
    def __init__(self, question_manager):
        pass

    def start(self):
        pass

class Profile:
    def __init__(self, name):
        pass

    def update_statistics(self, question_id, is_correct):
        pass

    def save_statistics(self):
        pass

    def load_statistics(self):
        pass


def main():
    pass

if __name__ == "__main__":
    main()
