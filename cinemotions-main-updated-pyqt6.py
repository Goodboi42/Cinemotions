import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWebEngineWidgets import QWebEngineView
import spacy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineMotions")
        self.setGeometry(100, 100, 1000, 800)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.file_button = QtWidgets.QPushButton("Select Script File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.character_input = QtWidgets.QLineEdit()
        self.character_input.setPlaceholderText("Enter character names (comma-separated)")
        layout.addWidget(self.character_input)

        self.analyze_button = QtWidgets.QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_script)
        layout.addWidget(self.analyze_button)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.statusBar().showMessage("Ready")

        self.nlp = spacy.load("en_core_web_sm")
        self.sid = SentimentIntensityAnalyzer()

    # ... [rest of the class implementation remains the same]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
