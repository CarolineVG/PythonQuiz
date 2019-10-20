from tkinter import *
import json
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

class Main():
    def __init__(self):
        parsed_json = None
        with open("data.json", 'r') as f:
            parsed_json = json.load(f)
            f.close()

        for a in range(0, len(parsed_json)):
            a = str(a)
            question = parsed_json[a]["question"]
            answers = parsed_json[a]["answers"]
            correctAnswer = parsed_json[a]["correctAnswer"]
            self.QuestionGenerator(
                question, answers, correctAnswer)

        # shuffle the question array
        for x in range(0, random.randrange(0, 100)):
            random.shuffle(questionArray)

        # ask questions after question data is loaded
        self.askQuestions()

    # used for creating the array of questions
    def QuestionGenerator(self, question, answers, correctAnswer):
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
        for questionDict in questionArray:
            global correctAnswer
            global answers
            isCorrect = None
            question = questionDict["question"]
            answers = questionDict["answers"]
            correctAnswer = questionDict["correctAnswer"].lower()

            # add question to label
            questionLabel = Label(playQuestionScreen, text=question, fg='#FC8FB8', bg='#CCF2FF', font=('arial', 14, 'bold')).pack()

            # radio buttons defined seperatly due to issues with freezing
            r1 = Radiobutton(playQuestionScreen, text=answers[0], variable=radiobuttonValue, value=0,
                             command=self.ShowChoice).pack()
            r2 = Radiobutton(playQuestionScreen, text=answers[1], variable=radiobuttonValue, value=1,
                             command=self.ShowChoice).pack()
            r3 = Radiobutton(playQuestionScreen, text=answers[2], variable=radiobuttonValue, value=2,
                             command=self.ShowChoice).pack()
            r4 = Radiobutton(playQuestionScreen, text=answers[3], variable=radiobuttonValue, value=3,
                             command=self.ShowChoice).pack()

            radiobuttonsList.append(r1)
            radiobuttonsList.append(r2)
            radiobuttonsList.append(r3)
            radiobuttonsList.append(r4)

            # wait for a radio button to be pressed, then move on to next question
            playQuestionScreen.wait_variable(radiobuttonValue)
        # end quiz
        if questionsAnswered == len(questionArray):
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print("-------Final Score: " + str(score) + "/4------")
            print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")


if __name__ == "__main__":
    Main()
