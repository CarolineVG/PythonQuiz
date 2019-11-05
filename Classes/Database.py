# class Database
import sqlite3


class Database:
    def __init__(self):
        # quizes
        self.conn = sqlite3.connect("Quiz.db")
        self.cursor = self.conn.cursor()
        self.conn.execute('CREATE TABLE IF NOT EXISTS Quizes(Id INTEGER NOT NULL PRIMARY KEY, QuizName TEXT)')

        # questions
        self.conn.execute('CREATE TABLE IF NOT EXISTS Questions(Id INTEGER NOT NULL PRIMARY KEY, QuizId NUMBER, Question TEXT, Solution NUMBER, Answer1 TEXT, Answer2 TEXT, Answer3 TEXT, Answer4 TEXT, Timer NUMBER, Points NUMBER)')
        self.conn.commit()

    def getConnection(self):
        self.conn = sqlite3.connect("Quiz.db")
        return self.conn

    def closeConnection(self):
        self.conn.close()

    # # get data
    # def getData(self):
    #     self.cursor.execute('SELECT * FROM Questions')
    #     records = self.cursor.fetchall()
    #     print(f'data from db: {records}')
    #     self.conn.commit()
    #
    # # insert data
    # def insertData(self, quizId, question, solution, answer1, answer2, answer3, answer4):
    #     self.conn.execute('INSERT INTO Questions(QuizId, Question, Solution, Answer1, Answer2, Answer3, Answer4) VALUES(?,?,?,?,?,?,?,?,?)', (quizId, question, solution, answer1, answer2, answer3, answer4, 60, 10))
    #     self.conn.commit()
    #
    #     # this does work!
    #     self.cursor.execute('SELECT * FROM Questions')
    #     records = self.cursor.fetchall()
    #     print(f'after db - {records}')
    #
