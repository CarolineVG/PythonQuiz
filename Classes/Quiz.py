# class Quiz
from Classes.Database import Database


class Quiz:
    def __init__(self, id, quizName):
        self.id = id
        self.quizName = quizName

    def addQuizToDatabase(self):
        db = Database()
        conn = db.getConnection()

        # insert one value: var should be a tuple
        conn.execute('INSERT INTO Quizes(QuizName) VALUES(?)', (self.quizName,))

        conn.commit()

    def getDataFromDatabase(self):
        db = Database()
        conn = db.getConnection()
        cursor = conn.cursor()

        # get data from db
        cursor.execute('SELECT * FROM Quizes')
        records = cursor.fetchall()
        print(f'db - {records}')

