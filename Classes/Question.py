# class Question
class Question:
    questionNumber = 0

    def __init__(self, id, quizId, question, solution, answer1, answer2, answer3, answer4, timer, points):
        self.id = id
        self.quizId = quizId
        self.question = question
        self.solution = solution
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4
        self.timer = timer
        self.points = points

    # to do

