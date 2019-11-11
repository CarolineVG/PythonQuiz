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

    def sendQuestionToServer(self):
        # test with first question
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Questions WHERE id=1')
        records = cursor.fetchall()
        print(f'first question - {records}')

        question = records[0]
        answers = []
        answers.append((question[5]))
        answers.append((question[6]))
        answers.append((question[7]))
        answers.append((question[8]))

        print(f'answers: {answers}')

        # question = '{"type":"question", "sender": "Host", "id":"' + question['Id'] + '", "question": "' + json.dumps(question['Question']) + '}'

        # + '", "options":' + json.dumps(answers) + ',"time":' + question['Timer'] + question['Points'] + '}'

        questionsDictionary = []

        question = {
            "type": "question",
            "sender": "Host",
            "id": question[0],
            "question": question[2],
            "solution": question[3],
            "options": {
                "answer1": question[4],
                "answer2": question[5],
                "answer3": question[6],
                "answer4": question[7]
            },
            "time": question[8],
            "points": question[9]
        }

        questionsDictionary.append(question)

        print(f'string: {question}')

