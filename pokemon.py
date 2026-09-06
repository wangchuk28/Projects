import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


class PokemonDetails(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokemon Details")

        # Loaded once here; drawn on every repaint in paintEvent below.
        self.background_pixmap = QPixmap("images.jpg")

        self.title_label = QLabel("Welcome to Pokemon Details")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #d62828;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Pokemon name")

        self.search_button = QPushButton("Get Pokemon Details")
        self.search_button.clicked.connect(self.get_pokemon_details)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px; padding: 10px;")

        input_row = QHBoxLayout()
        input_row.addWidget(self.name_input)
        input_row.addWidget(self.search_button)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addLayout(input_row)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def paintEvent(self, event):
        # Draw the background image to fill the current window size, every
        # time the window is painted. Widgets in the layout are drawn after
        # this, so they always appear on top.
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)
        super().paintEvent(event)

    def get_pokemon_details(self):
        name = self.name_input.text().strip().lower()
        if not name:
            self.result_label.setText("Please enter a Pokemon name.")
            return

        try:
            response = requests.get(f"{BASE_URL}{name}", timeout=10)
        except requests.RequestException:
            self.result_label.setText("Could not connect to the Pokemon API.")
            return

        if response.status_code != 200:
            self.result_label.setText("Pokemon not found.")
            return

        data = response.json()
        types = ", ".join(t["type"]["name"] for t in data["types"])
        self.result_label.setText(
            f"Name: {data['name'].title()}\n"
            f"ID: {data['id']}\n"
            f"Types: {types}\n"
            f"Height: {data['height'] / 10:.1f} m\n"
            f"Weight: {data['weight'] / 10:.1f} kg"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PokemonDetails()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())