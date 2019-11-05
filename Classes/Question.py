# class Question
from Classes.Database import Database


class Question:
    questionNumber = 0

    def __init__(self, quizId, question, solution, answer1, answer2, answer3, answer4, timer, points):
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
    def addQuestionToDatabase(self):
        db = Database()
        conn = db.getConnection()

        # insert one value: var should be a tuple
        conn.execute('INSERT INTO Questions(QuizId, Question, Solution, Answer1, Answer2, Answer3, Answer4, Timer, Points) VALUES'
                     '(?,?,?,?,?,?,?,?,?)', (self.quizId, self.question, self.solution, self.answer1, self.answer2, self.answer3, self.answer4, 60, 10))
        conn.commit()

    def getQuestionFromDatabase(self):
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Questions')
        records = cursor.fetchall()
        print(f'db - {records}')


