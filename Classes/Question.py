# class Question
import json

from Classes.Database import Database


class Question:
    questionNumber = 0

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

    def getQuestionFromDatabase(self):
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Questions')
        records = cursor.fetchall()
        print(f'db - {records}')

    def createQuizWithQuestions(self, val):
        # CREATE LIST OF ALL QUESTION FROM SAME QUIZ ID
        quizId = val

        # test with first question
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Questions WHERE QuizId = ?', (quizId,))
        records = cursor.fetchall()
        print(f'questions {quizId} - {records}')

        # question = '{"type":"question", "sender": "Host", "id":"' + question['Id'] + '", "question": "' + json.dumps(question['Question']) + '}'

        # + '", "options":' + json.dumps(answers) + ',"time":' + question['Timer'] + question['Points'] + '}'

        questionsDictionary = []

        i = 0


        for i in range(len(records)):
            q = records[i]

            # options
            options = {}

            if q[4] != None:
                options["option1"] = q[4]
            if q[5] != None:
                options["option2"] = q[5]
            if q[6] != None:
                options["option3"] = q[6]
            if q[7] != None:
                options["option4"] = q[7]

            question = {
                "id": str(q[0]),
                "question": q[2],
                "solution": q[3],
                "options": options,
                "time": q[8],
                "points": str(q[9]),
                "score": str(10)
            }

            questionsDictionary.append(question)

            print(f'string: {question}')
            i = i+1

        print(f'Quiz: {questionsDictionary}')
        return questionsDictionary
