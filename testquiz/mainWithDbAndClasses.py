import sqlite3
from tkinter import *
import random

# vars
questionArray = []
score = 0
questionsAnswered = 0

# home
playQuestionScreen = Tk()
playQuestionScreen.geometry('600x667')
playQuestionScreen.title('Play Quiz')

# create radiobutton after screen is created
radiobuttonValue = IntVar()
radiobuttonValue.set(1)
radiobuttonsList = []
answersList = []
correctAnswer = ""


class Database():

    def __init__(self):
        # quizes
        self.conn = sqlite3.connect("testQuiz.db")
        self.cursor = self.conn.cursor()
        self.conn.execute('CREATE TABLE IF NOT EXISTS Quizes(Id INTEGER NOT NULL PRIMARY KEY, quizName TEXT, Description TEXT)')
        # questions
        self.conn.execute('CREATE TABLE IF NOT EXISTS Questions(Id INTEGER NOT NULL PRIMARY KEY, QuizId NUMBER, Question TEXT, Solution NUMBER, Answer1 TEXT, Answer2 TEXT, Answer3 TEXT, Answer4 TEXT)')
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()

    # get data
    def getData(self):
        self.cursor.execute('SELECT * FROM Questions')
        records = self.cursor.fetchall()
        dataList = list(records)
        print(f'data from db: {records}')
        self.conn.commit()
        return dataList

    # insert data
    def insertData(self, quizId, question, solution, answer1, answer2, answer3, answer4):
        self.conn.execute('INSERT INTO Questions(QuizId, Question, Solution, Answer1, Answer2, Answer3, Answer4) VALUES(?,?,?,?,?,?,?)', (quizId, question, solution, answer1, answer2, answer3, answer4))
        self.conn.commit()

        # this does work!
        self.cursor.execute('SELECT * FROM Questions')
        records = self.cursor.fetchall()
        print(f'after db - {records}')


class Main():
    def __init__(self):
        # get questions from db
        print(f'get data from db')
        db = Database()
        myList = db.getData()

        print(f'my list: {myList}')
        for i in myList:
            question = i[2]
            # add all answers
            answers = []
            answers.append((i[4]))
            answers.append((i[5]))
            answers.append((i[6]))
            answers.append((i[7]))

            # answer 1,2,3,4 is correct: get index of correct answer
            index = i[3]
            correctAnswer = answers[index-1]
            print(f'q: {question}, solution: {correctAnswer}, answers: {answers}')

            self.createQuestion(question, answers, correctAnswer)

        # shuffle the questions
        for x in range(0, random.randrange(0, 100)):
            random.shuffle(questionArray)

        # ask questions after question data is loaded
        self.askQuestions()

    # used for creating the array of questions
    def createQuestion(self, question, answers, correctAnswer):
        question = {
            "question": question,
            "answers": answers,
            "correctAnswer": correctAnswer
        }
        questionArray.append(question)

    # Callback for radiobutton answer click, handles score, removes old radio buttons and questions answered
    def ShowChoice(self):
        global questionsAnswered
        questionsAnswered += 1
        if answers[radiobuttonValue.get()].lower() == correctAnswer.lower():
            print("correct")
            global score
            score += 1
            # destroy radiobuttons
            #for rb in radiobuttonsList:
             #   rb.remove()
        else:
            print("wrong")
            # destroy radiobuttons
            #for rb in radiobuttonsList:
             #   rb.remove()

    # waiting for button press reference: https://stackoverflow.com/questions/44790449/making-tkinter-wait-untill-button-is-pressed
    def askQuestions(self):
        print(f'ask questions')

        # loops the questions in the array
        for question in questionArray:
            global correctAnswer
            global answers
            isCorrect = None
            newQuestion = question["question"]
            answers = question["answers"]
            correctAnswer = question["correctAnswer"].lower()

            # add question to label
            questionLabel = Label(playQuestionScreen, text=newQuestion, fg='#FC8FB8', bg='#CCF2FF', font=('arial', 14, 'bold')).pack()

            r1 = Radiobutton(playQuestionScreen, text=answers[0], variable=radiobuttonValue, value=0,
                             command=self.ShowChoice).pack()
            r2 = Radiobutton(playQuestionScreen, text=answers[1], variable=radiobuttonValue, value=1,
                             command=self.ShowChoice).pack()
            r3 = Radiobutton(playQuestionScreen, text=answers[2], variable=radiobuttonValue, value=2,
                             command=self.ShowChoice).pack()
            r4 = Radiobutton(playQuestionScreen, text=answers[3], variable=radiobuttonValue, value=3,
                             command=self.ShowChoice).pack()

            # add radiobuttons to list
            radiobuttonsList.append(r1)
            radiobuttonsList.append(r2)
            radiobuttonsList.append(r3)
            radiobuttonsList.append(r4)

            # wait for a radio button to be pressed, then move on to next question
            playQuestionScreen.wait_variable(radiobuttonValue)

        # end quiz
        if questionsAnswered == len(questionArray):
            print(f'score: {str(score)}')


if __name__ == "__main__":
    Main()
