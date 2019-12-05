# class Question
from Classes.Database import Database


class Question:

    def __init__(self):
        self.quizId = 0
        self.question = ''
        self.solution = 0
        self.answer1 = ''
        self.answer2 = ''
        self.answer3 = ''
        self.answer4 = ''
        self.timer = 0
        self.points = 0

    def addQuestion(self, quizId, question, solution, answer1, answer2, answer3, answer4, timer, points):
        self.quizId = quizId
        self.question = question
        self.solution = solution
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4
        self.timer = timer
        self.points = points

    def addQuestionToDatabase(self):
        db = Database()
        conn = db.getConnection()

        # insert one value: var should be a tuple
        conn.execute('INSERT INTO Questions(QuizId, Question, Solution, Answer1, Answer2, Answer3, Answer4, Timer, Points) VALUES'
                     '(?,?,?,?,?,?,?,?,?)', (self.quizId, self.question, self.solution, self.answer1, self.answer2, self.answer3, self.answer4, self.timer, self.points))
        conn.commit()
        db.closeConnection()

    def getQuestionFromDatabase(self):
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Questions')
        records = cursor.fetchall()

    def createQuizWithQuestions(self, val):
        # CREATE LIST OF ALL QUESTION FROM SAME QUIZ ID
        quizId = val

        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Questions WHERE QuizId = ?', (quizId,))
        records = cursor.fetchall()
        questionsDictionary = []

        i = 0
        for i in range(len(records)):
            q = records[i]

            # options
            options = {}

            if q[4]:
                options["option1"] = q[4]
            if q[5]:
                options["option2"] = q[5]
            if q[6]:
                options["option3"] = q[6]
            if q[7]:
                options["option4"] = q[7]

            question = {
                "id": str(q[0]),
                "question": q[2],
                "solution": q[3],
                "options": options,
                "time": q[8],
                "score": q[9]
            }

            questionsDictionary.append(question)
            i = i+1

        db.closeConnection()
        return questionsDictionary

    def deleteQuestion(self, val):
        id = val
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Questions WHERE QuizId = ?', (id,))
        conn.commit()
        db.closeConnection()
