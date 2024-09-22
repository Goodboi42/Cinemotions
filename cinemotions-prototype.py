import sys
import os
from PySide6 import QtWidgets, QtCore, QtGui
import spacy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineMotions Prototype")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # File selection
        self.file_button = QtWidgets.QPushButton("Select Script File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Character selection
        self.character_input = QtWidgets.QLineEdit()
        self.character_input.setPlaceholderText("Enter character name")
        layout.addWidget(self.character_input)

        # Analyze button
        self.analyze_button = QtWidgets.QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_script)
        layout.addWidget(self.analyze_button)

        # Matplotlib Figure
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Status bar
        self.statusBar().showMessage("Ready")

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

    def select_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Script File", "", "Text Files (*.txt)")
        if file_name:
            self.file_path = file_name
            self.statusBar().showMessage(f"Selected file: {os.path.basename(file_name)}")

    def analyze_script(self):
        if not hasattr(self, 'file_path'):
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a script file first.")
            return

        character = self.character_input.text().strip()
        if not character:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a character name.")
            return

        # Read the script
        with open(self.file_path, 'r', encoding='utf-8') as file:
            script = file.read()

        # Simple sentiment analysis
        doc = self.nlp(script)
        sentences = list(doc.sents)
        sentiment_scores = []

        for sent in sentences:
            if character.lower() in sent.text.lower():
                sentiment_scores.append(sent.sentiment)

        # Plot the results
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(sentiment_scores)
        ax.set_title(f"Emotional Arc for {character}")
        ax.set_xlabel("Scene")
        ax.set_ylabel("Sentiment")
        self.canvas.draw()

        self.statusBar().showMessage(f"Analysis complete for {character}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
