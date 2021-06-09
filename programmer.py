import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from urllib.request import urlopen
import json
import pandas as pd
import random


class TriviaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.WIDGETS = {
            "logos": [],
            "buttons": [],
            "score": [],
            "questions": [],
            "answers": [],
            "messages": []
        }

        self.parameters = {
            "questions": [],
            "answers": [],
            "correct": [],
            "score": [],
            "index": []
        }
        self.setWindowTitle("Who wants to be a Programmer??")
        self.screen_width, self.screen_height = (
            self.geometry().width(),
            self.geometry().height(),
        )
        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.grid = QGridLayout()
        wid.setLayout(self.grid)
        self.setStyleSheet("background: #161219;")
        self.setFixedWidth(1000)
        self.showMaximized()
        self.mainFrame()

    def getDatafromAPI(self):
        # open api link to database
        with urlopen("https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple") as webpage:
            # read JSON file & extract data
            data = json.loads(webpage.read().decode())
            self.df = pd.DataFrame(data["results"])

    def checkIndex(self):
        r = random.randint(0, 49)
        return r if r not in self.parameters["index"] else self.checkIndex()

    def clear_parameters(self):
        # clear the global dictionary of parameters
        for parm in self.parameters:
            if self.parameters[parm] != []:
                self.parameters[parm] = []
        # populate with initial index & score values
        idx = self.checkIndex()
        self.parameters["index"].append(idx)
        self.parameters["score"].append(0)

    def preload_data(self, idx):
        # idx parm: selected randomly time and again at function call
        question = self.df["question"][idx]
        correct = self.df["correct_answer"][idx]
        wrong = self.df["incorrect_answers"][idx]

        # fixing charecters with bad formatting
        formatting = [
            ("#039;", "'"),
            ("&'", "'"),
            ("&quot;", '"'),
            ("&lt;", "<"),
            ("&gt;", ">")
        ]

        # replace bad charecters in strings
        for tuple in formatting:
            question = question.replace(tuple[0], tuple[1])
            correct = correct.replace(tuple[0], tuple[1])
        # replace bad charecters in lists
        for tuple in formatting:
            wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

        # store local values globally
        self.parameters["questions"].append(question)
        self.parameters["correct"].append(correct)

        all_answers = wrong + [correct]
        random.shuffle(all_answers)

        self.parameters["answers"] = all_answers[:]

        for i, widget in enumerate(self.WIDGETS["answers"]):
            widget.setText(self.parameters["answers"][i])
        self.WIDGETS["score"][-1].setText(str(sum(self.parameters["score"])))
        self.WIDGETS["questions"][0].setText(self.parameters["questions"][-1])
        # print correct answer to the terminal (for testing)
        print(self.parameters["correct"][-1])

    def create_buttons(self, answer):
        button = QPushButton(answer)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            '''
            border: 4px solid '#BC006C';
            color: white;
            font-family: 'shanti';
            font-size: 16px;
            border-radius: 25px;
            padding: 15px 0;
            margin: 20px 50px;
            margin-top: 20px;
            }
            *:hover{
                background: '#BC006C';
            }
            '''
        )
        button.clicked.connect(lambda x: self.is_correct(button))
        return button

    def is_correct(self, btn):
        if btn.text() == self.parameters["correct"][-1]:
            # a function to evaluate wether user answer is correct
            self.parameters["score"].append(10 if btn.text() == self.parameters["correct"][-1] else 0) 
            self.parameters["index"].append(self.checkIndex())
            # preload data for new index value
            self.preload_data(self.parameters["index"][-1])
            if sum(self.parameters["score"]) == 100:
                # WON THE GAME
                self.clear_widgets()
                self.frame3()
        else:
            # WRONG ANSWER - LOST GAME
            self.clear_widgets()
            self.frame4()

    def clear_widgets(self):
        ''' hide all existing widgets and erase
            them from the global dictionary'''
        for _, widget in self.WIDGETS.items():
            if widget != []:
                for w in widget:
                    w.hide()
            if widget:
                self.WIDGETS[_] = []

        # print(self.WIDGETS)
    def start_game(self):
        # start the game, reset all widgets and parameters
        self.clear_widgets()
        self.getDatafromAPI()
        self.clear_parameters()
        # display the game frame
        self.frame1()
        self.preload_data(self.parameters["index"][-1])

    def mainFrame(self):
        # Clear all widgets before coming to mainframe
        self.clear_widgets()
        self.clear_parameters()
        # display logo
        image = QPixmap('logo.png')
        logo = QLabel()
        logo.setPixmap(image)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet("margin-top: 100px;")
        self.WIDGETS['logos'].append(logo)
        # button widget
        button = QPushButton("Play")
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            '''
            *{
                border: 4px solid '#BC006C';
                border-radius: 45px;
                font-size: 35px;
                color: 'white';
                padding: 25px 0;
                margin: 100px 200px;
            }
            *:hover{
                background: '#BC006C';
            }
            '''

        )
        self.WIDGETS['buttons'].append(button)
        self.grid.addWidget(self.WIDGETS['logos'][-1], 0, 0, 1, 2)
        self.grid.addWidget(self.WIDGETS['buttons'][-1], 1, 0, 1, 2)
        button.clicked.connect(self.start_game)

    def frame1(self):
        score = QLabel("80")
        score.setAlignment(QtCore.Qt.AlignCenter)
        score.setStyleSheet(
            '''
            font-size: 35px;
            color: white;
            padding: 15px 10px;
            margin: 20px 200px;
            background: #64A314;
            border: 1px solid #64A314;
            border-radius: 35px;
            '''
        )
        self.WIDGETS['score'].append(score)

        # Questions
        question = QLabel("Placeholder text will go here")
        question.setAlignment(QtCore.Qt.AlignCenter)
        question.setWordWrap(True)
        question.setStyleSheet(
            '''
            font-family: 'shanti';
            font-size: 25px;
            color: 'white';
            padding: 75px;
            '''
        )

        self.WIDGETS['questions'].append(question)
        for i in range(1, 5):
            button = self.create_buttons(f"answer{i}")  # change those options
            self.WIDGETS['answers'].append(button)
        # print(WIDGETS['answers'])

        image = QPixmap('logo_bottom.png')
        logo = QLabel()
        logo.setPixmap(image)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet("margin-top: 75px; margin-bottom: 30px")
        self.WIDGETS['logos'].append(logo)

        self.grid.addWidget(self.WIDGETS['questions'][-1], 1, 0, 1, 2)
        self.grid.addWidget(self.WIDGETS['score'][-1], 0, 1)
        for i, button in enumerate(self.WIDGETS['answers'], 1):
            if i <= 2:
                self.grid.addWidget(button, 2, i-1)
            else:
                self.grid.addWidget(button, 3, i-3)
        self.grid.addWidget(self.WIDGETS['logos'][-1], 4, 0, 1, 2)

    #*********************************************
    #             FRAME 3 - WIN GAME
    #*********************************************

    def frame3(self):
        #congradulations widget
        message = QLabel("Congratulations! You\nare a true programmer!\n your score is:")
        message.setAlignment(QtCore.Qt.AlignRight)
        message.setStyleSheet(
            "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
            )
        self.WIDGETS["messages"].append(message)

        #score widget
        score = QLabel("100")
        score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
        self.WIDGETS["score"].append(score)

        #go back to work widget
        message2 = QLabel("OK. Now go back to WORK.")
        message2.setAlignment(QtCore.Qt.AlignCenter)
        message2.setStyleSheet(
            "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
            )
        self.WIDGETS["messages"].append(message2)

        #button widget
        button = QPushButton('TRY AGAIN')
        button.setStyleSheet(
            "*{background:'#BC006C'; padding:25px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#ff1b9e';}"
            )
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.clicked.connect(self.mainFrame)

        self.WIDGETS["buttons"].append(button)

        #logo widget
        pixmap = QPixmap('logo_bottom.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet(
            "padding :10px; margin-top:75px; margin-bottom: 20px;"
        )
        self.WIDGETS["logos"].append(logo)

        #place widgets on the grid
        self.grid.addWidget(self.WIDGETS["messages"][-1], 2, 0)
        self.grid.addWidget(self.WIDGETS["score"][-1], 2, 1)
        self.grid.addWidget(self.WIDGETS["messages"][-1], 3, 0, 1, 2)
        self.grid.addWidget(self.WIDGETS["buttons"][-1], 4, 0, 1, 2)
        self.grid.addWidget(self.WIDGETS["logos"][-1], 5, 0, 2, 2)


    def frame4(self):
        #sorry widget
        message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
        message.setAlignment(QtCore.Qt.AlignRight)
        message.setStyleSheet(
            "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
            )
        self.WIDGETS["messages"].append(message)

        #score widget
        score = QLabel(str(sum(self.parameters["score"])))
        score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
        self.WIDGETS["score"].append(score)

        #button widget
        button = QPushButton('TRY AGAIN')
        button.setStyleSheet(
            '''*{
                padding: 25px 0px;
                background: '#BC006C';
                color: 'white';
                font-family: 'Arial';
                font-size: 35px;
                border-radius: 40px;
                margin: 10px 200px;
            }
            *:hover{
                background: '#ff1b9e';
            }'''
            )
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.clicked.connect(self.mainFrame)

        self.WIDGETS["buttons"].append(button)

        #logo widget
        pixmap = QPixmap('logo_bottom.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet(
            "padding :10px; margin-top:75px;"
        )
        self.WIDGETS["logos"].append(logo)

        #place widgets on the grid
        self.grid.addWidget(self.WIDGETS["messages"][-1], 1, 0)
        self.grid.addWidget(self.WIDGETS["score"][-1], 1, 1)
        self.grid.addWidget(self.WIDGETS["buttons"][-1], 2, 0, 1, 2)
        self.grid.addWidget(self.WIDGETS["logos"][-1], 3, 0, 1, 2)

app = QApplication(sys.argv)
trivia = TriviaApp()
sys.exit(app.exec())
