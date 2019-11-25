# class Database
import sqlite3


class Database:
    def __init__(self):
        # quizes
        self.conn = sqlite3.connect("Quiz.db")
        self.cursor = self.conn.cursor()
        self.conn.execute('CREATE TABLE IF NOT EXISTS Quizes(Id INTEGER NOT NULL PRIMARY KEY, QuizName TEXT)')

        # questions
        self.conn.execute('CREATE TABLE IF NOT EXISTS Questions(Id INTEGER NOT NULL PRIMARY KEY, QuizId NUMBER, Question TEXT, Solution TEXT, Answer1 TEXT, Answer2 TEXT, Answer3 TEXT, Answer4 TEXT, Timer NUMBER, Points NUMBER)')
        self.conn.commit()

    def getConnection(self):
        self.conn = sqlite3.connect("Quiz.db")
        return self.conn

    def closeConnection(self):
        self.conn.close()