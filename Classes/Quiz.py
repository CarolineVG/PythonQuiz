# class Quiz
from Classes.Database import Database


class Quiz:
    def __init__(self):
        self.quizName = ''
        self.id = id

    def addQuizToDatabase(self):
        db = Database()
        conn = db.getConnection()

        # insert one value: var should be a tuple
        conn.execute('INSERT INTO Quizes(QuizName) VALUES(?)', (self.quizName,))

        conn.commit()
        db.closeConnection()

    def setQuizName(self, value):
        self.quizName = value

    def getDataFromDatabase(self):
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Quizes')
        records = cursor.fetchall()

        return records

    def getIdFromQuizName(self, val):
        quizName = val
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        # WHERE: you need to pass the var as a tuple
        cursor.execute('SELECT Id FROM Quizes WHERE QuizName = ?', (quizName,))
        records = cursor.fetchone()

        db.closeConnection()

        return records

    def deleteQuiz(self, val):
        id = val
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Quizes WHERE Id = ?', (id,))
        conn.commit()
        db.closeConnection()
