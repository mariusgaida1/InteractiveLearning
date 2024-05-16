# InteractiveLearning
An interactive learning tool that allows users to create, practice, and test their knowledge using multiple-choice and freeform text questions. The program track user statistics and provide options to manage the questions.
## Requirements
When the program starts, user is able to choose between the following modes:
* Adding questions.
* Statistics viewing.
* Disable/enable questions.
* Practice mode.
* Test mode.
### Adding questions mode:
In this mode, users is able to add two types of questions - quiz questions or free-form text questions. A quiz question requires the user to choose one of the given answer options. A free-form question requires the user to enter some text and compare it with the expected answer to determine whether it is correct.

The questions are saved in a file so that once the program is closed and opened again, the questions remain.

The user is not be able to enter practice or test modes until at least 5 questions have been added.
### Statistics viewing mode:
The program print out all the questions currently in the system. Each question list: its unique ID number; whether the question is active or not; the question text; the number of times it was shown during practice or tests; the percentage of times it was answered correctly.
### Disable/Enable Questions mode:
Users are able to write the ID of the question they want to disable or enable. The question information (question text, answer) are shown and the user is being asked to confirm whether they want to disable/enable it. Disabled questions are not appear in practice and test modes. The enabled/disabled status is stored in a file, within others questions attributes.
### Practice mode:
A mode in which questions are given non-stop so that the user can practice. However, the questions are chosen in such a way that the questions that are answered correctly become less likely to appear, while questions that are answered incorrectly become more likely to appear.
### Test mode:
A mode for testing your knowledge. Users first select the number of questions for the test which is not larger than the total number of questions added. The questions get chosen fully randomly and each question can only appear once at most in the test. At the end of the questions, the user is shown the score. The list of scores is saved in a separate results.txt file – the date and time are added next to the score as well.
