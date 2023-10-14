import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QTransform, QPainter

import tarot
import random

class TarotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tarot Reading')
        self.setGeometry(100, 100, 100, 100)

        # Create widgets for the GUI
        self.spreadview = QLabel()
        self.reading_textbox = QLabel()
        self.reading_textbox.setWordWrap(True)

        # Create layout for the GUI
        layout = QVBoxLayout()
        #card_layout = QHBoxLayout()
        layout.addWidget(self.spreadview)
        #layout.addLayout(card_layout)
        layout.addWidget(self.reading_textbox)

        # Add a button to draw cards
        draw_button = QPushButton('Draw Cards', self)
        draw_button.clicked.connect(self.draw_cards)
        layout.addWidget(draw_button)

        # Set the layout for the widget
        self.setLayout(layout)

    def draw_cards(self):
        # TODO: Implement your tarot card drawing logic here
        # For now, we'll just randomly select three cards
        deck = tarot.getFullDeck()
        random.shuffle(deck)

        spreadlayout = {"Past": (0,0,0), "Present": (1,0,0), "Future": (2,0,0)}
        spread = tarot.drawSpread(deck, spreadlayout)

        cardw = 175
        cardh = 300

        cardgap = cardw
        rows = 0
        columns = 0
        for spot in spreadlayout:
            if spreadlayout[spot][0] > columns:
                columns = spreadlayout[spot][0]
            if spreadlayout[spot][1] > rows:
                row = spreadlayout[spot][1]
            if spreadlayout[spot][2] != 0:
                cardgap = cardh

        # Display the selected cards in the GUI
        clxoffset = 50
        clyoffset = 0

        # Create the card image
        cardlayout = QPixmap(int((columns+1)*cardgap)+clxoffset*2, int((rows+1)*cardh)+clyoffset*2)
        cardlayout.fill(Qt.transparent)
        painter = QPainter(cardlayout)
        for i, card in enumerate(spread):
            # Load the card image
            card_filename = card[2]
            card_image = QPixmap("Rider Waite/"+card_filename+".jpg")

            #Scale cards keeping aspect ratio
            card_image = card_image.scaled(cardw, cardh, Qt.KeepAspectRatio)

            spreadpos = spreadlayout[card[0]]

            # Rotate the card image (just for demonstration purposes)
            if spreadpos[2] != 0:
                #rotation_angle = 90 #(i + 1) * 10
                rotation_angle = spreadpos[2]
                card_image = card_image.transformed(QTransform().rotate(rotation_angle))
                x = clxoffset+(cardgap*(spreadpos[0])-50)
                y = clyoffset+((cardh*spreadpos[1])+50)
            else:
                x = clxoffset+(cardgap*spreadpos[0])
                y = clyoffset+(cardh*spreadpos[1])
            
            painter.drawPixmap(x, y, card_image)
        painter.end()

            # Set the image for the label
            #self.card_labels[position].setPixmap(card_image)
        self.spreadview.setPixmap(cardlayout)
        #Generate Reading
        reading = tarot.getTarotReading(spread)
        # Display the reading in the GUI
        self.reading_textbox.setText(reading)
        self.adjustSize()

# Create the application and show the GUI
app = QApplication(sys.argv)
gui = TarotGUI()
gui.show()
sys.exit(app.exec_())
